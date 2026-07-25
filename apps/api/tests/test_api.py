"""Tests for the API Gateway."""

from typing import Any

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response: Any = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_portfolio_snapshot_endpoint() -> None:
    response: Any = client.get("/portfolio/snapshot")
    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    assert "positions" in data
    assert "total_realized_pnl" in data
