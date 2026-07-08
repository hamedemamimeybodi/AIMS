from __future__ import annotations

import json

from packages.aims_bim.bim_mapping import apply_bim_mapping
from packages.aims_bim.readiness import compute_bim_readiness
from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry, ValidationIssue
from packages.aims_gis.readiness import compute_gis_readiness
from packages.aims_plugins.loader import PluginRunSummary
from packages.aims_report.html_report import write_html_report
from packages.aims_report.json_report import write_json_report
from packages.aims_report.summary import build_report_summary, compute_overall_score
from packages.aims_rules.engine import RuleResult


def _doc() -> ADFDocument:
    return ADFDocument(
        source_file="unit-test.dxf",
        units="mm",
        entities=[
            ADFEntity(
                id="wall-1",
                entity_type="LWPOLYLINE",
                layer="A-WALL",
                category=ADFCategory.WALL,
                geometry=ADFGeometry(type="polyline", closed=True, points=[[0, 0], [1, 0], [1, 1], [0, 0]]),
                properties={"level": "Ground Floor", "material": "Concrete", "thickness": 200, "height": 3000},
                issues=[ValidationIssue(code="sample", severity="warning", message="Sample warning")],
            )
        ],
    )


def test_compute_overall_score() -> None:
    assert compute_overall_score([100, 80, 60]) == 80
    assert compute_overall_score([]) == 0
    assert compute_overall_score([120, -20]) == 50


def test_build_report_summary_contains_scorecard() -> None:
    doc = _doc()
    apply_bim_mapping(doc)
    summary = build_report_summary(
        doc,
        compute_bim_readiness(doc),
        compute_gis_readiness(doc),
        RuleResult(total_rules=1, evaluated_entities=1, passed=1),
        PluginRunSummary(enabled_plugins=1, executed_plugins=1),
    )
    assert summary.total_entities == 1
    assert summary.total_issues == 1
    assert 0 <= summary.scorecard.overall <= 100
    assert summary.category_counts["Wall"] == 1


def test_write_json_report(tmp_path) -> None:
    doc = _doc()
    apply_bim_mapping(doc)
    out = write_json_report(doc, tmp_path / "aims_report.json")
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["source_file"] == "unit-test.dxf"
    assert payload["scorecard"]["overall"] >= 0
    assert payload["entities"][0]["id"] == "wall-1"


def test_write_html_report(tmp_path) -> None:
    doc = _doc()
    apply_bim_mapping(doc)
    out = write_html_report(doc, tmp_path / "aims_report.html")
    html = out.read_text(encoding="utf-8")
    assert "AIMS Architectural BIM QA/QC Report" in html
    assert "Overall" in html
    assert "wall-1" in html
