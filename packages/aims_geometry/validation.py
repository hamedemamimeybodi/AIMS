from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Any

from packages.aims_geometry.adf import ADFDocument, ADFEntity


@dataclass(slots=True)
class ValidationIssue:
    rule_code: str
    severity: str
    message: str
    entity_id: int | None = None


@dataclass(slots=True)
class ValidationResult:
    issues: list[ValidationIssue]

    @property
    def is_valid(self) -> bool:
        return not any(issue.severity.upper() == "ERROR" for issue in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity.upper() == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity.upper() == "WARNING")


def _same_point(a: list[float], b: list[float]) -> bool:
    return len(a) == len(b) and all(isclose(float(x), float(y), abs_tol=1e-9) for x, y in zip(a, b))


def _validate_entity(entity: ADFEntity) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if not entity.layer:
        issues.append(ValidationIssue("AIMS-VAL-001", "ERROR", "Entity has empty layer.", entity.entity_id))

    if entity.entity_type == "LINE":
        start = entity.geometry.get("start", [])
        end = entity.geometry.get("end", [])
        if _same_point(start, end):
            issues.append(ValidationIssue("AIMS-VAL-002", "WARNING", "Zero-length line detected.", entity.entity_id))

    if entity.entity_type == "LWPOLYLINE":
        vertices: list[Any] = entity.geometry.get("vertices", [])
        if len(vertices) < 2:
            issues.append(ValidationIssue("AIMS-VAL-003", "ERROR", "Polyline has fewer than two vertices.", entity.entity_id))
        if entity.geometry.get("closed") and len(vertices) >= 2 and not _same_point(vertices[0], vertices[-1]):
            issues.append(ValidationIssue("AIMS-VAL-004", "INFO", "Closed flag is set; first and last vertices differ, which is valid for DXF LWPOLYLINE.", entity.entity_id))

    if entity.entity_type in {"TEXT", "MTEXT"} and not (entity.text or "").strip():
        issues.append(ValidationIssue("AIMS-VAL-005", "WARNING", "Text entity has empty value.", entity.entity_id))

    return issues


def validate_adf(adf: ADFDocument) -> ValidationResult:
    issues: list[ValidationIssue] = []

    if adf.version != "0.1":
        issues.append(ValidationIssue("AIMS-DOC-001", "WARNING", f"Unexpected ADF version: {adf.version}"))

    if not adf.entities:
        issues.append(ValidationIssue("AIMS-DOC-002", "ERROR", "Document contains no supported entities."))

    for entity in adf.entities:
        issues.extend(_validate_entity(entity))

    return ValidationResult(issues=issues)


def build_validation_report(adf: ADFDocument, result: ValidationResult) -> str:
    lines = [
        "# AIMS Validation Report",
        "",
        f"Source: `{adf.source_path}`",
        f"ADF version: `{adf.version}`",
        f"Entity count: `{adf.entity_count}`",
        f"Layer count: `{len(adf.layers)}`",
        "",
        "## Summary",
        "",
        f"Valid: `{result.is_valid}`",
        f"Errors: `{result.error_count}`",
        f"Warnings: `{result.warning_count}`",
        f"Issues: `{len(result.issues)}`",
        "",
        "## Issues",
        "",
    ]

    if not result.issues:
        lines.append("No validation issues found.")
    else:
        lines.append("| Rule | Severity | Entity | Message |")
        lines.append("|---|---:|---:|---|")
        for issue in result.issues:
            entity = "" if issue.entity_id is None else str(issue.entity_id)
            lines.append(f"| {issue.rule_code} | {issue.severity} | {entity} | {issue.message} |")

    lines.append("")
    return "\n".join(lines)
