# Usage Guide

This guide walks through a typical workflow:

1. **Configuration**: create a `.env` file with at least `STORAGE_PATH` and `OUTPUT_FORMAT`.
2. **Run the app**:
   ```bash
   uvicorn workweek_survey.main:app --reload
   ```
3. **Fill out the survey**: navigate to `http://localhost:8000/survey`.
4. **Export data**: download responses from `/export`.
5. **Analyze**: run `analytics/summary.ipynb` for quick stats.
