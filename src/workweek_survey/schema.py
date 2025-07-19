from dataclasses import dataclass, asdict
from typing import List, Optional
import json


@dataclass
class TaskEntry:
    """Single task reported in the survey."""
    name: str
    duration_hours: float
    category: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        if self.duration_hours <= 0:
            raise ValueError("duration_hours must be positive")
        if not self.category:
            raise ValueError("category must not be empty")


@dataclass
class SurveyResponse:
    """All tasks submitted by a team member."""
    tasks: List[TaskEntry]
    respondent: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.tasks:
            raise ValueError("tasks must not be empty")


def loads(data: str) -> SurveyResponse:
    """Parse a JSON string into a SurveyResponse."""
    raw = json.loads(data)
    tasks = [TaskEntry(**item) for item in raw.get("tasks", [])]
    respondent = raw.get("respondent")
    return SurveyResponse(tasks=tasks, respondent=respondent)


def dumps(response: SurveyResponse) -> str:
    """Serialize a SurveyResponse into JSON."""
    return json.dumps(asdict(response))
