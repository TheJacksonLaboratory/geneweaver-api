"""Tests for geneset API."""
from unittest.mock import patch

import pytest

from tests.controllers.conftest import test_data


@patch("geneweaver.api.services.geneset.get_geneset")
@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_response(mock_genset_is_readable, mock_get_genenset, client):
    """Test get geneset ID data response."""
    mock_genset_is_readable.return_value = True
    mock_get_genenset.return_value = test_data

    response = client.get("/api/genesets/1234")
    assert response.status_code == 200
    assert response.json() == test_data


@patch("geneweaver.api.services.geneset.db_is_readable")
def test_get_geneset_forbidden(mock_genset_is_readable, client):
    """Test forbidden response."""
    mock_genset_is_readable.return_value = False
    response = client.get("/api/genesets/1234")

    assert response.json() == {"detail": "Forbidden"}
    assert response.status_code == 403


@patch("geneweaver.api.services.geneset.db_is_readable")
def test_get_geneset_unexpected_error(mock_genset_is_readable, client):
    """Test unexpected error response."""
    mock_genset_is_readable.side_effect = Exception

    with pytest.raises(expected_exception=Exception):
        client.get("/api/genesets/1234")
