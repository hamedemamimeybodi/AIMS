from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable

from packages.aims_core.adf import ADFDocument, ADFEntity, ValidationIssue

BIM_RELEVANT_CLASSES = {"IfcWall", "IfcDoor", "IfcWindow", "IfcColumn", "IfcSpace"}


@dataclass(frozen=True)
class BIMReadinessReport:
    total_entities: int
    bim_entities: int
    mapped_entities: int
    missing_level: int
    missing_material: int
    missing_required_properties: int
    ifc_class_counts: Dict[str, int] = field(default_factory=dict)
    score: int = 0


def _required_properties_for(entity: ADFEntity, standard: Dict[str, Any] | None) -> list[str]:
    if not standard:
        return []
    bim = standard.get("bim", {}) or standard.get("bim_mapping", {}) or {}
    required = bim.get("required_properties", {}) or {}
    return list(required.get(entity.bim_class or "", []))


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or value == "UNASSIGNED"


def _dedupe_issue(entity: ADFEntity, code: str, severity: str, message: str) -> None:
    if any(issue.code == code for issue in entity.issues):
        return
    entity.issues.append(ValidationIssue(code=code, severity=severity, message=message))


def compute_bim_readiness(document: ADFDocument, standard: Dict[str, Any] | None = None) -> BIMReadinessReport:
    total = len(document.entities)
    mapped = 0
    bim_entities = 0
    missing_level = 0
    missing_material = 0
    missing_required = 0
    counts: dict[str, int] = {}

    for entity in document.entities:
        if entity.bim_class:
            mapped += 1
            counts[entity.bim_class] = counts.get(entity.bim_class, 0) + 1

        if entity.bim_class in BIM_RELEVANT_CLASSES:
            bim_entities += 1

            if _is_missing(entity.properties.get("level")):
                missing_level += 1
                _dedupe_issue(entity, "BIM_MISSING_LEVEL", "warning", "BIM element has no assigned level.")

            if entity.bim_class in {"IfcWall", "IfcDoor", "IfcWindow", "IfcColumn"} and _is_missing(entity.properties.get("material")):
                missing_material += 1
                _dedupe_issue(entity, "BIM_MISSING_MATERIAL", "info", "BIM element has no assigned material.")

            for prop in _required_properties_for(entity, standard):
                if _is_missing(entity.properties.get(prop)):
                    missing_required += 1
                    _dedupe_issue(entity, "BIM_MISSING_REQUIRED_PROPERTY", "warning", f"Missing required BIM property: {prop}")

    if total == 0:
        score = 0
    else:
        mapped_ratio = mapped / total
        denominator = max(bim_entities, 1)
        level_ratio = 1 - (missing_level / denominator)
        material_ratio = 1 - (missing_material / denominator)
        required_ratio = 1 - (missing_required / max(denominator, 1))
        score = round((mapped_ratio * 45) + (level_ratio * 25) + (material_ratio * 15) + (required_ratio * 15))
        score = max(0, min(100, score))

    return BIMReadinessReport(
        total_entities=total,
        bim_entities=bim_entities,
        mapped_entities=mapped,
        missing_level=missing_level,
        missing_material=missing_material,
        missing_required_properties=missing_required,
        ifc_class_counts=counts,
        score=score,
    )
