# AIMS Roadmap

AIMS is developed as an open, standards-driven engineering data quality platform. The roadmap is intentionally staged so the project grows from a stable foundation instead of collapsing under feature ambition, which is apparently a thing software projects enjoy doing.

## Genesis

Goal: define the project identity, architecture, governance, and core specifications.

Deliverables:

- Vision and mission
- Project charter
- Constitution
- Architecture baseline
- Ontology baseline
- RFC process
- ADR process
- Repository structure

Exit criteria:

- Core documents exist and are versioned.
- Major architectural decisions have ADRs.
- The scope of v0.1 Foundation is explicit.

## v0.1 Foundation

Goal: implement the first working pipeline.

```text
DXF -> ADF -> SQLite -> Validation Report
```

Deliverables:

- ASCII DXF parser
- ADF document model
- SQLite storage
- Basic validation engine
- Markdown validation report
- CLI entry point
- Smoke tests
- GitHub Actions CI

Exit criteria:

- Example DXF can be parsed.
- ADF can be persisted to SQLite.
- Validation report is generated.
- Tests pass in CI.

## v0.2 Rule Engine

Goal: move validation from hard-coded checks to data-driven rules.

Deliverables:

- Rule loader
- JSON/YAML rule schema
- Rule profiles
- ACS rule catalog skeleton
- JSON validation report
- Rule test fixtures

## v0.3 Auto Fix

Goal: introduce controlled, reversible repair operations.

Deliverables:

- Fix engine
- Fix safety levels: automatic, semi-automatic, manual
- Before/after reporting
- Fix audit trail
- Re-validation after fix

## v0.4 Geometry and Topology

Goal: provide deeper engineering-grade geometry checks.

Deliverables:

- Geometry primitives
- Polygon area and perimeter
- Self-intersection detection
- Gap and overlap checks
- Spatial index
- Topology validation rules

## v0.5 GIS Integration

Goal: support common geospatial outputs and workflows.

Deliverables:

- GeoJSON export
- CRS metadata support
- Shapefile and GeoPackage planning
- GIS-oriented validation profiles

## v0.6 Plugin SDK

Goal: make AIMS extensible without modifying the core.

Deliverables:

- Parser plugin interface
- Validator plugin interface
- Exporter plugin interface
- Analyzer plugin interface
- SDK documentation

## v0.7 API

Goal: expose AIMS workflows through a service interface.

Deliverables:

- FastAPI service
- OpenAPI documentation
- Batch validation endpoint
- Report retrieval endpoint

## v0.8 Desktop

Goal: provide a usable visual interface for engineers and reviewers.

Deliverables:

- Desktop shell
- File validation workflow
- Report viewer
- Rule/profile selector

## v0.9 Benchmark and Dashboard

Goal: measure engine accuracy, performance, and quality trends.

Deliverables:

- Benchmark suite
- Regression datasets
- Quality score model
- Dashboard prototype

## v1.0 Stable Platform

Goal: release a stable, documented, extensible CAD/GIS quality platform.

Minimum criteria:

- ADF 1.0 specification
- ACS 1.0 specification
- ACE 1.0 validation engine
- Stable CLI
- Stable plugin interfaces
- Complete documentation
- Repeatable benchmarks
- Regression test coverage
