from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict

from packages.aims_core.adf import ADFDocument, ValidationIssue
from packages.aims_gis.topology import TopologyReport, analyze_topology


@dataclass
class GISReadinessReport:
    score: int
    total_entities: int
    geospatial_entities: int
    exportable_features: int
    missing_geometry: int
    unknown_category: int
    missing_level: int
    topology: TopologyReport
    geometry_type_counts: dict[str, int] = field(default_factory=dict)
    category_counts: dict[str, int] = field(default_factory=dict)


def _has_exportable_geometry(entity) -> bool:
    return bool(entity.geometry and entity.geometry.points and entity.geometry.type in {"point", "line", "polyline"})


def compute_gis_readiness(document: ADFDocument, standard: Dict[str, Any] | None = None, *, annotate: bool = True) -> GISReadinessReport:
    total = len(document.entities)
    missing_geometry = 0
    unknown_category = 0
    missing_level = 0
    exportable = 0
    geometry_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()

    for entity in document.entities:
        category_counts[entity.category.value] += 1
        if entity.geometry:
            geometry_counts[entity.geometry.type] += 1
        else:
            missing_geometry += 1

        if entity.category.value == "Unknown":
            unknown_category += 1
        if _has_exportable_geometry(entity):
            exportable += 1
        if entity.category.value in {"Wall", "Door", "Window", "Column", "Room"} and not entity.properties.get("level"):
            missing_level += 1
            if annotate:
                entity.issues.append(ValidationIssue(code="GIS_MISSING_LEVEL", severity="warning", message="GIS/BIM export entity has no level/floor assignment."))

    topology = analyze_topology(document, annotate=annotate)
    geospatial = exportable

    penalties = 0
    penalties += missing_geometry * 4
    penalties += unknown_category * 3
    penalties += missing_level * 2
    penalties += topology.open_boundary_count * 3
    penalties += topology.zero_area_polygon_count * 10
    penalties += topology.duplicate_geometry_count * 2
    penalties += topology.overlap_pair_count * 4

    if total == 0:
        score = 0
    else:
        export_ratio = exportable / total
        base = int(round(export_ratio * 100))
        score = max(0, min(100, base - penalties))

    return GISReadinessReport(
        score=score,
        total_entities=total,
        geospatial_entities=geospatial,
        exportable_features=exportable,
        missing_geometry=missing_geometry,
        unknown_category=unknown_category,
        missing_level=missing_level,
        topology=topology,
        geometry_type_counts=dict(geometry_counts),
        category_counts=dict(category_counts),
    )
