"""Tests for geneset API."""

from unittest.mock import patch

from geneweaver.api.controller import message

from tests.data import test_geneset_data, test_publication_data

geneset_by_id_resp = test_geneset_data.get("geneset_by_id_resp")
geneset_w_gene_id_type_resp = test_geneset_data.get("geneset_w_gene_id_type_resp")
geneset_metadata_w_pub_info = test_geneset_data.get("geneset_metadata_w_pub_info")
publication_by_id_resp = test_publication_data.get("publication_by_id")
geneset_genes_values_resp = test_geneset_data.get("geneset_genes_values_resp_1")


@patch("geneweaver.api.services.geneset.get_geneset")
def test_get_geneset_response(mock_get_genenset, client):
    """Test get geneset ID data response."""
    mock_get_genenset.return_value = geneset_by_id_resp.get("geneset")

    response = client.get("/api/genesets/1234")
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
    assert int(response.headers.get("content-length")) > 0
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
