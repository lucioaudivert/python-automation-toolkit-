from pathlib import Path

import pytest
from pydantic import ValidationError

from automation_toolkit.validate import load_records, validate_records


def test_load_records_csv(tmp_path: Path) -> None:
    content = (
        "id,name,email,stage,last_contacted_at,notes\n"
        "1,Ana,a@example.com,new,2026-01-01T10:00:00,hello\n"
    )
    sample = tmp_path / "sample.csv"
    sample.write_text(content, encoding="utf-8")

    rows = load_records(sample)

    assert len(rows) == 1
    assert rows[0]["name"] == "Ana"


def test_load_records_json_list(tmp_path: Path) -> None:
    sample = tmp_path / "sample.json"
    sample.write_text(
        '[{"id": 1, "name": "Ana", "email": "a@example.com", "stage": "new", '
        '"last_contacted_at": "2026-01-01T10:00:00"}]',
        encoding="utf-8",
    )

    rows = load_records(sample)

    assert len(rows) == 1
    assert rows[0]["email"] == "a@example.com"


def test_load_records_json_wrapped(tmp_path: Path) -> None:
    sample = tmp_path / "sample.json"
    sample.write_text(
        '{"candidates": [{"id": 1, "name": "Ana", "email": "a@example.com", '
        '"stage": "new", "last_contacted_at": "2026-01-01T10:00:00"}]}',
        encoding="utf-8",
    )

    rows = load_records(sample)

    assert len(rows) == 1
    assert rows[0]["stage"] == "new"


def test_load_records_invalid_extension(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("text", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported input"):
        load_records(sample)


def test_validate_records_success() -> None:
    records = [
        {
            "id": 1,
            "name": "Ana",
            "email": "a@example.com",
            "stage": "new",
            "last_contacted_at": "2026-01-01T10:00:00",
            "notes": "Hi",
        }
    ]

    result = validate_records(records)

    assert result.count == 1
    assert result.candidates[0].stage == "new"


def test_validate_records_invalid_stage() -> None:
    records = [
        {
            "id": 1,
            "name": "Ana",
            "email": "a@example.com",
            "stage": "invalid",
            "last_contacted_at": "2026-01-01T10:00:00",
        }
    ]

    with pytest.raises(ValidationError):
        validate_records(records)
