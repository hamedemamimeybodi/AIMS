# AIMS

AIMS v0.1 Foundation implements the first practical pipeline:

```text
DXF -> ADF -> SQLite -> Validation Report
```

ADF means **AIMS Data Format**: a small JSON-compatible internal model used between parsing, storage, and validation.

## What v0.1 includes

- Minimal DXF parser for common CAD entities: `LINE`, `LWPOLYLINE`, `TEXT`, and `MTEXT`.
- ADF model with document metadata, layers, and entities.
- SQLite persistence layer.
- Validation report generator in Markdown.
- Command-line interface.
- Pytest tests and GitHub Actions CI.

## Install for development

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Run the pipeline

```bash
aims-pipeline examples/simple_site.dxf --db build/aims.sqlite --report build/validation-report.md
```

Or with Python:

```bash
python -m aims.cli examples/simple_site.dxf --db build/aims.sqlite --report build/validation-report.md
```

## Run tests

```bash
pytest
```

## Repository layout

```text
packages/aims_parser/      DXF parsing
packages/aims_geometry/    ADF data model
packages/aims_database/    SQLite schema and writer
aims/                      CLI orchestration
tests/                     automated tests
examples/                  sample DXF input
```

## v0.1 scope limits

This is a foundation release. It intentionally avoids pretending to be AutoCAD, because apparently one universe of CAD pain is enough.

Supported now:

- ASCII DXF group-code parsing.
- Basic entity extraction.
- SQLite export.
- Structural validation.

Not yet included:

- Full CAD geometry engine.
- Blocks, dimensions, hatches, splines, arcs, coordinate systems.
- GUI.
- Production-grade DXF compatibility.
