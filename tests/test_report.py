from datetime import date, datetime
from pathlib import Path

from automation_toolkit.models import Candidate
from automation_toolkit.report import build_report, render_report_text, write_report


def _candidates() -> list[Candidate]:
    return [
        Candidate(
            id=1,
            name="Ana",
            email="a@example.com",
            stage="new",
            last_contacted_at=datetime(2026, 1, 1, 10, 0, 0),
        ),
        Candidate(
            id=2,
            name="Luis",
            email="l@example.com",
            stage="offer",
            last_contacted_at=datetime(2026, 1, 3, 9, 0, 0),
        ),
    ]


def test_build_report_summary() -> None:
    report = build_report(_candidates(), reference_date=date(2026, 1, 5))

    assert report["total_candidates"] == 2
    assert report["stage_breakdown"]["new"] == 1
    assert report["most_recent_contact"] == "2026-01-03"


def test_render_report_text() -> None:
    report = build_report(_candidates(), reference_date=date(2026, 1, 5))

    text = render_report_text(report)

    assert "Candidate Pipeline Report" in text
    assert "- new: 1" in text


def test_write_report_json(tmp_path: Path) -> None:
    report = build_report(_candidates(), reference_date=date(2026, 1, 5))
    output = tmp_path / "report.json"

    write_report(output, report)

    assert output.exists()
    assert "total_candidates" in output.read_text(encoding="utf-8")


def test_write_report_text(tmp_path: Path) -> None:
    report = build_report(_candidates(), reference_date=date(2026, 1, 5))
    output = tmp_path / "report.txt"

    write_report(output, report)

    assert "Stage breakdown" in output.read_text(encoding="utf-8")
