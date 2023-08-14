"""Namespace for the config class for the Geneweaver API."""
from typing import Any, Dict, Optional, List

from pydantic import BaseSettings, PostgresDsn, validator
from geneweaver.db.core.settings_class import Settings


class GeneweaverAPIConfig(BaseSettings):
    """Config class for the Geneweaver API."""

    API_PREFIX: str = ""

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
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
    AUTH_CLIENT_ID: str = "oVm9omUtLBpVyL7YfJA8gp3hHaHwyVt8"

    class Config:
        """Configuration for the BaseSettings class."""

        env_file = ".env"
        case_sensitive = True
