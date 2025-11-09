"""Integration tests for API endpoints."""
import pytest


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_info_endpoint(client):
    """Test info endpoint."""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "agent_type" in data
    assert "available_tools" in data
