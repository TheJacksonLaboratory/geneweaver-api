"""Endpoints related to publications."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from geneweaver.api import dependencies as deps
from geneweaver.api.services import publications as publication_service
from typing_extensions import Annotated

from . import message as api_message

router = APIRouter(prefix="/publications", tags=["publications"])


@router.get("/{pub_id}")
def get_publication_by_id(
    pub_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> dict:
    """Get a publication by id."""
    response = publication_service.get_publication(cursor, pub_id)

    if response.get("publication") is None:
        raise HTTPException(status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR)

    return response


@router.get("/pubmed/{pubmed_id}")
def get_publication_by_pubmed_id(
    pubmed_id: str, cursor: Optional[deps.Cursor] = Depends(deps.cursor)
) -> dict:
    """Get a publication by id."""
    response = publication_service.get_publication_by_pubmed_id(cursor, pubmed_id)

    if response.get("publication") is None:
        raise HTTPException(status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR)

    return response
