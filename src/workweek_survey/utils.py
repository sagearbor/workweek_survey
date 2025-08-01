from __future__ import annotations

from datetime import datetime, UTC


def current_survey_year() -> int:
    """Return the current year for tagging exports."""
    return datetime.now(UTC).year
