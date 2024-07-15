"""Tests for system monitor apis."""

from unittest.mock import patch

from tests.data import test_monitors_data

db_health_status = test_monitors_data.get("db_health_status")


@patch("geneweaver.api.services.monitors.check_db_health")
def test_valid_url_req(mock_db_heath_service_call, client):
    """Test valid url request to get system health status."""
    response = client.get(
        url="/api/monitors/servers/health", params={"db_health_check": False}
    )
    assert response.status_code == 200

    mock_db_heath_service_call.return_value = db_health_status.get("DB_status")
    response = client.get(
        url="/api/monitors/servers/health", params={"db_health_check": True}
    )
    assert response.status_code == 200
    assert response.json().get("DB_status") == db_health_status.get("DB_status")
