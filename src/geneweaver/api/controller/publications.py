"""Endpoints related to publications."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from geneweaver.api import dependencies as deps
from geneweaver.api.services import publications as publication_service
from geneweaver.core.schema.publication import Publication
from typing_extensions import Annotated

from . import message as api_message

router = APIRouter(prefix="/publications", tags=["publications"])


@router.get("/{publication_id}")
def get_publication_by_id(
    publication_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    as_pubmed_id: Optional[bool] = True,
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> Publication:
    """Get a publication by id."""
    if as_pubmed_id:
        response = publication_service.get_publication_by_pubmed_id(
            cursor, publication_id
        )
    else:
        response = publication_service.get_publication(cursor, publication_id)

    if response is None:
        raise HTTPException(status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR)

    return response
