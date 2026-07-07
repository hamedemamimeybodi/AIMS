from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FixPlan:
    rule_id: str
    feature_id: str | None
    safety_level: str
    description: str
    reversible: bool = True
