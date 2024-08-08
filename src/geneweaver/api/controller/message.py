"""Constants key/value messages."""

##Errors
ACCESS_FORBIDDEN = "Forbidden"
INACCESSIBLE_OR_FORBIDDEN = "Record not found or forbidden access"
UNEXPECTED_ERROR = "Unexpected Error"
GENE_IDENTIFIER_TYPE_VALUE_ERROR = "Invalid gene identifier type"
RECORD_NOT_FOUND_ERROR = "Record not found"
INVALID_PUBMED_ID_ERROR = "Invalid pubmed id"
RECORD_EXISTS = "Record already in the system"
PUBMED_RETRIEVING_ERROR = "Error retrieving publication info from PubMed API"

##FORM field descriptions
GENE_REFERENCE = "The reference id to search for"
GENE_PREFERRED = "Whether to search for preferred genes"
LIMIT = "The limit of results to return"
OFFSET = "The offset of results to return"
GENESET_ID = "Geneset ID"
ONLY_MY_GS = "Show only geneset results owned by this user ID"
NAME = "Show only results with this name"
ABBREVIATION = "Show only results with this abbreviation"
PUBLICATION_ID = "Show only results with this publication ID"
PUBMED_ID = "Show only results with this PubMed ID"
SEARCH_TEXT = "Return genesets that match this search text"
WITH_PUBLICATION = "Include publication info in the return"
GS_PUB_SEARCH_ENTITIES = "Entites to search, genesets and/or publications"
GS_PUB_SEARCH_TEXT = (
    "Gensets and/or publications search types ('genesets', 'publications') "
)
CHECK_DB_HEALTH = "Check DB health flag"
ONTOLOGY_ID = "Ontology term reference ID"
CREATE_DATE = "Create date limit (before or after). E.g. 2024-08-01"
UPDATE_DATE = "Update date limit (before or after). E.g. 2023-07-01"
GENESET_SIZE = "Geneset size (Genes count)"
