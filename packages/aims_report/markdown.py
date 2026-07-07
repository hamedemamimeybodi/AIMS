from __future__ import annotations

from packages.aims_domain import ADFDocument
from packages.aims_validator.engine import ValidationReport


def to_markdown(adf: ADFDocument, report: ValidationReport) -> str:
    lines = [
        "# AIMS Validation Report",
        "",
        f"Source: `{adf.source_path}`",
        f"ADF version: `{adf.adf_version}`",
        f"Features: `{adf.feature_count}`",
        f"Layers: `{len(adf.layers)}`",
        "",
        "## Summary",
        "",
        f"Valid: `{report.is_valid}`",
        f"Errors: `{report.error_count}`",
        f"Warnings: `{report.warning_count}`",
        f"Info: `{report.info_count}`",
        "",
        "## Issues",
        "",
    ]

    if not report.issues:
        lines.append("No validation issues found.")
    else:
        lines.append("| Rule | Severity | Feature | Message | Suggested Fix |")
        lines.append("|---|---:|---|---|---|")
        for issue in report.issues:
            lines.append(
                f"| {issue.rule_id} | {issue.severity} | {issue.feature_id or ''} | "
                f"{issue.message} | {issue.suggested_fix} |"
            )

    lines.append("")
    return "\n".join(lines)
