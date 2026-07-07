# AIMS Architecture

## Core Pipeline

```text
External Format -> Parser Adapter -> ADF -> ACE -> Storage -> Report / Export
```

## Architecture Layers

```text
Applications
Interfaces
Application Services
Compliance Engine
Ontology Engine
ADF Model
Infrastructure Adapters
```

## Key Rule

No business logic inside parsers.

Parsers only translate external formats into ADF. Validation belongs in ACE. Storage belongs in storage providers. Reports belong in report engines. Humanity survives one responsibility boundary at a time.

## Packages

| Package | Purpose |
|---|---|
| aims-core | Shared primitives and contracts |
| aims-domain | Domain model |
| aims-ontology | Engineering vocabulary and relations |
| aims-parser | Format adapters |
| aims-validator | ACE validation engine |
| aims-storage | Storage providers |
| aims-report | Report generation |
| aims-export | Exporters |
| aims-sdk | Plugin APIs |
