# ADR-0001: Use Domain-Driven Design

## Status

Accepted

## Context

AIMS could be designed around file formats such as DXF or around engineering-domain concepts.

## Decision

AIMS will use domain-driven design. File formats are adapters. The engineering domain is the core.

## Consequences

- Parsers remain replaceable.
- ADF remains vendor-neutral.
- Domain logic is not trapped inside import code.
