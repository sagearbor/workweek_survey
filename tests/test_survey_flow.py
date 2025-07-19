import os
from fastapi.testclient import TestClient
from workweek_survey.main import app

client = TestClient(app)


def sample_payload():
    return {
        "respondent": "e2e-user",
        "tasks": [
            {"name": "code", "duration_hours": 2, "category": "dev"},
            {"name": "review", "duration_hours": 1, "category": "dev"},
        ],
    }


def test_end_to_end_flow(tmp_path, monkeypatch):
    monkeypatch.setenv("STORAGE_PATH", str(tmp_path))
    monkeypatch.setenv("OUTPUT_FORMAT", "json")

    # GET survey page
    response = client.get("/survey")
    assert response.status_code == 200
    assert "<form" in response.text

    # Submit payload
    response = client.post("/submit", json=sample_payload())
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    # Export responses
    response = client.get("/export")
    assert response.status_code == 200
    data = response.json()
    assert "survey_year" in data
    assert data["responses"][-1]["respondent"] == "e2e-user"
    assert data["responses"][-1]["tasks"][0]["name"] == "code"
