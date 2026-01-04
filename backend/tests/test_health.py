"""
Tests for health check endpoint
"""
import pytest

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"




