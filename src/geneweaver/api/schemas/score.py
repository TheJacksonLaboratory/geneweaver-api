"""Pydantic schemas for score types.

NOTE: These schemas might be duplicates of schemas available in geneweaver.core.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ScoreType(Enum):
    """Enum for defining score types."""

    P_VALUE = 1
    Q_VALUE = 2
    BINARY = 3
    CORRELATION = 4
    EFFECT = 5


class GenesetScoreType(BaseModel):
    """Pydantic schema for geneset score type."""

    score_type: ScoreType
    threshold_low: Optional[float] = None
    threshold: float = 0.05
