"""Dependency injection capabilities for the GeneWeaver API."""
from typing import Generator
from fastapi import Depends
import psycopg
from psycopg.rows import dict_row
# from psycopg_pool import ConnectionPool
# pool = ConnectionPool(conninfo, **kwargs)

from geneweaver.api.core.config import settings, db_settings
from geneweaver.db.user import user_id_from_sso_id
from geneweaver.api.core.security import Auth0, UserInternal
from geneweaver.db.user import by_sso_id

auth = Auth0(
    domain=settings.AUTH_DOMAIN,
    api_audience=settings.AUTH_AUDIENCE,
    scopes=settings.AUTH_SCOPES,
    auto_error=False,
)

Cursor = psycopg.Cursor


def cursor() -> Generator:
    """Get a cursor from the connection pool."""
    with psycopg.connect(db_settings.URI, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            yield cur


def full_user(
    cursor: Cursor = Depends(cursor),
    user: UserInternal = Depends(auth.get_user_strict),
) -> UserInternal:
    user.id = by_sso_id(cursor, user.sso_id)[0]['usr_id']
    yield user
