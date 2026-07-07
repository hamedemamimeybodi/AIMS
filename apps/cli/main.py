from __future__ import annotations

import argparse
from pathlib import Path

from packages.aims_parser import parse_dxf
from packages.aims_report import to_json, to_markdown
from packages.aims_storage import save_document
from packages.aims_validator import validate_document


def validate_command(args: argparse.Namespace) -> int:
    print("Reading DXF...")
    adf = parse_dxf(args.input)

    print("Creating ADF...")
    report = validate_document(adf)

    print("Saving SQLite...")
    save_document(adf, report, args.db)

    print("Writing Markdown report...")
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(to_markdown(adf, report), encoding="utf-8")

    if args.json:
        print("Writing JSON report...")
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(to_json(report), encoding="utf-8")

    print("Done")
    return 0 if report.is_valid else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aims")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("input")
    validate.add_argument("--db", default="build/aims.sqlite")
    validate.add_argument("--report", default="build/validation-report.md")
    validate.add_argument("--json", default="build/validation-report.json")
    validate.set_defaults(func=validate_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
