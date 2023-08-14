"""Endpoints related to genesets."""
from typing import Optional

from fastapi import APIRouter, Security, Depends, HTTPException

from geneweaver.api import dependencies as deps
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.db import geneset_value as db_geneset_value
from geneweaver.db import geneset as db_geneset
from geneweaver.db import gene as db_gene
from geneweaver.db.geneset import by_id, by_user_id, is_readable
from geneweaver.db.geneset_value import by_geneset_id
from geneweaver.db.user import by_sso_id
from geneweaver.core.schema.geneset import GenesetUpload


router = APIRouter(prefix="/genesets")


@router.get("")
def get_visible_genesets(
    user: UserInternal = Security(deps.full_user),
        cursor: Optional[deps.Cursor] = Depends(deps.cursor),
):
    """Get all visible genesets."""
    user_genesets = db_geneset.by_user_id(cursor, user.id)
    return {"genesets": user_genesets}


@router.get("/{geneset_id}")
def get_geneset(
    geneset_id: int,
    user: UserInternal = Security(deps.full_user),
    cursor: Optional[deps.Cursor] = Depends(deps.cursor),
):
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
):
    """Upload a geneset."""
    formatted_geneset_values = db_geneset_value.format_geneset_values_for_file_insert(
        geneset.gene_list
    )
    return {"geneset_id": 0}