"""Tests for geneset Service."""

from unittest.mock import patch

import pytest
from geneweaver.api.controller import message
from geneweaver.api.schemas.auth import User
from geneweaver.api.services import geneset
from geneweaver.core.enum import GeneIdentifier, GenesetTier, Species

from tests.data import test_geneset_data

geneset_by_id_resp = test_geneset_data.get("geneset_by_id_resp")
geneset_list_resp = test_geneset_data.get("geneset_list_resp")
geneset_w_gene_id_type_resp = test_geneset_data.get("geneset_w_gene_id_type_resp")
geneset_metadata_w_pub_info = test_geneset_data.get("geneset_metadata_w_pub_info")
mock_user = User()
mock_user.id = 1


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset(mock_db_geneset, mock_db_genset_value):
    """Test basic get geneset by ID."""
    mock_db_geneset.get.return_value = {}
    mock_db_genset_value.get.return_value = [{}]
    response = geneset.get_geneset(None, 1234, mock_user)
    assert response.get("error") is None


def test_get_geneset_no_user_access():
    """Test get geneset by ID with no user access."""
    response = geneset.get_geneset(None, 1234, None)
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_returned_values(mock_db_genset_value, mock_db_geneset):
    """Test get geneset by ID data response structure."""
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    mock_db_genset_value.by_geneset_id.return_value = geneset_by_id_resp.get(
        "geneset_values"
    )
    response = geneset.get_geneset(None, 1234, mock_user)

    assert response.get("geneset") == geneset_by_id_resp["geneset"]
    assert response.get("geneset_values") == geneset_by_id_resp["geneset_values"]


@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_db_call_error(mock_db_geneset):
    """Test error in get DB call."""
    mock_db_geneset.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_geneset(None, 1234, mock_user)


@patch("geneweaver.api.services.geneset.db_gene")
@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_w_gene_id_type_response(
    mock_db_genset_value,
    mock_db_geneset,
    mock_db_gene,
):
    """Test get geneset by ID with gene identifier type data response."""
    mock_db_geneset.get.return_value = [geneset_w_gene_id_type_resp.get("geneset")]
    mock_db_genset_value.by_geneset_id.return_value = geneset_w_gene_id_type_resp.get(
        "geneset_values"
    )
    mock_db_gene.gene_database_by_id.return_value = [{"sp_id": 0}]

    response = geneset.get_geneset_w_gene_id_type(
        None, 1234, mock_user, GeneIdentifier(2)
    )

    assert response.get("geneset") == geneset_w_gene_id_type_resp["geneset"]
    assert (
        response.get("gene_identifier_type")
        == geneset_w_gene_id_type_resp["gene_identifier_type"]
    )
    assert (
        response.get("geneset_values") == geneset_w_gene_id_type_resp["geneset_values"]
    )


@patch("geneweaver.api.services.geneset.db_gene")
@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_w_gene_id_type_2_response(
    mock_db_genset_value,
    mock_db_geneset,
    mock_db_gene,
):
    """Test get geneset by ID with gene identifier type data response."""
    mock_db_geneset.get.return_value = [geneset_w_gene_id_type_resp.get("geneset")]
    mock_db_genset_value.by_geneset_id.return_value = geneset_w_gene_id_type_resp.get(
        "geneset_values"
    )
    mock_db_gene.gene_database_by_id.return_value = [{"sp_id": 1}]

    response = geneset.get_geneset_w_gene_id_type(
        None, 1234, mock_user, GeneIdentifier(2)
    )

    assert response.get("geneset") == geneset_w_gene_id_type_resp["geneset"]
    assert (
        response.get("gene_identifier_type")
        == geneset_w_gene_id_type_resp["gene_identifier_type"]
    )
    assert (
        response.get("geneset_values") == geneset_w_gene_id_type_resp["geneset_values"]
    )


def test_get_geneset_w_gene_id_type_no_user():
    """Test get_geneset_w_gene_id_type with invalid user."""
    response = geneset.get_geneset_w_gene_id_type(None, 1234, None, GeneIdentifier(2))
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    response = geneset.get_geneset_w_gene_id_type(
        None, 1234, User(id=None), GeneIdentifier(2)
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN


@patch("geneweaver.api.services.geneset.db_geneset")
def test_geneset_w_gene_id_type_db_call_error(mock_db_geneset):
    """Test error in get DB call."""
    mock_db_geneset.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_geneset_w_gene_id_type(None, 1234, mock_user, GeneIdentifier(2))


@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_metadata(mock_db_geneset):
    """Test get geneset metadata by geneset id."""
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    response = geneset.get_geneset_metadata(None, 1234, mock_user)

    assert response.get("geneset") == geneset_by_id_resp["geneset"]

    response = geneset.get_geneset_metadata(None, 1234, None)
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    response = geneset.get_geneset_metadata(None, 1234, User(id=None))
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN


@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_metadata_w_pub_info(mock_db_geneset):
    """Test get geneset metadata by geneset id with publication info."""
    mock_db_geneset.get.return_value = [geneset_metadata_w_pub_info]
    response = geneset.get_geneset_metadata(None, 1234, mock_user, True)

    assert response.get("geneset") == geneset_metadata_w_pub_info


@patch("geneweaver.api.services.geneset.db_geneset")
def test_geneset_metadata_db_call_error(mock_db_geneset):
    """Test error in get DB call."""
    mock_db_geneset.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_geneset_metadata(None, 1234, mock_user, True)


@patch("geneweaver.api.services.geneset.db_geneset")
def test_visible_geneset_response(mock_db_geneset):
    """Test general get geneset data no parameters -- default limit."""
    mock_db_geneset.get.return_value = geneset_list_resp.get("geneset_resp_1_list_10")

    response = geneset.get_visible_genesets(None, mock_user)
    assert response.get("geneset") == geneset_list_resp.get("geneset_resp_1_list_10")


def test_visible_geneset_no_user():
    """Test general get geneset data invalid user."""
    response = geneset.get_visible_genesets(None, None)
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    response = geneset.get_visible_genesets(None, User(id=None))
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN


@patch("geneweaver.api.services.geneset.db_geneset")
def test_visible_geneset_all_expected_parameters(mock_db_geneset):
    """Test general get geneset data no parameters -- default limit."""
    mock_db_geneset.get.return_value = geneset_list_resp.get("geneset_resp_1_list_10")

    response = geneset.get_visible_genesets(
        cursor=None,
        user=mock_user,
        gs_id=1,
        only_my_genesets=False,
        curation_tier=GenesetTier("Tier I"),
        species=Species(2),
        name="test Name",
        abbreviation="test",
        publication_id=123,
        pubmed_id="p123",
        gene_id_type=GeneIdentifier(5),
        limit=10,
        offset=0,
        with_publication_info=True,
    )

    assert response.get("geneset") == geneset_list_resp.get("geneset_resp_1_list_10")


@patch("geneweaver.api.services.geneset.db_geneset")
def test_visible_geneset_db_call_error(mock_db_geneset):
    """Test error in get DB call."""
    mock_db_geneset.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_visible_genesets(None, mock_user)


@patch("geneweaver.api.services.geneset.db_gene")
def test_map_geneset_homology(mock_db_gene):
    """Test map_geneset_homology call."""
    mock_db_gene.get_homolog_ids_by_ode_id.return_value = geneset_by_id_resp[
        "geneset_values"
    ]

    response = geneset.map_geneset_homology(
        None, geneset_by_id_resp["geneset_values"], GeneIdentifier(2)
    )
    assert response == geneset_by_id_resp["geneset_values"]


@patch("geneweaver.api.services.geneset.db_gene")
def test_map_geneset_homology_db_call_error(mock_db_gene):
    """Test error in get DB call."""
    mock_db_gene.get_homolog_ids_by_ode_id.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.map_geneset_homology(
            None, geneset_by_id_resp["geneset_values"], GeneIdentifier(2)
        )
