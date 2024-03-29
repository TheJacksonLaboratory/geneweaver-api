"""Module for defining schemas for batch endpoints."""

from typing import List

from geneweaver.api.schemas.messages import MessageResponse
from pydantic import BaseModel


class BatchResponse(BaseModel):
    """Class for defining a response containing batch results."""

    genesets: List[int]
    messages: MessageResponse
