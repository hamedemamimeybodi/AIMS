from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.aims_core.adf import ADFDocument, ADFEntity

EXPORTABLE_IFC_CLASSES = {
    "IfcWall",
    "IfcDoor",
    "IfcWindow",
    "IfcColumn",
    "IfcSpace",
    "IfcAnnotation",
}


@dataclass(frozen=True)
class IFCExportResult:
    total_entities: int
    exportable_entities: int
    skipped_entities: int
    ifc_class_counts: dict[str, int] = field(default_factory=dict)
    output_path: str | None = None


def _safe(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    return text.replace("\\", "\\\\").replace("'", "\\'")


def _point_list(entity: ADFEntity) -> str:
    if not entity.geometry or not entity.geometry.points:
        return "[]"
    return "[" + ", ".join(f"({float(p[0]):.6f},{float(p[1]):.6f})" for p in entity.geometry.points) + "]"


def _ifc_line(index: int, entity: ADFEntity, project_guid: str) -> str:
    ifc_class = entity.bim_class or "IfcProxy"
    guid = _safe(entity.properties.get("ifc_guid") or entity.id)
    name = _safe(entity.properties.get("name") or entity.properties.get("room_name") or entity.category.value)
    level = _safe(entity.properties.get("level") or "UNASSIGNED")
    material = _safe(entity.properties.get("material") or "UNASSIGNED")
    source_layer = _safe(entity.layer)
    category = _safe(entity.category.value)
    points = _safe(_point_list(entity))
    props = f"Layer={source_layer};Category={category};Level={level};Material={material};Points={points}"
    return f"#{index}={ifc_class}('{guid}',#1,'{name}','{props}',$,$,$);"


def export_ifc_text(document: ADFDocument, standard: dict[str, Any] | None = None) -> tuple[str, IFCExportResult]:
    """Create a deterministic IFC-like STEP text export for early OpenBIM integration.

    This v0.8 exporter is intentionally conservative: it writes IFC class records and
    property payloads from ADF entities without pretending to be a complete geometry
    kernel. The output is useful for pipeline tests, review, and future replacement
    with IfcOpenShell-backed IFC generation.
    """
    openbim = (standard or {}).get("openbim", {}) if standard else {}
    project_name = _safe(openbim.get("project_name") or Path(document.source_file).stem or "AIMS Project")
    project_guid = _safe(openbim.get("project_guid") or "AIMS-PROJECT-GUID")

    lines = [
        "ISO-10303-21;",
        "HEADER;",
        "FILE_DESCRIPTION(('AIMS v0.8.0 OpenBIM foundation export'),'2;1');",
        f"FILE_NAME('{project_name}.ifc','',('AIMS'),('AIMS'),'AIMS','AIMS','');",
        "FILE_SCHEMA(('IFC4'));",
        "ENDSEC;",
        "DATA;",
        f"#1=IFCPROJECT('{project_guid}',$,'{project_name}',$,$,$,$,$);",
    ]

    counts: dict[str, int] = {}
    exportable = 0
    next_index = 10
    for entity in document.entities:
        if entity.bim_class not in EXPORTABLE_IFC_CLASSES:
            continue
        exportable += 1
        counts[entity.bim_class or "IfcProxy"] = counts.get(entity.bim_class or "IfcProxy", 0) + 1
        lines.append(_ifc_line(next_index, entity, project_guid))
        next_index += 1

    lines.extend(["ENDSEC;", "END-ISO-10303-21;"])
    result = IFCExportResult(
        total_entities=len(document.entities),
        exportable_entities=exportable,
        skipped_entities=len(document.entities) - exportable,
        ifc_class_counts=counts,
    )
    return "\n".join(lines) + "\n", result


def write_ifc(document: ADFDocument, output_path: str | Path, standard: dict[str, Any] | None = None) -> IFCExportResult:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text, result = export_ifc_text(document, standard=standard)
    output_path.write_text(text, encoding="utf-8")
    return IFCExportResult(
        total_entities=result.total_entities,
        exportable_entities=result.exportable_entities,
        skipped_entities=result.skipped_entities,
        ifc_class_counts=result.ifc_class_counts,
        output_path=str(output_path),
    )
