"""Transform candidate data into normalized output."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any

from .models import Candidate, normalize_email, normalize_name


def transform_candidates(
    candidates: list[Candidate],
    reference_date: date | None = None,
) -> list[dict[str, Any]]:
    """Normalize fields and add derived values."""

    if reference_date is None:
        reference_date = date.today()

    output: list[dict[str, Any]] = []
    for candidate in candidates:
        last_contact_date = candidate.last_contacted_at.date()
        days_since = (reference_date - last_contact_date).days
        days_since = max(days_since, 0)

        output.append(
            {
                "id": candidate.id,
                "name": normalize_name(candidate.name),
                "email": normalize_email(str(candidate.email)),
                "stage": candidate.stage,
                "last_contacted_at": candidate.last_contacted_at.isoformat(),
                "notes": candidate.notes,
                "days_since_last_contact": days_since,
            }
        )

    return output


def write_transformed(output_path: Path, rows: list[dict[str, Any]]) -> None:
    """Write transformed rows to CSV or JSON."""

    if output_path.suffix.lower() == ".json":
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=2, ensure_ascii=False)
        return

    if output_path.suffix.lower() == ".csv":
        if not rows:
            raise ValueError("No rows to write")
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return

    raise ValueError("Unsupported output type. Use .csv or .json")
