"""Namespace for the config class for the Geneweaver API."""

from typing import List, Optional

from geneweaver.db.core.settings_class import Settings as DBSettings
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


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

    @model_validator(mode="after")
    def assemble_db_settings(self) -> Self:
        """Build the database settings."""
        if not isinstance(self.DB, DBSettings):
            self.DB = DBSettings(
                SERVER=self.DB_HOST,
                NAME=self.DB_NAME,
                USERNAME=self.DB_USERNAME,
                PASSWORD=self.DB_PASSWORD,
                PORT=self.DB_PORT,
            )
        return self

    AUTH_DOMAIN: str = "thejacksonlaboratory.auth0.com"
    AUTH_AUDIENCE: str = "https://cube.jax.org"
    AUTH_ALGORITHMS: List[str] = ["RS256"]
    AUTH_EMAIL_CLAIM: str = "email"
    AUTH_SCOPES: dict = {
        "openid profile email": "read",
    }
    JWT_PERMISSION_PREFIX: str = "approle"
    AUTH_CLIENT_ID: str = "aE6dpT04mGlvPeUXl4RYGSnCjvHEuawd"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )
