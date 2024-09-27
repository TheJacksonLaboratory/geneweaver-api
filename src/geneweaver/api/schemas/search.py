"""Schema for search API."""

from datetime import date
from typing import Optional, Set

from geneweaver.core.enum import GenesetTier, ScoreType, Species
from pydantic import BaseModel, Field


class GenesetSearch(BaseModel):
    """Schema for geneset search."""

    search_text: str
    publication_id: Optional[int] = None
    pubmed_id: Optional[int] = None
    species: Optional[Set[Species]] = None
    curation_tier: Optional[Set[GenesetTier]] = None
    score_type: Optional[Set[ScoreType]] = None
    lte_count: Optional[int] = None
    gte_count: Optional[int] = None
    created_before: Optional[date] = None
    created_after: Optional[date] = None
    updated_before: Optional[date] = None
    updated_after: Optional[date] = None
    limit: Optional[int] = Field(25, ge=0, le=1000)
    offset: Optional[int] = None
