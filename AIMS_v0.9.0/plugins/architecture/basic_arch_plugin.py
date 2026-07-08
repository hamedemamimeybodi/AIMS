from __future__ import annotations

from packages.aims_core.adf import ADFCategory, ADFDocument
from packages.aims_geometry.geometry import polygon_area
from packages.aims_plugins.base import PluginContext, PluginIssue, PluginResult


class BasicArchitecturePlugin:
    name = "architecture.basic"
    version = "0.6.0"
    description = "Checks basic architectural ADF consistency for rooms, walls, doors, and windows."

    def run(self, document: ADFDocument, context: PluginContext) -> PluginResult:
        result = PluginResult(plugin_name=self.name, version=self.version)
        min_room_area = float(context.options.get("min_room_area", 1.0))
        door_layers = set(context.options.get("door_layers", ["A-DOOR"]))
        window_layers = set(context.options.get("window_layers", ["A-WINDOW"]))

        for entity in document.entities:
            if entity.category in {ADFCategory.WALL, ADFCategory.DOOR, ADFCategory.WINDOW, ADFCategory.ROOM}:
                result.checked_entities += 1

            if entity.category == ADFCategory.ROOM:
                if not entity.geometry or not entity.geometry.closed:
                    result.issues.append(
                        PluginIssue(
                            code="PLUGIN_ROOM_OPEN_BOUNDARY",
                            severity="error",
                            message="Room boundary must be a closed polyline.",
                            entity_id=entity.id,
                            plugin=self.name,
                        )
                    )
                    continue
                area = polygon_area(entity.geometry.points)
                entity.properties.setdefault("area", area)
                if area < min_room_area:
                    result.issues.append(
                        PluginIssue(
                            code="PLUGIN_ROOM_AREA_TOO_SMALL",
                            severity="warning",
                            message=f"Room area is below plugin minimum ({min_room_area}).",
                            entity_id=entity.id,
                            plugin=self.name,
                        )
                    )

            if entity.category == ADFCategory.DOOR and entity.layer not in door_layers:
                result.issues.append(
                    PluginIssue(
                        code="PLUGIN_DOOR_LAYER_MISMATCH",
                        severity="warning",
                        message="Door entity is not on an approved door layer.",
                        entity_id=entity.id,
                        plugin=self.name,
                    )
                )

            if entity.category == ADFCategory.WINDOW and entity.layer not in window_layers:
                result.issues.append(
                    PluginIssue(
                        code="PLUGIN_WINDOW_LAYER_MISMATCH",
                        severity="warning",
                        message="Window entity is not on an approved window layer.",
                        entity_id=entity.id,
                        plugin=self.name,
                    )
                )

        if result.issues:
            result.status = "warning"
        result.metrics = {
            "checked_entities": result.checked_entities,
            "issue_count": len(result.issues),
            "min_room_area": min_room_area,
        }
        return result
