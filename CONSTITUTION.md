# AIMS Constitution

This document defines the non-negotiable principles of AIMS. Implementation may change. Tools may change. File formats may change. These principles should not change casually.

## Article 0: Never lose engineering knowledge

AIMS must preserve not only geometry, but also meaning, validation history, repair history, rule versions, and decision context.

## Article 1: Engineering data is the asset

Software is temporary. Engineering data is long-lived. AIMS exists to protect the data, not to worship the tool that created it.

## Article 2: Vendor neutrality

AIMS must not be architecturally dependent on AutoCAD, MicroStation, ArcGIS, QGIS, Civil 3D, or any other vendor platform. Those systems are adapters, not the core.

## Article 3: Domain first

The domain model must be centered on engineering concepts such as geometry, parcel, boundary, road, building, annotation, topology, metadata, and validation. File entities such as DXF `LWPOLYLINE` are input representations, not the identity of the system.

## Article 4: ADF is the internal foundation

All parsed data must be normalized into ADF before validation, storage, reporting, or export. Output formats must be derived from ADF, not from raw source files.

## Article 5: ACS defines correctness

The code should not silently invent standards. ACS defines what correct, acceptable, risky, or invalid data means.

## Article 6: ACE executes the standards

ACE is the compliance engine. It executes standards and profiles. It does not replace the standards.

## Article 7: Parsers do not validate business rules

Parsers translate external formats into ADF. They may report structural parse errors, but they must not contain domain-specific compliance logic.

## Article 8: Every validation result must be explainable

AIMS must explain what failed, why it matters, which rule was applied, what impact it has, and how it may be fixed.

## Article 9: Every automatic fix must be reversible

No automatic repair operation is acceptable unless the original state can be reconstructed or audited.

## Article 10: Every major decision must be traceable

Architectural decisions require ADRs. Major feature proposals require RFCs. Rule changes require versioned specifications and tests.

## Article 11: Standards before implementation

When a feature changes the meaning of engineering quality, the relevant specification must be updated before or alongside implementation.

## Article 12: Quality before feature count

A small, reliable, tested foundation is better than a large pile of glamorous bugs wearing a trench coat.
