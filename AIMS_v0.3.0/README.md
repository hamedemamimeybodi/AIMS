# AIMS v0.3.0

**Architectural Intelligence Mapping System** is a local CAD/BIM preflight toolkit. It reads DXF, normalizes entities into **ADF**, validates architectural quality, maps entities to BIM/IFC classes, saves to SQLite, and generates Markdown QA/QC reports.

This release focuses on **BIM Readiness**. It does not claim to magically convert messy CAD into a perfect BIM model, because apparently reality has standards. It prepares the data so a future IFC/Revit/OpenBIM pipeline has something structured to work with.

## What v0.3.0 Adds

- BIM/IFC mapping engine
- IFC class assignment by category, layer, and block name
- BIM readiness score
- Missing Level validation
- Missing Material validation
- Required BIM property checks from YAML
- BIM entity snapshot in Markdown report
- IFC class summary in report
- `--bim-standard` CLI option
- Tests for BIM mapping and readiness scoring

## Project Structure

```text
AIMS/
├── aims/
│   ├── __init__.py
│   └── cli.py
├── packages/
│   ├── aims_architecture/
│   ├── aims_bim/
│   ├── aims_core/
│   ├── aims_database/
│   ├── aims_geometry/
│   ├── aims_parser/
│   ├── aims_report/
│   └── aims_rules/
├── standards/
│   ├── architectural_layers.yaml
│   ├── architecture/basic_bim_preflight.yaml
│   └── bim/ifc_mapping.yaml
├── examples/
├── tests/
├── reports/
├── docs/
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
aims audit examples/simple_site.dxf \
  --standard standards/architectural_layers.yaml \
  --bim-standard standards/bim/ifc_mapping.yaml \
  --sqlite reports/aims_output.sqlite \
  --out reports/aims_report.md
```

Expected outputs:

```text
reports/aims_output.sqlite
reports/aims_report.md
```

## BIM Readiness Scope

v0.3.0 checks:

- Entity mapped to IFC class or not
- Category to IFC mapping
- Layer to IFC mapping
- Block to IFC mapping
- Missing Level
- Missing Material
- Missing required BIM properties
- IFC class counts
- BIM readiness score

## ADF to BIM Flow

```text
DXF Entity
   ↓
ADF Entity
   ↓
Architectural Category
   ↓
IFC Class Mapping
   ↓
BIM Readiness Validation
   ↓
SQLite + Markdown Report
```

Example ADF BIM fields:

```json
{
  "category": "Wall",
  "bim_class": "IfcWall",
  "properties": {
    "level": "Ground Floor",
    "material": "Concrete",
    "ifc_class": "IfcWall"
  }
}
```

## Manual Push

After unzipping inside the repository root:

```bash
git add .
git commit -m "feat: add AIMS v0.3.0 BIM readiness engine"
git push origin main
```

## Roadmap

- v0.4.0: GIS/GeoJSON export and topology report
- v0.5.0: expanded YAML rule engine
- v0.6.0: plugin system
- v1.0.0: professional CAD/BIM QA suite
