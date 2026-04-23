import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock redis before importing app
mock_redis_instance = MagicMock()
mock_redis_instance.incr.return_value = 1
mock_redis_instance.hset.return_value = True
mock_redis_instance.lpush.return_value = True
mock_redis_instance.hgetall.return_value = {
    "id": "1",
    "status": "pending",
    "task": "test"
}

with patch('redis.Redis', return_value=mock_redis_instance):
    from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test GET / returns correct message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_health_endpoint():
    """Test GET /health returns healthy message"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}


def test_create_job():
    """Test POST /jobs creates a job and returns id"""
    response = client.post("/jobs", json={"task": "test"})
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_job_status():
    """Test GET /jobs/:id returns job data"""
    response = client.get("/jobs/1")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_content_type_is_json():
    """Test all endpoints return application/json"""
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]
