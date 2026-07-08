# AIMS - Architectural Intelligence Mapping System

`v0.9.0 - IFC/OpenBIM Foundation`

AIMS is a CAD/BIM/GIS QA/QC toolkit for converting architectural DXF content into ADF, validating it, storing it in SQLite, exporting GeoJSON and IFC-like STEP text, and producing Markdown/HTML/JSON reports.

## Current pipeline

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
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
```

## Run audit

```bash
aims audit examples/simple_site.dxf \
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

## v0.9.0 additions

- OpenBIM validation engine
- IFC GUID fallback assignment
- spatial container / level validation
- required property-set validation from YAML
- deterministic IFC-like STEP export
- OpenBIM score in Markdown, HTML, and JSON reports

## Important limitation

The `.ifc` output in v0.9.0 is an early OpenBIM foundation export. It is intentionally simple and deterministic. Full geometry-rich IFC authoring should be implemented later with an IFC library such as IfcOpenShell. Pretending otherwise would be software theater, and we already have enough of that.

## Test

```bash
pytest
```


## v0.9.0 Automation & CI Foundation

This release adds automation features for manual and GitHub-based quality gates.

### New commands

```bash
python -m aims.cli validate
python -m aims.cli audit examples/simple_site.dxf
```

### CI

A GitHub Actions workflow is included at `.github/workflows/ci.yml`. It runs tests, project validation, and a smoke audit on the example DXF.

### Release manifest

`aims validate` writes `reports/release_manifest.json` with file count, byte count, and SHA-256 checksums.
