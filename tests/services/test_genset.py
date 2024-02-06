"""Tests for geneset Service."""

from unittest.mock import patch

import pytest
from geneweaver.api.controller import message
from geneweaver.api.services import geneset
from geneweaver.core.enum import GeneIdentifier

from tests.data import test_geneset_data

geneset_by_id_resp = test_geneset_data.get("geneset_by_id_resp")
geneset_w_gene_id_type_resp = test_geneset_data.get("geneset_w_gene_id_type_resp")
geneset_metadata_w_pub_info = test_geneset_data.get("geneset_metadata_w_pub_info")


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset(mock_genset_readable_func, mock_db_geneset, mock_db_genset_value):
    """Test basic get geneset by ID."""
    mock_genset_readable_func.return_value = True
    mock_db_geneset.by_id.return_value = {}
    mock_db_genset_value.by_id.return_value = {}
    response = geneset.get_geneset(None, 1234, None)
    assert response.get("error") is None


@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_no_user_access(mock_genset_readable_func):
    """Test get geneset by ID with no user access."""
    mock_genset_readable_func.return_value = False
    response = geneset.get_geneset(None, 1234, None)
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_returned_values(
    mock_genset_readable_func, mock_db_genset_value, mock_db_geneset
):
    """Test get geneset by ID data response structure."""
    mock_genset_readable_func.return_value = True
    mock_db_geneset.by_id.return_value = geneset_by_id_resp.get("geneset")
    mock_db_genset_value.by_geneset_id.return_value = geneset_by_id_resp.get(
        "geneset_values"
    )
    response = geneset.get_geneset(None, 1234, None)

    assert response.get("geneset") == geneset_by_id_resp["geneset"]
    assert response.get("geneset_values") == geneset_by_id_resp["geneset_values"]


@patch("geneweaver.api.services.geneset.db_is_readable")
@patch("geneweaver.api.services.geneset.User")
def test_is_redable_by_user(mock_user, mock_genset_is_readable):
    """Test is geneset ID readable by passed user."""
    mock_genset_is_readable.return_value = True
    response = geneset.is_geneset_readable_by_user(None, 1234, mock_user)
    assert response is True


@patch("geneweaver.db.geneset.is_readable")
@patch("geneweaver.api.services.geneset.User")
def test_is_redable_by_user_error(mock_user, mock_genset_is_readable):
    """Test is geneset ID readable with server error."""
    mock_genset_is_readable.sideEffect = Exception

    with pytest.raises(expected_exception=Exception):
        geneset.is_geneset_readable_by_user(None, 1234, mock_user)


@patch("geneweaver.api.services.geneset.db_gene")
@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_w_gene_id_type_reponse(
    mock_genset_readable_func, mock_db_genset_value, mock_db_geneset, mock_db_gene
):
    """Test get geneset by ID with gene identifier type data response."""
    mock_genset_readable_func.return_value = True
    mock_db_geneset.by_id.return_value = geneset_w_gene_id_type_resp.get("geneset")
    mock_db_genset_value.by_geneset_id.return_value = geneset_w_gene_id_type_resp.get(
        "geneset_values"
    )
    mock_db_gene.gene_database_by_id.return_value = [{"sp_id": 0}]

    response = geneset.get_geneset_w_gene_id_type(None, 1234, None, GeneIdentifier(2))

    assert response.get("geneset") == geneset_w_gene_id_type_resp["geneset"]
    assert (
        response.get("gene_identifier_type")
        == geneset_w_gene_id_type_resp["gene_identifier_type"]
    )
    assert (
        response.get("geneset_values") == geneset_w_gene_id_type_resp["geneset_values"]
    )


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_metadata(mock_genset_readable_func, mock_db_geneset):
    """Test get geneset metadata by geneset id."""
    mock_genset_readable_func.return_value = True
    mock_db_geneset.by_id.return_value = geneset_by_id_resp.get("geneset")
    response = geneset.get_geneset_metadata(None, 1234, None)

    assert response.get("geneset") == geneset_by_id_resp["geneset"]


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_metadata_w_pub_info(mock_genset_readable_func, mock_db_geneset):
    """Test get geneset metadata by geneset id with publication info."""
    mock_genset_readable_func.return_value = True
    mock_db_geneset.by_id.return_value = geneset_metadata_w_pub_info
    response = geneset.get_geneset_metadata(None, 1234, None, True)

    assert response.get("geneset") == geneset_metadata_w_pub_info
