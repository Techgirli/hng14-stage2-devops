from main import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import AFTER path setup

client = TestClient(app)

# -------------------------
# GLOBAL MOCK SETUP
# -------------------------
app.state.redis = MagicMock()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}


def test_create_job():
    mock_redis = app.state.redis
    mock_redis.incr.return_value = 1

    response = client.post("/jobs", json={"task": "test"})

    assert response.status_code == 200
    assert "id" in response.json()


def test_get_job_status():
    mock_redis = app.state.redis
    mock_redis.hgetall.return_value = {
        b"id": b"1",
        b"status": b"pending",
        b"task": b"test"
    }

    response = client.get("/jobs/1")
    assert response.status_code == 200


def test_content_type_is_json():
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]
