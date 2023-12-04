"""Authentication Related Schemas."""
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class AppRoles(str, Enum):
    """Roles that a user can have in the GeneWeaver application."""

    user = "user"
    curator = "curator"
    admin = "admin"


class User(BaseModel):
    """User model."""

    email: Optional[str]
    name: Optional[str]
    sso_id: str = Field(None, alias="sub")
    id: int = Field(None, alias="gw_id")  # noqa: A003
    role: Optional[AppRoles] = AppRoles.user


class UserInternal(User):
    """Internal User model."""

    auth_header: dict = {}
    token: str
    permissions: Optional[List[str]]

    class Config:
        """Pydantic config."""

        allow_population_by_field_name = True
