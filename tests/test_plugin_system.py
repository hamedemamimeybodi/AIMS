from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry
from packages.aims_plugins.loader import load_plugins_from_config, run_plugins


def test_plugin_registry_loads_from_manifest():
    config = {
        "plugins": [
            {
                "name": "architecture.basic",
                "path": "plugins.architecture.basic_arch_plugin.BasicArchitecturePlugin",
                "enabled": True,
            }
        ]
    }
    registry = load_plugins_from_config(config)
    assert registry.list() == ["architecture.basic"]


def test_basic_architecture_plugin_flags_open_room():
    doc = ADFDocument(
        source_file="unit-test.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-ROOM",
                category=ADFCategory.ROOM,
                geometry=ADFGeometry(type="polyline", points=[[0, 0], [2, 0], [2, 2]], closed=False),
            )
        ],
    )
    config = {
        "plugins": [
            {
                "name": "architecture.basic",
                "path": "plugins.architecture.basic_arch_plugin.BasicArchitecturePlugin",
                "enabled": True,
            }
        ]
    }
    summary = run_plugins(doc, config)
    assert summary.executed_plugins == 1
    assert summary.total_issues == 1
    assert doc.entities[0].issues[0].code == "PLUGIN_ROOM_OPEN_BOUNDARY"


def test_basic_architecture_plugin_computes_room_area():
    doc = ADFDocument(
        source_file="unit-test.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-ROOM",
                category=ADFCategory.ROOM,
                geometry=ADFGeometry(type="polyline", points=[[0, 0], [2, 0], [2, 2], [0, 2]], closed=True),
            )
        ],
    )
    config = {
        "plugins": [
            {
                "name": "architecture.basic",
                "path": "plugins.architecture.basic_arch_plugin.BasicArchitecturePlugin",
                "enabled": True,
                "min_room_area": 1.0,
            }
        ]
    }
    summary = run_plugins(doc, config)
    assert summary.total_issues == 0
    assert doc.entities[0].properties["area"] == 4.0
