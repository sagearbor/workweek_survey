from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

import yaml

from . import schema
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
    ext = "json" if fmt == "json" else "yaml"

    # Determine filename based on existing files count
    count = len(list(storage_dir.glob(f"*.{ext}")))
    filename = storage_dir / f"response_{count + 1}.{ext}"

    if fmt == "json":
        data = json.loads(schema.dumps(response))
        filename.write_text(json.dumps(data))
    elif fmt == "yaml":
        data = json.loads(schema.dumps(response))
        filename.write_text(yaml.safe_dump(data))
    else:
        raise ValueError(f"Unsupported OUTPUT_FORMAT: {fmt}")

    return filename


def read_responses() -> List[schema.SurveyResponse]:
    """Read all stored responses from disk."""
    storage_dir = _get_storage_dir()
    fmt = _get_format()
    ext = "json" if fmt == "json" else "yaml"
    responses = []
    for path in sorted(storage_dir.glob(f"*.{ext}")):
        text = path.read_text()
        if fmt == "json":
            raw = text
        else:
            raw = json.dumps(yaml.safe_load(text))
        responses.append(schema.loads(raw))
    return responses
