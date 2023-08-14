"""This file contains code to authenticate a user to the API."""
import requests
import urllib.parse

from typing import Optional, Dict, Type

from fastapi import HTTPException, Depends, Request
from fastapi.logger import logger
from fastapi.security import SecurityScopes, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows
from pydantic import ValidationError
from jose import jwt  # type: ignore

from geneweaver.api.schemas.auth import UserInternal

from geneweaver.api.core.exceptions import (
    Auth0UnauthenticatedException,
    Auth0UnauthorizedException,
)


class Auth0HTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # logger.debug('Called Auth0HTTPBearer')
        return await super().__call__(request)


class OAuth2ImplicitBearer(OAuth2):
    def __init__(
        self,
        authorizationUrl: str,
        scopes: Dict[str, str] = {},
        scheme_name: Optional[str] = None,
        auto_error: bool = True,
    ):
        flows = OAuthFlows(
            implicit={"authorizationUrl": authorizationUrl, "scopes": scopes}
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        # Overwrite parent call to prevent useless overhead, the actual auth is done in Auth0.get_user
        # This scheme is just for Swagger UI
        return None


class Auth0:
    def __init__(
        self,
        domain: str,
        api_audience: str,
        scopes: Dict[str, str] = {},
        auto_error: bool = True,
        scope_auto_error: bool = True,
        email_auto_error: bool = False,
        auth0user_model: Type[UserInternal] = UserInternal,
    ):
        self.domain = domain
        self.audience = api_audience

        self.auto_error = auto_error
        self.scope_auto_error = scope_auto_error
        self.email_auto_error = email_auto_error

        self.auth0_user_model = auth0user_model

        self.algorithms = ["RS256"]
        self.jwks: Dict = requests.get(f"https://{domain}/.well-known/jwks.json").json()

        authorization_url_qs = urllib.parse.urlencode({"audience": api_audience})
        authorization_url = f"https://{domain}/authorize?{authorization_url_qs}"
        self.implicit_scheme = OAuth2ImplicitBearer(
            authorizationUrl=authorization_url,
            scopes=scopes,
            scheme_name="Auth0ImplicitBearer",
        )

    async def public(
        self,
        security_scopes: SecurityScopes,
        creds: Optional[HTTPAuthorizationCredentials] = Depends(
            Auth0HTTPBearer(auto_error=False)
        ),
    ) -> bool:
        return not bool(await self.get_user(security_scopes, creds))

    async def authenticated(
        self,
        security_scopes: SecurityScopes,
        creds: Optional[HTTPAuthorizationCredentials] = Depends(
            Auth0HTTPBearer(auto_error=False)
        ),
    ) -> bool:
        try:
            authenticated = bool(await self.get_user(security_scopes, creds))
        except (Auth0UnauthorizedException, HTTPException):
            authenticated = False
        return authenticated

    async def get_auth_header(
        self,
        security_scopes: SecurityScopes,
        creds: Optional[HTTPAuthorizationCredentials] = Depends(
            Auth0HTTPBearer(auto_error=False)
        ),
        auto_error_auth: Optional[bool] = False,
    ) -> Optional[Dict[str, str]]:
        user = await self.get_user(security_scopes, creds, auto_error_auth)
        return user.auth_header if user else None

    async def get_user_strict(
        self,
        security_scopes: SecurityScopes,
        creds: Optional[HTTPAuthorizationCredentials] = Depends(
            Auth0HTTPBearer(auto_error=False)
        ),
    ):
        return await self.get_user(security_scopes, creds, True)

    async def get_user(
        self,
        security_scopes: SecurityScopes,
        creds: Optional[HTTPAuthorizationCredentials] = Depends(
            Auth0HTTPBearer(auto_error=False)
        ),
        auto_error_auth: Optional[bool] = True,
        disallow_public: Optional[bool] = True,
    ) -> Optional[UserInternal]:
        auto_error_auth = (
            self.auto_error if auto_error_auth is None else auto_error_auth
        )
        logger.debug(f"`auto_error` is {'ON' if auto_error_auth else 'OFF'}")
        logger.debug(f"`disallow_public` is {'ON' if disallow_public else 'OFF'}")
        if creds is None:
            if disallow_public:
                logger.debug(f"No credentials found, raising HTTP 403 exception")
                # See HTTPBearer from FastAPI:
                # latest - https://github.com/tiangolo/fastapi/blob/master/fastapi/security/http.py
                # 0.65.1 - https://github.com/tiangolo/fastapi/blob/aece74982d7c9c1acac98e2c872c4cb885677fc7/fastapi/security/http.py
                # must be 403 until solving https://github.com/tiangolo/fastapi/pull/2120
                raise HTTPException(403, detail="Missing bearer token")
            else:
                logger.debug(f"No credentials found, returning None")
                return None

        token = creds.credentials
        payload: Dict = {}
        try:
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in self.jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }
                    # break  # TODO: do we still need to iterate all keys after we found a match?
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.algorithms,
                    audience=self.audience,
                    issuer=f"https://{self.domain}/",
                )
                logger.debug(f"Decoded header token: {payload}")
            else:
                if auto_error_auth:
                    raise jwt.JWTError

        except jwt.ExpiredSignatureError:
            if auto_error_auth:
                raise Auth0UnauthenticatedException(detail="Expired token")
            else:
                return None

        except jwt.JWTClaimsError:
            if auto_error_auth:
                raise Auth0UnauthenticatedException(
                    detail="Invalid token claims (please check issuer and audience)"
                )
            else:
                return None

        except jwt.JWTError:
            if auto_error_auth:
                raise Auth0UnauthenticatedException(detail="Malformed token")
            else:
                return None

        except Exception as e:
            logger.error(f'Handled exception decoding token: "{e}"')
            if auto_error_auth:
                raise Auth0UnauthenticatedException(detail="Error decoding token")
            else:
                return None

        if self.scope_auto_error:
            token_scope_str: str = payload.get("scope", "")

            if isinstance(token_scope_str, str):
                token_scopes = token_scope_str.split()

                for scope in security_scopes.scopes:
                    if scope not in token_scopes:
                        raise Auth0UnauthorizedException(
                            detail=f'Missing "{scope}" scope',
                            headers={
                                "WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'
                            },
                        )
            else:
                # This is an unlikely case but handle it just to be safe (perhaps auth0 will change the scope format)
                raise Auth0UnauthorizedException(
                    detail='Token "scope" field must be a string'
                )

        try:
            self._add_auth_info(token, payload)
            self._process_payload(payload)
            user = self.auth0_user_model(**payload)
            if self.email_auto_error and not user.email:
                raise Auth0UnauthorizedException(
                    detail=f'Missing email claim (check auth0 rule "Add email to access token")'
                )

            logger.info(f"Successfully found user in header token: {user}")
            return user

        except ValidationError as e:
            logger.error(f'Handled exception parsing Auth0User: "{e}"')
            if auto_error_auth:
                raise Auth0UnauthorizedException(detail="Error parsing Auth0User")
            else:
                return None

        return None

    def _process_payload(self, payload: dict):
        self._process_email(payload)

    def _add_auth_info(self, token: str, payload: dict):
        payload["token"] = token
        payload["auth_header"] = {"Authorization": f"Bearer {token}"}

    def _process_email(self, payload: dict):
        payload["email"] = payload.pop(f"{self.audience}/claims/email")
