from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.aims_domain import ADFDocument, Feature, Geometry

from .reader import read_tokens
from .tokenizer import DXFToken

SUPPORTED = {"LINE", "LWPOLYLINE", "POLYLINE", "POINT", "TEXT", "MTEXT"}


def _entities_section(tokens: list[DXFToken]) -> list[DXFToken]:
    in_entities = False
    result: list[DXFToken] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.code == "0" and token.value == "SECTION":
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            in_entities = bool(next_token and next_token.code == "2" and next_token.value == "ENTITIES")
            i += 1
        elif token.code == "0" and token.value == "ENDSEC" and in_entities:
            break
        elif in_entities:
            result.append(token)
        i += 1
    return result


def _split_entities(tokens: list[DXFToken]) -> list[tuple[str, list[DXFToken]]]:
    entities: list[tuple[str, list[DXFToken]]] = []
    current_type: str | None = None
    current: list[DXFToken] = []

    for token in tokens:
        if token.code == "0":
            if current_type is not None:
                entities.append((current_type, current))
            current_type = token.value
            current = []
        elif current_type is not None:
            current.append(token)

    if current_type is not None:
        entities.append((current_type, current))
    return entities


def _first(raw: list[DXFToken], code: str, default: str = "") -> str:
    for token in raw:
        if token.code == code:
            return token.value
    return default


def _float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _layer(raw: list[DXFToken]) -> str:
    return _first(raw, "8", "0") or "0"


def _line(raw: list[DXFToken]) -> Geometry:
    return Geometry(
        type="LineString",
        coordinates=[
            [_float(_first(raw, "10")), _float(_first(raw, "20")), _float(_first(raw, "30"))],
            [_float(_first(raw, "11")), _float(_first(raw, "21")), _float(_first(raw, "31"))],
        ],
    )


def _point(raw: list[DXFToken]) -> Geometry:
    return Geometry(
        type="Point",
        coordinates=[_float(_first(raw, "10")), _float(_first(raw, "20")), _float(_first(raw, "30"))],
    )


def _lwpolyline(raw: list[DXFToken]) -> Geometry:
    vertices: list[list[float]] = []
    pending_x: float | None = None
    closed = False

    for token in raw:
        if token.code == "70":
            try:
                closed = bool(int(float(token.value)) & 1)
            except ValueError:
                closed = False
        elif token.code == "10":
            pending_x = _float(token.value)
        elif token.code == "20" and pending_x is not None:
            vertices.append([pending_x, _float(token.value), 0.0])
            pending_x = None

    return Geometry(type="Polyline", coordinates=vertices, properties={"closed": closed})


def _text(raw: list[DXFToken]) -> tuple[Geometry, str]:
    value = _first(raw, "1") or _first(raw, "3")
    geometry = Geometry(
        type="Point",
        coordinates=[_float(_first(raw, "10")), _float(_first(raw, "20")), _float(_first(raw, "30"))],
    )
    return geometry, value


def _feature(idx: int, entity_type: str, raw: list[DXFToken]) -> Feature | None:
    if entity_type not in SUPPORTED:
        return None

    text: str | None = None
    if entity_type == "LINE":
        geom = _line(raw)
    elif entity_type in {"LWPOLYLINE", "POLYLINE"}:
        geom = _lwpolyline(raw)
    elif entity_type == "POINT":
        geom = _point(raw)
    elif entity_type in {"TEXT", "MTEXT"}:
        geom, text = _text(raw)
    else:
        return None

    return Feature(
        feature_id=f"F-{idx:06d}",
        source_entity=entity_type,
        layer=_layer(raw),
        geometry=geom,
        text=text,
        attributes={"raw_group_count": len(raw)},
    )


def parse_dxf(path: str | Path) -> ADFDocument:
    path = Path(path)
    tokens = read_tokens(path)
    raw_entities = _split_entities(_entities_section(tokens))
    features: list[Feature] = []

    for idx, (entity_type, raw) in enumerate(raw_entities, start=1):
        feature = _feature(idx, entity_type, raw)
        if feature:
            features.append(feature)

    layers = sorted({f.layer for f in features})
    return ADFDocument(source_path=str(path), features=features, layers=layers)
