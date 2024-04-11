"""Service functions for Species."""

from typing import Optional

from fastapi.logger import logger
from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db import species as db_species
from psycopg import Cursor


def get_species(
    cursor: Cursor,
    taxonomy_id: Optional[int] = None,
    reference_gene_id_type: Optional[GeneIdentifier] = None,
) -> dict:
    """Get species from DB.

    @param cursor: DB cursor
    @param taxonomy_id:
    @param reference_gene_id_type:
    @return: dictionary response (species).
    """
    try:
        response = db_species.get(cursor, taxonomy_id, reference_gene_id_type)
        return {"data": response}

    except Exception as err:
        logger.error(err)
        raise err


def get_species_by_id(cursor: Cursor, species: Species) -> dict:
    """Get species from DB.

    @param cursor: DB cursor
    @param species: species id
    @return: dictionary response (species).
    """
    try:
        return db_species.get_by_id(cursor, species)

    except Exception as err:
        logger.error(err)
        raise err
