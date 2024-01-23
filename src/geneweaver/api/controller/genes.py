"""Endpoints related to genes."""
from typing import Optional

from fastapi import APIRouter, Depends
from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.apimodels import GeneIdMappingReq, GeneIdMappingResp
from geneweaver.api.services import genes as genes_service

router = APIRouter(prefix="/genes")


@router.post("/homologous-ids", response_model=GeneIdMappingResp)
def get_related_gene_ids(
    gene_id_mapping: GeneIdMappingReq,
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> GeneIdMappingResp:
    """Get homologous gene ids given list of gene ids."""
    response = genes_service.get_gene_mapping(
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
