"""Service functions for dealing with genesets."""

from datetime import date
from typing import Iterable, Optional, Set

from fastapi.logger import logger
from geneweaver.api.controller import message
from geneweaver.api.core.exceptions import UnauthorizedException
from geneweaver.api.schemas.auth import AppRoles, User
from geneweaver.core.enum import GeneIdentifier, GenesetTier, Species
from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db import gene as db_gene
from geneweaver.db import geneset as db_geneset
from geneweaver.db import geneset_value as db_geneset_value
from geneweaver.db import ontology as db_ontology
from geneweaver.db import threshold as db_threshold
from psycopg import Cursor, errors

ONTO_GSO_REF_TYPE = "GeneWeaver Primary Annotation"


def determine_geneset_access(
    user: Optional[User] = None,
    curation_tier: Optional[Set[GenesetTier]] = None,
    only_my_genesets: Optional[bool] = None,
) -> tuple:
    """Determine the geneset access based on the user and requested arguments.

    :param user: The user requesting the genesets.
    :param curation_tier: The curation tiers requested by the user.
    :param only_my_genesets: Show only results owned by the user.
    :return: A tuple containing the curation tier, owner ID, and is readable by.
    """
    user_is_none = user is None or user.id is None
    owner_id = None
    is_readable_by = None

    if user_is_none:
        curation_tier = determine_public_geneset_curation_tier(curation_tier)
        if only_my_genesets:
            raise UnauthorizedException()
    else:
        is_readable_by = user.id
        if only_my_genesets:
            owner_id = user.id

    return (
        curation_tier,
        owner_id,
        is_readable_by,
    )


def determine_public_geneset_curation_tier(
    curation_tier: Optional[Set[GenesetTier]] = None,
) -> Set[GenesetTier]:
    """Determine the curation tier for public geneset requests.

    Run this function when the user is None.

    :param curation_tier: The curation tier requested by the user.
    :return: The curation tier to use.
    :raises UnauthorizedException: If the user is not allowed to access the tier.
    """
    if curation_tier is None:
        curation_tier = {
            GenesetTier.TIER1,
            GenesetTier.TIER2,
            GenesetTier.TIER3,
            GenesetTier.TIER4,
        }
    elif curation_tier == {GenesetTier.TIER5}:
        raise UnauthorizedException()
    else:
        curation_tier = curation_tier - {GenesetTier.TIER5}

    return curation_tier


def get_visible_genesets(
    cursor: Cursor,
    user: Optional[User] = None,
    gs_id: Optional[int] = None,
    only_my_genesets: Optional[bool] = None,
    curation_tier: Optional[Set[GenesetTier]] = None,
    species: Optional[Species] = None,
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    publication_id: Optional[int] = None,
    pubmed_id: Optional[int] = None,
    gene_id_type: Optional[GeneIdentifier] = None,
    search_text: Optional[str] = None,
    ontology_term: Optional[str] = None,
    with_publication_info: bool = True,
    lte_count: Optional[int] = None,
    gte_count: Optional[int] = None,
    created_after: Optional[date] = None,
    created_before: Optional[date] = None,
    updated_after: Optional[date] = None,
    updated_before: Optional[date] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> dict:
    """Get genesets from the database.

    :param cursor: A database cursor.
    :param user: The user requesting the genesets.
    :param gs_id: Show only results with this geneset ID.
    :param only_my_genesets: Show only results owned by the user.
    :param curation_tier: Show only results of this curation tier.
    :param species: Show only results associated with this species.
    :param name: Show only results with this name.
    :param abbreviation: Show only results with this abbreviation.
    :param publication_id: Show only results with this publication ID (internal).
    :param pubmed_id: Show only results with this PubMed ID.
    :param gene_id_type: Show only results with this gene ID type.
    :param search_text: Return genesets that match this search text (using PostgreSQL
                        full-text search).
    :param ontology_term: Show only results associated with this ontology term.
    :param lte_count: less than or equal geneset count.
    :param gte_count: greater than or equal geneset count.
    :param updated_before: Show only results updated before this date.
    :param updated_after: Show only results updated after this date.
    :param created_before: Show only results created before this date.
    :param created_after: Show only results updated before this date.
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    :param with_publication_info: Include publication info in the return.
    """
    try:
        curation_tier, owner_id, is_readable_by = determine_geneset_access(
            user, curation_tier, only_my_genesets
        )

        results = db_geneset.get(
            cursor,
            is_readable_by=is_readable_by,
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
            ontology_term=ontology_term,
            lte_count=lte_count,
            gte_count=gte_count,
            created_after=created_after,
            created_before=created_before,
            updated_after=updated_after,
            updated_before=updated_before,
            limit=limit,
            offset=offset,
        )
        return {"data": results}

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


def get_geneset(
    cursor: Cursor, geneset_id: int, user: User, in_threshold: Optional[bool] = False
) -> dict:
    """Get a geneset by ID.

    :param cursor: DB cursor
    :param geneset_id: geneset identifier
    :param user: GW user
    :in_threshold: Optional[bool] = False,
    @return: dictionary response (geneset and genset values).
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
        if len(results) <= 0:
            return {"data": None}

        geneset = results[0]
        geneset_values = db_geneset_value.by_geneset_id(
            cursor=cursor, geneset_id=geneset_id, gsv_in_threshold=in_threshold
        )

        return {"geneset": geneset, "geneset_values": geneset_values}

    except Exception as err:
        logger.error(err)
        raise err


def get_geneset_gene_values(
    cursor: Cursor,
    geneset_id: int,
    user: User,
    gene_id_type: GeneIdentifier = None,
    in_threshold: Optional[bool] = False,
) -> dict:
    """Get a gene values for a given geneset ID.

    :param cursor: DB cursor
    :param geneset_id: geneset identifier
    :param user: GW user
    :param gene_id_type: gene identifier type object
    :param in_threshold: geneset’s threshold filter
    :return: dictionary response (geneset and genset values).
    """
    try:
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        ## Check genset exists and user can read it
        results = db_geneset.get(
            cursor,
            gs_id=geneset_id,
            is_readable_by=user.id,
            with_publication_info=False,
        )
        if len(results) <= 0:
            return {"data": None}

        # If gene id type is given, check gene species homology to
        # construct proper gene species mapping
        if gene_id_type is not None:
            geneset = results[0]
            geneset_values = get_gsv_w_gene_homology_update(
                cursor=cursor,
                geneset=geneset,
                gene_id_type=gene_id_type,
                in_threshold=in_threshold,
            )
        else:
            geneset_values = db_geneset_value.by_geneset_id(
                cursor, geneset_id, gsv_in_threshold=in_threshold
            )

        if geneset_values is None or len(geneset_values) <= 0:
            return {"data": None}

        genes_data = []
        for gsv in geneset_values:
            gene_value = {"symbol": gsv["ode_ref_id"], "value": float(gsv["gsv_value"])}
            genes_data.append(gene_value)

        return {"data": genes_data}

    except Exception as err:
        logger.error(err)
        raise err


def get_geneset_w_gene_id_type(
    cursor: Cursor,
    geneset_id: int,
    user: User,
    gene_id_type: GeneIdentifier,
    in_threshold: Optional[bool] = False,
) -> dict:
    """Get a geneset by ID and filter with gene identifier type.

    @param cursor: DB cursor
    @param geneset_id: geneset identifier
    @param user: GW user
    @param gene_id_type: gene identifier type object
    @param in_threshold: geneset’s threshold filter
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
        geneset_values = get_gsv_w_gene_homology_update(
            cursor=cursor,
            geneset=geneset,
            gene_id_type=gene_id_type,
            in_threshold=in_threshold,
        )

        return {
            "gene_identifier_type": gene_id_type.name,
            "geneset": geneset,
            "geneset_values": geneset_values,
        }

    except Exception as err:
        logger.error(err)
        raise err


def get_gsv_w_gene_homology_update(
    cursor: Cursor,
    geneset: dict,
    gene_id_type: GeneIdentifier,
    in_threshold: Optional[bool] = False,
) -> Iterable[dict]:
    """Check gene homology mapping and update it.

    @param cursor: DB cursor
    @param gene_id_type: geneset identifier
    @param in_threshold: geneset’s threshold filter
    @return: geneset value
    """
    mapping_across_species = False
    original_gene_id_type = gene_id_type
    genedb_sp_id = db_gene.gene_database_by_id(cursor, gene_id_type)[0]["sp_id"]

    if genedb_sp_id != 0 and geneset["species_id"] != genedb_sp_id:
        mapping_across_species = True
        gene_id_type = GeneIdentifier(7)

    geneset_values = db_geneset_value.by_geneset_id(
        cursor, geneset.get("id"), gene_id_type, gsv_in_threshold=in_threshold
    )

    if mapping_across_species:
        geneset_values = map_geneset_homology(
            cursor, geneset_values, original_gene_id_type
        )

    return geneset_values


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


def update_geneset_threshold(
    cursor: Cursor, geneset_id: int, geneset_score: GenesetScoreType, user: User
) -> dict:
    """Set geneset threshold if user is the owner."""
    try:
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        if not db_geneset.user_is_owner(
            cursor=cursor, user_id=user.id, geneset_id=geneset_id
        ):
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        db_threshold.set_geneset_threshold(
            cursor=cursor, geneset_id=geneset_id, geneset_score_type=geneset_score
        )
        return {}

    except Exception as err:
        logger.error(err)
        raise err


def get_geneset_ontology_terms(
    cursor: Cursor,
    geneset_id: int,
    user: User,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> dict:
    """Get geneset ontology terms by geneset id.

    :param cursor: DB cursor
    :param geneset_id: geneset identifier
    :param user: GW user
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    @return: dictionary response (ontology terms).
    """
    try:
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        is_gs_readable = db_geneset.is_readable(
            cursor=cursor, user_id=user.id, geneset_id=geneset_id
        )
        if is_gs_readable is False:
            return {"error": True, "message": message.INACCESSIBLE_OR_FORBIDDEN}

        results = db_ontology.by_geneset(
            cursor=cursor,
            geneset_id=geneset_id,
            limit=limit,
            offset=offset,
        )
        return {"data": results}

    except Exception as err:
        logger.error(err)
        raise err


def add_geneset_ontology_term(
    cursor: Cursor,
    geneset_id: int,
    term_ref_id: str,
    user: User,
    gso_ref_type: str = ONTO_GSO_REF_TYPE,
) -> dict:
    """Add ontology term to a geneset.

    :param cursor: DB cursor
    :param geneset_id: geneset identifier
    :param term_ref_id ref term identifier
    :param user: GW user
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    @return: persisted record  (geneset id, ontology term id).
    """
    try:
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        is_gs_readable = db_geneset.is_readable(
            cursor=cursor, user_id=user.id, geneset_id=geneset_id
        )
        if is_gs_readable is False:
            return {"error": True, "message": message.INACCESSIBLE_OR_FORBIDDEN}

        owner = db_geneset.user_is_owner(
            cursor=cursor, user_id=user.id, geneset_id=geneset_id
        )
        curator = user.role is AppRoles.curator

        if not owner and not curator:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        onto_term = db_ontology.by_ontology_term(
            cursor=cursor, onto_ref_term_id=term_ref_id
        )

        if onto_term is None:
            return {"error": True, "message": message.RECORD_NOT_FOUND_ERROR}

        results = db_ontology.add_ontology_term_to_geneset(
            cursor=cursor,
            geneset_id=geneset_id,
            ontology_term_id=onto_term.get("onto_id"),
            gso_ref_type=gso_ref_type,
        )
        return {"data": results}

    except errors.UniqueViolation:
        return {"error": True, "message": message.RECORD_EXISTS}

    except Exception as err:
        logger.error(err)
        raise err


def delete_geneset_ontology_term(
    cursor: Cursor,
    geneset_id: int,
    term_ref_id: str,
    user: User,
    gso_ref_type: str = ONTO_GSO_REF_TYPE,
) -> dict:
    """Delete ontology term from a geneset.

    :param cursor: DB cursor
    :param geneset_id: geneset identifier
    :param term_ref_id ref term identifier
    :param user: GW user
    :param limit: Limit the number of results.
    :param offset: Offset the results.
    @return: deleted record  (geneset id, ontology term id).
    """
    try:
        if user is None or user.id is None:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        is_gs_readable = db_geneset.is_readable(
            cursor=cursor, user_id=user.id, geneset_id=geneset_id
        )
        if is_gs_readable is False:
            return {"error": True, "message": message.INACCESSIBLE_OR_FORBIDDEN}

        owner = db_geneset.user_is_owner(
            cursor=cursor, user_id=user.id, geneset_id=geneset_id
        )
        curator = user.role is AppRoles.curator

        if not owner and not curator:
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        onto_term = db_ontology.by_ontology_term(
            cursor=cursor, onto_ref_term_id=term_ref_id
        )

        if onto_term is None:
            return {"error": True, "message": message.RECORD_NOT_FOUND_ERROR}

        results = db_ontology.delete_ontology_term_from_geneset(
            cursor=cursor,
            geneset_id=geneset_id,
            ontology_term_id=onto_term.get("onto_id"),
            gso_ref_type=gso_ref_type,
        )
        return {"data": results}

    except Exception as err:
        logger.error(err)
        raise err
