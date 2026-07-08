# AIMS

Architectural Intelligence Mapping System.

AIMS is a CAD/BIM/GIS preflight toolkit for converting DXF drawings into an ADF intermediate model, validating them, exporting SQLite/GeoJSON, and producing Markdown, HTML, and JSON QA reports.

## Current version

`v0.7.0 - Reporting & Dashboard Foundation`

## Pipeline

```text
DXF -> ADF -> Validation -> BIM Readiness -> GIS Readiness -> Rule Engine -> Plugin System -> SQLite/GeoJSON/Markdown/HTML/JSON
```

## Install

```bash
pip install -e .
```

## Run

```bash
aims audit examples/simple_site.dxf \
  --standard standards/architectural_layers.yaml \
  --bim-standard standards/bim/ifc_mapping.yaml \
  --gis-standard standards/gis/gis_readiness.yaml \
  --rules-standard standards/rules/architectural_qaqc.yaml \
  --plugins-standard standards/plugins/plugin_manifest.yaml \
  --sqlite reports/aims_output.sqlite \
  --geojson reports/aims_output.geojson \
  --out reports/aims_report.md \
  --html reports/aims_report.html \
  --json-report reports/aims_report.json
```

## v0.7.0 additions

- Central report summary model
- Overall scorecard
- Machine-readable JSON QA report
- HTML QA report for review and print workflows
- CLI support for `--html` and `--json-report`
- Report tests for summary, JSON, and HTML output
- Documentation for the reporting/dashboard foundation

## Tests

```bash
pytest
```
