from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Set

from packages.aims_core.adf import ADFCategory, ADFDocument, ValidationIssue
from packages.aims_geometry.geometry import geometry_signature, polygon_area, polyline_length
from packages.aims_rules.loader import normalize_standard


def validate_document(document: ADFDocument, standard: Dict[str, Any] | None = None) -> ADFDocument:
    standard = normalize_standard(standard)
    known_layers: Set[str] = {str(name).lower() for name in standard.get("layers", {}).keys()}
    known_blocks: Set[str] = {str(name).lower() for name in standard.get("blocks", {}).keys()}
    rules = standard.get("rules", {})
    min_room_area = float(rules.get("min_room_area", 0.01))

    signatures: dict[tuple, list[str]] = defaultdict(list)

    for entity in document.entities:
        if known_layers and entity.layer.lower() not in known_layers:
            entity.issues.append(ValidationIssue(code="UNKNOWN_LAYER", severity="warning", message=f"Layer '{entity.layer}' is not defined in the active standard."))

        if entity.category == ADFCategory.UNKNOWN:
            entity.issues.append(ValidationIssue(code="UNKNOWN_CATEGORY", severity="warning", message="Entity could not be classified into an architectural/BIM category."))

        if entity.geometry:
            sig = (entity.geometry.type, geometry_signature(entity.geometry.points))
            signatures[sig].append(entity.id)

            if entity.geometry.type == "line" and polyline_length(entity.geometry.points) <= 0.000001:
                entity.issues.append(ValidationIssue(code="ZERO_LENGTH", severity="error", message="Geometry length is zero or almost zero."))

            if entity.geometry.type == "polyline" and entity.category in {ADFCategory.WALL, ADFCategory.ROOM} and not entity.geometry.closed:
                entity.issues.append(ValidationIssue(code="OPEN_BOUNDARY", severity="warning", message="Wall/room polyline is not closed."))

            if entity.geometry.type == "polyline" and len(entity.geometry.points) < 2:
                entity.issues.append(ValidationIssue(code="INVALID_POLYLINE", severity="error", message="Polyline has fewer than two points."))

            if entity.geometry.type == "polyline" and entity.category == ADFCategory.ROOM and entity.geometry.closed:
                area = polygon_area(entity.geometry.points)
                entity.properties["area"] = area
                entity.properties["perimeter"] = polyline_length(entity.geometry.points, closed=True)
                if area < min_room_area:
                    entity.issues.append(ValidationIssue(code="ROOM_AREA_TOO_SMALL", severity="warning", message=f"Room boundary area is below minimum threshold: {area:.3f}."))

        if entity.entity_type == "INSERT":
            block_name = str(entity.properties.get("block_name", ""))
            if not block_name:
                entity.issues.append(ValidationIssue(code="UNKNOWN_BLOCK", severity="warning", message="Block insert has no block name."))
            elif known_blocks and block_name.lower() not in known_blocks:
                entity.issues.append(ValidationIssue(code="NON_STANDARD_BLOCK", severity="warning", message=f"Block '{block_name}' is not defined in the active standard."))

        if entity.category in {ADFCategory.DOOR, ADFCategory.WINDOW} and entity.entity_type != "INSERT":
            entity.issues.append(ValidationIssue(code="ARCH_OBJECT_NOT_BLOCK", severity="warning", message="Door/window should preferably be represented as a standard block insert."))

    for ids in signatures.values():
        if len(ids) > 1:
            duplicated = set(ids)
            for entity in document.entities:
                if entity.id in duplicated:
                    entity.issues.append(ValidationIssue(code="DUPLICATE_GEOMETRY", severity="warning", message="Another entity has the same geometry signature."))

    return document
