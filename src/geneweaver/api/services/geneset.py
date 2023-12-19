"""Service functions for dealing with genesets."""

from fastapi.logger import logger
from geneweaver.db import geneset as db_geneset
from geneweaver.db import geneset_value as db_geneset_value
from geneweaver.db.geneset import is_readable as db_is_readable

from geneweaver.api import dependencies as deps
from geneweaver.api.controller import message
from geneweaver.api.schemas.auth import User


def get_geneset(
    geneset_id: int,
    user: User,
    cursor: deps.Cursor
) -> dict:

    """Get a geneset by ID."""
    try:
        if not is_geneset_readable_by_user(geneset_id, user, cursor):
            return {"error": True, "message": message.ACCESS_FORBIDEN}

        geneset = db_geneset.by_id(cursor, geneset_id)
        geneset_values = db_geneset_value.by_geneset_id(cursor, geneset_id)
        return {"geneset": geneset, "geneset_values": geneset_values}

    except Exception as err:
        logger.error(err)
        raise err

def is_geneset_readable_by_user(
        geneset_id: int,
        user: User,
        cursor: deps.Cursor
) -> bool:

    """ check if the user can read the geneset from DB"""
    readable: bool = False
    try:
        readable = db_is_readable(cursor, user.id, geneset_id)
    except Exception as err:
        logger.error(err)
        raise err

    return readable