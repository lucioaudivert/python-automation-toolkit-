"""Validation helpers for CSV and JSON input files."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .models import Candidate


class ValidationResult:
    """Simple container for validation output."""

    def __init__(self, candidates: list[Candidate]) -> None:
        self.candidates = candidates

    @property
    def count(self) -> int:
        return len(self.candidates)


def _load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV file has no rows")

    return rows


def _load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict) and "candidates" in payload:
        payload = payload["candidates"]

    if not isinstance(payload, list):
        raise ValueError("JSON input must be a list of objects or a 'candidates' list")

    return payload


def load_records(path: Path) -> list[dict[str, Any]]:
    """Load raw records from a CSV or JSON file."""

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.suffix.lower() == ".csv":
        return _load_csv(path)
    if path.suffix.lower() == ".json":
        return _load_json(path)

    raise ValueError("Unsupported input type. Use .csv or .json")


def validate_records(records: list[dict[str, Any]]) -> ValidationResult:
    """Validate raw records into Candidate models."""

    candidates: list[Candidate] = []
    errors: list[ValidationError] = []

    for record in records:
        try:
            candidates.append(Candidate.model_validate(record))
        except ValidationError as exc:
            errors.append(exc)

    if errors:
        # Raise the first error; CLI shows friendly message.
        raise errors[0]

    return ValidationResult(candidates)


def validate_file(path: str | Path) -> ValidationResult:
    """Load and validate a file into Candidate models."""

    path = Path(path)
    records = load_records(path)
    return validate_records(records)
