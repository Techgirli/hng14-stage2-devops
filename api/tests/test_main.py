import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock redis before importing app
with patch('redis.Redis') as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test GET / returns correct message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_health_endpoint():
    """Test GET /health returns healthy"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}

def test_create_job():
    """Test POST /jobs creates a job"""
    with patch('main.r') as mock_r:
        mock_r.incr.return_value = 1
        mock_r.hset.return_value = True
        mock_r.lpush.return_value = True
        response = client.post("/jobs", json={"task": "test"})
        assert response.status_code == 200
        assert "id" in response.json()

def test_get_job_status():
    """Test GET /jobs/:id returns job status"""
    with patch('main.r') as mock_r:
        mock_r.hgetall.return_value = {
            b"id": b"1",
            b"status": b"pending",
            b"task": b"test"
        }
        response = client.get("/jobs/1")
        assert response.status_code == 200

def test_content_type_is_json():
    """Test all endpoints return application/json"""
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]
