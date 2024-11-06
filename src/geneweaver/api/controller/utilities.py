"""Utilities for FastAPI Controller."""

from fastapi import HTTPException

from . import message as api_message

EXCEPTION_MAP = {
    api_message.ACCESS_FORBIDDEN: HTTPException(
        status_code=403, detail=api_message.ACCESS_FORBIDDEN
    ),
    api_message.INACCESSIBLE_OR_FORBIDDEN: HTTPException(
        status_code=404, detail=api_message.INACCESSIBLE_OR_FORBIDDEN
    ),
    api_message.RECORD_NOT_FOUND_ERROR: HTTPException(
        status_code=404, detail=api_message.RECORD_NOT_FOUND_ERROR
    ),
    api_message.RECORD_EXISTS: HTTPException(
        status_code=412, detail=api_message.RECORD_EXISTS
    ),
}


def raise_http_error(response: dict) -> None:
    """Raise HTTPException based on response message.

    :param response: dict

    raises: HTTPException if "error" key is in response dict.
    """
    if "error" in response:
        try:
            raise EXCEPTION_MAP[response.get("message")]
        except KeyError:
            raise HTTPException(
                status_code=500, detail=api_message.UNEXPECTED_ERROR
            ) from None
