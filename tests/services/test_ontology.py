"""Tests for ontology service calls."""

from unittest.mock import patch

import pytest
from geneweaver.api.controller import message
from geneweaver.api.schemas.auth import User
from geneweaver.api.services import geneset

from tests.data import test_ontology_data

mock_user = User()
mock_user.id = 1


@patch("geneweaver.api.services.geneset.db_ontology")
@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_ontology_terms(mock_db_geneset, mock_db_ontology):
    """Test get geneset ontology terms."""
    mock_db_geneset.is_readable.return_value = True
    mock_db_ontology.by_geneset.return_value = test_ontology_data.get(
        "geneset_ontology_terms"
    ).get("data")

    response = geneset.get_geneset_ontology_terms(None, 1234, mock_user)

    assert response.get("data") == test_ontology_data.get("geneset_ontology_terms").get(
        "data"
    )


@patch("geneweaver.api.services.geneset.db_ontology")
@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_ontology_terms_no_access(mock_db_geneset, mock_db_ontology):
    """Test get geneset ontology terms."""
    mock_db_geneset.is_readable.return_value = False
    mock_db_ontology.by_geneset.return_value = test_ontology_data.get(
        "geneset_ontology_terms"
    ).get("data")

    response = geneset.get_geneset_ontology_terms(None, 1234, mock_user)

    assert response == {"error": True, "message": message.INACCESSIBLE_OR_FORBIDDEN}


@patch("geneweaver.api.services.geneset.db_ontology")
@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_ontology_terms_no_user(mock_db_geneset, mock_db_ontology):
    """Test get geneset ontology terms."""
    mock_db_geneset.is_readable.return_value = False
    mock_db_ontology.by_geneset.return_value = test_ontology_data.get(
        "geneset_ontology_terms"
    ).get("data")

    response = geneset.get_geneset_ontology_terms(None, 1234, None)

    assert response == {"error": True, "message": message.INACCESSIBLE_OR_FORBIDDEN}


@patch("geneweaver.api.services.geneset.db_ontology")
def test_get_geneset_ontology_term_error(mock_db_ontology):
    """Test error in get DB call."""
    mock_db_ontology.by_geneset.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_geneset_ontology_terms(None, 1234, mock_user)
