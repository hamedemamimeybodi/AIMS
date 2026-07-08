# AIMS v0.5.0 - Rule Engine

AIMS is an Architectural Intelligence Mapping System for CAD/BIM/GIS preflight workflows.

This release extends v0.4.0 with a YAML-driven rule engine. Project standards can now be edited in YAML instead of being buried inside Python code, because apparently future maintainers deserve at least one act of mercy.

## Pipeline

```text
DXF
  -> DXF Parser
  -> ADF Normalizer
  -> Architectural QA/QC
  -> BIM Readiness
  -> GIS Readiness
  -> YAML Rule Engine
  -> SQLite + GeoJSON + Markdown Report
```

## v0.5.0 Features

- YAML-driven rule engine
- Entity selectors by layer, category, entity type and BIM class
- Rule conditions:
  - exists
  - not_empty
  - equals
  - in
  - closed_geometry
  - geometry_type
  - min_area
  - min_length
  - block_name_matches
- Rule severity support
- Rule failure summary in Markdown report
- CLI support for `--rules-standard`
- Default rule pack: `standards/rules/architectural_qaqc.yaml`
- Tests for failing and passing rule scenarios

## Install

```bash
python -m pip install -e .[dev]
```

## Run

```bash
aims audit examples/simple_site.dxf \
  --standard standards/architectural_layers.yaml \
  --bim-standard standards/bim/ifc_mapping.yaml \
  --gis-standard standards/gis/gis_readiness.yaml \
  --rules-standard standards/rules/architectural_qaqc.yaml \
  --sqlite reports/aims_output.sqlite \
  --geojson reports/aims_output.geojson \
  --out reports/aims_report.md
```

## Manual GitHub Push

```bash
git add .
git commit -m "feat: add AIMS v0.5.0 YAML rule engine"
git push origin main
```

## Notes

v0.5.0 is not yet a plugin system. It is the rule layer that prepares AIMS for future plugin packs such as architecture, structure, MEP, municipality, IFC and cadastral validation.
