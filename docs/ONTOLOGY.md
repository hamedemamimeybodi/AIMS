# AIMS Ontology

The AIMS ontology defines shared engineering meaning. It prevents AIMS from becoming just another file parser with delusions of grandeur.

## Core Ontology Entities

- Project
- Drawing
- Feature
- Geometry
- Boundary
- Parcel
- Road
- Building
- Utility
- Annotation
- ControlPoint
- TopologyRelation
- ValidationIssue

## Example

```yaml
entity: Parcel
inherits: Boundary
required:
  - parcel_id
  - geometry
optional:
  - owner
  - area
  - description
relations:
  - touches Road
  - contains Building
  - adjacent Parcel
```

## Rule

Ontology describes meaning. ADF stores meaning. ACE validates meaning.
