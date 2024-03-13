"""Service functions for Species."""

from typing import Optional

from fastapi.logger import logger
from geneweaver.core.enum import GeneIdentifier
from geneweaver.db import species as db_species
from psycopg import Cursor


def get_species(
    cursor: Cursor,
    taxonomy_id: Optional[int] = None,
    gene_id_type: Optional[GeneIdentifier] = None,
) -> dict:
    """Get species from DB.

    @param cursor: DB cursor
    @param taxonomy_id:
    @param gene_id_type:
    @return: dictionary response (species).
    """
    try:
        species = db_species.get(cursor, taxonomy_id, gene_id_type)
        return {"species": species}

    except Exception as err:
        logger.error(err)
        raise err
