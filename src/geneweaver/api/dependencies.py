"""Dependency injection capabilities for the GeneWeaver API."""
# ruff: noqa: B008
from typing import Generator

import psycopg
from fastapi import Depends
from geneweaver.api.core.config import settings
from geneweaver.api.core.security import Auth0, UserInternal
from geneweaver.db import user as db_user
from psycopg.rows import dict_row

from geneweaver.api.core.exceptions import AuthenticationMismatch

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


def full_user(
    cursor: Cursor = Depends(cursor),
    user: UserInternal = Depends(auth.get_user_strict),
) -> UserInternal:
    """Get the full user object.""" ""
    try:
        user.id = db_user.by_sso_id_and_email(cursor, user.sso_id, user.email)[0][
            "usr_id"
        ]
    except IndexError:
        if db_user.sso_id_exists(cursor, user.sso_id):
            raise AuthenticationMismatch(
                detail="Email and SSO ID Mismatch. Please contact and administrator."
            )
        elif db_user.email_exists(cursor, user.email):
            user.id = db_user.link_user_id_with_sso_id(cursor, user.id, user.sso_id)
        else:
            user.id = db_user.create_sso_user(
                cursor, user.name, user.email, user.sso_id
            )

    yield user
