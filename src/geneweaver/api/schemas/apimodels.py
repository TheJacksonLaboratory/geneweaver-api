"""Models for API requests."""
from typing import Iterable, Optional

from fastapi import Query
from geneweaver.core.enum import GeneIdentifier, Species
from pydantic import BaseModel

gene_id_type_options = [f"{choice.name} ({choice.value})" for choice in GeneIdentifier]
species_type_options = [f"{choice.name} ({choice.value})" for choice in Species]


class GeneIdMappingResp(BaseModel):
    """Model for gene id mapping."""

    gene_ids_map: list


class GeneIdMappingReq(BaseModel):
    """Model for gene id mapping request."""

    source_ids: Iterable[str]
    target_gene_id_type: GeneIdentifier = Query(
        None, description=f"Options: {gene_id_type_options}"
    )
    source_gene_id_type: Optional[GeneIdentifier] = Query(
        None, description=f"Options: {gene_id_type_options}"
    )
    target_species: Optional[Species] = Query(
        None, description=f"Options: {species_type_options}"
    )
    source_species: Optional[Species] = Query(
        None, description=f"Options: {species_type_options}"
    )
