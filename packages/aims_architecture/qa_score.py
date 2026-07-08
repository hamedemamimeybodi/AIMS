from __future__ import annotations

from packages.aims_core.adf import ADFDocument

SEVERITY_PENALTY = {
    "info": 0.5,
    "warning": 2.0,
    "error": 8.0,
    "critical": 20.0,
}


def compute_quality_score(document: ADFDocument) -> int:
    if not document.entities:
        return 0
    penalty = 0.0
    for entity in document.entities:
        for issue in entity.issues:
            penalty += SEVERITY_PENALTY.get(issue.severity.lower(), 2.0)
    score = round(max(0.0, min(100.0, 100.0 - penalty)))
    return int(score)
