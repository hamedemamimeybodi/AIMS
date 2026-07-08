# Changelog

## v1.0.0 - Professional Release Candidate

### Added

- `release-check` CLI command.
- Release gate validation module.
- v1.0.0 release documentation.
- Install guide.
- User guide.
- Release checklist.
- GitHub Actions CI workflow.
- Stricter healthcheck required paths.
- Version normalized to `1.0.0`.

### Changed

- README updated for v1.0.0.
- Release manifest default version updated to `1.0.0`.
- Smoke validation default version updated to `1.0.0`.

### Notes

This is a professional release candidate, not the final end of the roadmap. Next versions should focus on real DWG ingestion strategy, stronger IFC output through IfcOpenShell, and richer CAD topology repair.

## Previous milestones

- v0.9.0 Automation & CI Foundation
- v0.8.0 IFC/OpenBIM Foundation
- v0.7.0 Reporting & Dashboard Foundation
- v0.6.0 Plugin System
- v0.5.0 YAML Rule Engine
- v0.4.0 GIS Readiness
- v0.3.0 BIM Readiness
- v0.2.0 Architectural QA/QC
- v0.1.0 DXF to ADF/SQLite Foundation

### v1.0.0 build validation

- Tests: `41 passed`
- Project health: `100/100`
- Release gate: `100/100`
- Smoke audit: completed against `examples/simple_site.dxf`
- Fallback DXF parser: available when `ezdxf` is not installed
