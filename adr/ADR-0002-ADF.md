# ADR-0002: Use ADF as Internal Foundation

## Status

Accepted

## Context

The system needs a common model for validation, storage, reporting, and export.

## Decision

All external data will be normalized into ADF.

## Consequences

- Validation is consistent.
- Exporters can target one internal model.
- Parser complexity is isolated.
