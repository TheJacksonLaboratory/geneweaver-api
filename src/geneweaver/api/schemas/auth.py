"""Authentication Related Schemas."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AppRoles(str, Enum):
    """Roles that a user can have in the GeneWeaver application."""

    user = "user"
    curator = "curator"
    admin = "admin"


class User(BaseModel):
    """User model."""

    email: Optional[str] = None
    name: Optional[str] = None
    sso_id: str = Field(None, alias="sub")
    id: int = Field(None, alias="gw_id")  # noqa: A003
    role: Optional[AppRoles] = AppRoles.user


class UserInternal(User):
    """Internal User model."""

    auth_header: dict = {}
    token: str
    permissions: Optional[List[str]] = None

    model_config = ConfigDict(populate_by_name=True)
