from automation_toolkit.cli import run_cli


def test_cli_invalid_data_returns_nonzero(tmp_path, capsys) -> None:
    sample = tmp_path / "bad.json"
    sample.write_text('[{"id": 0}]', encoding="utf-8")

    exit_code = run_cli(["validate", "--input", str(sample)])

    assert exit_code != 0
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_cli_validate_success(tmp_path, capsys) -> None:
    sample = tmp_path / "good.json"
    sample.write_text(
        '[{"id": 1, "name": "Ana", "email": "a@example.com", "stage": "new", "last_contacted_at": "2026-01-01T10:00:00"}]',
        encoding="utf-8",
    )

    exit_code = run_cli(["validate", "--input", str(sample)])

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "OK" in captured.out
