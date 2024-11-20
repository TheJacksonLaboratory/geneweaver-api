"""Fixtures for the controller tests."""

from unittest.mock import Mock

import psycopg
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from geneweaver.api.core.config_class import GeneweaverAPIConfig


# Mock dependencies
def mock_full_user() -> Mock:
    """User auth mock."""
    m1 = Mock()
    return m1.AsyncMock()


def mock_cursor() -> psycopg.Cursor:
    """DB cursor mock."""
    m2 = Mock()
    return m2.AsyncMock()


@pytest.fixture()
def mock_settings(monkeypatch) -> GeneweaverAPIConfig:
    """Patch the settings class to return a test settings instance.

    returns: A patched settings instance.
    """
    test_settings = GeneweaverAPIConfig(
        DB_HOST="localhost",
        DB_USERNAME="postgres",
        DB_PASSWORD="postgres",
        DB_NAME="geneweaver",
    )

    monkeypatch.setattr(
        "geneweaver.api.core.config_class.GeneweaverAPIConfig", lambda: test_settings
    )

    return test_settings


@pytest.fixture()
def app(mock_settings) -> FastAPI:
    """Provide a mocked FastAPI application.

    returns: A mocked FastAPI application.
    """
    from geneweaver.api.dependencies import cursor, full_user
    from geneweaver.api.main import app

    app.dependency_overrides.update({full_user: mock_full_user, cursor: mock_cursor})

    return app


@pytest.fixture()
def client(mock_settings, app) -> TestClient:
    """Provide a mocked FastAPI application.

    returns: A mocked FastAPI application.
    """
    test_client = TestClient(app)
    return test_client
