"""Models for API requests."""
from typing import Iterable, List, Optional

from geneweaver.core.enum import GeneIdentifier, Species
from pydantic import BaseModel


class GeneIdHomologReq(BaseModel):
    """Model for homolog gene id mapping request."""

    source_ids: Iterable[str]
    target_gene_id_type: GeneIdentifier
    source_gene_id_type: Optional[GeneIdentifier] = None
    target_species: Optional[Species] = None
    source_species: Optional[Species] = None

class GeneIdHomologResp(BaseModel):
    """Model for homolog gene id mapping."""

    gene_ids_map: list[dict]

class GeneIdMappingReq(BaseModel):
    """Model for gene id mapping request."""

    source_ids: List[str]
    target_gene_id_type: GeneIdentifier
    species: Species

class GeneIdMappingResp(BaseModel):
    """Model for gene id mapping."""

    gene_ids_map: list[dict]


class GeneIdMappingAonReq(BaseModel):
    """Model for AON gene id mapping request."""

    source_ids: List[str]
    target_species: Species

class GeneIdMappingAonResp(BaseModel):
    """Model for gene id mapping."""

    gene_ids_map: list[dict]
    species: Species

