"""Tests for geneset API."""

import importlib.resources
import json
from unittest.mock import Mock, patch

import psycopg
import pytest
from fastapi.testclient import TestClient
from geneweaver.api.dependencies import cursor, full_user
from geneweaver.api.main import app

client = TestClient(app)

### Load test data
# Opening JSON file
str_json = importlib.resources.read_text("tests.data", "response_geneset_1234.json")
# returns JSON string as a dictionary
test_data = json.loads(str_json)

response_mock = Mock()
response_mock.status_code = 200
response_mock.json.return_value = test_data


### Mock dependencies
def mock_full_user() -> Mock:
    """User auth mock."""
    m1 = Mock()
    return m1.AsyncMock()


def mock_cursor() -> psycopg.Cursor:
    """DB cursor mock."""
    m2 = Mock()
    return m2.AsyncMock()


app.dependency_overrides.update({full_user: mock_full_user, cursor: mock_cursor})


@patch.object(client, "get", return_value=response_mock)
def test_get_geneset(mock_client):
    """Test get request for geneset ID."""
    response = client.get("/api/genesets/1234")
    assert response.status_code == 200


@patch("geneweaver.api.services.geneset.get_geneset")
@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_response(mock_genset_is_readable, mock_get_genenset):
    """Test get geneset ID data response."""
    mock_genset_is_readable.return_value = True
    mock_get_genenset.return_value = test_data

    response = client.get("/api/genesets/1234")
    assert response.status_code == 200
    assert response.json() == test_data


@patch("geneweaver.api.services.geneset.db_is_readable")
def test_get_geneset_forbidden(mock_genset_is_readable):
    """Test forbidden response."""
    mock_genset_is_readable.return_value = False
    response = client.get("/api/genesets/1234")

    assert response.json() == {"detail": "Forbidden"}
    assert response.status_code == 403


@patch("geneweaver.api.services.geneset.db_is_readable")
def test_get_geneset_unexpected_error(mock_genset_is_readable):
    """Test unexpected error response."""
    mock_genset_is_readable.side_effect = Exception

    with pytest.raises(expected_exception=Exception):
        client.get("/api/genesets/1234")
