"""Models for API requests."""
from typing import Iterable, Optional

from geneweaver.core.enum import GeneIdentifier, Species
from pydantic import BaseModel


class GeneIdMappingResp(BaseModel):
    """Model for gene id mapping."""

    gene_ids_map: list[dict]


class GeneIdMappingReq(BaseModel):
    """Model for gene id mapping request."""

    source_ids: Iterable[str]
    target_gene_id_type: GeneIdentifier
    source_gene_id_type: Optional[GeneIdentifier] = None
    target_species: Optional[Species] = None
    source_species: Optional[Species] = None
