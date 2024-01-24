"""Tests for geneset API."""
import json
from unittest.mock import patch

from tests.data import test_gene_data

gene_ids_map_req_1 = test_gene_data.get("gene_ids_map_req_1_gene_ids_species")
gene_ids_map_resp_1 = test_gene_data.get("gene_ids_map_resp_1")


@patch("geneweaver.api.services.genes.get_gene_mapping")
def test_gene_id_mapping_response_post_req(mock_gene_id_mapping, client):
    """Test genes homologous ids url and post request."""
    mock_gene_id_mapping.return_value = {
        "ids_map": gene_ids_map_resp_1.get("gene_ids_map")
    }

    response = client.post(
        url="/api/genes/homologous-ids", data=json.dumps(gene_ids_map_req_1)
    )
    print(response)
    assert response.status_code == 200
    assert response.json() == gene_ids_map_resp_1


@patch("geneweaver.api.services.genes.get_gene_mapping")
def test_gene_id_mapping_invalid_url(mock_gene_id_mapping, client):
    """Test genes homologous ids invalid url."""
    mock_gene_id_mapping.return_value = {
        "ids_map": gene_ids_map_resp_1.get("gene_ids_map")
    }

    response = client.post(
        url="/api/genes/homologous_ids", data=json.dumps(gene_ids_map_req_1)
    )
    print(response)
    assert response.status_code == 404


@patch("geneweaver.api.services.genes.get_gene_mapping")
def test_gene_id_mapping_invalid_post_data_(mock_gene_id_mapping, client):
    """Test genes homologous ids url and invalid post data request."""
    mock_gene_id_mapping.return_value = {
        "ids_map": gene_ids_map_resp_1.get("gene_ids_map")
    }

    response = client.post(
        url="/api/genes/homologous-ids", data=json.dumps({"test": "test"})
    )
    assert response.status_code == 422


@patch("geneweaver.api.services.genes.get_gene_mapping")
def test_gene_id_mapping_missing_target_gene_identifier(mock_gene_id_mapping, client):
    """Test genes homologous ids url and invalid post data request."""
    mock_gene_id_mapping.return_value = {
        "ids_map": gene_ids_map_resp_1.get("gene_ids_map")
    }

    req_gene_map = gene_ids_map_req_1.copy()
    req_gene_map.pop("target_gene_id_type")
    response = client.post(
        url="/api/genes/homologous-ids", data=json.dumps(req_gene_map)
    )
    assert response.status_code == 422


@patch("geneweaver.api.services.genes.get_gene_mapping")
def test_gene_id_mapping_missing_gene_list(mock_gene_id_mapping, client):
    """Test genes homologous ids url and invalid post data request."""
    mock_gene_id_mapping.return_value = {
        "ids_map": gene_ids_map_resp_1.get("gene_ids_map")
    }

    req_gene_map = gene_ids_map_req_1.copy()
    req_gene_map.pop("source_ids")
    response = client.post(
        url="/api/genes/homologous-ids", data=json.dumps(req_gene_map)
    )
    assert response.status_code == 422
