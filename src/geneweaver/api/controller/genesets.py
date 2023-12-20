"""Endpoints related to genesets."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.logger import logger
from geneweaver.core.schema.geneset import GenesetUpload
from geneweaver.db import geneset as db_geneset
from geneweaver.db import geneset_value as db_geneset_value

from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.api.services import geneset as genset_service
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
    cursor: Optional[deps.Cursor] = Depends(deps.cursor)
) -> dict:
    """Get a geneset by ID."""
    try:
        response = genset_service.get_geneset(geneset_id, user, cursor)

    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    if "error" in response:
        if response.get("message") == api_message.ACCESS_FORBIDEN:
            raise HTTPException(status_code=403, detail=api_message.ACCESS_FORBIDEN)
        else:
            raise HTTPException(status_code=500, detail=api_message.UNEXPECTED_ERROR)

    return response

@router.post("")
def upload_geneset(
    geneset: GenesetUpload,
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> dict:
    """Upload a geneset."""
    db_geneset_value.format_geneset_values_for_file_insert(geneset.gene_list)
    return {"geneset_id": 0}
