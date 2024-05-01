"""Tests for publications Service."""

from unittest.mock import patch

import pytest
from geneweaver.api.controller import message
from geneweaver.api.schemas.auth import User
from geneweaver.api.services import publications as pub_service
from geneweaver.core.exc import ExternalAPIError

from tests.data import test_publication_data

publication_by_id_resp = test_publication_data.get("publication_by_id")
publication_by_pubmed_id_resp = test_publication_data.get("publication_by_pubmed_id")
add_pubmed_info = test_publication_data.get("add_pubmed_info")
add_pubmed_resp = test_publication_data.get("add_pubmed_resp")
mock_user = User()
mock_user.id = 1


@patch("geneweaver.api.services.publications.db_publication")
def test_get_publication_by_id(mock_db_publication):
    """Test get publication by ID data response structure."""
    mock_db_publication.by_id.return_value = publication_by_id_resp

    response = pub_service.get_publication(None, 123)

    assert response == publication_by_id_resp


@patch("geneweaver.api.services.publications.db_publication")
def test_get_publication_by_pubmed_id(mock_db_publication):
    """Test get publication by ID data response structure."""
    mock_db_publication.by_pubmed_id.return_value = publication_by_id_resp

    response = pub_service.get_publication_by_pubmed_id(None, "17931734")

    assert response == publication_by_id_resp


@patch("geneweaver.api.services.publications.db_publication")
def test_get_publication_errors(mock_db_publication):
    """Test get publication by ID data response structure."""
    # unexpected error
    mock_db_publication.by_pubmed_id.side_effect = Exception()
    with pytest.raises(expected_exception=Exception):
        pub_service.get_publication_by_pubmed_id(cursor=None, pubmed_id=1234)

    # unexpected error
    mock_db_publication.by_id.side_effect = Exception()
    with pytest.raises(expected_exception=Exception):
        pub_service.get_publication(cursor=None, pub_id=123)


@patch("geneweaver.api.services.publications.pubmed")
@patch("geneweaver.api.services.publications.db_publication")
def test_add_pubmed_publication(mock_db_publication, mock_pubmed):
    """Test persisting non-existing pubmed publication."""
    mock_pubmed.get_publication.return_value = add_pubmed_info
    mock_db_publication.by_pubmed_id.return_value = None
    mock_db_publication.add.return_value = {"pub_id": add_pubmed_resp.get("pub_id")}

    response = pub_service.add_pubmed_record(
        cursor=None, user=mock_user, pubmed_id=1234
    )

    assert response == add_pubmed_resp


@patch("geneweaver.api.services.publications.pubmed")
@patch("geneweaver.api.services.publications.db_publication")
def test_add_pubmed_publication_errors(mock_db_publication, mock_pubmed):
    """Test errors adding pubmed info."""
    mock_pubmed.get_publication.return_value = add_pubmed_info
    mock_db_publication.by_pubmed_id.return_value = None
    mock_db_publication.add.return_value = {"pub_id": add_pubmed_resp.get("pub_id")}

    # user is not logged-in
    response = pub_service.add_pubmed_record(cursor=None, user=None, pubmed_id=1234)
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    # pubmed found in DB
    mock_db_publication.by_pubmed_id.return_value = add_pubmed_info
    response = pub_service.add_pubmed_record(
        cursor=None, user=mock_user, pubmed_id=1234
    )
    assert response.get("error") is True
    assert response.get("message") == message.RECORD_EXISTS

    # Error retrieving pubmed info
    mock_db_publication.by_pubmed_id.return_value = None
    mock_pubmed.get_publication.side_effect = ExternalAPIError()
    response = pub_service.add_pubmed_record(
        cursor=None, user=mock_user, pubmed_id=1234
    )
    assert response.get("error") is True
    assert response.get("message") == message.PUBMED_RETRIEVING_ERROR

    # No record returned by DB call
    mock_pubmed.get_publication.side_effect = None
    mock_pubmed.get_publication.return_value = add_pubmed_info
    mock_db_publication.by_pubmed_id.return_value = None
    mock_db_publication.add.return_value = None
    response = pub_service.add_pubmed_record(
        cursor=None, user=mock_user, pubmed_id=1234
    )
    assert response.get("error") is True
    assert response.get("message") == message.UNEXPECTED_ERROR

    # unexpected error
    mock_db_publication.add.side_effect = Exception()
    with pytest.raises(expected_exception=Exception):
        response = pub_service.add_pubmed_record(
            cursor=None, user=mock_user, pubmed_id=1234
        )
