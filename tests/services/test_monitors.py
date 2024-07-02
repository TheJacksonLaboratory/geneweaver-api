"""Tests for system monitor services."""

from unittest.mock import patch

import pytest
from geneweaver.api.services import monitors

from tests.data import test_monitors_data

db_health_status = test_monitors_data.get("db_health_status")


@patch("geneweaver.api.services.monitors.db_health_check")
def test_db_health_check(mock_db_heath):
    """Test call to get db health status."""
    mock_db_heath.return_value = db_health_status.get("DB_status")
    response = monitors.check_db_health(None)

    assert response == db_health_status.get("DB_status")


@patch("geneweaver.api.services.monitors.db_health_check")
def test_db_health_check_error(mock_db_heath):
    """Test error in call to get db health status."""
    mock_db_heath.side_effect = Exception("ERROR")

    with pytest.raises(expected_exception=Exception):
        monitors.check_db_health(None)
