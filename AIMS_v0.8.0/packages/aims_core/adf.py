from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class ADFCategory(str, Enum):
    WALL = "Wall"
    DOOR = "Door"
    WINDOW = "Window"
    COLUMN = "Column"
    ROOM = "Room"
    TEXT = "Text"
    ANNOTATION = "Annotation"
    UNKNOWN = "Unknown"


class ValidationIssue(BaseModel):
    code: str
    severity: str = "warning"
    message: str


class ADFGeometry(BaseModel):
    type: str
    points: List[List[float]] = Field(default_factory=list)
    closed: bool = False
    raw: Dict[str, Any] = Field(default_factory=dict)


class ADFEntity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: str = "DXF"
    handle: Optional[str] = None
    entity_type: str
    layer: str = "0"
    category: ADFCategory = ADFCategory.UNKNOWN
    bim_class: Optional[str] = None
    geometry: Optional[ADFGeometry] = None
    text: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    issues: List[ValidationIssue] = Field(default_factory=list)


class ADFDocument(BaseModel):
    source_file: str
    units: Optional[str] = None
    entities: List[ADFEntity] = Field(default_factory=list)

    def issue_count(self) -> int:
        return sum(len(e.issues) for e in self.entities)

    def by_category(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for entity in self.entities:
            out[entity.category.value] = out.get(entity.category.value, 0) + 1
        return out
