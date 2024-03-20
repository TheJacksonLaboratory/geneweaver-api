"""Tests for species API."""
from unittest.mock import patch

from tests.data import test_species_data

species_no_params = test_species_data.get("species_no_parameters")
species_by_taxonomy_id_10090 = test_species_data.get("species_by_taxonomy_id_10090")
species_by_gene_id_type_flybase = test_species_data.get(
    "species_by_gene_id_type_flybase"
)


@patch("geneweaver.api.services.species.get_species")
def test_valid_species_url_req(mock_species_service_call, client):
    """Test valid url request to get species."""
    mock_species_service_call.return_value = species_no_params

    response = client.get(url="/api/species")

    assert response.status_code == 200
    assert response.json() == species_no_params


@patch("geneweaver.api.services.species.get_species")
def test_species_url_taxonomy_req(mock_species_service_call, client):
    """Test valid url request to get species."""
    mock_species_service_call.return_value = species_by_taxonomy_id_10090

    response = client.get(url="/api/species?taxonomy_id=10090")

    assert response.status_code == 200
    assert response.json() == species_by_taxonomy_id_10090


@patch("geneweaver.api.services.species.get_species")
def test_valid_species_url_gene_id_type_req(mock_species_service_call, client):
    """Test valid url request to get species."""
    mock_species_service_call.return_value = species_by_gene_id_type_flybase

    response = client.get(url="/api/species?gene_id_type=14")

    assert response.status_code == 200
    assert response.json() == species_by_gene_id_type_flybase
