from datetime import date, datetime
from pathlib import Path

import pytest

from automation_toolkit.models import Candidate
from automation_toolkit.transform import transform_candidates, write_transformed


def _candidate() -> Candidate:
    return Candidate(
        id=1,
        name="ana lopez",
        email="ANA@example.com",
        stage="new",
        last_contacted_at=datetime(2026, 1, 1, 10, 0, 0),
        notes="hello",
    )


def test_transform_candidates_normalizes() -> None:
    candidate = _candidate()

    rows = transform_candidates([candidate], reference_date=date(2026, 1, 5))

    assert rows[0]["name"] == "Ana Lopez"
    assert rows[0]["email"] == "ana@example.com"
    assert rows[0]["days_since_last_contact"] == 4


def test_transform_candidates_negative_days() -> None:
    candidate = _candidate()

    rows = transform_candidates([candidate], reference_date=date(2025, 12, 31))

    assert rows[0]["days_since_last_contact"] == 0


def test_write_transformed_json(tmp_path: Path) -> None:
    candidate = _candidate()
    rows = transform_candidates([candidate], reference_date=date(2026, 1, 5))
    output = tmp_path / "out.json"

    write_transformed(output, rows)

    assert output.exists()
    assert "days_since_last_contact" in output.read_text(encoding="utf-8")


def test_write_transformed_csv(tmp_path: Path) -> None:
    candidate = _candidate()
    rows = transform_candidates([candidate], reference_date=date(2026, 1, 5))
    output = tmp_path / "out.csv"

    write_transformed(output, rows)

    content = output.read_text(encoding="utf-8")
    assert "days_since_last_contact" in content


def test_write_transformed_invalid_extension(tmp_path: Path) -> None:
    candidate = _candidate()
    rows = transform_candidates([candidate], reference_date=date(2026, 1, 5))
    output = tmp_path / "out.txt"

    with pytest.raises(ValueError, match="Unsupported output"):
        write_transformed(output, rows)
