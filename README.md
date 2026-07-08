# AIMS v0.2.0

**Architectural Intelligence Mapping System** is a local CAD/BIM preflight toolkit for converting DXF drawings into an intermediate **ADF** model, saving results to SQLite, validating architectural quality, and generating Markdown QA/QC reports.

This release focuses on **Architectural QA/QC**. It is intentionally small and practical: DXF in, ADF normalized entities, SQLite storage, validation warnings, and a readable report. No mystical BIM promises, because those usually end with a meeting and no model.

## What v0.2.0 Adds

- Architectural metrics engine
- Quality score calculation
- Layer, block, geometry, and category validation
- Duplicate geometry detection
- Room area/perimeter calculation for closed room polylines
- Door/window block-preference warning
- Richer Markdown report with BIM readiness snapshot
- Basic BIM preflight YAML standard

## Project Structure

```text
AIMS/
├── aims/
│   ├── __init__.py
│   └── cli.py
├── packages/
│   ├── aims_architecture/
│   ├── aims_core/
│   ├── aims_database/
│   ├── aims_geometry/
│   ├── aims_parser/
│   ├── aims_report/
│   └── aims_rules/
├── standards/
│   ├── architectural_layers.yaml
│   └── architecture/basic_bim_preflight.yaml
├── examples/
├── tests/
├── reports/
├── CHANGELOG.md
├── README.md
├── requirements.txt
└── pyproject.toml
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Run Audit

```bash
aims audit examples/simple_site.dxf --standard standards/architectural_layers.yaml --sqlite reports/aims_output.sqlite --out reports/aims_report.md
```

Expected outputs:

```text
reports/aims_output.sqlite
reports/aims_report.md
```

## Validation Scope

v0.2.0 checks:

- Unknown layers
- Unknown architectural categories
- Non-standard block names
- Duplicate geometry signatures
- Zero-length lines
- Invalid polylines
- Open wall/room boundaries
- Small room boundaries
- Door/window entities that should preferably be standard blocks

## ADF Concept

ADF is the neutral internal format. Parsers should produce ADF; validators, reports, SQLite, BIM mapping, and future exporters should consume ADF.

```text
DXF/DWG/IFC/DGN/etc.
        ↓
      Parser
        ↓
       ADF
   ┌────┼────┬──────┬──────┐
 SQLite QA/QC Report BIM GIS
```

## Manual Push

After unzipping inside the repository root:

```bash
git add .
git commit -m "feat: add AIMS v0.2.0 architectural QA QC"
git push origin main
```

## Roadmap

- v0.3.0: BIM mapping engine and IFC-class readiness rules
- v0.4.0: GIS/GeoJSON/GeoPackage export
- v0.5.0: YAML rule engine expansion
- v1.0.0: Professional CAD/BIM QA suite
