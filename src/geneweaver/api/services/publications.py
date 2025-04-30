"""Service functions for publications."""

from typing import Optional

from fastapi.logger import logger
from geneweaver.api.controller import message
from geneweaver.api.schemas.auth import User
from geneweaver.core.exc import ExternalAPIError
from geneweaver.core.publication import pubmed
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

    except Exception as err:
        logger.error(err)
        raise err

    return pub


def get_publication_by_pubmed_id(cursor: Cursor, pubmed_id: int) -> dict:
    """Get a publication by Pubmed Id from the DB.

    @param cursor: DB cursor
    @param pubmed_id: pub med identifier
    @return: dictionary response (publication).
    """
    print("pubmed_id", pubmed_id)
    try:
        pub = db_publication.by_pubmed_id(cursor, pubmed_id)
        return pub
    except Exception as err:
        logger.error(err)
        raise err


def add_pubmed_record(cursor: Cursor, user: User, pubmed_id: str) -> dict:
    """Add pubmed publication to the DB given pub-med id.

    @param cursor: DB cursor
    @param user: logged-in user
    @param pubmed_id: pubmed id
    @return:
    """
    try:
        # check logged-in user
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}
        # check publication is not already in the DB
        pub = db_publication.by_pubmed_id(cursor, pubmed_id)
        if pub:
            return {"pubmed_id": pubmed_id, "pub_id": pub.get("id")}

        # retrieve publication info to be stored
        pub_record = pubmed.get_publication(pubmed_id=pubmed_id)
        # persist publication in DB
        results = db_publication.add(cursor, pub_record)

        if results is None:
            return {"error": True, "message": message.UNEXPECTED_ERROR}

        return {"pubmed_id": pubmed_id, "pub_id": results.get("pub_id")}

    except ExternalAPIError as err:
        logger.error(err)
        return {"error": True, "message": message.PUBMED_RETRIEVING_ERROR}

    except Exception as err:
        logger.error(err)
        raise err


def get(
    cursor: Cursor,
    pub_id: Optional[int] = None,
    authors: Optional[str] = None,
    title: Optional[str] = None,
    abstract: Optional[str] = None,
    journal: Optional[str] = None,
    volume: Optional[str] = None,
    pages: Optional[str] = None,
    month: Optional[str] = None,
    year: Optional[str] = None,
    pubmed: Optional[str] = None,
    search_text: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> dict:
    """Get publications by some criteria.

    :param cursor: A database cursor.
    :param pub_id: Show only results with this publication id
    :param authors: Show only results with these authors
    :param title: Show only results with this title
    :param abstract: Show only results with this abstract
    :param journal: Show only results with this journal
    :param volume: Show only results with volume
    :param pages: Show only results with these pages
    :param month: Show only results with this publication month
    :param year: Show only results with publication year
    :param pubmed: Show only results with pubmed id
    :param search_text: Show only results that match this search text (using PostgreSQL
                        full-text search).
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    """
    try:
        results = db_publication.get(
            cursor=cursor,
            pub_id=pub_id,
            authors=authors,
            title=title,
            abstract=abstract,
            journal=journal,
            volume=volume,
            pages=pages,
            month=month,
            year=year,
            pubmed=pubmed,
            search_text=search_text,
            limit=limit,
            offset=offset,
        )

    except Exception as err:
        logger.error(err)
        raise err

    return {"data": results}
