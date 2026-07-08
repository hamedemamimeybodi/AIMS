from __future__ import annotations

from typing import Any, Dict, Optional

from packages.aims_core.adf import ADFCategory

DEFAULT_LAYER_KEYWORDS = {
    ADFCategory.WALL: ["wall", "walls", "a-wall", "diwar"],
    ADFCategory.DOOR: ["door", "doors", "a-door", "dar"],
    ADFCategory.WINDOW: ["window", "windows", "a-window", "panjere"],
    ADFCategory.COLUMN: ["column", "columns", "a-column", "col"],
    ADFCategory.ROOM: ["room", "rooms", "space", "a-room"],
    ADFCategory.TEXT: ["text", "txt", "a-text"],
    ADFCategory.ANNOTATION: ["dim", "hatch", "grid", "anno", "a-dim", "a-hatch"],
}

BIM_CLASS_BY_CATEGORY = {
    ADFCategory.WALL: "IfcWall",
    ADFCategory.DOOR: "IfcDoor",
    ADFCategory.WINDOW: "IfcWindow",
    ADFCategory.COLUMN: "IfcColumn",
    ADFCategory.ROOM: "IfcSpace",
    ADFCategory.TEXT: None,
    ADFCategory.ANNOTATION: None,
    ADFCategory.UNKNOWN: None,
}


def classify_layer(layer_name: str, standard: Optional[Dict[str, Any]] = None) -> ADFCategory:
    normalized = (layer_name or "").strip().lower()

    if standard:
        layers = standard.get("layers", {})
        for layer, meta in layers.items():
            if normalized == str(layer).lower():
                category = str(meta.get("category", "Unknown"))
                try:
                    return ADFCategory(category)
                except ValueError:
                    return ADFCategory.UNKNOWN

    for category, keywords in DEFAULT_LAYER_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return ADFCategory.UNKNOWN


def bim_class_for(category: ADFCategory, layer_name: str | None = None, standard: Optional[Dict[str, Any]] = None) -> Optional[str]:
    if standard and layer_name:
        layers = standard.get("layers", {})
        for layer, meta in layers.items():
            if str(layer).lower() == layer_name.lower() and meta.get("bim_class"):
                return str(meta["bim_class"])
    return BIM_CLASS_BY_CATEGORY.get(category)
