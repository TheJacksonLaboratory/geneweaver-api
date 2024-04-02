"""Endpoints related to species."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from geneweaver.api import dependencies as deps
from geneweaver.api.services import species as species_service
from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.core.schema.species import Species as SpeciesSchema
from typing_extensions import Annotated

router = APIRouter(prefix="/species", tags=["species"])


@router.get("")
def get_species(
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    taxonomy_id: Annotated[
        Optional[int], Query(format="int64", minimum=0, maxiumum=9223372036854775807)
    ] = None,
    reference_gene_id_type: Optional[GeneIdentifier] = None,
) -> List[SpeciesSchema]:
    """Get species."""
    return species_service.get_species(cursor, taxonomy_id, reference_gene_id_type)


@router.get("/{species_id}")
def get_species_by_id(
    species_id: Species, cursor: Optional[deps.Cursor] = Depends(deps.cursor)
) -> SpeciesSchema:
    """Get species."""
    return species_service.get_species_by_id(cursor, species_id)
