# AIMS Domain Model

## Primary Concepts

```text
Project
  Drawing
    Layer
      Feature
        Geometry
        Attributes
        Metadata
        Validation
        History
```

## Feature Types

- Boundary
- Parcel
- Road
- Building
- Utility
- Annotation
- Dimension
- ControlPoint

## Rule Levels

- Document Rule
- Layer Rule
- Feature Rule
- Geometry Rule
- Relation Rule

## Relation Examples

```text
Building INSIDE Parcel
Parcel TOUCHES Road
Utility CROSSES Boundary
Annotation LABELS Feature
```
