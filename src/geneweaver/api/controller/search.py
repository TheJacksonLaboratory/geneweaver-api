"""Endpoints related to searching."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Security
from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.apimodels import GsPubSearchType, SeachResponse
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.api.services import geneset as genset_service
from geneweaver.api.services import publications as publication_service
from typing_extensions import Annotated

from . import message as api_message

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search(
    entities: Annotated[
        List[GsPubSearchType], Query(description=api_message.GS_PUB_SEARCH_TEXT)
    ],
    search_text: Annotated[str, Query(description=api_message.SEARCH_TEXT)],
    user: UserInternal = Security(deps.optional_full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
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
) -> SeachResponse:
    """Search genesets and publications."""
    data = {}
    response = SeachResponse(data=data)
    if "genesets" in entities:
        geneset_response = genset_service.get_visible_genesets(
            cursor=cursor,
            user=user,
            search_text=search_text,
            limit=limit,
            offset=offset,
        )

        data["geneset"] = geneset_response.get("data")

    if "publications" in entities:
        pub_response = publication_service.get(
            cursor,
            search_text=search_text,
            limit=limit,
            offset=offset,
        )

        data["publications"] = pub_response.get("data")

    response.data = data

    return response
