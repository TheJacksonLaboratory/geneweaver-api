"""Endpoints related to publications."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Security
from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.apimodels import NewPubmedRecord
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.api.services import publications as publication_service
from geneweaver.core.schema.publication import Publication
from jax.apiutils import CollectionResponse, Response
from typing_extensions import Annotated

from . import message as api_message

router = APIRouter(prefix="/publications", tags=["publications"])


@router.get("")
def get_publication(
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    publication_id: Annotated[
        int, Query(format="int64", minimum=0, maxiumum=9223372036854775807)
    ] = None,
    authors: Optional[str] = None,
    title: Optional[str] = None,
    abstract: Optional[str] = None,
    journal: Optional[str] = None,
    volume: Optional[str] = None,
    pages: Optional[str] = None,
    month: Optional[str] = None,
    year: Optional[str] = None,
    pubmed_id: Optional[str] = None,
    search_text: Annotated[
        Optional[str], Query(description=api_message.SEARCH_TEXT)
    ] = None,
    limit: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=1000,
            description=api_message.LIMIT,
        ),
    ] = 10,
    offset: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
            description=api_message.OFFSET,
        ),
    ] = None,
) -> CollectionResponse[Publication]:
    """Get all publication publications with optional filters."""
    response = publication_service.get(
        cursor,
        pub_id=publication_id,
        authors=authors,
        title=title,
        abstract=abstract,
        journal=journal,
        volume=volume,
        pages=pages,
        month=month,
        year=year,
        pubmed=pubmed_id,
        search_text=search_text,
        limit=limit,
        offset=offset,
    )

    return CollectionResponse(**response)


@router.get("/{publication_id}")
def get_publication_by_id(
    publication_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    as_pubmed_id: Optional[bool] = True,
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> Response[Publication]:
    """Get a publication by id."""
    if as_pubmed_id:
        response = publication_service.get_publication_by_pubmed_id(
            cursor, publication_id
        )
    else:
        response = publication_service.get_publication(cursor, publication_id)

    if response is None:
        raise HTTPException(status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR)

    return Response(response)


@router.put("/{publication_id}")
def add_publication(
    publication_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> Response[NewPubmedRecord]:
    """Add pubmed publication endpoint."""
    response = publication_service.add_pubmed_record(
        cursor=cursor, user=user, pubmed_id=str(publication_id)
    )

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)
        elif response.get("message") == api_message.RECORD_EXISTS:
            raise HTTPException(status_code=412, detail=api_message.RECORD_EXISTS)
        elif response.get("message") == api_message.PUBMED_RETRIEVING_ERROR:
            raise HTTPException(
                status_code=422, detail=api_message.PUBMED_RETRIEVING_ERROR
            )
        else:
            raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    return Response(response)
