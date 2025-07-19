from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
import json
import os
from typing import List
import yaml

from . import schema

app = FastAPI()

# In-memory storage for submitted survey responses
_RESPONSES: List[schema.SurveyResponse] = []

@app.get("/survey", response_class=HTMLResponse)
async def get_survey() -> str:
    """Serve the survey form. Placeholder HTML for now."""
    return "<html><body><h1>Workweek Survey</h1></body></html>"

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
    fmt = os.getenv("OUTPUT_FORMAT", "json").lower()
    if fmt == "json":
        data = [json.loads(schema.dumps(r)) for r in _RESPONSES]
        return JSONResponse(content=data)
    elif fmt == "yaml":
        data = [json.loads(schema.dumps(r)) for r in _RESPONSES]
        yaml_str = yaml.safe_dump(data)
        return Response(content=yaml_str, media_type="application/x-yaml")
    else:
        raise HTTPException(status_code=500, detail="Unsupported OUTPUT_FORMAT")
