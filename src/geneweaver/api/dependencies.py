"""Dependency injection capabilities for the GeneWeaver API."""
# ruff: noqa: B008
import logging
from contextlib import asynccontextmanager
from tempfile import TemporaryDirectory
from typing import Generator

import psycopg
from fastapi import Depends, FastAPI, Request
from geneweaver.api.core.config import settings
from geneweaver.api.core.exceptions import AuthenticationMismatch
from geneweaver.api.core.security import Auth0, UserInternal
from geneweaver.db import user as db_user
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

auth = Auth0(
    domain=settings.AUTH_DOMAIN,
    api_audience=settings.AUTH_AUDIENCE,
    scopes=settings.AUTH_SCOPES,
    auto_error=False,
)

Cursor = psycopg.Cursor

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Open and close the DB connection pool.

    :param app: The FastAPI application (dependency injection).
    """
    logger.info("Opening DB Connection Pool.")
    app.pool = ConnectionPool(settings.DB.URI)
    app.pool.open()
    app.pool.wait()
    with app.pool.connection() as conn:
        with conn.cursor() as cur:
            logger.info("Setting search path.")
            cur.execute(
                'SET search_path = "$user", '
                "public, production, extsrc, odestatic, curation;"
            )
            conn.commit()
    yield
    logger.info("Closing DB Connection Pool.")
    app.pool.close()


def cursor(request: Request) -> Generator:
    """Get a cursor from the connection pool."""
    with request.app.pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
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
    try:
        user.id = db_user.by_sso_id_and_email(cursor, user.sso_id, user.email)[0][
            "usr_id"
        ]
    except IndexError as e:
        if db_user.sso_id_exists(cursor, user.sso_id):
            raise AuthenticationMismatch(
                detail="Email and SSO ID Mismatch. Please contact and administrator."
            ) from e
        elif db_user.email_exists(cursor, user.email):
            user.id = db_user.link_user_id_with_sso_id(cursor, user.id, user.sso_id)
        else:
            if not user.name:
                user.name = user.email
            user.id = db_user.create_sso_user(
                cursor, user.name, user.email, user.sso_id
            )

    yield user


async def get_temp_dir() -> TemporaryDirectory:
    """Get a temp directory."""
    temp_dir = TemporaryDirectory()
    try:
        yield temp_dir.name
    finally:
        del temp_dir
