from __future__ import annotations

import json

from packages.aims_validator.engine import ValidationReport


def to_json(report: ValidationReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
