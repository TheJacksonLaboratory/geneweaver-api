"""Service methods for genes."""

from typing import Iterable, List, Optional

from fastapi.logger import logger
from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db import gene as db_gene
from psycopg import Cursor


def get_genes(
    cursor: Cursor,
    reference_id: Optional[str] = None,
    gene_database: Optional[GeneIdentifier] = None,
    species: Optional[Species] = None,
    preferred: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> dict:
    """Get geneweaver genes from DB.

    :param cursor: The database cursor.
    :param reference_id: The reference id to search for.
    :param gene_database: The gene database to search for.
    :param species: The species to search for.
    :param preferred: Whether to search for preferred genes.
    :param limit: The limit of results to return.
    :param offset: The offset of results to return.
    """
    if limit is None:
        limit = 100

    try:
        gene_list = db_gene.get(
            cursor, reference_id, gene_database, species, preferred, limit, offset
        )

    except Exception as err:
        logger.error(err)
        raise err

    return {"genes": gene_list}


def get_homolog_ids(
    cursor: Cursor,
    gene_id_list: Iterable,
    target_gene_id_type: GeneIdentifier,
    source_gene_id_type: Optional[GeneIdentifier] = None,
    target_species: Optional[Species] = None,
    source_species: Optional[Species] = None,
) -> dict:
    """Get homologus gene identifier mappings.

    Get gene id mappings based on source/target GeneIdentifier id and
    source/target species.

    @param cursor: DB Cursor
    @param gene_id_list: list of ids to search
    @param source_gene_id_type: source gene identifier to translate from
    @param target_gene_id_type: target gene identifier type to search for
    @param target_species: target species identifier to translate to
    @param source_species: source species identifier to search for
    @return: dictionary with id mappings.
    """
    ids_map = None
    try:
        ids_map = db_gene.get_homolog_ids(
            cursor,
            gene_id_list,
            target_gene_id_type,
            source_gene_id_type,
            target_species,
            source_species,
        )

    except Exception as err:
        logger.error(err)
        raise err

    return {"ids_map": ids_map}


def get_gene_mapping(
    cursor: Cursor,
    source_ids: List[str],
    species: Species,
    target_gene_id_type: GeneIdentifier,
) -> dict:
    """Get gene identifier mappings.

    Get gene id mappings based on target GeneIdentifier id.

    @param cursor: DB Cursor
    @param source_ids: list of gene ids to search
    @param target_gene_id_type: gene identifier
    @param species: target species identifier
    @return: dictionary with id mappings.
    """
    ids_map = None
    try:
        ids_map = db_gene.mapping(cursor, source_ids, species, target_gene_id_type)

    except Exception as err:
        logger.error(err)
        raise err

    return {"ids_map": ids_map}


def get_gene_aon_mapping(
    cursor: Cursor,
    source_ids: List[str],
    species: Species,
) -> dict:
    """Get gene identifier AON mappings.

    Get gene id mappings based on species and default gene identifier type.

    @param cursor: DB Cursor
    @param source_ids: list of gene ids to search
    @param species: target species identifier
    @return: dictionary with id mappings.
    """
    ids_map = None
    try:
        ids_map = db_gene.aon_mapping(
            cursor,
            source_ids,
            species,
        )

    except Exception as err:
        logger.error(err)
        raise err

    return {"ids_map": ids_map}
