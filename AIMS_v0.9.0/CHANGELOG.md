# Changelog

## v0.9.0 - Automation & CI Foundation

- Added `aims validate` command for project layout validation.
- Added release manifest generation with SHA-256 checksums.
- Added GitHub Actions workflow for tests and smoke audit.
- Added local smoke scripts for Bash and PowerShell.
- Added automation package: `aims_automation`.
- Added tests for healthcheck and release manifest.

## v0.8.0 - IFC/OpenBIM Foundation

Added the first OpenBIM foundation layer for AIMS.

### Added

- `packages/aims_openbim/ifc_export.py`
- `packages/aims_openbim/openbim_validation.py`
- `standards/openbim/openbim.yaml`
- IFC-like STEP text export via `--ifc`
- OpenBIM validation score
- OpenBIM section in Markdown report
- OpenBIM score in HTML report
- OpenBIM payload in JSON report
- Tests for IFC export, OpenBIM validation, and report integration
- `docs/v0.8.0-openbim-foundation.md`

### Notes

This is a foundation exporter, not a full certified IFC authoring engine. It prepares the project for a later IfcOpenShell-backed implementation without poisoning the architecture with premature complexity, a rare mercy in software.

## v0.7.0 - Reporting & Dashboard Foundation

- Markdown, HTML, and JSON report outputs
- Scorecard summary
- Dashboard-oriented report data

## v0.6.0 - Plugin System

- Plugin registry, loader, base classes, and sample architecture plugin

## v0.5.0 - Rule Engine

- YAML-driven rule engine

## v0.4.0 - GIS Readiness

- GeoJSON export and GIS readiness scoring

## v0.3.0 - BIM Readiness

- BIM/IFC mapping and readiness scoring

## v0.2.0 - Architectural QA/QC

- Architectural metrics and QA scoring

## v0.1.0 - Foundation

- DXF to ADF to SQLite to Markdown report pipeline
