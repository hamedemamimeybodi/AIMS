from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List

from packages.aims_core.adf import ADFDocument, ADFEntity, ValidationIssue
from packages.aims_geometry.geometry import polygon_area, polyline_length
from packages.aims_rules.loader import normalize_standard


@dataclass
class RuleResult:
    total_rules: int = 0
    evaluated_entities: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    failure_counts: dict[str, int] = field(default_factory=dict)

    @property
    def score(self) -> int:
        total = self.passed + self.failed
        if total == 0:
            return 100
        return max(0, min(100, round((self.passed / total) * 100)))


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _matches(entity: ADFEntity, selector: dict[str, Any]) -> bool:
    if not selector:
        return True
    layers = [str(v).lower() for v in _as_list(selector.get("layer"))]
    categories = [str(v).lower() for v in _as_list(selector.get("category"))]
    entity_types = [str(v).lower() for v in _as_list(selector.get("entity_type"))]
    bim_classes = [str(v).lower() for v in _as_list(selector.get("bim_class"))]

    if layers and entity.layer.lower() not in layers:
        return False
    if categories and entity.category.value.lower() not in categories:
        return False
    if entity_types and entity.entity_type.lower() not in entity_types:
        return False
    if bim_classes and str(entity.bim_class or "").lower() not in bim_classes:
        return False
    return True


def _property_value(entity: ADFEntity, name: str) -> Any:
    if name == "layer":
        return entity.layer
    if name == "category":
        return entity.category.value
    if name == "entity_type":
        return entity.entity_type
    if name == "bim_class":
        return entity.bim_class
    if name == "text":
        return entity.text
    if name.startswith("geometry.") and entity.geometry:
        return getattr(entity.geometry, name.split(".", 1)[1], None)
    return entity.properties.get(name)


def _check_condition(entity: ADFEntity, condition: dict[str, Any]) -> bool:
    op = condition.get("op")
    field_name = str(condition.get("field", ""))
    value = _property_value(entity, field_name)

    if op == "exists":
        return value not in (None, "")
    if op == "not_empty":
        return value not in (None, "", [], {})
    if op == "equals":
        return value == condition.get("value")
    if op == "in":
        return value in _as_list(condition.get("values"))
    if op == "closed_geometry":
        return bool(entity.geometry and entity.geometry.closed)
    if op == "geometry_type":
        return bool(entity.geometry and entity.geometry.type == condition.get("value"))
    if op == "min_area":
        if not entity.geometry or not entity.geometry.points:
            return False
        area = polygon_area(entity.geometry.points)
        return area >= float(condition.get("value", 0))
    if op == "min_length":
        if not entity.geometry or not entity.geometry.points:
            return False
        length = polyline_length(entity.geometry.points, closed=bool(entity.geometry.closed))
        return length >= float(condition.get("value", 0))
    if op == "block_name_matches":
        block_name = str(entity.properties.get("block_name", "")).lower()
        allowed = [str(v).lower() for v in _as_list(condition.get("values"))]
        return bool(block_name and block_name in allowed)
    return True


def apply_rule_engine(document: ADFDocument, standard: Dict[str, Any] | None = None, annotate: bool = True) -> RuleResult:
    """Run YAML-defined entity rules against an ADF document.

    Expected YAML shape:

    rule_sets:
      architectural_qaqc:
        rules:
          - id: ROOM_REQUIRES_NAME
            selector: {category: Room}
            severity: warning
            message: Room should have a room_name property.
            conditions:
              - {op: not_empty, field: room_name}
    """
    standard = normalize_standard(standard)
    rule_sets = standard.get("rule_sets", {}) or {}
    rules: list[dict[str, Any]] = []
    for rule_set in rule_sets.values():
        rules.extend(rule_set.get("rules", []) or [])
    rules.extend(standard.get("entity_rules", []) or [])

    result = RuleResult(total_rules=len(rules), evaluated_entities=len(document.entities))
    if not rules:
        return result

    for entity in document.entities:
        for rule in rules:
            if not _matches(entity, rule.get("selector", {}) or {}):
                result.skipped += 1
                continue
            conditions = rule.get("conditions", []) or []
            ok = all(_check_condition(entity, condition) for condition in conditions)
            if ok:
                result.passed += 1
            else:
                result.failed += 1
                code = str(rule.get("id", "RULE_FAILED"))
                result.failure_counts[code] = result.failure_counts.get(code, 0) + 1
                if annotate:
                    entity.issues.append(
                        ValidationIssue(
                            code=code,
                            severity=str(rule.get("severity", "warning")),
                            message=str(rule.get("message", f"Rule failed: {code}")),
                        )
                    )
    return result
