# AIMS User Guide

## Run a full audit

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

## Main outputs

| Output | Purpose |
|---|---|
| SQLite | structured ADF storage |
| GeoJSON | GIS preview/export |
| IFC | early IFC-like OpenBIM handoff |
| Markdown | readable QA/QC report |
| HTML | dashboard-style report |
| JSON | machine-readable report |

## Standards

Most validation behavior is controlled by YAML files under `standards/`. This is intentional. Standards should not be hardcoded unless suffering is the goal.
