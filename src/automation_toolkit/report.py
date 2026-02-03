"""Generate summary reports from candidate data."""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from .models import Candidate


def build_report(candidates: list[Candidate], reference_date: date | None = None) -> dict[str, Any]:
    """Build a report dictionary from candidates."""

    if reference_date is None:
        reference_date = date.today()

    total = len(candidates)
    stages = Counter(candidate.stage for candidate in candidates)
    last_contacted_dates = [candidate.last_contacted_at.date() for candidate in candidates]

    most_recent = max(last_contacted_dates) if last_contacted_dates else None
    oldest = min(last_contacted_dates) if last_contacted_dates else None

    days_since = [max((reference_date - date_value).days, 0) for date_value in last_contacted_dates]
    average_days_since = round(sum(days_since) / total, 2) if total else 0.0

    return {
        "total_candidates": total,
        "stage_breakdown": dict(sorted(stages.items())),
        "most_recent_contact": most_recent.isoformat() if most_recent else None,
        "oldest_contact": oldest.isoformat() if oldest else None,
        "average_days_since_last_contact": average_days_since,
    }


def render_report_text(report: dict[str, Any]) -> str:
    """Render a human-readable report."""

    lines = [
        "Candidate Pipeline Report",
        "=========================",
        f"Total candidates: {report['total_candidates']}",
        f"Most recent contact: {report['most_recent_contact']}",
        f"Oldest contact: {report['oldest_contact']}",
        f"Average days since last contact: {report['average_days_since_last_contact']}",
        "",
        "Stage breakdown:",
    ]

    for stage, count in report["stage_breakdown"].items():
        lines.append(f"- {stage}: {count}")

    return "\n".join(lines)


def write_report(output_path: Path, report: dict[str, Any]) -> None:
    """Write report as JSON or text."""

    if output_path.suffix.lower() == ".json":
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, ensure_ascii=False)
        return

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write(render_report_text(report))
