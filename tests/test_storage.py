import json
import os
os.environ.setdefault("STORAGE_PATH", "/tmp/workweek_test")

from workweek_survey import schema, storage


def sample_payload():
    return {
        "respondent": "alice",
        "tasks": [
            {"name": "coding", "duration_hours": 5, "category": "dev"},
            {"name": "meeting", "duration_hours": 1, "category": "communication"},
        ],
    }


def test_append_and_read_json(tmp_path, monkeypatch):
    monkeypatch.setenv("STORAGE_PATH", str(tmp_path))
    monkeypatch.setenv("OUTPUT_FORMAT", "json")
    resp = schema.loads(json.dumps(sample_payload()))
    path = storage.append_response(resp)
    assert path.exists()
    assert path.suffix == ".json"
    responses = storage.read_responses()
    assert responses == [resp]


def test_append_and_read_yaml(tmp_path, monkeypatch):
    monkeypatch.setenv("STORAGE_PATH", str(tmp_path))
    monkeypatch.setenv("OUTPUT_FORMAT", "yaml")
    resp = schema.loads(json.dumps(sample_payload()))
    path = storage.append_response(resp)
    assert path.exists()
    assert path.suffix == ".yaml"
    responses = storage.read_responses()
    assert responses == [resp]
