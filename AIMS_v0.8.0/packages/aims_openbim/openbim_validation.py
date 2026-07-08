from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.aims_core.adf import ADFDocument, ADFEntity, ValidationIssue

OPENBIM_CLASSES = {"IfcWall", "IfcDoor", "IfcWindow", "IfcColumn", "IfcSpace", "IfcAnnotation"}


@dataclass(frozen=True)
class OpenBIMValidationReport:
    total_entities: int
    openbim_entities: int
    missing_ifc_guid: int
    missing_spatial_container: int
    missing_pset_properties: int
    unsupported_ifc_classes: int
    ifc_class_counts: dict[str, int] = field(default_factory=dict)
    score: int = 0


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or value == "UNASSIGNED"


def _issue(entity: ADFEntity, code: str, severity: str, message: str) -> None:
    if any(i.code == code and i.message == message for i in entity.issues):
        return
    entity.issues.append(ValidationIssue(code=code, severity=severity, message=message))


def _required_psets(standard: dict[str, Any] | None, ifc_class: str | None) -> list[str]:
    if not standard or not ifc_class:
        return []
    openbim = standard.get("openbim", {}) or {}
    required = openbim.get("required_pset_properties", {}) or {}
    return list(required.get(ifc_class, []))


def validate_openbim(document: ADFDocument, standard: dict[str, Any] | None = None, annotate: bool = True) -> OpenBIMValidationReport:
    openbim_entities = 0
    missing_ifc_guid = 0
    missing_spatial = 0
    missing_pset = 0
    unsupported = 0
    counts: dict[str, int] = {}

    for entity in document.entities:
        if not entity.bim_class:
            continue
        counts[entity.bim_class] = counts.get(entity.bim_class, 0) + 1

        if entity.bim_class not in OPENBIM_CLASSES:
            unsupported += 1
            if annotate:
                _issue(entity, "OPENBIM_UNSUPPORTED_IFC_CLASS", "warning", f"Unsupported IFC class for v0.8 export: {entity.bim_class}")
            continue

        openbim_entities += 1
        if _is_missing(entity.properties.get("ifc_guid")):
            missing_ifc_guid += 1
            if annotate:
                entity.properties["ifc_guid"] = entity.id
                _issue(entity, "OPENBIM_GUID_ASSIGNED", "info", "IFC GUID was missing; ADF entity id was used as fallback.")

        if _is_missing(entity.properties.get("spatial_container")) and _is_missing(entity.properties.get("level")):
            missing_spatial += 1
            if annotate:
                _issue(entity, "OPENBIM_MISSING_SPATIAL_CONTAINER", "warning", "OpenBIM entity has no spatial container or level assignment.")

        for prop in _required_psets(standard, entity.bim_class):
            if _is_missing(entity.properties.get(prop)):
                missing_pset += 1
                if annotate:
                    _issue(entity, "OPENBIM_MISSING_PSET_PROPERTY", "warning", f"Missing OpenBIM property set value: {prop}")

    denominator = max(openbim_entities, 1)
    guid_ratio = 1 - (missing_ifc_guid / denominator)
    spatial_ratio = 1 - (missing_spatial / denominator)
    pset_ratio = 1 - (missing_pset / max(denominator, 1))
    unsupported_penalty = min(40, unsupported * 30)
    score = round((guid_ratio * 30) + (spatial_ratio * 35) + (pset_ratio * 35)) - unsupported_penalty
    score = max(0, min(100, score)) if document.entities else 0

    return OpenBIMValidationReport(
        total_entities=len(document.entities),
        openbim_entities=openbim_entities,
        missing_ifc_guid=missing_ifc_guid,
        missing_spatial_container=missing_spatial,
        missing_pset_properties=missing_pset,
        unsupported_ifc_classes=unsupported,
        ifc_class_counts=counts,
        score=score,
    )
