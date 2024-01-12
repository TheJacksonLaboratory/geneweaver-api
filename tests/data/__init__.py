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

# returns JSON string as a dictionary
test_geneset_data = {
    "geneset_by_id_resp": json.loads(geneset_response_json),
    "geneset_w_gene_id_type_resp": json.loads(geneset_w_gene_id_type_json),
}
