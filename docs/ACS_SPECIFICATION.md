# ACS Specification Draft

ACS means **AIMS CAD Standard**.

ACS defines what valid, risky, or invalid engineering data means.

## Rule Groups

- ACS-1000 File
- ACS-2000 Layers
- ACS-3000 Geometry
- ACS-4000 Text and Annotation
- ACS-5000 Dimensions
- ACS-6000 Blocks
- ACS-7000 Coordinates
- ACS-8000 GIS and Topology
- ACS-9000 Metadata and Delivery

## Rule Example

```json
{
  "id": "ACS-3001",
  "title": "Closed Boundary Polyline",
  "severity": "ERROR",
  "target": "Boundary",
  "condition": "closed == true",
  "message": "Boundary geometry must be closed."
}
```
