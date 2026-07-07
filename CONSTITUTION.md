# AIMS Constitution

This document defines the non-negotiable principles of AIMS.

## Article 0: Never Lose Engineering Knowledge

AIMS must preserve geometry, meaning, validation history, repair history, rule versions, and decision context.

## Article 1: Engineering Data Is the Asset

Software is temporary. Engineering data is long-lived. AIMS exists to protect the data.

## Article 2: Vendor Neutrality

AIMS must not be architecturally dependent on AutoCAD, MicroStation, ArcGIS, QGIS, Civil 3D, or any other vendor platform.

## Article 3: Domain First

The domain model must be centered on engineering concepts such as geometry, parcel, boundary, road, building, annotation, topology, metadata, and validation.

## Article 4: ADF Is the Internal Foundation

All parsed data must be normalized into ADF before validation, storage, reporting, or export.

## Article 5: ACS Defines Correctness

The code should not silently invent standards. ACS defines what correct, acceptable, risky, or invalid data means.

## Article 6: ACE Executes the Standards

ACE is the compliance engine. It executes standards and profiles. It does not replace the standards.

## Article 7: Parsers Do Not Validate Business Rules

Parsers translate external formats into ADF. They may report structural parse errors, but they must not contain domain-specific compliance logic.

## Article 8: Every Validation Result Must Be Explainable

AIMS must explain what failed, why it matters, which rule was applied, what impact it has, and how it may be fixed.

## Article 9: Every Automatic Fix Must Be Reversible

No automatic repair operation is acceptable unless the original state can be reconstructed or audited.

## Article 10: Every Major Decision Must Be Traceable

Architectural decisions require ADRs. Major feature proposals require RFCs. Rule changes require versioned specifications and tests.
