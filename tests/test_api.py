import os
os.environ.setdefault("STORAGE_PATH", "/tmp/workweek_test")
from fastapi.testclient import TestClient
from workweek_survey.main import app

client = TestClient(app)


def sample_payload():
    return {
        "respondent": "alice",
        "tasks": [
            {"name": "coding", "duration_hours": 5, "category": "dev"},
            {"name": "meeting", "duration_hours": 1, "category": "communication"},
        ],
    }


def test_submit_returns_200():
    response = client.post("/submit", json=sample_payload())
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_survey_page():
    response = client.get("/survey")
    assert response.status_code == 200
    assert "<form" in response.text


def test_export_json():
    os.environ["OUTPUT_FORMAT"] = "json"
    client.post("/submit", json=sample_payload())
    response = client.get("/export")
    assert response.status_code == 200
    data = response.json()
    assert "survey_year" in data
    assert isinstance(data["responses"], list)
    assert data["responses"][-1]["respondent"] == "alice"


def test_export_yaml():
    os.environ["OUTPUT_FORMAT"] = "yaml"
    client.post("/submit", json=sample_payload())
    response = client.get("/export")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/x-yaml")
    import yaml
    data = yaml.safe_load(response.text)
    assert "survey_year" in data
    assert data["responses"][-1]["respondent"] == "alice"


def test_export_csv():
    os.environ["OUTPUT_FORMAT"] = "csv"
    client.post("/submit", json=sample_payload())
    response = client.get("/export")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    import csv
    rows = list(csv.reader(response.text.splitlines()))
    assert rows[0] == [
        "survey_year",
        "respondent",
        "org_branch",
        "name",
        "duration_hours",
        "category",
    ]
    assert rows[-1][1] == "alice"
