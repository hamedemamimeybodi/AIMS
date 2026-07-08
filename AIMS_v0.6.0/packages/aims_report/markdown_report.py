from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.aims_architecture.metrics import compute_architectural_metrics
from packages.aims_architecture.qa_score import compute_quality_score
from packages.aims_bim.readiness import BIMReadinessReport, compute_bim_readiness
from packages.aims_core.adf import ADFDocument
from packages.aims_gis.readiness import GISReadinessReport, compute_gis_readiness
from packages.aims_rules.engine import RuleResult
from packages.aims_plugins.loader import PluginRunSummary


def _table(title: str, data: dict[str, int]) -> list[str]:
    lines = [f"## {title}", "", "| Name | Count |", "|---|---:|"]
    if not data:
        lines.append("| _none_ | 0 |")
    else:
        for key, value in sorted(data.items()):
            lines.append(f"| {key} | {value} |")
    lines.append("")
    return lines


def _bim_section(bim: BIMReadinessReport) -> list[str]:
    lines = ["## BIM Readiness", ""]
    lines.append(f"**BIM readiness score:** **{bim.score}/100**")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Total entities | {bim.total_entities} |")
    lines.append(f"| BIM-relevant entities | {bim.bim_entities} |")
    lines.append(f"| Mapped entities | {bim.mapped_entities} |")
    lines.append(f"| Missing level | {bim.missing_level} |")
    lines.append(f"| Missing material | {bim.missing_material} |")
    lines.append(f"| Missing required properties | {bim.missing_required_properties} |")
    lines.append("")
    lines.extend(_table("IFC Class Summary", bim.ifc_class_counts))
    return lines


def _gis_section(gis: GISReadinessReport) -> list[str]:
    lines = ["## GIS Readiness", ""]
    lines.append(f"**GIS readiness score:** **{gis.score}/100**")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Total entities | {gis.total_entities} |")
    lines.append(f"| Geospatial entities | {gis.geospatial_entities} |")
    lines.append(f"| Exportable GeoJSON features | {gis.exportable_features} |")
    lines.append(f"| Missing geometry | {gis.missing_geometry} |")
    lines.append(f"| Unknown category | {gis.unknown_category} |")
    lines.append(f"| Missing level/floor | {gis.missing_level} |")
    lines.append(f"| Polygon candidates | {gis.topology.polygon_count} |")
    lines.append(f"| Open boundaries | {gis.topology.open_boundary_count} |")
    lines.append(f"| Zero-area polygons | {gis.topology.zero_area_polygon_count} |")
    lines.append(f"| Duplicate geometries | {gis.topology.duplicate_geometry_count} |")
    lines.append(f"| Bounding-box overlap pairs | {gis.topology.overlap_pair_count} |")
    lines.append("")
    lines.extend(_table("GIS Geometry Type Summary", gis.geometry_type_counts))
    return lines



def _rule_engine_section(rule_result: RuleResult) -> list[str]:
    lines = ["## Rule Engine", ""]
    lines.append(f"**Rule engine score:** **{rule_result.score}/100**")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Total rules | {rule_result.total_rules} |")
    lines.append(f"| Evaluated entities | {rule_result.evaluated_entities} |")
    lines.append(f"| Passed checks | {rule_result.passed} |")
    lines.append(f"| Failed checks | {rule_result.failed} |")
    lines.append(f"| Skipped checks | {rule_result.skipped} |")
    lines.append("")
    lines.extend(_table("Rule Failure Summary", rule_result.failure_counts))
    return lines


def _plugin_section(plugin_summary: PluginRunSummary) -> list[str]:
    lines = ["## Plugin System", ""]
    lines.append(f"**Plugin score:** **{plugin_summary.score}/100**")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Enabled plugins | {plugin_summary.enabled_plugins} |")
    lines.append(f"| Executed plugins | {plugin_summary.executed_plugins} |")
    lines.append(f"| Failed plugins | {plugin_summary.failed_plugins} |")
    lines.append(f"| Plugin issues | {plugin_summary.total_issues} |")
    lines.append("")
    lines.append("| Plugin | Version | Status | Checked Entities | Issues |")
    lines.append("|---|---|---|---:|---:|")
    if not plugin_summary.results:
        lines.append("| _none_ |  |  | 0 | 0 |")
    else:
        for result in plugin_summary.results:
            lines.append(
                f"| {result.plugin_name} | {result.version} | {result.status} | "
                f"{result.checked_entities} | {len(result.issues)} |"
            )
    lines.append("")
    if plugin_summary.total_issues:
        lines.append("### Plugin Issues")
        lines.append("")
        lines.append("| Plugin | Entity ID | Severity | Code | Message |")
        lines.append("|---|---|---|---|---|")
        for result in plugin_summary.results:
            for issue in result.issues:
                message = issue.message.replace("|", "\|")
                lines.append(
                    f"| {issue.plugin or result.plugin_name} | `{issue.entity_id or ''}` | "
                    f"{issue.severity} | {issue.code} | {message} |"
                )
        lines.append("")
    return lines

def write_markdown_report(
    document: ADFDocument,
    report_path: str | Path,
    bim_readiness: BIMReadinessReport | None = None,
    gis_readiness: GISReadinessReport | None = None,
    rule_result: RuleResult | None = None,
    plugin_summary: PluginRunSummary | None = None,
) -> Path:
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    metrics = compute_architectural_metrics(document)
    score = compute_quality_score(document)
    bim = bim_readiness or compute_bim_readiness(document)
    gis = gis_readiness or compute_gis_readiness(document, annotate=False)
    rules = rule_result or RuleResult(evaluated_entities=len(document.entities))
    plugins = plugin_summary or PluginRunSummary()

    lines: list[str] = []
    lines.append("# AIMS Architectural BIM QA/QC Report")
    lines.append("")
    lines.append(f"**Source file:** `{document.source_file}`")
    lines.append(f"**Units:** `{document.units}`")
    lines.append(f"**Total entities:** {metrics.total_entities}")
    lines.append(f"**Total issues:** {document.issue_count()}")
    lines.append(f"**Architectural quality score:** **{score}/100**")
    lines.append(f"**BIM readiness score:** **{bim.score}/100**")
    lines.append(f"**GIS readiness score:** **{gis.score}/100**")
    lines.append(f"**Rule engine score:** **{rules.score}/100**")
    lines.append(f"**Plugin score:** **{plugins.score}/100**")
    lines.append("")
    lines.extend(_table("Category Summary", metrics.category_counts))
    lines.extend(_table("Layer Summary", metrics.layer_counts))
    lines.extend(_table("Block Summary", metrics.block_counts))
    lines.extend(_table("Issue Severity Summary", metrics.severity_counts))
    lines.extend(_table("Issue Code Summary", metrics.issue_counts))
    lines.extend(_bim_section(bim))
    lines.extend(_gis_section(gis))
    lines.extend(_rule_engine_section(rules))
    lines.extend(_plugin_section(plugins))

    lines.append("## BIM Entity Snapshot")
    lines.append("")
    lines.append("| Entity ID | Category | IFC Class | Level | Material |")
    lines.append("|---|---|---|---|---|")
    for entity in document.entities:
        if entity.bim_class:
            level = entity.properties.get("level") or ""
            material = entity.properties.get("material") or ""
            lines.append(f"| `{entity.id}` | {entity.category.value} | {entity.bim_class} | {level} | {material} |")
    lines.append("")

    lines.append("## Entity Issues")
    lines.append("")
    if document.issue_count() == 0:
        lines.append("No issues detected.")
    else:
        lines.append("| Entity ID | Type | Layer | Category | BIM Class | Severity | Code | Message |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for entity in document.entities:
            for issue in entity.issues:
                message = issue.message.replace("|", "\\|")
                lines.append(
                    f"| `{entity.id}` | {entity.entity_type} | {entity.layer} | {entity.category.value} | "
                    f"{entity.bim_class or ''} | {issue.severity} | {issue.code} | {message} |"
                )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path
