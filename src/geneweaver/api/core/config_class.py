"""Namespace for the config class for the Geneweaver API."""

from typing import Any, Dict, List, Optional

from geneweaver.db.core.settings_class import Settings as DBSettings
from pydantic import BaseSettings, validator


class GeneweaverAPIConfig(BaseSettings):
    """Config class for the Geneweaver API."""

    LOG_LEVEL: str = "INFO"

    API_PREFIX: str = "/api"

    DB_HOST: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 5432
    DB: Optional[DBSettings] = None

    @validator("DB", pre=True)
    def assemble_db_settings(
        cls, v: Optional[DBSettings], values: Dict[str, Any]  # noqa: N805
    ) -> DBSettings:
        """Build the database settings."""
        if isinstance(v, DBSettings):
            return v
        return DBSettings(
            SERVER=values.get("DB_HOST"),
            NAME=values.get("DB_NAME"),
            USERNAME=values.get("DB_USERNAME"),
            PASSWORD=values.get("DB_PASSWORD"),
            PORT=values.get("DB_PORT"),
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
