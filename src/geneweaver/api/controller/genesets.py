"""Endpoints related to genesets."""
import json
import os
import time
from tempfile import TemporaryDirectory
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Security
from fastapi.responses import FileResponse
from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.api.services import geneset as genset_service
from geneweaver.core.enum import GeneIdentifier
from geneweaver.db import geneset as db_geneset
from typing_extensions import Annotated

from . import message as api_message

router = APIRouter(prefix="/genesets", tags=["genesets"])


@router.get("")
def get_visible_genesets(
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> dict:
    """Get all visible genesets."""
    user_genesets = db_geneset.by_user_id(cursor, user.id)
    return {"genesets": user_genesets}


@router.get("/{geneset_id}")
def get_geneset(
    geneset_id: Annotated[
        int, Path(format="int64", minimum=0, maxiumum=9223372036854775807)
    ],
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    gene_id_type: Optional[GeneIdentifier] = None,
) -> dict:
    """Get a geneset by ID. Optional filter results by gene identifier type."""
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
) -> FileResponse:
    """Export geneset into JSON file. Search by ID and optional gene identifier type."""
    timestr = time.strftime("%Y%m%d-%H%M%S")

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
    temp_file_path = os.path.join(temp_dir, geneset_filename)
    with open(temp_file_path, "w") as f:
        json.dump(response, f, default=str)

    # Return as a download
    return FileResponse(
        path=temp_file_path,
        media_type="application/octet-stream",
        filename=geneset_filename,
    )
