"""Tests for gene Service."""

from unittest.mock import patch

import pytest
from geneweaver.api.services import genes

from tests.data import test_gene_homolog_data, test_gene_mapping_data, test_genes_data

# genes
genes_list_10 = test_genes_data.get("genes_list_10")
gene_preferred_resp_1 = test_genes_data.get("gene_preferred_resp_1")

# gene homolog ids test data
gene_ids_homolog_req_1 = test_gene_homolog_data.get(
    "gene_ids_map_req_1_gene_ids_species"
)
gene_ids_homolog_req_2 = test_gene_homolog_data.get(
    "gene_ids_map_req_2_gene_ids_target_species"
)
gene_ids_homolog_req_3 = test_gene_homolog_data.get(
    "gene_ids_map_req_3_gene_ids_no_species"
)

gene_ids_homolog_resp_1 = test_gene_homolog_data.get("gene_ids_map_resp_1")
gene_ids_homolog_resp_2 = test_gene_homolog_data.get("gene_ids_map_resp_2")
gene_ids_homolog_resp_3 = test_gene_homolog_data.get("gene_ids_map_resp_3")

# gene id mapping test data
gene_id_mapping_req_1 = test_gene_mapping_data.get("gene_mapping_req_1")
gene_id_mapping_resp_1 = test_gene_mapping_data.get("gene_mapping_resp_1")
gene_id_mapping_req_2 = test_gene_mapping_data.get("gene_mapping_req_2")
gene_id_mapping_resp_2 = test_gene_mapping_data.get("gene_mapping_resp_2")
gene_id_aon_mapping_req_1 = test_gene_mapping_data.get("gene_aon_mapping_req_1")
gene_id_aon_mapping_resp_1 = test_gene_mapping_data.get("gene_aon_mapping_resp_1")


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_id_map_by_gene_ids_and_species(mock_db_gene):
    """Test gene ids map by gene identifiers and species."""
    mock_db_gene.get_homolog_ids.return_value = gene_ids_homolog_resp_1.get(
        "gene_ids_map"
    )

    # Request:
    # (source_ids, target gene id type, source gene id type,
    # target species, source species)
    response = genes.get_homolog_ids(
        None,
        gene_ids_homolog_req_1.get("source_ids"),
        gene_ids_homolog_req_1.get("target_gene_id_type"),
        gene_ids_homolog_req_1.get("source_gene_id_type"),
        gene_ids_homolog_req_1.get("target_species"),
        gene_ids_homolog_req_1.get("source_species"),
    )

    assert response.get("error") is None
    assert response.get("ids_map") == gene_ids_homolog_resp_1.get("gene_ids_map")


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_id_map_by_gene_ids_and_target_no_source_species(mock_db_gene):
    """Test gene ids map by gene identifiers.

    Target species but no source species.
    """
    mock_db_gene.get_homolog_ids.return_value = gene_ids_homolog_resp_2.get(
        "gene_ids_map"
    )

    # Request:
    # (source_ids, target gene id type, source gene id type, target species)
    response = genes.get_homolog_ids(
        None,
        gene_ids_homolog_req_2.get("source_ids"),
        gene_ids_homolog_req_2.get("target_gene_id_type"),
        gene_ids_homolog_req_2.get("source_gene_id_type"),
        gene_ids_homolog_req_2.get("target_species"),
        None,
    )

    assert response.get("error") is None
    assert response.get("ids_map") == gene_ids_homolog_resp_2.get("gene_ids_map")


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_id_map_by_gene_ids_and_target_no_species(mock_db_gene):
    """Test gene ids map by gene identifiers.

    Target species but no source or target species.
    """
    mock_db_gene.get_homolog_ids.return_value = gene_ids_homolog_resp_3.get(
        "gene_ids_map"
    )

    # Request:
    # (source_ids, target gene id type, source gene id type)
    response = genes.get_homolog_ids(
        None,
        gene_ids_homolog_req_3.get("source_ids"),
        gene_ids_homolog_req_3.get("target_gene_id_type"),
        gene_ids_homolog_req_3.get("source_gene_id_type"),
        None,
        None,
    )

    assert response.get("error") is None
    assert response.get("ids_map") == gene_ids_homolog_resp_3.get("gene_ids_map")


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_id_homolog_error(mock_db_gene):
    """Test error in DB call."""
    mock_db_gene.get_homolog_ids.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        genes.get_homolog_ids(
            None,
            gene_ids_homolog_req_3.get("source_ids"),
            gene_ids_homolog_req_3.get("target_gene_id_type"),
            gene_ids_homolog_req_3.get("source_gene_id_type"),
            None,
            None,
        )


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_id_map_missing_target_gene_identifier(mock_db_gene):
    """Test error with get gene ids map by gene Identifiers.

    Missing target identifier.
    """
    mock_db_gene.get_homolog_ids.return_value = gene_ids_homolog_resp_3.get(
        "gene_ids_map"
    )

    with pytest.raises(expected_exception=TypeError):
        genes.get_homolog_ids(
            cursor=None,
            gene_id_list=gene_ids_homolog_req_3.get("source_ids"),
            # no target gene identifier
            source_gene_id_type=gene_ids_homolog_req_3.get("source_gene_id_type"),
        )


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_map_mouse(mock_db_gene):
    """Test gene ids map by gene id type and species - Mouse."""
    mock_db_gene.mapping.return_value = gene_id_mapping_resp_1.get("gene_ids_map")

    # Request:
    # (source_ids, target gene id type, target species)
    response = genes.get_gene_mapping(
        None,
        gene_id_mapping_req_1.get("source_ids"),
        gene_id_mapping_req_1.get("species"),
        gene_id_mapping_req_1.get("target_gene_id_type"),
    )

    assert response.get("error") is None
    assert response.get("ids_map") == gene_id_mapping_resp_1.get("gene_ids_map")


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_map_human(mock_db_gene):
    """Test gene ids map by gene id type and species - Human."""
    mock_db_gene.mapping.return_value = gene_id_mapping_resp_2.get("gene_ids_map")

    # Request:
    # (source_ids, target gene id type, target species)
    response = genes.get_gene_mapping(
        None,
        gene_id_mapping_req_2.get("source_ids"),
        gene_id_mapping_req_2.get("species"),
        gene_id_mapping_req_2.get("target_gene_id_type"),
    )

    assert response.get("error") is None
    assert response.get("ids_map") == gene_id_mapping_resp_2.get("gene_ids_map")


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_map_error(mock_db_gene):
    """TTest error in DB call."""
    mock_db_gene.mapping.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        genes.get_gene_mapping(
            None,
            gene_id_mapping_req_2.get("source_ids"),
            gene_id_mapping_req_2.get("species"),
            gene_id_mapping_req_2.get("target_gene_id_type"),
        )


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_aon_map(mock_db_gene):
    """Test gene ids map by gene id type and species - Human."""
    mock_db_gene.aon_mapping.return_value = gene_id_aon_mapping_resp_1.get(
        "gene_ids_map"
    )

    # Request:
    # (source_ids, target gene id type, target species)
    response = genes.get_gene_aon_mapping(
        None,
        gene_id_aon_mapping_req_1.get("source_ids"),
        gene_id_aon_mapping_req_1.get("species"),
    )

    assert response.get("error") is None
    assert response.get("ids_map") == gene_id_aon_mapping_resp_1.get("gene_ids_map")


@patch("geneweaver.api.services.genes.db_gene")
def test_get_aon_gene_map_error(mock_db_gene):
    """Test error in DB call."""
    mock_db_gene.aon_mapping.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        genes.get_gene_aon_mapping(
            None,
            gene_id_aon_mapping_req_1.get("source_ids"),
            gene_id_aon_mapping_req_1.get("species"),
        )


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_error(mock_db_gene):
    """Test error in DB call."""
    mock_db_gene.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        genes.get_genes(None)


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene(mock_db_gene):
    """Test get gene."""
    mock_db_gene.get.return_value = genes_list_10

    response = genes.get_genes(None)

    assert response.get("error") is None
    assert response.get("data") == genes_list_10

    response = genes.get_genes(
        None,
        gene_database=10,
        species=1,
        preferred=False,
        reference_id="MGI:87853",
        limit=10,
        offset=10,
    )

    assert response.get("error") is None


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_preferred(mock_db_gene):
    """Test get gene preferred."""
    mock_db_gene.get_preferred.return_value = gene_preferred_resp_1

    response = genes.get_gene_preferred(None, gene_id=1000)

    assert response.get("error") is None
    assert response == gene_preferred_resp_1


@patch("geneweaver.api.services.genes.db_gene")
def test_get_gene_preferred_error(mock_db_gene):
    """Test error in DB call gene_preferred."""
    mock_db_gene.get_preferred.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        genes.get_gene_preferred(None, gene_id=1000)
