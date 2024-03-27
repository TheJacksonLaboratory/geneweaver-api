"""Tests for geneset API."""
from unittest.mock import patch

from tests.data import test_geneset_data, test_publication_data

geneset_by_id_resp = test_geneset_data.get("geneset_by_id_resp")
geneset_w_gene_id_type_resp = test_geneset_data.get("geneset_w_gene_id_type_resp")
geneset_metadata_w_pub_info = test_geneset_data.get("geneset_metadata_w_pub_info")
publication_by_id_resp = test_publication_data.get("publication_by_id")


@patch("geneweaver.api.services.geneset.get_geneset")
# @patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_response(mock_get_genenset, client):
    """Test get geneset ID data response."""
    mock_get_genenset.return_value = geneset_by_id_resp.get("geneset")

    response = client.get("/api/genesets/1234")
    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


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


@patch("geneweaver.api.services.geneset.get_geneset_metadata")
def test_get_geneset_metadata(mock_get_genenset, client):
    """Test get geneset metadata."""
    mock_get_genenset.return_value = geneset_by_id_resp.get("geneset")
    response = client.get("/api/genesets/1234/metadata")

    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp.get("geneset")


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
    mock_get_genenset_metadata.return_value = geneset_by_id_resp.get("geneset")
    mock_pub_service_call.return_value = {"publication": None}

    response = client.get("/api/genesets/1234/publication")

    assert response.status_code == 404
