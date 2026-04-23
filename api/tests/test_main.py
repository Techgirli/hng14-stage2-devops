import sys
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock redis BEFORE importing app
mock_redis_instance = MagicMock()
mock_redis_instance.incr.return_value = 1
mock_redis_instance.hset.return_value = True
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
    with patch('main.get_redis', return_value=mock_redis_instance):
        response = client.post("/jobs", json={"task": "test"})
        assert response.status_code == 200
        assert "id" in response.json()


def test_get_job_status():
    """Test GET /jobs/:id returns job data"""
    with patch('main.get_redis', return_value=mock_redis_instance):
        response = client.get("/jobs/1")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


def test_get_job_not_found():
    """Test GET /jobs/:id returns 404 when job doesnt exist"""
    mock_empty = MagicMock()
    mock_empty.hgetall.return_value = {}
    with patch('main.get_redis', return_value=mock_empty):
        response = client.get("/jobs/999")
        assert response.status_code == 404


def test_content_type_is_json():
    """Test all endpoints return application/json"""
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]
