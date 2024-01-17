"""Dependency injection capabilities for the GeneWeaver API."""
# ruff: noqa: B008
from tempfile import TemporaryDirectory
from typing import Generator

import psycopg
from fastapi import Depends
from geneweaver.api.core.config import settings
from geneweaver.api.core.security import Auth0, UserInternal
from geneweaver.db.user import by_sso_id
from psycopg.rows import dict_row

auth = Auth0(
    domain=settings.AUTH_DOMAIN,
    api_audience=settings.AUTH_AUDIENCE,
    scopes=settings.AUTH_SCOPES,
    auto_error=False,
)

Cursor = psycopg.Cursor


def cursor() -> Generator:
    """Get a cursor from the connection pool."""
    with psycopg.connect(settings.DB.URI, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            yield cur


async def full_user(
    cursor: Cursor = Depends(cursor),
    user: UserInternal = Depends(auth.get_user_strict),
) -> UserInternal:
    """Get the full user object.

    Since there are external dependencies to wait for,
    the recommendation is to use async
    Also, Workaround FASTAPI issue, where logs hide exact place of errors
    https://github.com/tiangolo/fastapi/discussions/8428
    Geneweaver issue: G3-96.
    @param cursor: DB cursor
    @param user: GW user.
    """
    user.id = by_sso_id(cursor, user.sso_id)[0]["usr_id"]
    yield user


async def get_temp_dir() -> TemporaryDirectory:
    """Get a temp directory."""
    temp_dir = TemporaryDirectory()
    try:
        yield temp_dir.name
    finally:
        del temp_dir
