from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from packages.aims_domain import ADFDocument, Feature


@dataclass(slots=True)
class ValidationIssue:
    rule_id: str
    severity: str
    message: str
    feature_id: str | None = None
    why_it_matters: str = ""
    suggested_fix: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ValidationReport:
    source: str
    issues: list[ValidationIssue]

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity.upper() == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity.upper() == "WARNING")

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity.upper() == "INFO")

    @property
    def is_valid(self) -> bool:
        return self.error_count == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "valid": self.is_valid,
            "summary": {
                "errors": self.error_count,
                "warnings": self.warning_count,
                "info": self.info_count,
                "issues": len(self.issues),
            },
            "issues": [issue.to_dict() for issue in self.issues],
        }


def _validate_feature(feature: Feature) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if not feature.layer or feature.layer == "0":
        issues.append(ValidationIssue(
            rule_id="ACS-2001",
            severity="WARNING",
            feature_id=feature.feature_id,
            message="Feature is on layer 0 or has an empty layer.",
            why_it_matters="Layer 0 is usually not suitable for controlled deliverables.",
            suggested_fix="Move the feature to a named standard layer.",
        ))

    if feature.source_entity == "LINE":
        coords = feature.geometry.coordinates
        if len(coords) == 2 and coords[0] == coords[1]:
            issues.append(ValidationIssue(
                rule_id="ACS-3005",
                severity="WARNING",
                feature_id=feature.feature_id,
                message="Zero-length line detected.",
                why_it_matters="Zero-length geometry can break topology, reports, and exports.",
                suggested_fix="Delete the line or correct its endpoints.",
            ))

    if feature.source_entity in {"LWPOLYLINE", "POLYLINE"}:
        vertices = feature.geometry.coordinates
        if len(vertices) < 2:
            issues.append(ValidationIssue(
                rule_id="ACS-3003",
                severity="ERROR",
                feature_id=feature.feature_id,
                message="Polyline has fewer than two vertices.",
                why_it_matters="A polyline needs at least two vertices.",
                suggested_fix="Repair or remove the invalid polyline.",
            ))

    if feature.source_entity in {"TEXT", "MTEXT"} and not (feature.text or "").strip():
        issues.append(ValidationIssue(
            rule_id="ACS-4001",
            severity="WARNING",
            feature_id=feature.feature_id,
            message="Text entity is empty.",
            why_it_matters="Empty labels provide no engineering meaning.",
            suggested_fix="Enter a value or remove the text entity.",
        ))

    return issues


def validate_document(adf: ADFDocument) -> ValidationReport:
    issues: list[ValidationIssue] = []

    if not adf.features:
        issues.append(ValidationIssue(
            rule_id="ACS-1001",
            severity="ERROR",
            message="Document contains no supported features.",
            why_it_matters="AIMS cannot validate an empty parsed engineering model.",
            suggested_fix="Check source file format and parser support.",
        ))

    for feature in adf.features:
        issues.extend(_validate_feature(feature))

    return ValidationReport(source=adf.source_path, issues=issues)
