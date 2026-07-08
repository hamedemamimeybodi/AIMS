# Changelog

## v0.5.0 - Rule Engine

### Added

- `packages/aims_rules/engine.py` rule engine.
- YAML rule standard at `standards/rules/architectural_qaqc.yaml`.
- Rule selectors for layer, category, entity type and BIM class.
- Rule conditions for properties, geometry closure, area, length and block names.
- Rule result scoring model.
- Rule Engine section in Markdown reports.
- CLI `--rules-standard` option.
- Documentation: `docs/v0.5.0-rule-engine.md`.
- Tests for rule failures and passing entities.

### Changed

- Project version updated to `0.5.0`.
- README updated for the rule-engine pipeline.
- Audit pipeline now runs rule checks after BIM/GIS readiness calculations.

### Scope

This release moves AIMS toward configurable standards and prepares the project for future plugin packs.

## v0.4.0 - GIS Ready

### Added

- `packages/aims_gis` package.
- GeoJSON export from ADF entities.
- GIS readiness scoring model.
- Basic topology analyzer.
- GIS readiness YAML standard.
- GIS section in Markdown report.
- CLI `--geojson` option.
- CLI `--gis-standard` option.
- Tests for GeoJSON, topology, GIS readiness and Markdown GIS reporting.
