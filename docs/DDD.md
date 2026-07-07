# Domain-Driven Design for AIMS

## Decision

AIMS is designed around engineering-domain concepts rather than file-format entities.

## Why

DXF, DWG, DGN, SHP, GPKG, IFC, and LandXML are input or output formats. They are not the identity of the project.

## Bounded Contexts

- Geometry
- Topology
- CAD Parsing
- GIS Export
- Validation
- Reporting
- Storage
- Rules and Profiles

## Anti-Corruption Layer

Parser adapters act as anti-corruption layers between vendor-specific formats and the ADF domain model.
