import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import json
import pytest

from workweek_survey import schema


def sample_payload():
    return {
        "respondent": "alice",
        "tasks": [
            {"name": "coding", "duration_hours": 5, "category": "dev"},
            {"name": "meeting", "duration_hours": 1, "category": "communication"},
        ],
    }


def test_loads_valid():
    payload = sample_payload()
    data = json.dumps(payload)
    resp = schema.loads(data)
    assert resp.respondent == "alice"
    assert len(resp.tasks) == 2
    assert resp.tasks[0].name == "coding"
    assert resp.tasks[0].duration_hours == 5


def test_loads_invalid_duration():
    payload = sample_payload()
    payload["tasks"][0]["duration_hours"] = 0
    data = json.dumps(payload)
    with pytest.raises(ValueError):
        schema.loads(data)


def test_dumps_round_trip():
    payload = sample_payload()
    resp = schema.loads(json.dumps(payload))
    dumped = schema.dumps(resp)
    reloaded = schema.loads(dumped)
    assert reloaded == resp
