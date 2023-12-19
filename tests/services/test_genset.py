import importlib.resources
import json
from unittest.mock import patch

import pytest

import geneweaver.api.controller.message as message
import geneweaver.api.services.geneset as geneset

## Load test data
# Opening JSON file
str_json = importlib.resources.read_text("tests.data", "response_geneset_1234.json")
# returns JSON string as a dictionary
test_data = json.loads(str_json)

@patch('geneweaver.api.services.geneset.db_geneset')
@patch('geneweaver.api.services.geneset.db_geneset_value')
@patch('geneweaver.api.services.geneset.is_geneset_readable_by_user')
def test_get_geneset_no_errors(mock_genset_readable_func, mock_db_geneset, mock_db_genset_value):

    mock_genset_readable_func.return_value = True
    mock_db_geneset.by_id.return_value = {}
    mock_db_genset_value.by_id.return_value = {}
    response = geneset.get_geneset(1234, None, None)
    assert response.get('error') == None


@patch('geneweaver.api.services.geneset.is_geneset_readable_by_user')
def test_get_geneset_no_user_access(mock_genset_readable_func):

    mock_genset_readable_func.return_value = False
    response = geneset.get_geneset(1234, None, None)
    assert response.get('error') == True
    assert response.get('message') == message.ACCESS_FORBIDEN


@patch('geneweaver.api.services.geneset.db_geneset')
@patch('geneweaver.api.services.geneset.db_geneset_value')
@patch('geneweaver.api.services.geneset.is_geneset_readable_by_user')
def test_get_geneset_returned_values(mock_genset_readable_func, mock_db_genset_value, mock_db_geneset):

    mock_genset_readable_func.return_value = True
    mock_db_geneset.by_id.return_value = test_data.get('geneset')
    mock_db_genset_value.by_geneset_id.return_value = test_data.get('geneset_values')
    response = geneset.get_geneset(1234, None, None)

    assert response.get('genset') == test_data['geneset']
    assert response.get('geneset_values') == test_data['geneset_values']


@patch('geneweaver.api.services.geneset.db_is_readable')
@patch('geneweaver.api.services.geneset.User')
def test_is_redable_by_user(mock_user, mock_genset_is_readable):

    mock_genset_is_readable.return_value = True
    response = geneset.is_geneset_readable_by_user(1234, mock_user, None)
    assert response == True


@patch('geneweaver.db.geneset.is_readable')
@patch('geneweaver.api.services.geneset.User')
def test_is_redable_by_user_error(mock_user, mock_genset_is_readable):
    mock_genset_is_readable.sideEffect = Exception

    with pytest.raises(Exception):
        geneset.is_geneset_readable_by_user(1234, mock_user, None)


