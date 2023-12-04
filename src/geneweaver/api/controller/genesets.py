"""Endpoints related to genesets."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.core.schema.geneset import GenesetUpload
from geneweaver.db import geneset as db_geneset
from geneweaver.db import geneset_value as db_geneset_value
from geneweaver.db.geneset import is_readable

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
) -> dict:
    """Get a geneset by ID."""
    if not is_readable(cursor, user.id, geneset_id):
        raise HTTPException(status_code=403, detail="Forbidden")

    geneset = db_geneset.by_id(cursor, geneset_id)
    geneset_values = db_geneset_value.by_geneset_id(cursor, geneset_id)
    return {"geneset": geneset, "geneset_values": geneset_values}


@router.post("")
def upload_geneset(
    geneset: GenesetUpload,
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
) -> dict:
    """Upload a geneset."""
    db_geneset_value.format_geneset_values_for_file_insert(geneset.gene_list)
    return {"geneset_id": 0}
