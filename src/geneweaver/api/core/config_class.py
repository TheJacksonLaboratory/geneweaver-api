"""Namespace for the config class for the Geneweaver API."""
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator


class GeneweaverAPIConfig(BaseSettings):
    """Config class for the Geneweaver API."""

    API_PREFIX: str = ""

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]  # noqa: N805
    ) -> Union[str, PostgresDsn]:
        """Build the database connection string."""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    AUTH_DOMAIN: str = "geneweaver.auth0.com"
    AUTH_AUDIENCE: str = "https://api.geneweaver.org"
    AUTH_ALGORITHMS: List[str] = ["RS256"]
    AUTH_EMAIL_NAMESPACE: str = AUTH_AUDIENCE
    AUTH_SCOPES = {
        "openid profile email": "read",
    }
    JWT_PERMISSION_PREFIX: str = "approle"
    AUTH_CLIENT_ID: str = "T7bj6wlmtVcAN2O6kzDRwPVFyIj4UQNs"

    class Config:
        """Configuration for the BaseSettings class."""

        env_file = ".env"
        case_sensitive = True
