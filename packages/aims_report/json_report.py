from __future__ import annotations

import json
from pathlib import Path

from packages.aims_bim.readiness import BIMReadinessReport
from packages.aims_core.adf import ADFDocument
from packages.aims_gis.readiness import GISReadinessReport
from packages.aims_plugins.loader import PluginRunSummary
from packages.aims_openbim.openbim_validation import OpenBIMValidationReport
from packages.aims_report.summary import build_report_summary
from packages.aims_rules.engine import RuleResult


def write_json_report(
    document: ADFDocument,
    report_path: str | Path,
    bim_readiness: BIMReadinessReport | None = None,
    gis_readiness: GISReadinessReport | None = None,
    rule_result: RuleResult | None = None,
    plugin_summary: PluginRunSummary | None = None,
    openbim_validation: OpenBIMValidationReport | None = None,
) -> Path:
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = build_report_summary(document, bim_readiness, gis_readiness, rule_result, plugin_summary, openbim_validation)
    payload = summary.to_dict()
    payload["entities"] = [entity.model_dump(mode="json") for entity in document.entities]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
