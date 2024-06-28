"""Data package for tests."""

import importlib.resources
import json

from geneweaver.core.enum import GeneIdentifier

## Load test data
# Opening JSON files
geneset_response_json = importlib.resources.read_text(
    "tests.data", "response_geneset_1234.json"
)
geneset_w_gene_id_type_json = importlib.resources.read_text(
    "tests.data", "response_geneset_w_gene_id_type.json"
)

geneset_list_response_json = importlib.resources.read_text("tests.data", "geneset.json")

gene_homologus_ids_json = importlib.resources.read_text(
    "tests.data", "homologus_ids.json"
)

gene_id_mapping_json = importlib.resources.read_text("tests.data", "gene_maping.json")

publications_json = importlib.resources.read_text("tests.data", "publications.json")

jwt_test_keys_json = importlib.resources.read_text(
    "tests.data", "security_jwt_RS256_keys.json"
)

species_json = importlib.resources.read_text("tests.data", "species.json")

genes_json = importlib.resources.read_text("tests.data", "genes.json")

monitors_json = importlib.resources.read_text("tests.data", "monitors.json")

## laod and returns JSON string as a dictionary

# geneset test data
test_geneset_data = {
    "geneset_by_id_resp": json.loads(geneset_response_json),
    "geneset_w_gene_id_type_resp": json.loads(geneset_w_gene_id_type_json),
    "geneset_metadata_w_pub_info": json.loads(geneset_response_json).get(
        "geneset_with_publication_info"
    ),
    "geneset_list_resp": json.loads(geneset_list_response_json).get(
        "geneset_resp_1_list_10"
    ),
    "geneset_genes_values_resp_1": json.loads(geneset_list_response_json).get(
        "geneset_genes_values_resp_1"
    ),
    "geneset_threshold_update_req": json.loads(geneset_list_response_json).get(
        "geneset_threshold_update_req"
    ),
}

# Gene homolog ids test data
test_gene_homolog_data = {
    "gene_ids_map_req_1_gene_ids_species": json.loads(gene_homologus_ids_json).get(
        "gene_ids_map_req_1_gene_ids_species"
    ),
    "gene_ids_map_resp_1": json.loads(gene_homologus_ids_json).get(
        "gene_ids_map_resp_1"
    ),
    "gene_ids_map_req_2_gene_ids_target_species": json.loads(
        gene_homologus_ids_json
    ).get("gene_ids_map_req_2_gene_ids_target_species"),
    "gene_ids_map_resp_2": json.loads(gene_homologus_ids_json).get(
        "gene_ids_map_resp_2"
    ),
    "gene_ids_map_req_3_gene_ids_no_species": json.loads(gene_homologus_ids_json).get(
        "gene_ids_map_req_3_gene_ids_no_species"
    ),
    "gene_ids_map_resp_3": json.loads(gene_homologus_ids_json).get(
        "gene_ids_map_resp_3"
    ),
}

# Gene mapping test data
test_gene_mapping_data = {
    "gene_mapping_req_1": json.loads(gene_id_mapping_json).get(
        "gene_mapping_request_1"
    ),
    "gene_mapping_resp_1": json.loads(gene_id_mapping_json).get(
        "gene_mapping_response_1"
    ),
    "gene_mapping_req_2": json.loads(gene_id_mapping_json).get(
        "gene_mapping_request_2"
    ),
    "gene_mapping_resp_2": json.loads(gene_id_mapping_json).get(
        "gene_mapping_response_2"
    ),
    "gene_aon_mapping_req_1": json.loads(gene_id_mapping_json).get(
        "gene_aon_mapping_request_1"
    ),
    "gene_aon_mapping_resp_1": json.loads(gene_id_mapping_json).get(
        "gene_aon_mapping_response_1"
    ),
}

# Publication test data
test_publication_data = {
    "publication_by_id": json.loads(publications_json).get("publication_by_id"),
    "publication_by_pubmed_id": json.loads(publications_json).get(
        "publication_by_pubmed_id"
    ),
    "add_pubmed_info": json.loads(publications_json).get("add_pubmed_info"),
    "add_pubmed_resp": json.loads(publications_json).get("add_pubmed_resp"),
    "get_publications": json.loads(publications_json).get("get_publications"),
}


# Json web token keys data
test_jwt_keys_data = {
    "test_private_key": json.loads(jwt_test_keys_json).get("private_key"),
    "test_public_key": json.loads(jwt_test_keys_json).get("public_key"),
}


## Species test data
test_species_data = {
    "species_no_parameters": json.loads(species_json).get("species_no_parameters"),
    "species_by_taxonomy_id_10090": json.loads(species_json).get(
        "species_by_taxonomy_id_10090"
    ),
    "species_by_gene_id_type_flybase": json.loads(species_json).get(
        "species_by_gene_id_type_flybase"
    ),
}


## geneweaver genes test data
test_genes_data = {
    "genes_list_10": json.loads(genes_json).get("genes_list_10"),
    "gene_preferred_resp_1": json.loads(genes_json).get("gene_preferred_resp_1"),
}


## monitors test data
test_monitors_data = {
    "db_health_status": json.loads(monitors_json).get("db_health_status"),
}


def get_species_db_resp(species_data: list) -> list:
    """Get species data as returned by DB."""
    species = species_data
    for species_record in species:
        ref_gene_id_type = species_record.get("reference_gene_identifier", None)
        if ref_gene_id_type:
            species_record["reference_gene_identifier"] = GeneIdentifier(
                ref_gene_id_type
            )

    return species
