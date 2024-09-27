"""Endpoints related to genesets."""

import json
from datetime import date, datetime
from tempfile import TemporaryDirectory
from typing import Optional, Set

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Security
from fastapi.responses import FileResponse, StreamingResponse
from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.apimodels import GeneValueReturn, SearchResponse
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.api.schemas.search import GenesetSearch
from geneweaver.api.services import geneset as genset_service
from geneweaver.api.services import publications as publication_service
from geneweaver.core.enum import GeneIdentifier, GenesetTier, Species
from geneweaver.core.schema.score import GenesetScoreType, ScoreType
from geneweaver.db import search as db_search
from typing_extensions import Annotated

from . import message as api_message

router = APIRouter(prefix="/genesets", tags=["genesets"])


@router.get("")
def get_visible_genesets(
    cursor: deps.CursorDep,
    user: deps.OptionalFullUserDep,
    gs_id: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
            description=api_message.GENESET_ID,
        ),
    ] = None,
    only_my_genesets: Annotated[
        Optional[bool], Query(description=api_message.ONLY_MY_GS)
    ] = False,
    curation_tier: Annotated[Optional[Set[GenesetTier]], Query()] = None,
    species: Optional[Species] = None,
    name: Annotated[Optional[str], Query(description=api_message.NAME)] = None,
    abbreviation: Annotated[
        Optional[str], Query(description=api_message.ABBREVIATION)
    ] = None,
    publication_id: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
            description=api_message.PUBLICATION_ID,
        ),
    ] = None,
    pubmed_id: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
            description=api_message.PUBMED_ID,
        ),
    ] = None,
    gene_id_type: Optional[GeneIdentifier] = None,
    ontology_term: Optional[str] = None,
    search_text: Annotated[
        Optional[str], Query(description=api_message.SEARCH_TEXT)
    ] = None,
    with_publication_info: Annotated[
        bool, Query(description=api_message.ONLY_MY_GS)
    ] = True,
    score_type: Annotated[Optional[Set[ScoreType]], Query()] = None,
    size_less_than: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
            description=api_message.GENESET_SIZE,
        ),
    ] = None,
    size_greater_than: Annotated[
        Optional[int],
        Query(
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
            description=api_message.GENESET_SIZE,
        ),
    ] = None,
    created_after: Annotated[date, Query(description=api_message.CREATE_DATE)] = None,
    created_before: Annotated[date, Query(description=api_message.CREATE_DATE)] = None,
    updated_after: Annotated[date, Query(description=api_message.UPDATE_DATE)] = None,
    updated_before: Annotated[date, Query(description=api_message.UPDATE_DATE)] = None,
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
) -> dict:
    """Get all visible genesets."""
    response = genset_service.get_visible_genesets(
        cursor=cursor,
        user=user,
        gs_id=gs_id,
        curation_tier=curation_tier,
        species=species,
        name=name,
        abbreviation=abbreviation,
        publication_id=publication_id,
        pubmed_id=pubmed_id,
        gene_id_type=gene_id_type,
        search_text=search_text,
        with_publication_info=with_publication_info,
        ontology_term=ontology_term,
        only_my_genesets=only_my_genesets,
        score_type=score_type,
        lte_count=size_less_than,
        gte_count=size_greater_than,
        created_after=created_after,
        created_before=created_before,
        updated_after=updated_after,
        updated_before=updated_before,
        limit=limit,
        offset=offset,
    )

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)
        else:
            raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    return response


@router.get("/search")
def search(
    geneset_search: Annotated[GenesetSearch, Query()],
    user: UserInternal = Security(deps.optional_full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> SearchResponse:
    """Search genesets."""
    return SearchResponse(
        db_search.genesets(
            cursor,
            is_readable_by=0 if user is None else user.user_id,
            **geneset_search.model_dump(exclude_none=True),
        )
    )


@router.get("/{geneset_id}")
def get_geneset(
    geneset_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    gene_id_type: Optional[GeneIdentifier] = None,
    in_threshold: Optional[bool] = None,
) -> dict:
    """Get a geneset by ID. Optional filter results by gene identifier type."""
    if gene_id_type:
        response = genset_service.get_geneset_w_gene_id_type(
            cursor, geneset_id, user, gene_id_type
        )
    else:
        response = genset_service.get_geneset(
            cursor=cursor, geneset_id=geneset_id, user=user, in_threshold=in_threshold
        )

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)
        else:
            raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    return response


@router.get("/{geneset_id}/values")
def get_geneset_values(
    geneset_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    gene_id_type: Optional[GeneIdentifier] = None,
    in_threshold: Optional[bool] = None,
) -> GeneValueReturn:
    """Get geneset gene values by geneset ID."""
    response = genset_service.get_geneset_gene_values(
        cursor=cursor,
        geneset_id=geneset_id,
        user=user,
        gene_id_type=gene_id_type,
        in_threshold=in_threshold,
    )

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)
        else:
            raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    if response.get("data") is None:
        raise HTTPException(
            status_code=404, detail=api_message.INACCESSIBLE_OR_FORBIDDEN
        )

    return response


@router.get("/{geneset_id}/file", response_class=FileResponse)
def get_export_geneset_by_id_type(
    geneset_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    temp_dir: TemporaryDirectory = Depends(deps.get_temp_dir),
    gene_id_type: Optional[GeneIdentifier] = None,
) -> StreamingResponse:
    """Export geneset into JSON file. Search by ID and optional gene identifier type."""
    current_datetime = datetime.now()
    timestr = current_datetime.strftime("%Y%m%d-%H%M%S")

    # Validate gene identifier type
    if gene_id_type:
        response = genset_service.get_geneset_w_gene_id_type(
            cursor, geneset_id, user, gene_id_type
        )
    else:
        response = genset_service.get_geneset(cursor, geneset_id, user)

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)
        else:
            raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    id_type = response.get("gene_identifier_type")
    if id_type:
        geneset_filename = f"geneset_{geneset_id}_{id_type}_{timestr}.json"
    else:
        geneset_filename = f"geneset_{geneset_id}_{timestr}.json"

    # Write the data to temp file
    from io import StringIO

    buffer = StringIO()

    json.dump(response, buffer, default=str)

    buffer.seek(0)

    # Return as a download
    return StreamingResponse(
        buffer,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={geneset_filename}"},
    )


@router.get("/{geneset_id}/metadata")
def get_geneset_metadata(
    geneset_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    include_pub_info: Optional[bool] = False,
) -> dict:
    """Get a geneset metadata by geneset id."""
    response = genset_service.get_geneset_metadata(
        cursor, geneset_id, user, include_pub_info
    )

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)
        else:
            raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    return response


@router.get("/{geneset_id}/publication")
def get_publication_for_geneset(
    geneset_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> dict:
    """Get the publication associated with the geneset."""
    geneset_resp = genset_service.get_geneset_metadata(cursor, geneset_id, user, True)

    if "error" in geneset_resp:
        if geneset_resp.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)
        else:
            raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    geneset = geneset_resp.get("geneset")
    if geneset is None:
        raise HTTPException(status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR)

    pub_id = geneset.get("publication_id")
    if pub_id is None:
        raise HTTPException(status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR)

    pub_resp = publication_service.get_publication(cursor, pub_id)

    if pub_resp is None:
        raise HTTPException(status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR)

    return pub_resp


@router.put("/{geneset_id}/threshold", status_code=204)
def put_geneset_threshold(
    geneset_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    gene_score_type: GenesetScoreType,
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> None:
    """Set geneset threshold for geneset owner."""
    response = genset_service.update_geneset_threshold(
        cursor, geneset_id, gene_score_type, user
    )

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)


@router.get("/{geneset_id}/ontologies")
def get_geneset_ontology_terms(
    geneset_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    user: UserInternal = Security(deps.full_user),
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
) -> dict:
    """Get geneset ontology terms."""
    terms_resp = genset_service.get_geneset_ontology_terms(
        cursor, geneset_id, user, limit, offset
    )

    if "error" in terms_resp:
        if terms_resp.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)

        if terms_resp.get("message") == api_message.INACCESSIBLE_OR_FORBIDDEN:
            raise HTTPException(
                status_code=404, detail=api_message.INACCESSIBLE_OR_FORBIDDEN
            )

    return terms_resp


@router.put("/{geneset_id}/ontologies", status_code=204)
def put_geneset_ontology_term(
    geneset_id: Annotated[
        int,
        Path(
            description=api_message.GENESET_ID,
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
        ),
    ],
    ontology_id: Annotated[str, Query(description=api_message.ONTOLOGY_ID)],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> None:
    """Set geneset threshold for geneset owner."""
    response = genset_service.add_geneset_ontology_term(
        cursor=cursor,
        geneset_id=geneset_id,
        term_ref_id=ontology_id,
        user=user,
    )

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)

        if response.get("message") == api_message.RECORD_NOT_FOUND_ERROR:
            raise HTTPException(
                status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR
            )

        if response.get("message") == api_message.RECORD_EXISTS:
            raise HTTPException(status_code=412, detail=api_message.RECORD_EXISTS)

        if response.get("message") == api_message.INACCESSIBLE_OR_FORBIDDEN:
            raise HTTPException(
                status_code=404, detail=api_message.INACCESSIBLE_OR_FORBIDDEN
            )


@router.delete("/{geneset_id}/ontologies/{ontology_id}", status_code=204)
def delete_geneset_ontology_term(
    geneset_id: Annotated[
        int,
        Path(
            description=api_message.GENESET_ID,
            format="int64",
            minimum=0,
            maxiumum=9223372036854775807,
        ),
    ],
    ontology_id: Annotated[str, Path(description=api_message.ONTOLOGY_ID)],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> None:
    """Set geneset threshold for geneset owner."""
    response = genset_service.delete_geneset_ontology_term(
        cursor=cursor,
        geneset_id=geneset_id,
        term_ref_id=ontology_id,
        user=user,
    )

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDDEN)

        if response.get("message") == api_message.RECORD_NOT_FOUND_ERROR:
            raise HTTPException(
                status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR
            )

        if response.get("message") == api_message.INACCESSIBLE_OR_FORBIDDEN:
            raise HTTPException(
                status_code=404, detail=api_message.INACCESSIBLE_OR_FORBIDDEN
            )
