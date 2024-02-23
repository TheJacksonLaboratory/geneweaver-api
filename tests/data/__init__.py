"""Data package for tests."""

import importlib.resources
import json

## Load test data
# Opening JSON files
geneset_response_json = importlib.resources.read_text(
    "tests.data", "response_geneset_1234.json"
)
geneset_w_gene_id_type_json = importlib.resources.read_text(
    "tests.data", "response_geneset_w_gene_id_type.json"
)

gene_homologus_ids_json = importlib.resources.read_text(
    "tests.data", "homologus_ids.json"
)

publications_json = importlib.resources.read_text("tests.data", "publications.json")

jwt_test_keys_json = importlib.resources.read_text(
    "tests.data", "security_jwt_RS256_keys.json"
)


## laod and returns JSON string as a dictionary

# geneset test data
test_geneset_data = {
    "geneset_by_id_resp": json.loads(geneset_response_json),
    "geneset_w_gene_id_type_resp": json.loads(geneset_w_gene_id_type_json),
    "geneset_metadata_w_pub_info": json.loads(geneset_response_json).get(
        "geneset_with_publication_info"
    ),
}

# Gene test data
test_gene_data = {
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

# publication test data
test_publication_data = {
    "publication_by_id": json.loads(publications_json).get("publication_by_id"),
    "publication_by_pubmed_id": json.loads(publications_json).get(
        "publication_by_pubmed_id"
    ),
}

# Json web token keys data =
test_jwt_keys_data = {
    "test_private_key": json.loads(jwt_test_keys_json).get("private_key"),
    "test_public_key": json.loads(jwt_test_keys_json).get("public_key"),
}
