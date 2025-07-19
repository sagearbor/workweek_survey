# Workweek Survey

## Background
The **Workweek Survey** is a lightweight web app designed to gather a snapshot of every team member’s average work week: what they do, how long tasks take, and where AI-driven improvements can deliver the highest ROI. Respondents complete a 3-4 minute survey; results are stored as JSON/YAML/CSV for easy analysis.

## Install

```bash
git clone https://example.com/your-org/workweek_survey.git
cd workweek_survey
python3 -m venv .venv
source .venv/bin/activate
pip install .[dev]
```

## Usage

1. Populate `.env` (see `.env.example`).
2. Start the server:
   ```bash
   uvicorn workweek_survey.main:app --reload --host 0.0.0.0 --port ${PORT:-8000}
   ```
3. Share the survey link: `http://<your-host>:${PORT:-8000}/survey`
4. Download results from `/export` in the desired format.

See [docs/usage.md](docs/usage.md) for a full walkthrough including analysis tips.

### Annual updates

At the start of each year, clear previous responses and invite the team to fill
out the survey again. Exported data now includes a `survey_year` field so you
can track results over time.

## Testing

```bash
pytest
```

## Contributing

1. Fork the repo, create a feature branch.
2. Write tests for any new functionality.
3. Open a PR against `main`, describe your changes, link issues.
4. Ensure CI passes before merging.
