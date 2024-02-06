"""Service functions for publications."""

from fastapi.logger import logger
from geneweaver.db import publication as db_publication
from psycopg import Cursor


def get_publication(cursor: Cursor, pub_id: int) -> dict:
    """Get a publication by ID from the DB.

    @param cursor: DB cursor
    @param pub_id: publication identifier
    @return: dictionary response (publication).
    """
    try:
        pub = db_publication.by_id(cursor, pub_id)
        return {"publication": pub}

    except Exception as err:
        logger.error(err)
        raise err


def get_publication_by_pubmed_id(cursor: Cursor, pub_med_id: str) -> dict:
    """Get a publication by Pubmed Id from the DB.

    @param cursor: DB cursor
    @param pub_med_id: pub med identifier
    @return: dictionary response (publication).
    """
    try:
        pub = db_publication.by_pubmed_id(cursor, pub_med_id)
        return {"publication": pub}

    except Exception as err:
        logger.error(err)
        raise err
