"""Endpoints related to genesets."""
import json
import os
import time
from tempfile import TemporaryDirectory
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Security
from fastapi.responses import FileResponse
from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.apimodels import gene_id_type_options
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.api.services import geneset as genset_service
from geneweaver.core.enum import GeneIdentifier
from geneweaver.core.schema.geneset import GenesetUpload
from geneweaver.db import geneset as db_geneset
from geneweaver.db import geneset_value as db_geneset_value

from . import message as api_message

router = APIRouter(prefix="/genesets")


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
    geneset_id: int,
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    # using int type and adding doc options here as using GeneIdentifier
    # won't produce the right docs for gene identifier options
    gene_id_type: Optional[int] = Query(
        None, description=f"Options: {gene_id_type_options}"
    ),
) -> dict:
    """Get a geneset by ID. Optional filter results by gene identifier type."""
    if gene_id_type:
        gene_identifier_type = get_gene_identifier_type(gene_id_type)
        response = genset_service.get_geneset_w_gene_id_type(
            cursor, geneset_id, user, gene_identifier_type
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
    geneset_id: int,
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
    temp_dir: TemporaryDirectory = Depends(deps.get_temp_dir),
    # using int type and adding doc options here as using
    # GeneIdentifier won't produce the right docs for gene identifier options
    gene_id_type: Optional[int] = Query(
        None, description=f"Options: {gene_id_type_options}"
    ),
) -> dict:
    """Export geneset into JSON file. Search by ID and optional gene identifier type."""
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Validate gene identifier type
    if gene_id_type:
        gene_identifier_type = get_gene_identifier_type(gene_id_type)
        response = genset_service.get_geneset_w_gene_id_type(
            cursor, geneset_id, user, gene_identifier_type
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


@router.post("")
def upload_geneset(
    geneset: GenesetUpload,
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> dict:
    """Upload a geneset."""
    db_geneset_value.format_geneset_values_for_file_insert(geneset.gene_list)
    return {"geneset_id": 0}


def get_gene_identifier_type(gene_id_type: int) -> GeneIdentifier:
    """Get a valid GeneIdentifier object. Raise HTTP exception if invalid value.

    @param gene_id_type: gene identifier type
    @return: GeneIdentifier obj or HTTP exception if invalid id value.
    """
    try:
        gene_identifier = GeneIdentifier(gene_id_type)
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail=f"{api_message.GENE_IDENTIFIER_TYPE_VALUE_ERROR}, "
            f"valid options= {gene_id_type_options}",
        ) from err
    return gene_identifier
