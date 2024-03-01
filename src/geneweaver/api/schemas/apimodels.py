"""Models for API requests."""
from typing import Iterable, List, Optional

from geneweaver.core.enum import GeneIdentifier, Species
from pydantic import BaseModel


class GeneIdMappingResp(BaseModel):
    """Model for gene id mapping response."""

    gene_ids_map: list[dict]


class GeneIdHomologReq(BaseModel):
    """Model for homolog gene id mapping request."""

    source_ids: Iterable[str]
    target_gene_id_type: GeneIdentifier
    source_gene_id_type: Optional[GeneIdentifier] = None
    target_species: Optional[Species] = None
    source_species: Optional[Species] = None


class GeneIdMappingReq(BaseModel):
    """Model for gene id mapping request."""

    source_ids: List[str]
    target_gene_id_type: GeneIdentifier
    species: Species


class GeneIdMappingAonReq(BaseModel):
    """Model for AON gene id mapping request."""

    source_ids: List[str]
    species: Species
