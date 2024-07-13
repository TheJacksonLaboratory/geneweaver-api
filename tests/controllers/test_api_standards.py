"""API Standards Tests.

https://devops.jax.org/Development/Best_Practices/API_Standards/http_standards/
"""

import re

import pytest
from fastapi.testclient import TestClient
from geneweaver.api.core.config_class import GeneweaverAPIConfig

CURLY_BRACE_REGEX = re.compile(r"\{[^}]*\}|[^{}_]+")


def get_openapi_json():
    """Get the openapi json file for parameterizing tests."""
    from unittest.mock import patch

    config = GeneweaverAPIConfig(
        _env_file=None,
        DB_HOST="localhost",
        DB_USERNAME="postgres",
        DB_PASSWORD="postgres",
        DB_NAME="geneweaver",
    )

    with (
        patch("geneweaver.api.core.config_class.GeneweaverAPIConfig", lambda: config),
        patch("geneweaver.api.dependencies.lifespan", lambda app: None),
    ):
        from geneweaver.api.main import app

        test_app = TestClient(app)
        resp = test_app.get(f"{config.API_PREFIX}/openapi.json")

    return resp.json()


OPENAPI_JSON = get_openapi_json()
PATH_KEYS = OPENAPI_JSON["paths"].keys()


@pytest.fixture()
def openapi_json():
    """Provide the auto-rendered openapi.json file from the test client."""
    return OPENAPI_JSON


@pytest.fixture(params=PATH_KEYS)
def openapi_json_path(request):
    """Return a path from the openapi.json file."""
    return request.param


def test_defines_2xx_response(openapi_json, openapi_json_path):
    """Test that the OpenAPI spec defines a 2xx response."""
    path = openapi_json_path
    path_details = openapi_json["paths"][path]
    for method, method_details in path_details.items():
        assert any(
            "2" in response_code for response_code in method_details["responses"].keys()
        ), (
            f"Response for {method.upper()} {path} "
            f"does not contain a 2xx status code"
        )


def test_no_underscores(openapi_json_path):
    """Test that no underscores are present in API endpoint names."""
    segments = re.findall(CURLY_BRACE_REGEX, openapi_json_path)

    assert not any(
        "_" in segment
        for segment in segments
        if "{" not in segment and "}" not in segment
    ), (openapi_json_path + "contains underscores in endpoint name")


def test_no_trailing_slashes(openapi_json_path):
    """Test that no trailing slashes are present in API endpoint names."""
    assert not openapi_json_path.endswith(
        "/"
    ), f"{openapi_json_path} contains a trailing slash"


def test_endpoint_names_are_plural(openapi_json_path):
    """Test that all endpoint names are in plural form."""
    url = openapi_json_path
    segments = url.split("/")
    n_segments = len(segments)
    while len(segments) > 0:
        segment = segments.pop()
        if segment == "":
            continue
        if "{" in segment:
            continue
        if segment == "api":
            continue
        if len(segments) == n_segments - 1:
            continue
        else:
            assert segment.endswith("s"), f"{segment} in {url} is not in plural form"


def test_no_uppercase_letters(openapi_json_path):
    """Test that no uppercase letters are present in API endpoint names."""
    url = openapi_json_path
    assert url == url.lower(), f"{url} contains uppercase letters"


@pytest.mark.skip(reason="Not all endpoints have a response schema defined")
def test_should_define_response_schema(openapi_json, openapi_json_path):
    """Test that all endpoints define a response schema."""
    path = openapi_json_path
    path_details = openapi_json["paths"][path]
    for method, method_details in path_details.items():
        for response_code, response_details in method_details["responses"].items():
            if response_code == "200":
                if "content" not in response_details:
                    continue
                assert (
                    "schema" in response_details["content"]["application/json"]
                ), f"Response for {path} {method} does not contain a schema"
                assert (
                    response_details["content"]["application/json"]["schema"].get(
                        "type"
                    )
                    != "object"
                ), (
                    f"Response for {method.upper()} {path} uses 'object' type "
                    "as schema. This is too vague."
                )
