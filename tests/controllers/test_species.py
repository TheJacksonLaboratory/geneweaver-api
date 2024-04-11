"""Tests for species API."""

from unittest.mock import patch

from tests.data import test_species_data

species_no_params = test_species_data.get("species_no_parameters")
species_by_taxonomy_id_10090 = test_species_data.get("species_by_taxonomy_id_10090")
species_by_gene_id_type_flybase = test_species_data.get(
    "species_by_gene_id_type_flybase"
)


def _validate_species_response(response_item: dict, expected_item: dict) -> None:
    """Validate species response."""
    assert response_item["id"] == expected_item["id"]
    assert response_item["name"] == expected_item["name"]
    assert response_item["taxonomic_id"] == expected_item["taxonomic_id"]
    assert (
        response_item["reference_gene_identifier"]
        == str(expected_item["reference_gene_identifier"])
        or response_item["reference_gene_identifier"] is None
        and expected_item["reference_gene_identifier"] is None
    )


@patch("geneweaver.api.services.species.get_species")
def test_valid_species_url_req(mock_species_service_call, client):
    """Test valid url request to get species."""
    mock_species_service_call.return_value = species_no_params
    print(species_no_params)
    response = client.get(url="/api/species")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    for idx, item in enumerate(response.json().get("data")):
        _validate_species_response(item, species_no_params.get("data")[idx])


@patch("geneweaver.api.services.species.get_species")
def test_species_url_taxonomy_req(mock_species_service_call, client):
    """Test valid url request to get species."""
    mock_species_service_call.return_value = species_by_taxonomy_id_10090

    response = client.get(url="/api/species?taxonomy_id=10090")

    assert response.status_code == 200


@patch("geneweaver.api.services.species.get_species")
def test_valid_species_url_gene_id_type_req(mock_species_service_call, client):
    """Test valid url request to get species."""
    mock_species_service_call.return_value = {"data": [species_by_gene_id_type_flybase]}

    response = client.get(url="/api/species?gene_id_type=14")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    _validate_species_response(
        response.json().get("data")[0], species_by_gene_id_type_flybase
    )


@patch("geneweaver.api.services.species.get_species_by_id")
def test_valid_url_species_by_id(mock_species_service_call, client):
    """Test valid url request to get species by id."""
    mock_species_service_call.return_value = species_by_gene_id_type_flybase

    response = client.get(url="/api/species/5")

    assert response.status_code == 200
    _validate_species_response(response.json(), species_by_gene_id_type_flybase)
