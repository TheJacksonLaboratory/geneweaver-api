"""API Controller definition for batch processing."""
from typing import Optional

from fastapi import APIRouter, UploadFile, Security

from geneweaver.api.core import deps
from geneweaver.api.schemas.auth import UserInternal
from geneweaver.api.schemas.batch import BatchResponse
from geneweaver.api.services.parse.batch import process_batch_file

router = APIRouter(prefix="/batch")


@router.post(path="")
async def batch(
    batch_file: UploadFile,
    curation_group_id: Optional[int] = None,
    user: UserInternal = Security(deps.auth.get_user_strict),
) -> BatchResponse:
    """Submit a batch file for processing."""
    user_id = 1  # TODO: Get user ID from session
    genesets, user_messages, system_messages = await process_batch_file(
        batch_file, user_id
    )

    return {
        "genesets": genesets,
        "messages": {
            "user_messages": user_messages,
            "system_messages": system_messages,
        },
    }
