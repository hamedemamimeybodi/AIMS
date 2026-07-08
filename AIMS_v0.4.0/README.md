# AIMS v0.4.0 - GIS Ready

AIMS is an Architectural Intelligence Mapping System for CAD/BIM/GIS preflight workflows.

This release extends the v0.3.0 BIM readiness package with GIS readiness checks, topology warnings and GeoJSON export.

## Pipeline

```text
DXF
  -> DXF Parser
  -> ADF Normalizer
  -> Architectural QA/QC
  -> BIM Readiness
  -> GIS Readiness
  -> SQLite + GeoJSON + Markdown Report
```

## v0.4.0 Features

- GIS readiness scoring
- GeoJSON FeatureCollection export
- Topology preflight checks:
  - open boundaries
  - duplicate geometry
  - zero-area polygons
  - bounding-box overlap warning
- GIS section in Markdown reports
- CLI support for `--geojson` and `--gis-standard`
- Tests for GIS export, topology, readiness and report integration

## Install

```bash
python -m pip install -e .[dev]
```

## Run

```bash
aims audit examples/simple_site.dxf   --standard standards/architectural_layers.yaml   --bim-standard standards/bim/ifc_mapping.yaml   --gis-standard standards/gis/gis_readiness.yaml   --sqlite reports/aims_output.sqlite   --geojson reports/aims_output.geojson   --out reports/aims_report.md
```

## Manual GitHub Push

```bash
git add .
git commit -m "feat: add AIMS v0.4.0 GIS readiness and GeoJSON export"
git push origin main
```

## Notes

v0.4.0 is still a preflight package, not a full GIS topology engine. Exact polygon overlay validation will come later with a dedicated geometry backend. Because apparently CAD drawings are not chaotic enough unless GIS gets invited too.
