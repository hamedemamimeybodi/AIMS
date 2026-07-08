from __future__ import annotations

from pathlib import Path

from packages.aims_architecture.metrics import compute_architectural_metrics
from packages.aims_architecture.qa_score import compute_quality_score
from packages.aims_core.adf import ADFDocument


def _table(title: str, data: dict[str, int]) -> list[str]:
    lines = [f"## {title}", "", "| Name | Count |", "|---|---:|"]
    if not data:
        lines.append("| _none_ | 0 |")
    else:
        for key, value in sorted(data.items()):
            lines.append(f"| {key} | {value} |")
    lines.append("")
    return lines


def write_markdown_report(document: ADFDocument, report_path: str | Path) -> Path:
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    metrics = compute_architectural_metrics(document)
    score = compute_quality_score(document)

    lines: list[str] = []
    lines.append("# AIMS Architectural QA/QC Report")
    lines.append("")
    lines.append(f"**Source file:** `{document.source_file}`")
    lines.append(f"**Units:** `{document.units}`")
    lines.append(f"**Total entities:** {metrics.total_entities}")
    lines.append(f"**Total issues:** {document.issue_count()}")
    lines.append(f"**Quality score:** **{score}/100**")
    lines.append("")
    lines.extend(_table("Category Summary", metrics.category_counts))
    lines.extend(_table("Layer Summary", metrics.layer_counts))
    lines.extend(_table("Block Summary", metrics.block_counts))
    lines.extend(_table("Issue Severity Summary", metrics.severity_counts))
    lines.extend(_table("Issue Code Summary", metrics.issue_counts))

    lines.append("## BIM Readiness Snapshot")
    lines.append("")
    lines.append("| BIM Category | Count |")
    lines.append("|---|---:|")
    for key in ["Wall", "Door", "Window", "Column", "Room", "Text", "Unknown"]:
        lines.append(f"| {key} | {metrics.category_counts.get(key, 0)} |")
    lines.append("")

    lines.append("## Entity Issues")
    lines.append("")
    if document.issue_count() == 0:
        lines.append("No issues detected.")
    else:
        lines.append("| Entity ID | Type | Layer | Category | Severity | Code | Message |")
        lines.append("|---|---|---|---|---|---|---|")
        for entity in document.entities:
            for issue in entity.issues:
                message = issue.message.replace("|", "\\|")
                lines.append(f"| `{entity.id}` | {entity.entity_type} | {entity.layer} | {entity.category.value} | {issue.severity} | {issue.code} | {message} |")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path
