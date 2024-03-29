"""Pytest fixtures for the batch parsing service tests."""

from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile

from tests.services import const


# Create a pytest fixture for the mocked UploadFile
@pytest.fixture()
def mock_upload_file():
    """Provide a mocked UploadFile object."""
    mock_file = AsyncMock(spec=UploadFile)
    return mock_file  # provide the mock object to the test


@pytest.fixture(
    params=[
        const.EXAMPLE_BATCH_FILE,
        "\n".join(const.EXAMPLE_BATCH_FILE.splitlines()[:124]),
        "\r".join(const.EXAMPLE_BATCH_FILE.splitlines()[:124]),
        "\n".join(const.EXAMPLE_BATCH_FILE.splitlines()[:309]),
        "\r".join(const.EXAMPLE_BATCH_FILE.splitlines()[:309]),
    ]
)
def example_batch_file_contents(request) -> str:
    """Provide the contents of the example batch file."""
    return request.param
