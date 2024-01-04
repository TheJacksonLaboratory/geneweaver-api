"""Service functions for dealing with genesets."""

from fastapi.logger import logger
from geneweaver.api.controller import message
from geneweaver.api.schemas.auth import User
from geneweaver.db import geneset as db_geneset
from geneweaver.db import geneset_value as db_geneset_value
from geneweaver.db.geneset import is_readable as db_is_readable
from psycopg import Cursor


def get_geneset(cursor: Cursor, geneset_id: int, user: User) -> dict:
    """Get a geneset by ID."""
    try:
        if not is_geneset_readable_by_user(cursor, geneset_id, user):
            return {"error": True, "message": message.ACCESS_FORBIDEN}

        geneset = db_geneset.by_id(cursor, geneset_id)
        geneset_values = db_geneset_value.by_geneset_id(cursor, geneset_id)
        return {"geneset": geneset, "geneset_values": geneset_values}

    except Exception as err:
        logger.error(err)
        raise err


def is_geneset_readable_by_user(cursor: Cursor, geneset_id: int, user: User) -> bool:
    """Check if the user can read the geneset from DB."""
    readable: bool = False
    try:
        readable = db_is_readable(cursor, user.id, geneset_id)
    except Exception as err:
        logger.error(err)
        raise err

    return readable
