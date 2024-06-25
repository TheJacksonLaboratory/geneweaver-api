"""Tests for search API."""

from unittest.mock import patch

from tests.data import test_geneset_data, test_publication_data

get_publications = test_publication_data.get("get_publications")
geneset_by_id_resp = test_geneset_data.get("geneset_by_id_resp")


@patch("geneweaver.api.services.publications.get")
def test_pub_search(mock_pub_service_call, client):
    """Test search for publications data response."""
    mock_pub_service_call.return_value = get_publications

    response = client.get(
        url="/api/search/", params={"entities": "publications", "search_text": "gene"}
    )

    assert response.status_code == 200
    assert response.json().get("data").get("publications") == get_publications.get(
        "data"
    )


@patch("geneweaver.api.services.geneset.get_visible_genesets")
def test_genesets_search_response(mock_get_visible_genesets, client):
    """Test search for geneset data response."""
    mock_data = geneset_by_id_resp.get("geneset")
    mock_get_visible_genesets.return_value = mock_data

    response = client.get(
        url="/api/search/", params={"entities": "genesets", "search_text": "gene"}
    )
    assert response.status_code == 200
    assert response.json().get("data").get("genesets") == mock_data.get("data")
