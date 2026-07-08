# Changelog

## v0.3.0 - BIM Readiness Engine

### Added

- `packages/aims_bim` package.
- BIM/IFC class mapping engine.
- BIM readiness scoring.
- Missing Level checks.
- Missing Material checks.
- Required BIM property validation from YAML.
- `standards/bim/ifc_mapping.yaml`.
- BIM readiness and IFC class sections in Markdown report.
- `--bim-standard` CLI option.
- BIM mapping and readiness tests.

### Changed

- Markdown report title updated to Architectural BIM QA/QC Report.
- CLI now prints BIM mapped count and BIM readiness score.
- Project version updated to `0.3.0`.

## v0.2.0 - Architectural QA/QC

- Architectural metrics engine.
- Quality score calculation.
- Layer, block, geometry, and category validation.
- Duplicate geometry detection.
- Room area/perimeter calculation.

## v0.1.0 - Foundation

- DXF parser.
- ADF core models.
- SQLite writer.
- Basic validator.
- Markdown report.
