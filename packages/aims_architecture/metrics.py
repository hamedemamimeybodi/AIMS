from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict

from packages.aims_core.adf import ADFDocument


@dataclass(frozen=True)
class ArchitecturalMetrics:
    total_entities: int
    category_counts: Dict[str, int] = field(default_factory=dict)
    layer_counts: Dict[str, int] = field(default_factory=dict)
    block_counts: Dict[str, int] = field(default_factory=dict)
    issue_counts: Dict[str, int] = field(default_factory=dict)
    severity_counts: Dict[str, int] = field(default_factory=dict)


def compute_architectural_metrics(document: ADFDocument) -> ArchitecturalMetrics:
    categories = Counter(entity.category.value for entity in document.entities)
    layers = Counter(entity.layer for entity in document.entities)
    blocks = Counter(
        str(entity.properties.get("block_name"))
        for entity in document.entities
        if entity.entity_type == "INSERT" and entity.properties.get("block_name")
    )
    issue_counts = Counter(issue.code for entity in document.entities for issue in entity.issues)
    severity_counts = Counter(issue.severity for entity in document.entities for issue in entity.issues)
    return ArchitecturalMetrics(
        total_entities=len(document.entities),
        category_counts=dict(categories),
        layer_counts=dict(layers),
        block_counts=dict(blocks),
        issue_counts=dict(issue_counts),
        severity_counts=dict(severity_counts),
    )
