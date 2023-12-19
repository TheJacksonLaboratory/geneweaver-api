import importlib.resources
import json
from unittest.mock import Mock
from unittest.mock import patch

import psycopg
import pytest
from fastapi.testclient import TestClient

from geneweaver.api.dependencies import full_user, cursor
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
m1 = Mock()
def mock_full_user() -> m1.AsyncMock:
    return m1
m2 = Mock()
def mock_cursor() -> psycopg.Cursor:
    return m2.AsyncMock()
m3 = Mock()
def mock_cursor_obj() -> psycopg.Cursor:
    return m3.AsyncMock()

app.dependency_overrides.update(
    {full_user: mock_full_user, cursor: mock_cursor}
)

@patch.object(client, 'get', return_value=response_mock)
def test_get_geneset(mock_client):
    response = client.get("/genesets/1234")
    assert response.status_code == 200

@patch('geneweaver.api.services.geneset.get_geneset')
@patch('geneweaver.api.services.geneset.is_geneset_readable_by_user')
def test_get_geneset_response(mock_genset_is_readable, mock_get_genenset):
    mock_genset_is_readable.return_value = True
    mock_get_genenset.return_value = test_data

    response = client.get("/genesets/1234")
    assert response.status_code == 200
    assert response.json() == test_data

@patch('geneweaver.api.services.geneset.db_is_readable')
def test_get_geneset_forbidden(mock_genset_is_readable):

    mock_genset_is_readable.return_value = False
    response = client.get("/genesets/1234")

    assert response.json() == {'detail': 'Forbidden'}
    assert response.status_code == 403

@patch('geneweaver.api.services.geneset.db_is_readable')
def test_get_geneset_unexpected_error(mock_genset_is_readable):

    mock_genset_is_readable.side_effect = Exception

    with pytest.raises(Exception):
        response = client.get("/genesets/1234")
        assert response.json() == {'detail': 'Unexpected error'}
        assert response.status_code == 500