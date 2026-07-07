from __future__ import annotations

import argparse
from pathlib import Path

from packages.aims_database.sqlite_store import write_adf_to_sqlite
from packages.aims_geometry.validation import build_validation_report, validate_adf
from packages.aims_parser.dxf_parser import parse_dxf_file


def run_pipeline(dxf_path: Path, db_path: Path, report_path: Path) -> int:
    adf = parse_dxf_file(dxf_path)
    write_adf_to_sqlite(adf, db_path)
    result = validate_adf(adf)
    report = build_validation_report(adf, result)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return 0 if result.is_valid else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aims-pipeline",
        description="Run AIMS v0.1 pipeline: DXF -> ADF -> SQLite -> Validation Report.",
    )
    parser.add_argument("dxf", type=Path, help="Input ASCII DXF file")
    parser.add_argument("--db", type=Path, default=Path("build/aims.sqlite"), help="Output SQLite path")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("build/validation-report.md"),
        help="Output Markdown validation report",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run_pipeline(args.dxf, args.db, args.report)


if __name__ == "__main__":
    raise SystemExit(main())
