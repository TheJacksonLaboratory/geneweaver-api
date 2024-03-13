"""Tests for publications Service."""

from unittest.mock import patch

import pytest
from geneweaver.api.services import species as species_service
from geneweaver.core.enum import GeneIdentifier

from tests.data import test_species_data

species_no_params = test_species_data.get("species_no_params")
species_by_taxonomy_id_10090 = test_species_data.get("species_by_taxonomy_id_10090")
species_by_gene_id_type_flybase = test_species_data.get(
    "species_by_gene_id_type_flybase"
)


@patch("geneweaver.api.services.species.db_species")
def test_get_species(mock_db_species):
    """Test get species no paramaters."""
    mock_db_species.get.return_value = species_no_params

    response = species_service.get_species(None)

    assert response.get("species") == species_no_params


@patch("geneweaver.api.services.species.db_species")
def test_get_species_by_taxonomy_id(mock_db_species):
    """Test speccies by taxonomy id."""
    mock_db_species.get.return_value = species_by_taxonomy_id_10090

    response = species_service.get_species(None, taxonomy_id=10090)

    assert response.get("species") == species_by_taxonomy_id_10090


@patch("geneweaver.api.services.species.db_species")
def test_get_species_by_gene_id_type(mock_db_species):
    """Test speccies by taxonomy id."""
    mock_db_species.get.return_value = species_by_gene_id_type_flybase

    response = species_service.get_species(None, gene_id_type=GeneIdentifier("FlyBase"))

    assert response.get("species") == species_by_gene_id_type_flybase


@patch("geneweaver.api.services.species.db_species")
def test_get_species_by_gene_id_type_and_taxonomy(mock_db_species):
    """Test speccies by taxonomy id."""
    mock_db_species.get.return_value = species_by_gene_id_type_flybase

    response = species_service.get_species(
        None, gene_id_type=GeneIdentifier("FlyBase"), taxonomy_id=7227
    )

    assert response.get("species") == species_by_gene_id_type_flybase


@patch("geneweaver.api.services.species.db_species")
def test_get_species_with_error(mock_db_species):
    """Test error in DB call."""
    mock_db_species.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        species_service.get(None)


@patch("geneweaver.api.services.species.db_species")
def test_get_species_invalid_params(mock_db_species):
    """Test speccies by taxonomy id."""
    mock_db_species.get.return_value = species_no_params

    # with pytest.raises(expected_exception=Exception):

    response = species_service.get_species(
        None, taxonomy_id="qweqw", gene_id_type="asdasd"
    )

    # with pytest.raises(expected_exception=TypeError):

    assert response.get("species") == species_no_params
