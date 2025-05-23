"""Models for API requests."""

# ruff: noqa: ANN002, ANN003

from enum import Enum
from typing import Dict, Generic, Iterable, List, Optional, TypeVar

from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.core.schema.gene import Gene as GeneSchema
from geneweaver.core.schema.geneset import GeneValue as GeneValueSchema
from geneweaver.core.schema.species import Species as SpeciesSchema
from pydantic import AnyUrl, BaseModel

T = TypeVar("T")


class PagingLinks(BaseModel):
    """Schema for holding paging links."""

    first: Optional[AnyUrl] = None
    previous: Optional[AnyUrl] = None
    next_page: Optional[AnyUrl] = None
    last_page: Optional[AnyUrl] = None


class Paging(BaseModel):
    """Schema for paging information."""

    page: Optional[int] = None
    items: Optional[int] = None
    total_pages: Optional[int] = None
    total_items: Optional[int] = None
    links: Optional[PagingLinks] = None


class CollectionResponse(BaseModel):
    """Schema for API responses with collections."""

    data: List
    paging: Optional[Paging] = None


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


class GeneReturn(CollectionResponse):
    """Model for gene endpoint return."""

    data: List[GeneSchema]


class SpeciesReturn(CollectionResponse):
    """Model for Species endpoint return."""

    data: List[SpeciesSchema]


class GeneValueReturn(BaseModel):
    """Model for geneset values endpoint return."""

    data: List[GeneValueSchema]


class NewPubmedRecord(BaseModel):
    """Model returned for adding new pubmed info into DB."""

    pub_id: int
    pubmed_id: int


class GsPubSearchType(str, Enum):
    """Enum model for genesets and publication search types."""

    GENESETS = "genesets"
    PUBLICATIONS = "publications"


class SearchResponse(CollectionResponse, Generic[T]):
    """Model for search response endpoint."""

    data: List[T]

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the search response model.

        First argument is assigned to `data`.
        """
        if args:
            kwargs["data"] = args[0]
        super().__init__(**kwargs)


class CombinedSearchResponse(BaseModel, Generic[T]):
    """Model for combined search response endpoint."""

    object: Dict[str, List[T]]

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the combined search response model.

        First argument is assigned to `object`.
        """
        if args:
            kwargs["object"] = args[0]
        super().__init__(**kwargs)
