from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import yaml
from rich.console import Console

from packages.aims_database.sqlite_store import write_sqlite
from packages.aims_geometry.validation import validate_document
from packages.aims_parser.dxf_parser import parse_dxf
from packages.aims_report.markdown_report import write_markdown_report

console = Console()


def load_yaml(path: str | Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Standard file not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def audit_command(args: argparse.Namespace) -> int:
    standard = load_yaml(args.standard)
    document = parse_dxf(args.input, standard=standard)
    validate_document(document, standard=standard)

    sqlite_path = Path(args.sqlite)
    report_path = Path(args.out)

    write_sqlite(document, sqlite_path)
    write_markdown_report(document, report_path)

    console.print("[bold green]AIMS audit completed[/bold green]")
    console.print(f"Entities: {len(document.entities)}")
    console.print(f"Issues: {document.issue_count()}")
    console.print(f"SQLite: {sqlite_path}")
    console.print(f"Report: {report_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aims", description="AIMS CAD/BIM preflight toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit", help="Audit a DXF file and generate SQLite plus Markdown report")
    audit.add_argument("input", help="Input DXF file")
    audit.add_argument("--standard", default="standards/architectural_layers.yaml", help="YAML layer/classification standard")
    audit.add_argument("--sqlite", default="reports/aims_output.sqlite", help="Output SQLite database path")
    audit.add_argument("--out", default="reports/aims_report.md", help="Output Markdown report path")
    audit.set_defaults(func=audit_command)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
