"""Tests for geneset API."""
from unittest.mock import patch

from geneweaver.api.controller import message

from tests.data import test_publication_data

publication_by_id_resp = test_publication_data.get("publication_by_id")
publication_by_pubmed_id_resp = test_publication_data.get("publication_by_pubmed_id")


@patch("geneweaver.api.services.publications.get_publication")
def test_valid_url_req(mock_pub_service_call, client):
    """Test valid url request to get publication by id."""
    mock_pub_service_call.return_value = publication_by_id_resp

    response = client.get(url="/api/publications/123", params={"as_pubmed_id": False})

    assert response.status_code == 200
    assert response.json() == publication_by_id_resp


@patch("geneweaver.api.services.publications.get_publication_by_pubmed_id")
def test_valid_pubmed_url_req(mock_pub_service_call, client):
    """Test valid url request to get publication by pubmed id."""
    mock_pub_service_call.return_value = publication_by_pubmed_id_resp

    response = client.get(
        url="/api/publications/17931734", params={"as_pubmed_id": True}
    )

    assert response.status_code == 200
    assert response.json() == publication_by_pubmed_id_resp


@patch("geneweaver.api.services.publications.get_publication")
def test_pub_record_not_found(mock_pub_service_call, client):
    """Test pub record not found response."""
    mock_pub_service_call.return_value = {"publication": None}

    response = client.get(
        url="/api/publications/456456", params={"as_pubmed_id": False}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": message.RECORD_NOT_FOUND_ERROR}


@patch("geneweaver.api.services.publications.get_publication_by_pubmed_id")
def test_pubmed_record_not_found(mock_pub_service_call, client):
    """Test pubmed record not found response."""
    mock_pub_service_call.return_value = {"publication": None}

    response = client.get(url="/api/publications/456456", params={"as_pubmed_id": True})

    assert response.status_code == 404
    assert response.json() == {"detail": message.RECORD_NOT_FOUND_ERROR}


@patch("geneweaver.api.services.publications.get_publication")
def test_invalid_pub_id_type(mock_pub_service_call, client):
    """Test pub record not found response."""
    mock_pub_service_call.return_value = {"publication": None}

    response = client.get(url="/api/publications/werte123")
    assert response.status_code == 422
