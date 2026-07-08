# Changelog

## v0.2.0 - Architectural QA/QC

### Added

- `aims_architecture` package
- Architectural metrics engine
- QA score calculator
- Basic room candidate helper
- `aims_rules` package for standard normalization
- Duplicate geometry detection
- Room area and perimeter calculation
- Non-standard block validation
- Door/window block-preference validation
- BIM readiness snapshot in Markdown report
- `standards/architecture/basic_bim_preflight.yaml`

### Changed

- Updated project version to `0.2.0`
- Improved classification support for annotation layers
- Report title changed to Architectural QA/QC Report
- Validation now normalizes missing standard sections safely

### Notes

This release is still a preflight layer, not a full BIM authoring system. It prepares the ground for BIM mapping in v0.3.0.
