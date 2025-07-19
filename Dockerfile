###########
# Builder #
###########
FROM python:3.11-slim AS builder
WORKDIR /install
COPY pyproject.toml ./
COPY src/ src/
RUN pip install --prefix=/install .[dev]

#########
# Final #
#########
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ src/
ENV PYTHONPATH=/app
ENV PORT=8000
CMD ["uvicorn", "workweek_survey.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
