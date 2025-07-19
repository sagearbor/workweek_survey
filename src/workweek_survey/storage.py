from __future__ import annotations

import json
import csv
from pathlib import Path
from typing import Iterable, List

import yaml

from . import schema, utils
from .config import get_settings


def _get_storage_dir() -> Path:
    settings = get_settings()
    path = Path(settings.storage_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_format() -> str:
    return get_settings().output_format


def append_response(response: schema.SurveyResponse) -> Path:
    """Append a SurveyResponse to disk.

    Each response is stored as a separate file inside STORAGE_PATH. The filename
    uses a monotonic counter to avoid collisions and the file extension matches
    OUTPUT_FORMAT (json or yaml).
    """
    storage_dir = _get_storage_dir()
    fmt = _get_format()
    if fmt == "json":
        ext = "json"
    elif fmt == "yaml":
        ext = "yaml"
    else:
        ext = "csv"

    # Determine filename based on existing files count
    count = len(list(storage_dir.glob(f"*.{ext}")))
    filename = storage_dir / f"response_{count + 1}.{ext}"

    if fmt == "json":
        data = json.loads(schema.dumps(response))
        filename.write_text(json.dumps(data))
    elif fmt == "yaml":
        data = json.loads(schema.dumps(response))
        filename.write_text(yaml.safe_dump(data))
    elif fmt == "csv":
        with filename.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "survey_year",
                "respondent",
                "org_branch",
                "name",
                "duration_hours",
                "category",
            ])
            year = utils.current_survey_year()
            for task in response.tasks:
                writer.writerow(
                    [
                        year,
                        response.respondent or "",
                        response.org_branch or "",
                        task.name,
                        task.duration_hours,
                        task.category,
                    ]
                )
    else:
        raise ValueError(f"Unsupported OUTPUT_FORMAT: {fmt}")

    return filename


def read_responses() -> List[schema.SurveyResponse]:
    """Read all stored responses from disk."""
    storage_dir = _get_storage_dir()
    fmt = _get_format()
    if fmt == "json":
        ext = "json"
    elif fmt == "yaml":
        ext = "yaml"
    else:
        ext = "csv"
    responses = []
    for path in sorted(storage_dir.glob(f"*.{ext}")):
        if fmt == "csv":
            with path.open(newline="") as f:
                reader = csv.DictReader(f)
                tasks = []
                respondent = None
                org_branch = None
                for row in reader:
                    respondent = row.get("respondent") or None
                    org_branch = row.get("org_branch") or None
                    tasks.append(
                        schema.TaskEntry(
                            name=row["name"],
                            duration_hours=float(row["duration_hours"]),
                            category=row["category"],
                        )
                    )
                responses.append(
                    schema.SurveyResponse(
                        tasks=tasks, respondent=respondent, org_branch=org_branch
                    )
                )
        else:
            text = path.read_text()
            if fmt == "json":
                raw = text
            else:
                raw = json.dumps(yaml.safe_load(text))
            responses.append(schema.loads(raw))
    return responses
