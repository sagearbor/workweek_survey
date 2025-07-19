from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path
from typing import List
import yaml

from . import schema
from .config import get_settings
from . import utils
from .dashboard import dashboard as dashboard_view

BASE_DIR = Path(__file__).parent
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# In-memory storage for submitted survey responses
_RESPONSES: List[schema.SurveyResponse] = []

@app.get("/survey", response_class=HTMLResponse)
async def get_survey(request: Request):
    """Serve the survey form."""
    return templates.TemplateResponse(request, "survey.html")

@app.post("/submit")
async def submit(request: Request):
    """Receive and validate a survey response."""
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    try:
        response = schema.loads(json.dumps(payload))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    _RESPONSES.append(response)
    return {"status": "ok"}

@app.get("/export")
async def export() -> Response:
    """Export collected responses in OUTPUT_FORMAT."""
    fmt = get_settings().output_format
    payload = {
        "survey_year": utils.current_survey_year(),
        "responses": [json.loads(schema.dumps(r)) for r in _RESPONSES],
    }
    if fmt == "json":
        return JSONResponse(content=payload)
    elif fmt == "yaml":
        yaml_str = yaml.safe_dump(payload)
        return Response(content=yaml_str, media_type="application/x-yaml")
    else:
        raise HTTPException(status_code=500, detail="Unsupported OUTPUT_FORMAT")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the interactive analytics dashboard."""
    return await dashboard_view(request)
