from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple

from packages.aims_core.adf import ADFDocument, ADFEntity, ValidationIssue
from packages.aims_geometry.geometry import bbox, geometry_signature, polygon_area

BBox = Tuple[float, float, float, float]


@dataclass
class TopologyReport:
    polygon_count: int = 0
    open_boundary_count: int = 0
    zero_area_polygon_count: int = 0
    duplicate_geometry_count: int = 0
    bbox_overlap_pairs: list[tuple[str, str]] = field(default_factory=list)

    @property
    def overlap_pair_count(self) -> int:
        return len(self.bbox_overlap_pairs)


def _is_polygon_candidate(entity: ADFEntity) -> bool:
    return bool(entity.geometry and entity.geometry.type == "polyline" and entity.geometry.closed and len(entity.geometry.points) >= 3)


def _bbox_intersects(a: BBox, b: BBox) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def analyze_topology(document: ADFDocument, *, annotate: bool = True) -> TopologyReport:
    report = TopologyReport()
    signatures: Dict[tuple, list[ADFEntity]] = {}
    polygons: list[tuple[ADFEntity, BBox]] = []

    for entity in document.entities:
        if not entity.geometry:
            continue

        if entity.geometry.type == "polyline" and not entity.geometry.closed:
            report.open_boundary_count += 1

        if entity.geometry.points:
            sig = (entity.geometry.type, geometry_signature(entity.geometry.points))
            signatures.setdefault(sig, []).append(entity)

        if _is_polygon_candidate(entity):
            report.polygon_count += 1
            area = polygon_area(entity.geometry.points)
            if area <= 0.000001:
                report.zero_area_polygon_count += 1
                if annotate:
                    entity.issues.append(ValidationIssue(code="GIS_ZERO_AREA_POLYGON", severity="error", message="Closed polygon has zero or near-zero area."))
            box = bbox(entity.geometry.points)
            if box:
                polygons.append((entity, box))

    for entities in signatures.values():
        if len(entities) > 1:
            report.duplicate_geometry_count += len(entities)
            if annotate:
                for entity in entities:
                    entity.issues.append(ValidationIssue(code="GIS_DUPLICATE_GEOMETRY", severity="warning", message="GIS topology found duplicate geometry."))

    for i, (left, left_box) in enumerate(polygons):
        for right, right_box in polygons[i + 1 :]:
            if _bbox_intersects(left_box, right_box):
                report.bbox_overlap_pairs.append((left.id, right.id))
                if annotate:
                    left.issues.append(ValidationIssue(code="GIS_BBOX_OVERLAP", severity="warning", message="Polygon bounding box overlaps another polygon. Review exact topology in GIS."))
                    right.issues.append(ValidationIssue(code="GIS_BBOX_OVERLAP", severity="warning", message="Polygon bounding box overlaps another polygon. Review exact topology in GIS."))

    return report
