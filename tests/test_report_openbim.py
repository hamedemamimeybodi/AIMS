import json
from pathlib import Path

from packages.aims_core.adf import ADFDocument, ADFEntity, ADFCategory
from packages.aims_openbim.openbim_validation import validate_openbim
from packages.aims_report.json_report import write_json_report
from packages.aims_report.markdown_report import write_markdown_report


def test_reports_include_openbim_section(tmp_path: Path):
    doc = ADFDocument(
        source_file="sample.dxf",
        entities=[
            ADFEntity(entity_type="INSERT", layer="A-DOOR", category=ADFCategory.DOOR, bim_class="IfcDoor", properties={"level": "L1"})
        ],
    )
    openbim = validate_openbim(doc, standard={"openbim": {"required_pset_properties": {"IfcDoor": ["level"]}}})
    md = tmp_path / "report.md"
    js = tmp_path / "report.json"
    write_markdown_report(doc, md, openbim_validation=openbim)
    write_json_report(doc, js, openbim_validation=openbim)
    assert "OpenBIM / IFC Foundation" in md.read_text(encoding="utf-8")
    payload = json.loads(js.read_text(encoding="utf-8"))
    assert "openbim" in payload
    assert payload["scorecard"]["openbim_readiness"] == openbim.score
