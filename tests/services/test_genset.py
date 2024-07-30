"""Tests for geneset Service."""

from unittest.mock import patch

import pytest
from geneweaver.api.controller import message
from geneweaver.api.core.exceptions import UnauthorizedException
from geneweaver.api.schemas.auth import AppRoles, User
from geneweaver.api.services import geneset
from geneweaver.core.enum import GeneIdentifier, GenesetTier, Species
from geneweaver.core.schema.score import GenesetScoreType

from tests.data import test_geneset_data

geneset_by_id_resp = test_geneset_data.get("geneset_by_id_resp")
geneset_list_resp = test_geneset_data.get("geneset_list_resp")
geneset_w_gene_id_type_resp = test_geneset_data.get("geneset_w_gene_id_type_resp")
geneset_metadata_w_pub_info = test_geneset_data.get("geneset_metadata_w_pub_info")
geneset_genes_values_resp = test_geneset_data.get("geneset_genes_values_resp_1")
geneset_threshold_update_req = test_geneset_data.get("geneset_threshold_update_req")
mock_user = User()
mock_user.id = 1


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset(mock_db_geneset, mock_db_genset_value):
    """Test basic get geneset by ID."""
    mock_db_geneset.get.return_value = {}
    mock_db_genset_value.get.return_value = [{}]
    response = geneset.get_geneset(None, 1234, mock_user)
    assert response.get("error") is None


@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_no_user_access(mock_db_geneset):
    """Test get geneset by ID with no user access."""
    response = geneset.get_geneset(None, 1234, None)
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    mock_db_geneset.get.return_value = []
    response = geneset.get_geneset(None, 1234, mock_user)
    assert response.get("data") is None


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_returned_values(mock_db_genset_value, mock_db_geneset):
    """Test get geneset by ID data response structure."""
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    mock_db_genset_value.by_geneset_id.return_value = geneset_by_id_resp.get(
        "geneset_values"
    )
    response = geneset.get_geneset(None, 1234, mock_user)

    assert response.get("geneset") == geneset_by_id_resp["geneset"]
    assert response.get("geneset_values") == geneset_by_id_resp["geneset_values"]


@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_db_call_error(mock_db_geneset):
    """Test error in get DB call."""
    mock_db_geneset.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_geneset(None, 1234, mock_user)


@patch("geneweaver.api.services.geneset.db_gene")
@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_w_gene_id_type_response(
    mock_db_genset_value,
    mock_db_geneset,
    mock_db_gene,
):
    """Test get geneset by ID with gene identifier type data response."""
    mock_db_geneset.get.return_value = [geneset_w_gene_id_type_resp.get("geneset")]
    mock_db_genset_value.by_geneset_id.return_value = geneset_w_gene_id_type_resp.get(
        "geneset_values"
    )
    mock_db_gene.gene_database_by_id.return_value = [{"sp_id": 0}]

    response = geneset.get_geneset_w_gene_id_type(
        None, 1234, mock_user, GeneIdentifier(2)
    )

    assert response.get("geneset") == geneset_w_gene_id_type_resp["geneset"]
    assert (
        response.get("gene_identifier_type")
        == geneset_w_gene_id_type_resp["gene_identifier_type"]
    )
    assert (
        response.get("geneset_values") == geneset_w_gene_id_type_resp["geneset_values"]
    )


@patch("geneweaver.api.services.geneset.db_gene")
@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_w_gene_id_type_2_response(
    mock_db_genset_value,
    mock_db_geneset,
    mock_db_gene,
):
    """Test get geneset by ID with gene identifier type data response."""
    mock_db_geneset.get.return_value = [geneset_w_gene_id_type_resp.get("geneset")]
    mock_db_genset_value.by_geneset_id.return_value = geneset_w_gene_id_type_resp.get(
        "geneset_values"
    )
    mock_db_gene.gene_database_by_id.return_value = [{"sp_id": 1}]

    response = geneset.get_geneset_w_gene_id_type(
        None, 1234, mock_user, GeneIdentifier(2)
    )

    assert response.get("geneset") == geneset_w_gene_id_type_resp["geneset"]
    assert (
        response.get("gene_identifier_type")
        == geneset_w_gene_id_type_resp["gene_identifier_type"]
    )
    assert (
        response.get("geneset_values") == geneset_w_gene_id_type_resp["geneset_values"]
    )


def test_get_geneset_w_gene_id_type_no_user():
    """Test get_geneset_w_gene_id_type with invalid user."""
    response = geneset.get_geneset_w_gene_id_type(None, 1234, None, GeneIdentifier(2))
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    response = geneset.get_geneset_w_gene_id_type(
        None, 1234, User(id=None), GeneIdentifier(2)
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN


@patch("geneweaver.api.services.geneset.db_geneset")
def test_geneset_w_gene_id_type_db_call_error(mock_db_geneset):
    """Test error in get DB call."""
    mock_db_geneset.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_geneset_w_gene_id_type(None, 1234, mock_user, GeneIdentifier(2))


@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_metadata(mock_db_geneset):
    """Test get geneset metadata by geneset id."""
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    response = geneset.get_geneset_metadata(None, 1234, mock_user)

    assert response.get("geneset") == geneset_by_id_resp["geneset"]

    response = geneset.get_geneset_metadata(None, 1234, None)
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    response = geneset.get_geneset_metadata(None, 1234, User(id=None))
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN


@patch("geneweaver.api.services.geneset.db_geneset")
def test_get_geneset_metadata_w_pub_info(mock_db_geneset):
    """Test get geneset metadata by geneset id with publication info."""
    mock_db_geneset.get.return_value = [geneset_metadata_w_pub_info]
    response = geneset.get_geneset_metadata(None, 1234, mock_user, True)

    assert response.get("geneset") == geneset_metadata_w_pub_info


@patch("geneweaver.api.services.geneset.db_geneset")
def test_geneset_metadata_db_call_error(mock_db_geneset):
    """Test error in get DB call."""
    mock_db_geneset.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_geneset_metadata(None, 1234, mock_user, True)


@patch("geneweaver.api.services.geneset.db_geneset")
def test_visible_geneset_response(mock_db_geneset):
    """Test general get geneset data no parameters -- default limit."""
    mock_db_geneset.get.return_value = geneset_list_resp

    response = geneset.get_visible_genesets(None, mock_user)
    assert response.get("data") == geneset_list_resp


@pytest.mark.parametrize(
    "user",
    [None, User(id=None), User(email="Something"), User(email="None", sso_id="None")],
)
@pytest.mark.parametrize(
    "curation_tier",
    [
        None,
        {GenesetTier("Tier I")},
        {GenesetTier("Tier II")},
        {GenesetTier("Tier II"), GenesetTier("Tier III")},
        {GenesetTier("Tier II"), GenesetTier("Tier III"), GenesetTier("Tier V")},
        {GenesetTier.TIER1, GenesetTier.TIER5},
        {GenesetTier.TIER2, GenesetTier.TIER5},
        {GenesetTier.TIER3, GenesetTier.TIER5},
        {GenesetTier.TIER4, GenesetTier.TIER5},
        {
            GenesetTier.TIER1,
            GenesetTier.TIER2,
            GenesetTier.TIER3,
            GenesetTier.TIER4,
            GenesetTier.TIER5,
        },
        {GenesetTier.TIER5},
    ],
)
@patch("geneweaver.api.services.geneset.db_geneset")
def test_visible_geneset_no_user(mock_db_geneset, user, curation_tier):
    """Test general get geneset data invalid user."""
    mock_db_geneset.get.return_value = geneset_list_resp

    if curation_tier == {GenesetTier.TIER5}:
        with pytest.raises(expected_exception=UnauthorizedException):
            _ = geneset.get_visible_genesets(None, user, curation_tier=curation_tier)
    else:
        response = geneset.get_visible_genesets(None, user, curation_tier=curation_tier)
        assert "Error" not in response
        assert mock_db_geneset.get.called is True
        assert mock_db_geneset.get.call_count == 1
        called_args, called_kwargs = mock_db_geneset.get.call_args
        if curation_tier is None:
            assert called_kwargs["curation_tier"] == {
                GenesetTier.TIER1,
                GenesetTier.TIER2,
                GenesetTier.TIER3,
                GenesetTier.TIER4,
            }
        else:
            assert called_kwargs["curation_tier"] == curation_tier - {GenesetTier.TIER5}


@patch("geneweaver.api.services.geneset.db_geneset")
def test_visible_geneset_all_expected_parameters(mock_db_geneset):
    """Test general get geneset data no parameters -- default limit."""
    mock_db_geneset.get.return_value = geneset_list_resp

    response = geneset.get_visible_genesets(
        cursor=None,
        user=mock_user,
        gs_id=1,
        only_my_genesets=False,
        curation_tier={GenesetTier("Tier I")},
        species=Species(2),
        name="test Name",
        abbreviation="test",
        publication_id=123,
        pubmed_id="p123",
        gene_id_type=GeneIdentifier(5),
        limit=10,
        offset=0,
        with_publication_info=True,
    )

    assert response.get("data") == geneset_list_resp


@patch("geneweaver.api.services.geneset.db_geneset")
def test_visible_geneset_db_call_error(mock_db_geneset):
    """Test error in get DB call."""
    mock_db_geneset.get.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_visible_genesets(None, mock_user)


@patch("geneweaver.api.services.geneset.db_gene")
def test_map_geneset_homology(mock_db_gene):
    """Test map_geneset_homology call."""
    mock_db_gene.get_homolog_ids_by_ode_id.return_value = geneset_by_id_resp[
        "geneset_values"
    ]

    response = geneset.map_geneset_homology(
        None, geneset_by_id_resp["geneset_values"], GeneIdentifier(2)
    )
    assert response == geneset_by_id_resp["geneset_values"]


@patch("geneweaver.api.services.geneset.db_gene")
def test_map_geneset_homology_db_call_error(mock_db_gene):
    """Test error in get DB call."""
    mock_db_gene.get_homolog_ids_by_ode_id.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.map_geneset_homology(
            None, geneset_by_id_resp["geneset_values"], GeneIdentifier(2)
        )


@patch("geneweaver.api.services.geneset.db_geneset_value")
@patch("geneweaver.api.services.geneset.db_geneset")
def test_geneset_gene_value_response(mock_db_geneset, mock_db_geneset_value):
    """Test geneset gene value data response."""
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    mock_db_geneset_value.by_geneset_id.return_value = geneset_by_id_resp.get(
        "geneset_values"
    )

    response = geneset.get_geneset_gene_values(
        None, user=mock_user, geneset_id=1234, gene_id_type=None
    )
    assert response == geneset_genes_values_resp


@pytest.mark.parametrize("gsv_in_threshold", [None, True, False])
@pytest.mark.parametrize("identifier", [None, GeneIdentifier.ENSEMBLE_GENE])
@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_gene")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_geneset_gene_value_within_threshold(
    mock_db_geneset_value, mock_db_gene, mock_db_geneset, gsv_in_threshold, identifier
):
    """Test geneset gene value data response with in threshold filter."""
    mock_db_gene.gene_database_by_id.return_value = [{"sp_id": 0}]
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    mock_db_geneset_value.by_geneset_id.return_value = geneset_by_id_resp.get(
        "geneset_values"
    )

    response = geneset.get_geneset_gene_values(
        None,
        user=mock_user,
        geneset_id=1234,
        gene_id_type=identifier,
        in_threshold=gsv_in_threshold,
    )
    assert response == geneset_genes_values_resp


@pytest.mark.parametrize("gsv_in_threshold", [None, True, False])
@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_with_threshold(
    mock_db_genset_value, mock_db_geneset, gsv_in_threshold
):
    """Test get genset with threshold."""
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    mock_db_genset_value.by_geneset_id.return_value = geneset_by_id_resp.get(
        "geneset_values"
    )
    response = geneset.get_geneset(
        cursor=None, geneset_id=1234, user=mock_user, in_threshold=gsv_in_threshold
    )

    assert response.get("geneset") == geneset_by_id_resp["geneset"]
    assert response.get("geneset_values") == geneset_by_id_resp["geneset_values"]


@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_gene_values_db_errors(mock_db_geneset_value):
    """Test error in get DB call."""
    mock_db_geneset_value.by_geneset_id.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        geneset.get_geneset_gene_values(
            None, user=mock_user, geneset_id=1234, gene_id_type=None
        )


@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_get_geneset_gene_values_invalid_user(mock_db_geneset_value):
    """Test invalid user."""
    response = geneset.get_geneset_gene_values(
        None, user=None, geneset_id=1234, gene_id_type=None
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_threshold")
def test_geneset_thershold_update(mock_db_threshold, mock_db_geneset):
    """Test geneset gene value data response."""
    mock_db_threshold.set_geneset_threshold.return_value = None
    mock_db_geneset.user_is_owner.return_value = True
    geneset_threshold = GenesetScoreType(**geneset_threshold_update_req)

    response = geneset.update_geneset_threshold(
        cursor=None, user=mock_user, geneset_id=1234, geneset_score=geneset_threshold
    )
    assert response == {}


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_threshold")
def test_geneset_thershold_update_errors(mock_db_threshold, mock_db_geneset):
    """Test geneset gene value data response."""
    mock_db_threshold.set_geneset_threshold.return_value = None
    mock_db_geneset.user_is_owner.return_value = False
    geneset_threshold = GenesetScoreType(**geneset_threshold_update_req)

    # user is not the geneset owner
    response = geneset.update_geneset_threshold(
        cursor=None, user=mock_user, geneset_id=1234, geneset_score=geneset_threshold
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    # user is not logged-in
    response = geneset.update_geneset_threshold(
        cursor=None, user=None, geneset_id=1234, geneset_score=geneset_threshold
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    # db error
    mock_db_geneset.user_is_owner.return_value = True
    mock_db_threshold.set_geneset_threshold.side_effect = Exception("ERROR")
    with pytest.raises(expected_exception=Exception):
        geneset.update_geneset_threshold(
            cursor=None,
            user=mock_user,
            geneset_id=1234,
            geneset_score=geneset_threshold,
        )


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_gene")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_geneset_gene_value_w_gene_id_type(
    mock_db_geneset_value, mock_db_gene, mock_db_geneset
):
    """Test geneset gene value data response."""
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    mock_db_gene.gene_database_by_id.return_value = [{"sp_id": 0}]
    mock_db_geneset_value.by_geneset_id.return_value = geneset_by_id_resp.get(
        "geneset_values"
    )

    response = geneset.get_geneset_gene_values(
        None, user=mock_user, geneset_id=1234, gene_id_type=GeneIdentifier(2)
    )
    assert response == geneset_genes_values_resp


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_gene")
@patch("geneweaver.api.services.geneset.db_geneset_value")
def test_geneset_gene_value_w_gene_id_type_none_resp(
    mock_db_geneset_value, mock_db_gene, mock_db_geneset
):
    """Test geneset gene value data empty response."""
    mock_db_geneset.get.return_value = [geneset_by_id_resp.get("geneset")]
    mock_db_gene.gene_database_by_id.return_value = [{"sp_id": 0}]
    mock_db_geneset_value.by_geneset_id.return_value = None
    response = geneset.get_geneset_gene_values(
        None, user=mock_user, geneset_id=1234, gene_id_type=GeneIdentifier(2)
    )
    assert response == {"data": None}


@patch("geneweaver.api.services.geneset.db_geneset")
def test_geneset_gene_value_w_gene_id_type_none_resp2(mock_db_geneset):
    """Test geneset gene value data empty response."""
    mock_db_geneset.get.return_value = []

    response = geneset.get_geneset_gene_values(
        None, user=mock_user, geneset_id=1234, gene_id_type=GeneIdentifier(2)
    )
    assert response == {"data": None}


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_ontology")
def test_add_geneset_ontology_term(mock_db_ontology, mock_db_geneset):
    """Test add geneset ontology terms response."""
    mock_reponse = {"data": {"gs_id": 1234, "ont_id": 1}}
    mock_db_ontology.by_ontology_term.return_value = {"onto_id": 123123}
    mock_db_geneset.user_is_owner.return_value = True
    mock_db_ontology.add_ontology_term_to_geneset.return_value = mock_reponse.get(
        "data"
    )

    response = geneset.add_geneset_ontology_term(
        cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
    )
    assert response == mock_reponse

    # user is not the geneset owner, but he is a curator
    mock_db_geneset.user_is_owner.return_value = False
    mock_user.role = AppRoles.curator
    response = geneset.add_geneset_ontology_term(
        cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
    )
    assert response == mock_reponse


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_ontology")
def test_add_geneset_ontology_term_errors(mock_db_ontology, mock_db_geneset):
    """Test add geneset ontology term errors."""
    mock_reponse = {"data": {"gs_id": 1234, "ont_id": 1}}
    mock_db_ontology.by_ontology_term.return_value = {"onto_id": 123123}
    mock_db_ontology.add_ontology_term_to_geneset.return_value = mock_reponse.get(
        "data"
    )

    # user is not the geneset owner and he is not a curator
    mock_db_geneset.user_is_owner.return_value = False
    mock_user.role = None
    response = geneset.add_geneset_ontology_term(
        cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    # user is not logged-in
    response = geneset.add_geneset_ontology_term(
        cursor=None, user=None, geneset_id=1234, ref_term_id="D001921"
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    # Ontology term is not found
    mock_db_ontology.by_ontology_term.return_value = None
    mock_db_geneset.user_is_owner.return_value = True
    response = geneset.add_geneset_ontology_term(
        cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
    )
    assert response.get("error") is True
    assert response.get("message") == message.RECORD_NOT_FOUND_ERROR

    # db error
    mock_db_geneset.user_is_owner.return_value = True
    mock_db_ontology.by_ontology_term.return_value = {"onto_id": 123123}
    mock_db_ontology.add_ontology_term_to_geneset.side_effect = Exception("ERROR")
    with pytest.raises(expected_exception=Exception):
        geneset.add_geneset_ontology_term(
            cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
        )


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_ontology")
def test_delete_geneset_ontology_term(mock_db_ontology, mock_db_geneset):
    """Test delete geneset ontology term response."""
    mock_reponse = {"data": {"gs_id": 1234, "ont_id": 1}}
    mock_db_ontology.by_ontology_term.return_value = {"onto_id": 123123}
    mock_db_geneset.user_is_owner.return_value = True
    mock_db_ontology.delete_ontology_term_from_geneset.return_value = mock_reponse.get(
        "data"
    )

    response = geneset.delete_geneset_ontology_term(
        cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
    )
    assert response == mock_reponse

    # user is not the geneset owner, but he is a curator
    mock_db_geneset.user_is_owner.return_value = False
    mock_user.role = AppRoles.curator
    response = geneset.delete_geneset_ontology_term(
        cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
    )
    assert response == mock_reponse


@patch("geneweaver.api.services.geneset.db_geneset")
@patch("geneweaver.api.services.geneset.db_ontology")
def test_delete_geneset_ontology_term_errors(mock_db_ontology, mock_db_geneset):
    """Test delete geneset ontology term errors."""
    mock_reponse = {"data": {"gs_id": 1234, "ont_id": 1}}
    mock_db_ontology.by_ontology_term.return_value = {"onto_id": 123123}
    mock_db_ontology.delete_ontology_term_from_geneset.return_value = mock_reponse.get(
        "data"
    )

    # user is not the geneset owner and he is not a curator
    mock_db_geneset.user_is_owner.return_value = False
    mock_user.role = None
    response = geneset.delete_geneset_ontology_term(
        cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    # user is not logged-in
    response = geneset.delete_geneset_ontology_term(
        cursor=None, user=None, geneset_id=1234, ref_term_id="D001921"
    )
    assert response.get("error") is True
    assert response.get("message") == message.ACCESS_FORBIDDEN

    # Ontology term is not found
    mock_db_ontology.by_ontology_term.return_value = None
    mock_db_geneset.user_is_owner.return_value = True
    response = geneset.delete_geneset_ontology_term(
        cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
    )
    assert response.get("error") is True
    assert response.get("message") == message.RECORD_NOT_FOUND_ERROR

    # db error
    mock_db_geneset.user_is_owner.return_value = True
    mock_db_ontology.by_ontology_term.return_value = {"onto_id": 123123}
    mock_db_ontology.delete_ontology_term_from_geneset.side_effect = Exception("ERROR")
    with pytest.raises(expected_exception=Exception):
        geneset.delete_geneset_ontology_term(
            cursor=None, user=mock_user, geneset_id=1234, ref_term_id="D001921"
        )
