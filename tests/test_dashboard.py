import os
from fastapi.testclient import TestClient
from workweek_survey.main import app

client = TestClient(app)


def test_dashboard_route():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Survey Dashboard" in response.text

