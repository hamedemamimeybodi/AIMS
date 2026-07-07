# AIMS

**Open Standards for Engineering Data Quality**

AIMS is an open, vendor-neutral engineering data quality platform for CAD, GIS, surveying, and digital infrastructure workflows.

AIMS does not exist to replace CAD or GIS software. It exists to make engineering data trustworthy, understandable, repairable, and durable across generations of software.

## Initial Genesis Scope

This repository starts with the **AIMS Genesis v0.0.0** baseline:

- Vision
- Mission
- Philosophy
- Constitution
- Project Charter
- Roadmap
- Architecture baseline
- Ontology baseline
- ADF / ACS / ACE specification drafts
- RFC and ADR process
- Repository structure
- CI and contribution templates
- Package skeletons
- Example and benchmark skeletons

## First Working Pipeline

```text
DXF -> ADF -> SQLite -> Validation Report
```

## Core Pillars

| Pillar | Meaning |
|---|---|
| Ontology | Shared engineering vocabulary |
| ADF | AIMS Digital Foundation, internal data model |
| ACS | AIMS CAD Standard, open rule catalog |
| ACE | AIMS Compliance Engine |
| SDK | Extension model for parsers, validators, exporters, and analyzers |

## Repository Layout

```text
apps/                 User-facing apps: CLI, API, desktop, web
packages/             Core Python packages
docs/                 Project documentation
specs/                Formal machine-readable and human-readable specs
rfcs/                 Request for Comments process
adr/                  Architecture Decision Records
examples/             Example input/output projects
testdata/             Good, bad, edge-case, and regression datasets
benchmarks/           Benchmark plans and datasets
.github/              GitHub templates and CI
```

## Development Status

This is a Genesis baseline. It intentionally favors architecture, traceability, and standards before feature expansion. Because apparently building the right thing first is still considered a bold move.
