import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.iot import metrics_history

client = TestClient(app)

API_KEY = "sup-secret-labpipo-key"


@pytest.fixture(autouse=True)
def clear_metrics_history():
    metrics_history.clear()


def get_auth_token():
    response = client.post(
        "/api/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_metrics_without_token_fails():
    response = client.get("/api/iot/metrics")

    assert response.status_code == 401


def test_post_metric_without_api_key_fails():
    payload = {
        "device": "pico-lab-01",
        "temperature": 24.5,
        "humidity": 51
    }

    response = client.post(
        "/api/iot/metrics",
        json=payload
    )

    assert response.status_code == 401


def test_post_metric_with_api_key_ok():
    payload = {
        "device": "pico-lab-01",
        "temperature": 24.5,
        "humidity": 51
    }

    response = client.post(
        "/api/iot/metrics",
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    assert response.status_code == 201


def test_post_metric_invalid_humidity_fails():
    payload = {
        "device": "pico-lab-01",
        "temperature": 24.5,
        "humidity": 150
    }

    response = client.post(
        "/api/iot/metrics",
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    assert response.status_code == 422


def test_post_metric_invalid_device_fails():
    payload = {
        "device": "x",
        "temperature": 24.5,
        "humidity": 51
    }

    response = client.post(
        "/api/iot/metrics",
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    assert response.status_code == 422


def test_get_metrics_with_valid_jwt():
    token = get_auth_token()

    payload = {
        "device": "pico-lab-01",
        "temperature": 24.5,
        "humidity": 51
    }

    client.post(
        "/api/iot/metrics",
        json=payload,
        headers={"X-API-Key": API_KEY}
    )

    response = client.get(
        "/api/iot/metrics",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["count"] == 1
