# AIMS - Architectural Intelligence Mapping System

`v1.0.0 - Professional Release Candidate`

AIMS is a CAD/BIM/GIS QA/QC toolkit for converting architectural DXF content into ADF, validating it, storing it in SQLite, exporting GeoJSON and IFC-like STEP text, and producing Markdown/HTML/JSON reports.

## Pipeline

```text
DXF
  ↓
DXF Parser
  ↓
ADF Normalizer
  ↓
Classification
  ↓
Geometry / Architecture / BIM / GIS / Rule / Plugin Validation
  ↓
OpenBIM Validation
  ↓
SQLite + GeoJSON + IFC + Markdown + HTML + JSON
  ↓
Release Health / CI / Manifest
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
```

## Run audit

```bash
python -m aims.cli audit examples/simple_site.dxf \
  --standard standards/architectural_layers.yaml \
  --bim-standard standards/bim/ifc_mapping.yaml \
  --gis-standard standards/gis/gis_readiness.yaml \
  --rules-standard standards/rules/architectural_qaqc.yaml \
  --plugins-standard standards/plugins/plugin_manifest.yaml \
  --openbim-standard standards/openbim/openbim.yaml \
  --sqlite reports/aims_output.sqlite \
  --geojson reports/aims_output.geojson \
  --ifc reports/aims_output.ifc \
  --out reports/aims_report.md \
  --html reports/aims_report.html \
  --json-report reports/aims_report.json
```

## Validate release

```bash
python -m aims.cli validate --version 1.0.0
python -m aims.cli release-check --version 1.0.0
pytest
```

## v1.0.0 additions

- release gate command
- stricter project health validation
- release checklist and installation guide
- GitHub Actions CI workflow
- release candidate documentation
- version normalization across CLI, package, and pyproject
- package cleaned from transient cache files
- lightweight DXF fallback parser for demo/smoke use when `ezdxf` is unavailable
- sample expected outputs under `samples/expected_outputs/`

## Important limitation

The `.ifc` output is an early OpenBIM foundation export. It is deterministic and useful for pipeline tests, but not a full geometry-rich IFC authoring engine. For production IFC authoring, integrate IfcOpenShell later. Pretending a tiny exporter is a full BIM engine would be software theater, and this project is already ambitious enough.
