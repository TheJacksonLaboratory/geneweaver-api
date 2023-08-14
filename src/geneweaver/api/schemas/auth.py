from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class AppRoles(str, Enum):
    user = "user"
    curator = "curator"
    admin = "admin"


class User(BaseModel):
    email: Optional[str]
    name: Optional[str]
    sso_id: str = Field(None, alias="sub")
    id: int = Field(None, alias="gw_id")
    role: Optional[AppRoles] = AppRoles.user


class UserInternal(User):
    auth_header: dict = {}
    token: str
    permissions: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True
