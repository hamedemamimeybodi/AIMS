from pathlib import Path

from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry
from packages.aims_plugins.loader import run_plugins
from packages.aims_report.markdown_report import write_markdown_report


def test_markdown_report_contains_plugin_section(tmp_path: Path):
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
    plugins = run_plugins(doc, config)
    out = write_markdown_report(doc, tmp_path / "report.md", plugin_summary=plugins)
    text = out.read_text(encoding="utf-8")
    assert "## Plugin System" in text
    assert "architecture.basic" in text
