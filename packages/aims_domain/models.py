from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


ADF_VERSION = "0.1"


@dataclass(slots=True)
class Point3D:
    x: float
    y: float
    z: float = 0.0

    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]


@dataclass(slots=True)
class Geometry:
    type: str
    coordinates: Any
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Feature:
    feature_id: str
    source_entity: str
    layer: str
    geometry: Geometry
    attributes: dict[str, Any] = field(default_factory=dict)
    text: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature_id": self.feature_id,
            "source_entity": self.source_entity,
            "layer": self.layer,
            "geometry": asdict(self.geometry),
            "attributes": self.attributes,
            "text": self.text,
        }


@dataclass(slots=True)
class ADFDocument:
    source_path: str
    features: list[Feature]
    layers: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)
    adf_version: str = ADF_VERSION

    @property
    def source_name(self) -> str:
        return Path(self.source_path).name

    @property
    def feature_count(self) -> int:
        return len(self.features)

    def to_dict(self) -> dict[str, Any]:
        return {
            "document": {
                "adf_version": self.adf_version,
                "source_path": self.source_path,
                "source_name": self.source_name,
                "feature_count": self.feature_count,
            },
            "layers": self.layers,
            "features": [feature.to_dict() for feature in self.features],
            "metadata": self.metadata,
        }
