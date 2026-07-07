# AIMS Roadmap

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

## v0.2 Rule Engine

- Rule loader
- JSON/YAML rule schema
- Rule profiles
- ACS rule catalog skeleton
- JSON validation report
- Rule test fixtures

## v0.3 Auto Fix

- Fix engine
- Fix safety levels
- Before/after reporting
- Fix audit trail
- Re-validation after fix

## v0.4 Geometry and Topology

- Geometry primitives
- Polygon area and perimeter
- Self-intersection detection
- Gap and overlap checks
- Spatial index
- Topology validation rules

## v0.5 GIS Integration

- GeoJSON export
- CRS metadata support
- Shapefile and GeoPackage planning
- GIS-oriented validation profiles

## v0.6 Plugin SDK

- Parser plugin interface
- Validator plugin interface
- Exporter plugin interface
- Analyzer plugin interface

## v0.7 API

- FastAPI service
- OpenAPI documentation
- Batch validation endpoint
- Report retrieval endpoint

## v0.8 Desktop

- Desktop shell
- File validation workflow
- Report viewer
- Rule/profile selector

## v0.9 Benchmark and Dashboard

- Benchmark suite
- Regression datasets
- Quality score model
- Dashboard prototype

## v1.0 Stable Platform

- ADF 1.0 specification
- ACS 1.0 specification
- ACE 1.0 validation engine
- Stable CLI
- Stable plugin interfaces
- Complete documentation
- Repeatable benchmarks
- Regression test coverage
