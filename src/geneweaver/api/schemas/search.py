"""Schema for search API."""

from datetime import date
from typing import Optional

from geneweaver.db.utils import (
    GenesetScoreTypeOrScoreTypes,
    GenesetTierOrTiers,
    SpeciesOrSpeciesSet,
)
from pydantic import BaseModel


class GenesetSearch(BaseModel):
    """Schema for geneset search."""

    search_text: str
    publication_id: Optional[int] = (None,)
    pubmed_id: Optional[int] = (None,)
    species: Optional[SpeciesOrSpeciesSet] = (None,)
    curation_tier: Optional[GenesetTierOrTiers] = (None,)
    score_type: Optional[GenesetScoreTypeOrScoreTypes] = (None,)
    lte_count: Optional[int] = (None,)
    gte_count: Optional[int] = (None,)
    created_before: Optional[date] = (None,)
    created_after: Optional[date] = (None,)
    updated_before: Optional[date] = (None,)
    updated_after: Optional[date] = (None,)
    limit: Optional[int] = (25,)
    offset: Optional[int] = (0,)
