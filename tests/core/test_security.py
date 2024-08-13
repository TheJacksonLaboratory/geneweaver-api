"""Tests for core security."""

from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, SecurityScopes
from geneweaver.api.core.exceptions import (
    Auth0UnauthenticatedException,
    Auth0UnauthorizedException,
)
from geneweaver.api.core.security import Auth0, UserInternal
from jose import jwt

from tests.data import test_jwt_keys_data

private_key = test_jwt_keys_data.get("test_private_key")
public_key = test_jwt_keys_data.get("test_public_key")

test_audience = "https://gw.test.org"
test_domain = "gw.test.auth0.com"
test_email = "test@test.org"
test_name = "Test Name"


# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockGetResponse:
    """Mock for get response."""

    # mock json()
    @staticmethod
    def json() -> dict:
        """Json response."""
        return {"mock_key": "mock_response"}


def do_auth():
    """Initialize Auth object with test config."""
    auth = Auth0(
        domain=test_domain,
        api_audience=test_audience,
        scopes={
            "openid profile email": "read",
        },
        auto_error=True,
        email_auto_error=True,
    )

    auth.jwks = public_key

    return auth


@patch("geneweaver.api.core.security.requests")
def create_test_token(mock_requests, claims=None):
    """Create a valid RS256 test JWT token."""
    mock_requests.get.return_value = MockGetResponse()

    # claims
    if claims is None:
        to_encode = {
            f"{test_audience}/email": test_email,
            "iss": f"https://{test_domain}/",
            "aud": test_audience,
            "name": test_name,
            "scope": "openid profile email",
        }
    else:
        to_encode = claims

    token = jwt.encode(to_encode, private_key, algorithm="RS256")

    return token


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.SecurityScopes")
@patch("geneweaver.api.core.security.requests")
async def test_get_user_no_creds_http_error(mock_requests, mock_security_scope):
    """Test get user with no credetials in the request."""
    auth = do_auth()

    with pytest.raises(expected_exception=HTTPException):
        await auth.get_user_strict(security_scopes=mock_security_scope, creds=None)


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.SecurityScopes")
@patch("geneweaver.api.core.security.requests")
async def test_invalid_token_format(mock_requests, mock_security_scope):
    """Test invalid token in credentials."""
    auth = do_auth()

    creds = HTTPAuthorizationCredentials(scheme="", credentials="token")

    with pytest.raises(expected_exception=Auth0UnauthenticatedException):
        await auth.get_user(
            security_scopes=mock_security_scope,
            creds=creds,
            auto_error_auth=True,
            disallow_public=True,
        )


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.SecurityScopes")
@patch("geneweaver.api.core.security.jwt.get_unverified_header")
@patch("geneweaver.api.core.security.requests")
async def test_valid_jwt_token(
    mock_requests, mock_jwt_unverified_header, mock_security_scope
):
    """Test get user with no credetials in the request."""
    auth = do_auth()
    mock_jwt_unverified_header.return_value = private_key

    # get test token
    token = create_test_token()
    creds = HTTPAuthorizationCredentials(credentials=token, scheme="")

    user: UserInternal = await auth.get_user(
        security_scopes=mock_security_scope,
        creds=creds,
        auto_error_auth=True,
        disallow_public=False,
    )

    print(user)
    assert user is not None
    assert user.email == test_email
    assert user.name == test_name


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.SecurityScopes")
@patch("geneweaver.api.core.security.jwt.get_unverified_header")
@patch("geneweaver.api.core.security.requests")
async def test_get_user_strict_valid_jwt_token(
    mock_requests, mock_jwt_unverified_header, mock_security_scope
):
    """Test get user strict with a valid token."""
    auth = do_auth()
    mock_jwt_unverified_header.return_value = private_key

    # get test token
    token = create_test_token()
    creds = HTTPAuthorizationCredentials(credentials=token, scheme="")

    user: UserInternal = await auth.get_user_strict(
        security_scopes=mock_security_scope, creds=creds
    )

    print(user)
    assert user is not None
    assert user.email == test_email
    assert user.name == test_name


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.jwt.get_unverified_header")
@patch("geneweaver.api.core.security.requests")
async def test_get_user_with_scopes(mock_requests, mock_jwt_unverified_header):
    """Test get user with secuirty scopes."""
    auth = do_auth()
    mock_jwt_unverified_header.return_value = private_key

    # get test token
    token = create_test_token()
    creds = HTTPAuthorizationCredentials(credentials=token, scheme="")

    scopes = SecurityScopes(scopes=["openid", "profile", "email"])
    user: UserInternal = await auth.get_user_strict(security_scopes=scopes, creds=creds)

    print(user)
    assert user is not None
    assert user.email == test_email
    assert user.name == test_name


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.jwt.get_unverified_header")
@patch("geneweaver.api.core.security.requests")
async def test_authenticated(mock_requests, mock_jwt_unverified_header):
    """Test get user authenticated."""
    auth = do_auth()
    mock_jwt_unverified_header.return_value = private_key

    # get test token
    token = create_test_token()
    creds = HTTPAuthorizationCredentials(credentials=token, scheme="")

    scopes = SecurityScopes(scopes=["openid", "profile", "email"])
    authenticated = await auth.authenticated(security_scopes=scopes, creds=creds)

    assert authenticated is True

    token = "token"
    creds = HTTPAuthorizationCredentials(credentials=token, scheme="")
    authenticated = await auth.authenticated(security_scopes=scopes, creds=creds)

    assert authenticated is False


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.jwt.get_unverified_header")
@patch("geneweaver.api.core.security.requests")
async def test_is_user_public(mock_requests, mock_jwt_unverified_header):
    """Test is user public."""
    auth = do_auth()
    mock_jwt_unverified_header.return_value = private_key

    # get test token
    token = create_test_token()
    creds = HTTPAuthorizationCredentials(credentials=token, scheme="")

    scopes = SecurityScopes(scopes=["openid", "profile", "email"])
    authenticated = await auth.public(security_scopes=scopes, creds=creds)

    assert authenticated is False


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.SecurityScopes")
@patch("geneweaver.api.core.security.jwt.get_unverified_header")
@patch("geneweaver.api.core.security.requests")
async def test_is_user_not_public(
    mock_requests, mock_jwt_unverified_header, mock_security_scope
):
    """Test user is not public."""
    auth = do_auth()
    is_public = await auth.get_user(
        security_scopes=mock_security_scope, creds=None, disallow_public=False
    )

    assert is_public is None


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.SecurityScopes")
@patch("geneweaver.api.core.security.jwt.get_unverified_header")
@patch("geneweaver.api.core.security.requests")
async def test_invalid_claim(
    mock_requests, mock_jwt_unverified_header, mock_security_scope
):
    """Test get user exception with invalid claim."""
    auth = do_auth()
    mock_jwt_unverified_header.return_value = private_key

    to_encode = {
        f"{test_audience}/email": test_email,
        "name": test_name,
        "scope": "openid profile email",
    }

    # get test token
    token = create_test_token(claims=to_encode)
    creds = HTTPAuthorizationCredentials(credentials=token, scheme="")

    with pytest.raises(expected_exception=Auth0UnauthenticatedException):
        await auth.get_user(
            security_scopes=mock_security_scope,
            creds=creds,
            auto_error_auth=True,
            disallow_public=True,
        )


@pytest.mark.asyncio()
@patch("geneweaver.api.core.security.SecurityScopes")
@patch("geneweaver.api.core.security.jwt.get_unverified_header")
@patch("geneweaver.api.core.security.requests")
async def test_missing_claim_email_error_claim(
    mock_requests, mock_jwt_unverified_header, mock_security_scope
):
    """Test get user exception with missing email in claim."""
    auth = do_auth()
    mock_jwt_unverified_header.return_value = private_key

    to_encode = {
        f"{test_audience}/email": None,
        "iss": f"https://{test_domain}/",
        "aud": test_audience,
        "name": test_name,
        "scope": "openid profile email",
    }

    # get test token
    token = create_test_token(claims=to_encode)
    creds = HTTPAuthorizationCredentials(credentials=token, scheme="")

    with pytest.raises(expected_exception=Auth0UnauthorizedException):
        await auth.get_user(
            security_scopes=mock_security_scope,
            creds=creds,
            auto_error_auth=True,
            disallow_public=True,
        )
