"""Service functions for dealing with genesets."""

from typing import Iterable, Optional
from fastapi.logger import logger
from geneweaver.api.controller import message
from geneweaver.api.schemas.auth import User
from geneweaver.core.enum import GeneIdentifier, GenesetTier, Species
from geneweaver.db import gene as db_gene
from geneweaver.db import geneset as db_geneset
from geneweaver.db import geneset_value as db_geneset_value
from psycopg import Cursor


def get_visible_genesets(
    cursor: Cursor,
    user: User,
    gs_id: Optional[int] = None,
    only_my_genesets: Optional[bool] = None,
    curation_tier: Optional[GenesetTier] = None,
    species: Optional[Species] = None,
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    publication_id: Optional[int] = None,
    pubmed_id: Optional[int] = None,
    gene_id_type: Optional[GeneIdentifier] = None,
    search_text: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    with_publication_info: bool = True,
) -> dict:
    """Get genesets from the database.

    :param cursor: An async database cursor.
    :param gs_id: Show only results with this geneset ID.
    :param curation_tier: Show only results of this curation tier.
    :param species: Show only results associated with this species.
    :param name: Show only results with this name.
    :param abbreviation: Show only results with this abbreviation.
    :param publication_id: Show only results with this publication ID (internal).
    :param pubmed_id: Show only results with this PubMed ID.
    :param gene_id_type: Show only results with this gene ID type.
    :param search_text: Return genesets that match this search text (using PostgreSQL
                        full-text search).
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    :param with_publication_info: Include publication info in the return.
    """
    try:
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        owner_id = None
        if only_my_genesets:
            owner_id = user.id

        results = db_geneset.get(
            cursor,
            is_readable_by=user.id,
            owner_id=owner_id,
            gs_id=gs_id,
            curation_tier=curation_tier,
            species=species,
            name=name,
            abbreviation=abbreviation,
            publication_id=publication_id,
            pubmed_id=pubmed_id,
            gene_id_type=gene_id_type,
            search_text=search_text,
            with_publication_info=with_publication_info,
            limit=limit,
            offset=offset,
        )
        return {"geneset": results}

    except Exception as err:
        logger.error(err)
        raise err


def get_geneset_metadata(
    cursor: Cursor, geneset_id: int, user: User, include_pub_info: bool = False
) -> dict:
    """Get a geneset metadata by geneset id.

    @param cursor: DB cursor
    @param geneset_id: geneset identifier
    @param user: GW user
    @param include_pub_info: bool (Optional with publication information)
    @return: dictionary response (geneset).
    """
    try:
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        results = db_geneset.get(
            cursor,
            is_readable_by=user.id,
            gs_id=geneset_id,
            with_publication_info=include_pub_info,
        )
        return {"geneset": results[0]}

    except Exception as err:
        logger.error(err)
        raise err


def get_geneset(cursor: Cursor, geneset_id: int, user: User) -> dict:
    """Get a geneset by ID.

    @param cursor: DB cursor
    @param geneset_id: geneset identifier
    @param user: GW user
    @return: dictionary response (geneset and genset values).
    """
    try:
        # if not is_geneset_readable_by_user(cursor, geneset_id, user):

        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        results = db_geneset.get(
            cursor,
            is_readable_by=user.id,
            gs_id=geneset_id,
            with_publication_info=False,
        )
        geneset = results[0]
        geneset_values = db_geneset_value.by_geneset_id(cursor, geneset_id)
        return {"geneset": geneset, "geneset_values": geneset_values}

    except Exception as err:
        logger.error(err)
        raise err


def get_geneset_w_gene_id_type(
    cursor: Cursor, geneset_id: int, user: User, gene_id_type: GeneIdentifier
) -> dict:
    """Get a geneset by ID and filter with gene identifier type.

    @param cursor: DB cursor
    @param geneset_id: geneset identifier
    @param user: GW user
    @param gene_id_type: gene identifier type object
    @return: Dictionary response (geneset identifier, geneset, and genset values).
    """
    try:
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        results = db_geneset.get(
            cursor,
            is_readable_by=user.id,
            gs_id=geneset_id,
            with_publication_info=False,
        )
        geneset = results[0]

        mapping_across_species = False
        original_gene_id_type = gene_id_type
        genedb_sp_id = db_gene.gene_database_by_id(cursor, gene_id_type)[0]["sp_id"]

        if genedb_sp_id != 0 and geneset["species_id"] != genedb_sp_id:
            mapping_across_species = True
            gene_id_type = GeneIdentifier(7)

        geneset_values = db_geneset_value.by_geneset_id(
            cursor, geneset_id, gene_id_type
        )

        if mapping_across_species:
            geneset_values = map_geneset_homology(
                cursor, geneset_values, original_gene_id_type
            )

            gene_id_type = original_gene_id_type

        return {
            "gene_identifier_type": gene_id_type.name,
            "geneset": geneset,
            "geneset_values": geneset_values,
        }

    except Exception as err:
        logger.error(err)
        raise err


def map_geneset_homology(
    cursor: Cursor, geneset_value: Iterable[dict], gene_id_type: GeneIdentifier
) -> Iterable[dict]:
    """Map geneset homology (result identifier species differs from source).

    @param cursor: DB cursor
    @param geneset_value: geneset value
    @param gene_id_type: gene identifier type object
    @return: geneset value
    """
    try:
        ode_ids = [gene["ode_gene_id"] for gene in geneset_value]
        gene_homologs = db_gene.get_homolog_ids_by_ode_id(cursor, ode_ids, gene_id_type)
        homolog_mapping = {
            gene["ode_gene_id"]: gene["ode_ref_id"] for gene in gene_homologs
        }

        for gene in geneset_value:
            gene["gdb_id"] = gene_id_type.value
            if gene["ode_gene_id"] in homolog_mapping:
                gene["ode_ref_id"] = homolog_mapping[gene["ode_gene_id"]]
            else:
                gene["ode_ref_id"] = None

        return geneset_value
    except Exception as err:
        logger.error(err)
        raise err
