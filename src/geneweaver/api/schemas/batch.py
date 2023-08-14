"""Module for defining schemas for batch endpoints."""
from typing import List, Optional

from pydantic import BaseModel, validator
from geneweaver.core.parse.score import parse_score

from geneweaver.api.schemas.messages import MessageResponse
from geneweaver.api.schemas.score import GenesetScoreType


class BatchResponse(BaseModel):
    """Class for defining a response containing batch results."""

    genesets: List[int]
    messages: MessageResponse


class Publication(BaseModel):
    authors: str
    title: str
    abstract: str
    journal: str
    volume: str
    pages: str
    month: str
    year: str
    pubmed: str


class GenesetValueInput(BaseModel):
    symbol: str
    value: float


class GenesetValue(BaseModel):
    ode_gene_id: str
    value: float
    ode_ref_id: str
    threshold: bool


class BatchUploadGeneset(BaseModel):
    score: GenesetScoreType
    # TODO: Use enum from core
    species: str
    gene_id_type: str
    pubmed_id: str
    private: bool = True
    curation_id: Optional[int] = None
    abbreviation: str
    name: str
    description: str
    values: List[GenesetValueInput]

    @validator("score", pre=True)
    def initialize_score(cls, v):
        return parse_score(v)

    @validator("private", pre=True)
    def private_to_bool(cls, v):
        return v.lower() != "public"

    @validator("curation_id", pre=True)
    def curation_id_to_int(cls, v, values):
        return 5 if values["private"] else 4
