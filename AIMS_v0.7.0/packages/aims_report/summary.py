from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from packages.aims_architecture.metrics import compute_architectural_metrics
from packages.aims_architecture.qa_score import compute_quality_score
from packages.aims_bim.readiness import BIMReadinessReport, compute_bim_readiness
from packages.aims_core.adf import ADFDocument
from packages.aims_gis.readiness import GISReadinessReport, compute_gis_readiness
from packages.aims_plugins.loader import PluginRunSummary
from packages.aims_rules.engine import RuleResult


@dataclass
class ReportScorecard:
    architectural_quality: int
    bim_readiness: int
    gis_readiness: int
    rule_engine: int
    plugin_system: int
    overall: int


@dataclass
class ReportSummary:
    source_file: str
    units: str | None
    total_entities: int
    total_issues: int
    scorecard: ReportScorecard
    category_counts: dict[str, int]
    layer_counts: dict[str, int]
    severity_counts: dict[str, int]
    issue_counts: dict[str, int]
    bim: dict[str, Any]
    gis: dict[str, Any]
    rules: dict[str, Any]
    plugins: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _safe_score(value: int | float | None) -> int:
    if value is None:
        return 0
    return max(0, min(100, int(round(value))))


def compute_overall_score(scores: list[int]) -> int:
    if not scores:
        return 0
    return _safe_score(sum(scores) / len(scores))


def build_report_summary(
    document: ADFDocument,
    bim_readiness: BIMReadinessReport | None = None,
    gis_readiness: GISReadinessReport | None = None,
    rule_result: RuleResult | None = None,
    plugin_summary: PluginRunSummary | None = None,
) -> ReportSummary:
    metrics = compute_architectural_metrics(document)
    arch_score = compute_quality_score(document)
    bim = bim_readiness or compute_bim_readiness(document)
    gis = gis_readiness or compute_gis_readiness(document, annotate=False)
    rules = rule_result or RuleResult(evaluated_entities=len(document.entities))
    plugins = plugin_summary or PluginRunSummary()

    scorecard = ReportScorecard(
        architectural_quality=_safe_score(arch_score),
        bim_readiness=_safe_score(bim.score),
        gis_readiness=_safe_score(gis.score),
        rule_engine=_safe_score(rules.score),
        plugin_system=_safe_score(plugins.score),
        overall=compute_overall_score([arch_score, bim.score, gis.score, rules.score, plugins.score]),
    )

    return ReportSummary(
        source_file=document.source_file,
        units=document.units,
        total_entities=metrics.total_entities,
        total_issues=document.issue_count(),
        scorecard=scorecard,
        category_counts=metrics.category_counts,
        layer_counts=metrics.layer_counts,
        severity_counts=metrics.severity_counts,
        issue_counts=metrics.issue_counts,
        bim={
            "score": bim.score,
            "total_entities": bim.total_entities,
            "bim_entities": bim.bim_entities,
            "mapped_entities": bim.mapped_entities,
            "missing_level": bim.missing_level,
            "missing_material": bim.missing_material,
            "missing_required_properties": bim.missing_required_properties,
            "ifc_class_counts": bim.ifc_class_counts,
        },
        gis={
            "score": gis.score,
            "total_entities": gis.total_entities,
            "geospatial_entities": gis.geospatial_entities,
            "exportable_features": gis.exportable_features,
            "missing_geometry": gis.missing_geometry,
            "unknown_category": gis.unknown_category,
            "missing_level": gis.missing_level,
            "geometry_type_counts": gis.geometry_type_counts,
            "topology": {
                "polygon_count": gis.topology.polygon_count,
                "open_boundary_count": gis.topology.open_boundary_count,
                "zero_area_polygon_count": gis.topology.zero_area_polygon_count,
                "duplicate_geometry_count": gis.topology.duplicate_geometry_count,
                "overlap_pair_count": gis.topology.overlap_pair_count,
            },
        },
        rules={
            "score": rules.score,
            "total_rules": rules.total_rules,
            "evaluated_entities": rules.evaluated_entities,
            "passed": rules.passed,
            "failed": rules.failed,
            "skipped": rules.skipped,
            "failure_counts": rules.failure_counts,
        },
        plugins={
            "score": plugins.score,
            "enabled_plugins": plugins.enabled_plugins,
            "executed_plugins": plugins.executed_plugins,
            "failed_plugins": plugins.failed_plugins,
            "total_issues": plugins.total_issues,
            "results": [
                {
                    "plugin_name": result.plugin_name,
                    "version": result.version,
                    "status": result.status,
                    "checked_entities": result.checked_entities,
                    "issues": [issue.__dict__ for issue in result.issues],
                }
                for result in plugins.results
            ],
        },
    )
