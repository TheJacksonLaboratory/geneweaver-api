"""Tests for publications Service."""

from unittest.mock import patch

from geneweaver.api.services import publications as pub_service

from tests.data import test_publication_data

publication_by_id_resp = test_publication_data.get("publication_by_id")
publication_by_pubmed_id_resp = test_publication_data.get("publication_by_pubmed_id")


@patch("geneweaver.api.services.publications.db_publication")
def test_get_publication_by_id(mock_db_publication):
    """Test get publication by ID data response structure."""
    mock_db_publication.by_id.return_value = publication_by_id_resp

    response = pub_service.get_publication(None, 123)

    assert response.get("publication") == publication_by_id_resp


@patch("geneweaver.api.services.publications.db_publication")
def test_get_publication_by_pubmed_id(mock_db_publication):
    """Test get publication by ID data response structure."""
    mock_db_publication.by_pubmed_id.return_value = publication_by_id_resp

    response = pub_service.get_publication_by_pubmed_id(None, "17931734")

    assert response.get("publication") == publication_by_id_resp
