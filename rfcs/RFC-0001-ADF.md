# RFC-0001: ADF Baseline

## Status

Draft

## Summary

Define ADF as the internal, vendor-neutral data foundation for AIMS.

## Motivation

AIMS needs a stable model that is not tied to DXF, DWG, SHP, IFC, or any other source format.

## Proposed Design

All parsed input is normalized into ADF before validation, storage, report generation, or export.

## Compatibility

ADF will be versioned. Breaking changes require migration notes.
