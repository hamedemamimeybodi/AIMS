from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ADF_VERSION = "0.1"


@dataclass(slots=True)
class ADFEntity:
    entity_id: int
    entity_type: str
    layer: str
    geometry: dict[str, Any]
    text: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ADFDocument:
    source_path: str
    layers: list[str]
    entities: list[ADFEntity]
    version: str = ADF_VERSION

    @property
    def entity_count(self) -> int:
        return len(self.entities)

    def to_dict(self) -> dict[str, Any]:
        return {
            "document": {
                "version": self.version,
                "source_path": self.source_path,
                "source_name": Path(self.source_path).name,
                "entity_count": self.entity_count,
            },
            "layers": self.layers,
            "entities": [entity.to_dict() for entity in self.entities],
        }
