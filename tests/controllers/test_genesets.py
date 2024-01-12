"""Tests for geneset API."""
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from geneweaver.api.controller.genesets import get_gene_identifier_type
from geneweaver.core.enum import GeneIdentifier

from tests.data import test_geneset_data

geneset_by_id_resp = test_geneset_data.get("geneset_by_id_resp")
geneset_w_gene_id_type_resp = test_geneset_data.get("geneset_w_gene_id_type_resp")


@patch("geneweaver.api.services.geneset.get_geneset")
@patch("geneweaver.api.services.geneset.is_geneset_readable_by_user")
def test_get_geneset_response(mock_genset_is_readable, mock_get_genenset, client):
    """Test get geneset ID data response."""
    mock_genset_is_readable.return_value = True
    mock_get_genenset.return_value = geneset_by_id_resp

    response = client.get("/api/genesets/1234")
    assert response.status_code == 200
    assert response.json() == geneset_by_id_resp


@patch("geneweaver.api.services.geneset.db_is_readable")
def test_get_geneset_forbidden(mock_genset_is_readable, client):
    """Test forbidden response."""
    mock_genset_is_readable.return_value = False
    response = client.get("/api/genesets/1234")

    assert response.json() == {"detail": "Forbidden"}
    assert response.status_code == 403


@patch("geneweaver.api.services.geneset.db_is_readable")
def test_get_geneset_unexpected_error(mock_genset_is_readable, client):
    """Test unexpected error response."""
    mock_genset_is_readable.side_effect = Exception

    with pytest.raises(expected_exception=Exception):
        client.get("/api/genesets/1234")


def test_get_gene_identifier_type():
    """Test get gene identifier type responses."""
    assert get_gene_identifier_type(2) == GeneIdentifier(2)
    with pytest.raises(expected_exception=HTTPException):
        get_gene_identifier_type(25)


@patch("geneweaver.api.services.geneset.get_geneset_w_gene_id_type")
def test_get_geneset_w_gene_id_type(mock_service_get_geneset_w_gene_id_type, client):
    """Test get geneset with gene id type response."""
    mock_service_get_geneset_w_gene_id_type.return_value = geneset_w_gene_id_type_resp
    response = client.get("/api/genesets/1234?gene_id_type=2")

    assert response.json() == geneset_w_gene_id_type_resp
    assert response.status_code == 200


@patch("geneweaver.api.services.geneset.db_is_readable")
def test_get_geneset_export_forbidden(mock_genset_is_readable, client):
    """Test export forbidden response."""
    mock_genset_is_readable.return_value = False
    response = client.get("/api/genesets/1234/export?gene_id_type=2")

    assert response.json() == {"detail": "Forbidden"}
    assert response.status_code == 403


@patch("geneweaver.api.services.geneset.get_geneset_w_gene_id_type")
def test_export_geneset_w_gene_id_type(mock_service_get_geneset_w_gene_id_type, client):
    """Test geneset file export."""
    mock_service_get_geneset_w_gene_id_type.return_value = geneset_w_gene_id_type_resp
    response = client.get("/api/genesets/1234/export?gene_id_type=2")

    assert response.headers.get("content-type") == "application/octet-stream"
    assert int(response.headers.get("content-length")) > 0
    assert response.status_code == 200
