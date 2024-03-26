"""Endpoints related to genes."""
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.apimodels import (
    GeneIdHomologReq,
    GeneIdMappingAonReq,
    GeneIdMappingReq,
    GeneIdMappingResp,
)
from geneweaver.api.services import genes as genes_service
from geneweaver.core.enum import GeneIdentifier, Species
from typing_extensions import Annotated

from . import message as api_message

router = APIRouter(prefix="/genes", tags=["genes"])


@router.get("")
def get_genes(
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    reference_id: Annotated[
        Optional[str], Query(description=api_message.GENE_REFERENCE)
    ] = None,
    gene_database: Optional[GeneIdentifier] = None,
    species: Optional[Species] = None,
    preferred: Annotated[
        Optional[bool], Query(description=api_message.GENE_PREFERRED)
    ] = None,
    limit: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=1000,
            description=api_message.LIMIT,
        ),
    ] = None,
    offset: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
            description=api_message.OFFSET,
        ),
    ] = None,
) -> dict:
    """Get geneweaver list of genes."""
    if limit is None:
        limit = 100

    response = genes_service.get_genes(
        cursor, reference_id, gene_database, species, preferred, limit, offset
    )
    return response


@router.get("/{gene_id}/preferred")
def get_gene_preferred(
    gene_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> dict:
    """Get preferred gene for a given gene ode_id."""
    response = genes_service.get_gene_preferred(cursor, gene_id)
    return response


@router.post("/homologs", response_model=GeneIdMappingResp, deprecated=True)
def get_related_gene_ids(
    gene_id_mapping: GeneIdHomologReq,
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> GeneIdMappingResp:
    """Get homologous gene ids given list of gene ids."""
    response = genes_service.get_homolog_ids(
        cursor,
        gene_id_mapping.source_ids,
        gene_id_mapping.target_gene_id_type,
        gene_id_mapping.source_gene_id_type,
        gene_id_mapping.target_species,
        gene_id_mapping.source_species,
    )

    resp_id_map = response.get("ids_map")
    gene_id_mapping_resp = GeneIdMappingResp(gene_ids_map=resp_id_map)

    return gene_id_mapping_resp


@router.post("/mappings", response_model=GeneIdMappingResp)
def get_genes_mapping(
    gene_id_mapping: GeneIdMappingReq,
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> GeneIdMappingResp:
    """Get gene ids mapping."""
    response = genes_service.get_gene_mapping(
        cursor,
        gene_id_mapping.source_ids,
        gene_id_mapping.species,
        gene_id_mapping.target_gene_id_type,
    )

    resp_id_map = response.get("ids_map")
    gene_id_mapping_resp = GeneIdMappingResp(gene_ids_map=resp_id_map)

    return gene_id_mapping_resp


@router.post("/mappings/aon", response_model=GeneIdMappingResp)
def get_genes_mapping_aon(
    gene_id_mapping: GeneIdMappingAonReq,
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> GeneIdMappingResp:
    """Get gene ids mapping given list of gene ids and target gene identifier type."""
    response = genes_service.get_gene_aon_mapping(
        cursor, gene_id_mapping.source_ids, gene_id_mapping.species
    )

    resp_id_map = response.get("ids_map")
    gene_id_mapping_resp = GeneIdMappingResp(gene_ids_map=resp_id_map)

    return gene_id_mapping_resp
