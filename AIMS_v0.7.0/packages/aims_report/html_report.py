from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from packages.aims_bim.readiness import BIMReadinessReport
from packages.aims_core.adf import ADFDocument
from packages.aims_gis.readiness import GISReadinessReport
from packages.aims_plugins.loader import PluginRunSummary
from packages.aims_report.summary import ReportSummary, build_report_summary
from packages.aims_rules.engine import RuleResult


def _rows(data: dict[str, Any]) -> str:
    if not data:
        return '<tr><td><em>none</em></td><td>0</td></tr>'
    return "\n".join(
        f"<tr><td>{escape(str(key))}</td><td>{escape(str(value))}</td></tr>" for key, value in sorted(data.items())
    )


def _score_class(score: int) -> str:
    if score >= 90:
        return "excellent"
    if score >= 75:
        return "good"
    if score >= 50:
        return "warning"
    return "critical"


def _score_card(label: str, score: int) -> str:
    return f'<div class="score {_score_class(score)}"><span>{escape(label)}</span><strong>{score}</strong></div>'


def render_html_report(summary: ReportSummary, document: ADFDocument) -> str:
    sc = summary.scorecard
    issue_rows: list[str] = []
    for entity in document.entities:
        for issue in entity.issues:
            issue_rows.append(
                "<tr>"
                f"<td><code>{escape(entity.id)}</code></td>"
                f"<td>{escape(entity.entity_type)}</td>"
                f"<td>{escape(entity.layer)}</td>"
                f"<td>{escape(entity.category.value)}</td>"
                f"<td>{escape(issue.severity)}</td>"
                f"<td>{escape(issue.code)}</td>"
                f"<td>{escape(issue.message)}</td>"
                "</tr>"
            )
    if not issue_rows:
        issue_rows.append('<tr><td colspan="7">No issues detected.</td></tr>')

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AIMS QA/QC Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #222; }}
    h1, h2 {{ margin-bottom: 8px; }}
    .meta {{ color: #555; margin-bottom: 24px; }}
    .scores {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 20px 0; }}
    .score {{ border: 1px solid #ddd; border-radius: 10px; padding: 12px 16px; min-width: 150px; }}
    .score span {{ display: block; font-size: 12px; color: #555; }}
    .score strong {{ font-size: 28px; }}
    .excellent {{ border-left: 6px solid #238636; }}
    .good {{ border-left: 6px solid #2f81f7; }}
    .warning {{ border-left: 6px solid #d29922; }}
    .critical {{ border-left: 6px solid #da3633; }}
    table {{ border-collapse: collapse; width: 100%; margin: 12px 0 24px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f3f4f6; }}
    code {{ background: #f3f4f6; padding: 2px 4px; border-radius: 4px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }}
  </style>
</head>
<body>
  <h1>AIMS Architectural BIM QA/QC Report</h1>
  <div class="meta">
    <div><strong>Source:</strong> <code>{escape(summary.source_file)}</code></div>
    <div><strong>Units:</strong> <code>{escape(str(summary.units))}</code></div>
    <div><strong>Total entities:</strong> {summary.total_entities}</div>
    <div><strong>Total issues:</strong> {summary.total_issues}</div>
  </div>

  <div class="scores">
    {_score_card('Overall', sc.overall)}
    {_score_card('Architecture', sc.architectural_quality)}
    {_score_card('BIM', sc.bim_readiness)}
    {_score_card('GIS', sc.gis_readiness)}
    {_score_card('Rules', sc.rule_engine)}
    {_score_card('Plugins', sc.plugin_system)}
  </div>

  <div class="grid">
    <section><h2>Category Summary</h2><table><tr><th>Name</th><th>Count</th></tr>{_rows(summary.category_counts)}</table></section>
    <section><h2>Layer Summary</h2><table><tr><th>Name</th><th>Count</th></tr>{_rows(summary.layer_counts)}</table></section>
    <section><h2>Issue Severity Summary</h2><table><tr><th>Name</th><th>Count</th></tr>{_rows(summary.severity_counts)}</table></section>
    <section><h2>Issue Code Summary</h2><table><tr><th>Name</th><th>Count</th></tr>{_rows(summary.issue_counts)}</table></section>
  </div>

  <h2>Readiness Metrics</h2>
  <table>
    <tr><th>Area</th><th>Score</th><th>Key details</th></tr>
    <tr><td>BIM</td><td>{summary.bim['score']}</td><td>Mapped {summary.bim['mapped_entities']} of {summary.bim['bim_entities']} BIM-relevant entities</td></tr>
    <tr><td>GIS</td><td>{summary.gis['score']}</td><td>{summary.gis['exportable_features']} exportable GeoJSON features</td></tr>
    <tr><td>Rules</td><td>{summary.rules['score']}</td><td>{summary.rules['failed']} failed checks</td></tr>
    <tr><td>Plugins</td><td>{summary.plugins['score']}</td><td>{summary.plugins['executed_plugins']} executed plugins, {summary.plugins['total_issues']} plugin issues</td></tr>
  </table>

  <h2>Entity Issues</h2>
  <table>
    <tr><th>Entity ID</th><th>Type</th><th>Layer</th><th>Category</th><th>Severity</th><th>Code</th><th>Message</th></tr>
    {''.join(issue_rows)}
  </table>
</body>
</html>
"""


def write_html_report(
    document: ADFDocument,
    report_path: str | Path,
    bim_readiness: BIMReadinessReport | None = None,
    gis_readiness: GISReadinessReport | None = None,
    rule_result: RuleResult | None = None,
    plugin_summary: PluginRunSummary | None = None,
) -> Path:
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = build_report_summary(document, bim_readiness, gis_readiness, rule_result, plugin_summary)
    path.write_text(render_html_report(summary, document), encoding="utf-8")
    return path
