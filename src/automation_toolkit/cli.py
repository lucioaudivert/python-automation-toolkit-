"""Command-line interface for the automation toolkit."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from .report import build_report, write_report
from .transform import transform_candidates, write_transformed
from .validate import validate_file


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="automation-toolkit",
        description="Validate and transform candidate data files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate input data")
    validate_parser.add_argument("--input", required=True, help="Path to CSV or JSON data")

    transform_parser = subparsers.add_parser("transform", help="Transform input data")
    transform_parser.add_argument("--input", required=True, help="Path to CSV or JSON data")
    transform_parser.add_argument("--output", required=True, help="Output path (.csv or .json)")

    report_parser = subparsers.add_parser("report", help="Generate a summary report")
    report_parser.add_argument("--input", required=True, help="Path to CSV or JSON data")
    report_parser.add_argument("--output", required=True, help="Output path (.txt or .json)")

    return parser


def run_cli(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        validation = validate_file(args.input)

        if args.command == "validate":
            print(f"OK: {validation.count} records validated")
            return 0

        if args.command == "transform":
            output_path = Path(args.output)
            rows = transform_candidates(validation.candidates)
            write_transformed(output_path, rows)
            print(f"Wrote {len(rows)} records to {output_path}")
            return 0

        if args.command == "report":
            output_path = Path(args.output)
            report = build_report(validation.candidates)
            write_report(output_path, report)
            print(f"Report written to {output_path}")
            return 0

        parser.error("Unknown command")
        return 2

    except (FileNotFoundError, ValueError, ValidationError) as exc:
        print(f"Error: {exc}")
        return 1


def main(argv: Sequence[str] | None = None) -> None:
    raise SystemExit(run_cli(argv))


if __name__ == "__main__":
    main()
