# AIMS

Architectural Intelligence Mapping System.

AIMS is a CAD/BIM/GIS preflight toolkit for converting DXF drawings into an ADF intermediate model, validating them, exporting SQLite/GeoJSON, and producing Markdown QA reports.

## Current version

`v0.6.0 - Plugin System`

## Pipeline

```text
DXF -> ADF -> Validation -> BIM Readiness -> GIS Readiness -> Rule Engine -> Plugin System -> SQLite/GeoJSON/Markdown
```

## Install

```bash
pip install -e .
```

## Run

```bash
aims audit examples/simple_site.dxf   --standard standards/architectural_layers.yaml   --bim-standard standards/bim/ifc_mapping.yaml   --gis-standard standards/gis/gis_readiness.yaml   --rules-standard standards/rules/architectural_qaqc.yaml   --plugins-standard standards/plugins/plugin_manifest.yaml   --sqlite reports/aims_output.sqlite   --geojson reports/aims_output.geojson   --out reports/aims_report.md
```

## v0.6.0 additions

- Plugin base protocol and result models
- Plugin registry and YAML loader
- Built-in architecture plugin
- Plugin issues attached back to ADF entities
- Plugin score in Markdown reports

## Tests

```bash
pytest
```
