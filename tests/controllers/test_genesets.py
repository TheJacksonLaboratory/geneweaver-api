"""Tests for geneset API."""

import json
from unittest.mock import patch

import pytest
from geneweaver.api.controller import message

from tests.data import test_geneset_data, test_ontology_data, test_publication_data

geneset_by_id_resp = test_geneset_data.get("geneset_by_id_resp")
geneset_w_gene_id_type_resp = test_geneset_data.get("geneset_w_gene_id_type_resp")
geneset_metadata_w_pub_info = test_geneset_data.get("geneset_metadata_w_pub_info")
publication_by_id_resp = test_publication_data.get("publication_by_id")
geneset_genes_values_resp = test_geneset_data.get("geneset_genes_values_resp_1")
geneset_threshold_update_req = test_geneset_data.get("geneset_threshold_update_req")


@patch("geneweaver.api.services.geneset.get_geneset")
def test_get_geneset_response(mock_get_genenset, client):
    """Test get geneset ID data response."""
    mock_get_genenset.return_value = geneset_by_id_resp.get("geneset")

    response = client.get("/api/genesets/1234")
    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


@patch("geneweaver.api.services.geneset.get_geneset")
def test_get_geneset_in_threshold_response(mock_get_genenset, client):
    """Test get geneset ID data with threshold parameter request."""
    mock_get_genenset.return_value = geneset_by_id_resp.get("geneset")

    response = client.get("/api/genesets/1234?in_threshold=True")
    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


@patch("geneweaver.api.services.geneset.get_geneset")
def test_get_geneset_errors(mock_get_geneset, client):
    """Test get geneset ID data response."""
    mock_get_geneset.return_value = {"error": True, "message": message.ACCESS_FORBIDDEN}

    response = client.get("/api/genesets/1234")
    assert response.status_code == 403

    mock_get_geneset.return_value = {"error": True, "message": "other"}

    response = client.get("/api/genesets/1234")
    assert response.status_code == 500


@patch("geneweaver.api.services.geneset.get_geneset_w_gene_id_type")
def test_get_geneset_w_gene_id_type(mock_service_get_geneset_w_gene_id_type, client):
    """Test get geneset with gene id type response."""
    mock_service_get_geneset_w_gene_id_type.return_value = geneset_w_gene_id_type_resp
    response = client.get("/api/genesets/1234?gene_id_type=2")

    assert response.json() == geneset_w_gene_id_type_resp
    assert response.status_code == 200


@patch("geneweaver.api.services.geneset.get_geneset_w_gene_id_type")
def test_export_geneset_w_gene_id_type(mock_service_get_geneset_w_gene_id_type, client):
    """Test geneset file export."""
    mock_service_get_geneset_w_gene_id_type.return_value = geneset_w_gene_id_type_resp
    response = client.get("/api/genesets/1234/file?gene_id_type=2")

    assert response.headers.get("content-type") == "application/octet-stream"
    assert response.status_code == 200


@patch("geneweaver.api.services.geneset.get_geneset_w_gene_id_type")
def test_invalid_gene_type_id(mock_service_get_geneset_w_gene_id_type, client):
    """Test geneset file export."""
    mock_service_get_geneset_w_gene_id_type.return_value = geneset_w_gene_id_type_resp
    response = client.get("/api/genesets/1234/file?gene_id_type=25")

    assert "ctx" in response.json()["detail"][0]
    assert response.status_code == 422


@patch("geneweaver.api.services.geneset.get_geneset")
def test_export_geneset_errors(mock_get_geneset, client):
    """Test error in geneset file export."""
    mock_get_geneset.return_value = {"error": True, "message": message.ACCESS_FORBIDDEN}

    response = client.get("/api/genesets/1234/file")
    assert response.status_code == 403

    mock_get_geneset.return_value = {"error": True, "message": "other"}

    response = client.get("/api/genesets/1234/file")
    assert response.status_code == 500


@patch("geneweaver.api.services.geneset.get_geneset_metadata")
def test_get_geneset_metadata(mock_get_genenset, client):
    """Test get geneset metadata."""
    mock_get_genenset.return_value = geneset_by_id_resp.get("geneset")
    response = client.get("/api/genesets/1234/metadata")

    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


@patch("geneweaver.api.services.geneset.get_geneset_metadata")
def test_get_geneset_metadata_errors(mock_get_geneset_metadata, client):
    """Test errors in geneset metadata response."""
    mock_get_geneset_metadata.return_value = {
        "error": True,
        "message": message.ACCESS_FORBIDDEN,
    }

    response = client.get("/api/genesets/1234/metadata")
    assert response.status_code == 403

    mock_get_geneset_metadata.return_value = {"error": True, "message": "other"}

    response = client.get("/api/genesets/1234/metadata")
    assert response.status_code == 500


@patch("geneweaver.api.services.geneset.get_geneset_metadata")
def test_get_geneset_metadata_w_publication(mock_get_genenset, client):
    """Test get geneset ID data response."""
    mock_get_genenset.return_value = geneset_metadata_w_pub_info

    response = client.get("/api/genesets/1234/metadata?include_pub_info=true")
    assert response.status_code == 200
    assert response.json() == geneset_metadata_w_pub_info


@patch("geneweaver.api.services.geneset.get_geneset_metadata")
@patch("geneweaver.api.services.publications.get_publication")
def test_publication_for_geneset(
    mock_pub_service_call, mock_get_genenset_metadata, client
):
    """Test valid url request to get publication for a geneset."""
    mock_get_genenset_metadata.return_value = geneset_metadata_w_pub_info

    mock_pub_service_call.return_value = publication_by_id_resp

    response = client.get("/api/genesets/1234/publication")

    assert response.status_code == 200
    assert response.json() == publication_by_id_resp


@patch("geneweaver.api.services.geneset.get_geneset_metadata")
@patch("geneweaver.api.services.publications.get_publication")
def test_publication_not_found_for_geneset(
    mock_pub_service_call, mock_get_genenset_metadata, client
):
    """Test get publication for a geneset with not found record."""
    mock_get_genenset_metadata.return_value = geneset_metadata_w_pub_info
    mock_pub_service_call.return_value = None

    response = client.get("/api/genesets/1234/publication")

    assert response.status_code == 404

    geneset = geneset_metadata_w_pub_info.copy()
    geneset["publication_id"] = None

    mock_get_genenset_metadata.return_value = geneset
    response = client.get("/api/genesets/1234/publication")

    assert response.status_code == 404


@patch("geneweaver.api.services.geneset.get_geneset_metadata")
def test_get_publication_errors(mock_get_geneset_metadata, client):
    """Test get geneset ID data response."""
    mock_get_geneset_metadata.return_value = {
        "error": True,
        "message": message.ACCESS_FORBIDDEN,
    }

    response = client.get("/api/genesets/1234/publication")
    assert response.status_code == 403

    mock_get_geneset_metadata.return_value = {"error": True, "message": "other"}

    response = client.get("/api/genesets/1234/publication")
    assert response.status_code == 500


@patch("geneweaver.api.services.geneset.get_visible_genesets")
def test_get_visible_geneset_response(mock_get_visible_genesets, client):
    """Test get geneset ID data response."""
    mock_get_visible_genesets.return_value = geneset_by_id_resp.get("geneset")

    response = client.get("/api/genesets?gs_id=1234")
    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


@patch("geneweaver.api.services.geneset.get_visible_genesets")
def test_get_visible_geneset_errors(mock_get_visible_genesets, client):
    """Test get geneset ID data response."""
    mock_get_visible_genesets.return_value = {
        "error": True,
        "message": message.ACCESS_FORBIDDEN,
    }

    response = client.get("/api/genesets?gs_id=1234")
    assert response.status_code == 403

    mock_get_visible_genesets.return_value = {"error": True, "message": "other"}

    response = client.get("/api/genesets?gs_id=1234")
    assert response.status_code == 500


@patch("geneweaver.api.services.geneset.get_geneset_gene_values")
def test_get_geneset_gene_values_url_response(mock_get_geneset_gene_values, client):
    """Test get geneset gene values data response."""
    mock_get_geneset_gene_values.return_value = geneset_genes_values_resp

    response = client.get("/api/genesets/1234/values")
    assert response.status_code == 200
    assert response.json() == geneset_genes_values_resp


@patch("geneweaver.api.services.geneset.get_geneset_gene_values")
def test_get_geneset_gene_values_errors(mock_get_geneset_gene_values, client):
    """Test get geneset gene values error responses."""
    mock_get_geneset_gene_values.return_value = {
        "error": True,
        "message": message.ACCESS_FORBIDDEN,
    }
    response = client.get("/api/genesets/1234/values")
    assert response.status_code == 403

    mock_get_geneset_gene_values.return_value = {"error": True, "message": "other"}
    response = client.get("/api/genesets/1234/values")
    assert response.status_code == 500

    mock_get_geneset_gene_values.return_value = {"data": None}
    response = client.get("/api/genesets/1234/values")
    assert response.status_code == 404


@patch("geneweaver.api.services.geneset.get_geneset_gene_values")
def test_get_geneset_gene_values_w_gs_id_type(mock_get_geneset_gene_values, client):
    """Test get geneset gene values data response."""
    mock_get_geneset_gene_values.return_value = geneset_genes_values_resp

    response = client.get("/api/genesets/1234/values?gene_id_type=2")
    assert response.status_code == 200
    assert response.json() == geneset_genes_values_resp


@patch("geneweaver.api.services.geneset.get_geneset_gene_values")
def test_get_geneset_gene_values_w_gs_id_type_and_in_threshold(
    mock_get_geneset_gene_values, client
):
    """Test get geneset gene values data response."""
    mock_get_geneset_gene_values.return_value = geneset_genes_values_resp

    response = client.get("/api/genesets/1234/values?gene_id_type=2&in_threshold=True")
    assert response.status_code == 200
    assert response.json() == geneset_genes_values_resp


@patch("geneweaver.api.services.geneset.update_geneset_threshold")
def test_set_geneset_endpoint_response(mock_update_geneset_threshold, client):
    """Test set geneset threshold endpoint."""
    mock_update_geneset_threshold.return_value = {}

    response = client.put(
        "/api/genesets/1234/threshold", data=json.dumps(geneset_threshold_update_req)
    )
    assert response.status_code == 204


@patch("geneweaver.api.services.geneset.update_geneset_threshold")
def test_set_geneset_endpoint_response_errors(mock_update_geneset_threshold, client):
    """Test set geneset threshold endpoint errors."""
    mock_update_geneset_threshold.return_value = {
        "error": True,
        "message": message.ACCESS_FORBIDDEN,
    }

    response = client.put(
        "/api/genesets/1234/threshold", data=json.dumps(geneset_threshold_update_req)
    )
    assert response.status_code == 403


@patch("geneweaver.api.services.geneset.get_geneset_ontology_terms")
def test_get_geneset_ontology_terms_response(mock_get_genenset_onto_terms, client):
    """Test get geneset ontology terms response."""
    mock_resp = test_ontology_data.get("geneset_ontology_terms")
    mock_get_genenset_onto_terms.return_value = mock_resp

    response = client.get("/api/genesets/1234/ontologies")
    assert response.status_code == 200
    assert response.json() == mock_resp


@patch("geneweaver.api.services.geneset.get_geneset_ontology_terms")
def test_get_geneset_ontology_terms_errors(mock_get_genenset_onto_terms, client):
    """Test get geneset ontology terms errors."""
    mock_resp = {
        "error": True,
        "message": message.ACCESS_FORBIDDEN,
    }
    mock_get_genenset_onto_terms.return_value = mock_resp

    response = client.get("/api/genesets/1234/ontologies")
    assert response.status_code == 403

    mock_get_genenset_onto_terms.return_value = {
        "error": True,
        "message": message.INACCESSIBLE_OR_FORBIDDEN,
    }
    response = client.get("/api/genesets/1234/ontologies")
    assert response.status_code == 404


@patch("geneweaver.api.services.geneset.add_geneset_ontology_term")
def test_add_geneset_ontology_term_response(mock_add_genenset_onto_terms, client):
    """Test add geneset ontology_terms  response."""
    mock_resp = test_ontology_data.get("geneset_ontology_terms")
    mock_add_genenset_onto_terms.return_value = mock_resp

    response = client.put("/api/genesets/1234/ontologies?ontology_id=D001921")
    assert response.status_code == 204


@patch("geneweaver.api.services.geneset.add_geneset_ontology_term")
def test_add_geneset_ontology_terms_errors(mock_add_genenset_onto_terms, client):
    """Test add geneset ontology_terms errors."""
    mock_resp = {
        "error": True,
        "message": message.ACCESS_FORBIDDEN,
    }
    mock_add_genenset_onto_terms.return_value = mock_resp

    response = client.put("/api/genesets/1234/ontologies?ontology_id=D001921")
    assert response.status_code == 403

    mock_add_genenset_onto_terms.return_value = {
        "error": True,
        "message": message.RECORD_NOT_FOUND_ERROR,
    }
    response = client.put("/api/genesets/1234/ontologies?ontology_id=QEQWEWE")
    assert response.status_code == 404

    mock_add_genenset_onto_terms.return_value = {
        "error": True,
        "message": message.RECORD_EXISTS,
    }
    response = client.put("/api/genesets/1234/ontologies?ontology_id=D001921")
    assert response.status_code == 412

    mock_add_genenset_onto_terms.return_value = {
        "error": True,
        "message": message.INACCESSIBLE_OR_FORBIDDEN,
    }
    response = client.put("/api/genesets/1234/ontologies?ontology_id=D001921")
    assert response.status_code == 404


@patch("geneweaver.api.services.geneset.delete_geneset_ontology_term")
def test_delete_geneset_ontology_term_response(mock_delete_genenset_onto_terms, client):
    """Test delete geneset ontology_terms  response."""
    mock_resp = test_ontology_data.get("geneset_ontology_terms")
    mock_delete_genenset_onto_terms.return_value = mock_resp

    response = client.delete("/api/genesets/1234/ontologies/D001921")
    assert response.status_code == 204


@patch("geneweaver.api.services.geneset.delete_geneset_ontology_term")
def test_delete_geneset_ontology_terms_errors(mock_delete_genenset_onto_terms, client):
    """Test delete geneset ontology_terms errors."""
    mock_resp = {
        "error": True,
        "message": message.ACCESS_FORBIDDEN,
    }
    mock_delete_genenset_onto_terms.return_value = mock_resp

    response = client.delete("/api/genesets/1234/ontologies/D001921")
    assert response.status_code == 403

    mock_delete_genenset_onto_terms.return_value = {
        "error": True,
        "message": message.RECORD_NOT_FOUND_ERROR,
    }
    response = client.delete("/api/genesets/1234/ontologies/QEQWEWE")
    assert response.status_code == 404

    mock_delete_genenset_onto_terms.return_value = {
        "error": True,
        "message": message.INACCESSIBLE_OR_FORBIDDEN,
    }
    response = client.delete("/api/genesets/1234/ontologies/D001921")
    assert response.status_code == 404


@pytest.mark.parametrize("score_type", ["1", "binary"])
@patch("geneweaver.api.services.geneset.get_visible_genesets")
def test_get_geneset_by_score_type(mock_get_visible_genesets, score_type, client):
    """Test get geneset  data response."""
    mock_get_visible_genesets.return_value = geneset_by_id_resp.get("geneset")

    response = client.get("/api/genesets?score_type=" + score_type)
    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


@patch("geneweaver.api.services.geneset.get_visible_genesets")
def test_get_geneset_by_create_date(mock_get_visible_genesets, client):
    """Test get geneset  data response."""
    mock_get_visible_genesets.return_value = geneset_by_id_resp.get("geneset")

    response = client.get(
        "/api/genesets?created_after=2023-08-01&created_before=2024-07-01"
    )
    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


@patch("geneweaver.api.services.geneset.get_visible_genesets")
def test_get_geneset_by_update_date(mock_get_visible_genesets, client):
    """Test get geneset  data response."""
    mock_get_visible_genesets.return_value = geneset_by_id_resp.get("geneset")

    response = client.get(
        "/api/genesets?updated_after=2023-08-01&updated_before=2024-07-01"
    )
    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


@pytest.mark.parametrize("score_type", ["2342", "test"])
def test_invalid_score_type(score_type, client):
    """Test general get geneset data no parameters -- default limit."""
    response = client.get("/api/genesets?score_type=" + score_type)
    assert response.status_code == 422


@pytest.mark.parametrize("created_before", ["20-23-20", "08-01-2023", "80/01/2022"])
@pytest.mark.parametrize("created_after", ["20-23-20", "08-01-2023", "80/01/2022"])
def test_invalid_create_date_params(created_before, created_after, client):
    """Test general get geneset data no parameters -- default limit."""
    response = client.get(
        "/api/genesets?created_before="
        + created_before
        + ",created_after="
        + created_after
    )
    assert response.status_code == 422


@pytest.mark.parametrize("updated_before", ["20-23-20", "08-01-2023", "80/01/2022"])
@pytest.mark.parametrize("updated_after", ["20-23-20", "08-01-2023", "80/01/2022"])
def test_invalid_update_date_params(updated_before, updated_after, client):
    """Test general get geneset data no parameters -- default limit."""
    response = client.get(
        "/api/genesets?created_before="
        + updated_before
        + ",created_after="
        + updated_after
    )
    assert response.status_code == 422
