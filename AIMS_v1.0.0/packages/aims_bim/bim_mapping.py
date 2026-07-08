from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from packages.aims_core.adf import ADFDocument, ADFEntity, ValidationIssue

DEFAULT_IFC_BY_CATEGORY: dict[str, str] = {
    "Wall": "IfcWall",
    "Door": "IfcDoor",
    "Window": "IfcWindow",
    "Column": "IfcColumn",
    "Room": "IfcSpace",
    "Text": "IfcAnnotation",
    "Annotation": "IfcAnnotation",
}


@dataclass(frozen=True)
class BIMMappingResult:
    total_entities: int
    mapped_entities: int
    unmapped_entities: int
    ifc_class_counts: Dict[str, int]


def _standard_bim_rules(standard: Dict[str, Any] | None) -> Dict[str, Any]:
    if not standard:
        return {}
    return standard.get("bim", {}) or standard.get("bim_mapping", {}) or {}


def _ifc_class_for(entity: ADFEntity, standard: Dict[str, Any] | None = None) -> str | None:
    bim_rules = _standard_bim_rules(standard)
    category_map = bim_rules.get("ifc_by_category", {}) or {}
    layer_map = bim_rules.get("ifc_by_layer", {}) or {}
    block_map = bim_rules.get("ifc_by_block", {}) or {}

    block_name = str(entity.properties.get("block_name") or "").upper()
    layer_name = str(entity.layer or "").upper()
    category_name = entity.category.value

    if block_name and block_name in block_map:
        return block_map[block_name]
    if layer_name in layer_map:
        return layer_map[layer_name]
    if category_name in category_map:
        return category_map[category_name]
    return DEFAULT_IFC_BY_CATEGORY.get(category_name)


def apply_bim_mapping(document: ADFDocument, standard: Dict[str, Any] | None = None) -> BIMMappingResult:
    """Populate entity.bim_class and basic BIM properties from category/layer/block rules."""
    mapped = 0
    counts: dict[str, int] = {}

    for entity in document.entities:
        ifc_class = _ifc_class_for(entity, standard)
        if ifc_class:
            entity.bim_class = ifc_class
            entity.properties.setdefault("bim_category", entity.category.value)
            entity.properties.setdefault("ifc_class", ifc_class)
            entity.properties.setdefault("level", entity.properties.get("level") or "UNASSIGNED")
            entity.properties.setdefault("material", entity.properties.get("material"))
            mapped += 1
            counts[ifc_class] = counts.get(ifc_class, 0) + 1
        else:
            entity.issues.append(
                ValidationIssue(
                    code="BIM_UNMAPPED_ENTITY",
                    severity="warning",
                    message="Entity could not be mapped to a BIM/IFC class.",
                )
            )

    return BIMMappingResult(
        total_entities=len(document.entities),
        mapped_entities=mapped,
        unmapped_entities=len(document.entities) - mapped,
        ifc_class_counts=counts,
    )
