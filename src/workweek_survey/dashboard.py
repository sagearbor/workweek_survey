from __future__ import annotations

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


async def dashboard(request: Request) -> HTMLResponse:
    """Render the interactive analytics dashboard."""
    return templates.TemplateResponse(request, "dashboard.html")
