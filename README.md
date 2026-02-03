# Python Automation Toolkit

A lightweight CLI toolkit to validate and transform CSV/JSON candidate data and generate summary reports. It's designed as a clean, self-contained example for automation workflows.

Public sanitized portfolio sample; production work is under NDA.

## Features
- Validate CSV/JSON files using Pydantic models
- Normalize and transform records into CSV or JSON
- Generate summary reports as text or JSON
- Simple, well-tested CLI workflow

## Project Layout
```
python-automation-toolkit/
├── data/
├── src/automation_toolkit/
├── tests/
└── pyproject.toml
```

## Quickstart (Local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Validate sample data:
```bash
automation-toolkit validate --input data/sample_candidates.csv
```

Transform data (CSV → JSON):
```bash
automation-toolkit transform --input data/sample_candidates.csv --output /tmp/candidates.json
```

Generate a report:
```bash
automation-toolkit report --input data/sample_candidates.csv --output /tmp/report.txt
```

Example report output:
```
Candidate Pipeline Report
=========================
Total candidates: 6
Most recent contact: 2026-01-28
Oldest contact: 2025-12-22
Average days since last contact: 22.5

Stage breakdown:
- archived: 1
- hired: 1
- interview: 1
- new: 1
- offer: 1
- screen: 1
```

## Quickstart (Docker)
Build:
```bash
docker build -t automation-toolkit:latest .
```

Run validation:
```bash
docker run --rm -v $(pwd)/data:/data automation-toolkit:latest validate --input /data/sample_candidates.csv
```

Run transformation:
```bash
docker run --rm -v $(pwd)/data:/data automation-toolkit:latest transform --input /data/sample_candidates.csv --output /data/output.json
```

Run report:
```bash
docker run --rm -v $(pwd)/data:/data automation-toolkit:latest report --input /data/sample_candidates.csv --output /data/report.txt
```

## Testing
```bash
pytest
```

## Linting and formatting
```bash
ruff check .
black .
```

CI enabled