"""Service functions for dealing with genesets."""
from typing import Iterable

from fastapi.logger import logger
from geneweaver.api.controller import message
from geneweaver.api.schemas.auth import User
from geneweaver.core.enum import GeneIdentifier
from geneweaver.db import gene as db_gene
from geneweaver.db import geneset as db_geneset
from geneweaver.db import geneset_value as db_geneset_value
from geneweaver.db.geneset import is_readable as db_is_readable
from psycopg import Cursor


def get_geneset(cursor: Cursor, geneset_id: int, user: User) -> dict:
    """Get a geneset by ID.

    @param cursor: DB cursor
    @param geneset_id: geneset identifier
    @param user: GW user
    @return: dictionary response (geneset and genset values).
    """
    try:
        if not is_geneset_readable_by_user(cursor, geneset_id, user):
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        geneset = db_geneset.by_id(cursor, geneset_id)
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
        if not is_geneset_readable_by_user(cursor, geneset_id, user):
            return {"error": True, "message": message.ACCESS_FORBIDDEN}

        geneset = db_geneset.by_id(cursor, geneset_id)

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


def is_geneset_readable_by_user(cursor: Cursor, geneset_id: int, user: User) -> bool:
    """Check if the user can read the geneset from DB.

    @param cursor: DB cursor object
    @param geneset_id: geneset identifier
    @param user: GW user
    @return: True if geneset is readable by user.
    """
    readable: bool = False
    try:
        readable = db_is_readable(cursor, user.id, geneset_id)
    except Exception as err:
        logger.error(err)
        raise err

    return readable
