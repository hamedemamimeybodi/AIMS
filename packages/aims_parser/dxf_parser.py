from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.aims_geometry.adf import ADFDocument, ADFEntity

SUPPORTED_ENTITIES = {"LINE", "LWPOLYLINE", "TEXT", "MTEXT", "POINT"}


def _read_group_pairs(path: Path) -> list[tuple[str, str]]:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    pairs: list[tuple[str, str]] = []
    index = 0
    while index + 1 < len(lines):
        pairs.append((lines[index].strip(), lines[index + 1].rstrip()))
        index += 2
    return pairs


def _collect_entities_section(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    in_entities = False
    collected: list[tuple[str, str]] = []
    index = 0
    while index < len(pairs):
        code, value = pairs[index]
        if code == "0" and value == "SECTION":
            next_pair = pairs[index + 1] if index + 1 < len(pairs) else ("", "")
            in_entities = next_pair == ("2", "ENTITIES")
            index += 1
        elif code == "0" and value == "ENDSEC" and in_entities:
            break
        elif in_entities:
            collected.append((code, value))
        index += 1
    return collected


def _split_raw_entities(pairs: list[tuple[str, str]]) -> list[tuple[str, list[tuple[str, str]]]]:
    entities: list[tuple[str, list[tuple[str, str]]]] = []
    current_type: str | None = None
    current_pairs: list[tuple[str, str]] = []

    for code, value in pairs:
        if code == "0":
            if current_type is not None:
                entities.append((current_type, current_pairs))
            current_type = value
            current_pairs = []
        elif current_type is not None:
            current_pairs.append((code, value))

    if current_type is not None:
        entities.append((current_type, current_pairs))
    return entities


def _first(raw: list[tuple[str, str]], code: str, default: str = "") -> str:
    for item_code, value in raw:
        if item_code == code:
            return value
    return default


def _float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_line(raw: list[tuple[str, str]]) -> dict[str, Any]:
    return {
        "start": [_float(_first(raw, "10")), _float(_first(raw, "20")), _float(_first(raw, "30"))],
        "end": [_float(_first(raw, "11")), _float(_first(raw, "21")), _float(_first(raw, "31"))],
    }


def _parse_point(raw: list[tuple[str, str]]) -> dict[str, Any]:
    return {"point": [_float(_first(raw, "10")), _float(_first(raw, "20")), _float(_first(raw, "30"))]}


def _parse_lwpolyline(raw: list[tuple[str, str]]) -> dict[str, Any]:
    vertices: list[list[float]] = []
    pending_x: float | None = None
    closed = False
    for code, value in raw:
        if code == "70":
            closed = bool(int(_float(value)) & 1)
        elif code == "10":
            pending_x = _float(value)
        elif code == "20" and pending_x is not None:
            vertices.append([pending_x, _float(value), 0.0])
            pending_x = None
    return {"vertices": vertices, "closed": closed}


def _parse_text(raw: list[tuple[str, str]]) -> tuple[dict[str, Any], str]:
    text = _first(raw, "1") or _first(raw, "3")
    geometry = {
        "insert": [_float(_first(raw, "10")), _float(_first(raw, "20")), _float(_first(raw, "30"))]
    }
    return geometry, text


def _to_adf_entity(entity_id: int, entity_type: str, raw: list[tuple[str, str]]) -> ADFEntity | None:
    if entity_type not in SUPPORTED_ENTITIES:
        return None

    layer = _first(raw, "8", "0") or "0"
    text: str | None = None

    if entity_type == "LINE":
        geometry = _parse_line(raw)
    elif entity_type == "LWPOLYLINE":
        geometry = _parse_lwpolyline(raw)
    elif entity_type == "POINT":
        geometry = _parse_point(raw)
    elif entity_type in {"TEXT", "MTEXT"}:
        geometry, text = _parse_text(raw)
    else:
        geometry = {}

    return ADFEntity(
        entity_id=entity_id,
        entity_type=entity_type,
        layer=layer,
        geometry=geometry,
        text=text,
        attributes={"raw_group_count": len(raw)},
    )


def parse_dxf_file(path: str | Path) -> ADFDocument:
    dxf_path = Path(path)
    if not dxf_path.exists():
        raise FileNotFoundError(f"DXF file not found: {dxf_path}")

    pairs = _read_group_pairs(dxf_path)
    entity_pairs = _collect_entities_section(pairs)
    raw_entities = _split_raw_entities(entity_pairs)

    entities: list[ADFEntity] = []
    next_id = 1
    for entity_type, raw in raw_entities:
        entity = _to_adf_entity(next_id, entity_type, raw)
        if entity is None:
            continue
        entities.append(entity)
        next_id += 1

    layers = sorted({entity.layer for entity in entities})
    return ADFDocument(source_path=str(dxf_path), layers=layers, entities=entities)
