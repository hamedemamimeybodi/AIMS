# AIMS Architectural BIM QA/QC Report

**Source file:** `examples/simple_site.dxf`
**Units:** `fallback`
**Total entities:** 5
**Total issues:** 28
**Architectural quality score:** **47/100**
**BIM readiness score:** **31/100**
**GIS readiness score:** **73/100**
**Rule engine score:** **100/100**
**Plugin score:** **100/100**
**OpenBIM readiness score:** **0/100**

## Category Summary

| Name | Count |
|---|---:|
| Door | 1 |
| Room | 1 |
| Text | 1 |
| Unknown | 1 |
| Wall | 1 |

## Layer Summary

| Name | Count |
|---|---:|
| A-DOOR | 1 |
| A-ROOM | 1 |
| A-TEXT | 1 |
| A-WALL | 1 |
| BAD-LAYER | 1 |

## Block Summary

| Name | Count |
|---|---:|
| DOOR_900 | 1 |

## Issue Severity Summary

| Name | Count |
|---|---:|
| error | 1 |
| info | 6 |
| warning | 21 |

## Issue Code Summary

| Name | Count |
|---|---:|
| BIM_MISSING_LEVEL | 3 |
| BIM_MISSING_MATERIAL | 2 |
| BIM_MISSING_REQUIRED_PROPERTY | 3 |
| BIM_UNMAPPED_ENTITY | 1 |
| GIS_BBOX_OVERLAP | 2 |
| NON_STANDARD_BLOCK | 1 |
| OPENBIM_GUID_ASSIGNED | 4 |
| OPENBIM_MISSING_PSET_PROPERTY | 5 |
| OPENBIM_MISSING_SPATIAL_CONTAINER | 4 |
| UNKNOWN_CATEGORY | 1 |
| UNKNOWN_LAYER | 1 |
| ZERO_LENGTH | 1 |

## BIM Readiness

**BIM readiness score:** **31/100**

| Metric | Value |
|---|---:|
| Total entities | 5 |
| BIM-relevant entities | 3 |
| Mapped entities | 4 |
| Missing level | 3 |
| Missing material | 2 |
| Missing required properties | 5 |

## IFC Class Summary

| Name | Count |
|---|---:|
| IfcAnnotation | 1 |
| IfcDoor | 1 |
| IfcSpace | 1 |
| IfcWall | 1 |

## GIS Readiness

**GIS readiness score:** **73/100**

| Metric | Value |
|---|---:|
| Total entities | 5 |
| Geospatial entities | 4 |
| Exportable GeoJSON features | 4 |
| Missing geometry | 0 |
| Unknown category | 1 |
| Missing level/floor | 0 |
| Polygon candidates | 2 |
| Open boundaries | 0 |
| Zero-area polygons | 0 |
| Duplicate geometries | 0 |
| Bounding-box overlap pairs | 1 |

## GIS Geometry Type Summary

| Name | Count |
|---|---:|
| block_insert | 1 |
| line | 1 |
| point | 1 |
| polyline | 2 |

## Rule Engine

**Rule engine score:** **100/100**

| Metric | Value |
|---|---:|
| Total rules | 7 |
| Evaluated entities | 5 |
| Passed checks | 10 |
| Failed checks | 0 |
| Skipped checks | 25 |

## Rule Failure Summary

| Name | Count |
|---|---:|
| _none_ | 0 |

## Plugin System

**Plugin score:** **100/100**

| Metric | Value |
|---|---:|
| Enabled plugins | 1 |
| Executed plugins | 1 |
| Failed plugins | 0 |
| Plugin issues | 0 |

| Plugin | Version | Status | Checked Entities | Issues |
|---|---|---|---:|---:|
| architecture.basic | 0.6.0 | passed | 3 | 0 |

## OpenBIM / IFC Foundation

**OpenBIM readiness score:** **0/100**

| Metric | Value |
|---|---:|
| Total entities | 5 |
| OpenBIM entities | 4 |
| Missing IFC GUID | 4 |
| Missing spatial container | 4 |
| Missing PSet properties | 5 |
| Unsupported IFC classes | 0 |

## OpenBIM IFC Class Summary

| Name | Count |
|---|---:|
| IfcAnnotation | 1 |
| IfcDoor | 1 |
| IfcSpace | 1 |
| IfcWall | 1 |

## BIM Entity Snapshot

| Entity ID | Category | IFC Class | Level | Material |
|---|---|---|---|---|
| `00cf6974-e66d-4bad-92df-f7911731ffca` | Wall | IfcWall | UNASSIGNED |  |
| `f04eeb44-ef01-44d7-a2fc-d3ab1e70f54a` | Room | IfcSpace | UNASSIGNED |  |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | Door | IfcDoor | UNASSIGNED |  |
| `0d4ca13a-154e-4a7a-a82d-a7e52394ce15` | Text | IfcAnnotation | UNASSIGNED |  |

## Entity Issues

| Entity ID | Type | Layer | Category | BIM Class | Severity | Code | Message |
|---|---|---|---|---|---|---|---|
| `00cf6974-e66d-4bad-92df-f7911731ffca` | LWPOLYLINE | A-WALL | Wall | IfcWall | warning | BIM_MISSING_LEVEL | BIM element has no assigned level. |
| `00cf6974-e66d-4bad-92df-f7911731ffca` | LWPOLYLINE | A-WALL | Wall | IfcWall | info | BIM_MISSING_MATERIAL | BIM element has no assigned material. |
| `00cf6974-e66d-4bad-92df-f7911731ffca` | LWPOLYLINE | A-WALL | Wall | IfcWall | warning | BIM_MISSING_REQUIRED_PROPERTY | Missing required BIM property: level |
| `00cf6974-e66d-4bad-92df-f7911731ffca` | LWPOLYLINE | A-WALL | Wall | IfcWall | warning | GIS_BBOX_OVERLAP | Polygon bounding box overlaps another polygon. Review exact topology in GIS. |
| `00cf6974-e66d-4bad-92df-f7911731ffca` | LWPOLYLINE | A-WALL | Wall | IfcWall | info | OPENBIM_GUID_ASSIGNED | IFC GUID was missing; ADF entity id was used as fallback. |
| `00cf6974-e66d-4bad-92df-f7911731ffca` | LWPOLYLINE | A-WALL | Wall | IfcWall | warning | OPENBIM_MISSING_SPATIAL_CONTAINER | OpenBIM entity has no spatial container or level assignment. |
| `00cf6974-e66d-4bad-92df-f7911731ffca` | LWPOLYLINE | A-WALL | Wall | IfcWall | warning | OPENBIM_MISSING_PSET_PROPERTY | Missing OpenBIM property set value: level |
| `00cf6974-e66d-4bad-92df-f7911731ffca` | LWPOLYLINE | A-WALL | Wall | IfcWall | warning | OPENBIM_MISSING_PSET_PROPERTY | Missing OpenBIM property set value: material |
| `f04eeb44-ef01-44d7-a2fc-d3ab1e70f54a` | LWPOLYLINE | A-ROOM | Room | IfcSpace | warning | BIM_MISSING_LEVEL | BIM element has no assigned level. |
| `f04eeb44-ef01-44d7-a2fc-d3ab1e70f54a` | LWPOLYLINE | A-ROOM | Room | IfcSpace | warning | BIM_MISSING_REQUIRED_PROPERTY | Missing required BIM property: level |
| `f04eeb44-ef01-44d7-a2fc-d3ab1e70f54a` | LWPOLYLINE | A-ROOM | Room | IfcSpace | warning | GIS_BBOX_OVERLAP | Polygon bounding box overlaps another polygon. Review exact topology in GIS. |
| `f04eeb44-ef01-44d7-a2fc-d3ab1e70f54a` | LWPOLYLINE | A-ROOM | Room | IfcSpace | info | OPENBIM_GUID_ASSIGNED | IFC GUID was missing; ADF entity id was used as fallback. |
| `f04eeb44-ef01-44d7-a2fc-d3ab1e70f54a` | LWPOLYLINE | A-ROOM | Room | IfcSpace | warning | OPENBIM_MISSING_SPATIAL_CONTAINER | OpenBIM entity has no spatial container or level assignment. |
| `f04eeb44-ef01-44d7-a2fc-d3ab1e70f54a` | LWPOLYLINE | A-ROOM | Room | IfcSpace | warning | OPENBIM_MISSING_PSET_PROPERTY | Missing OpenBIM property set value: level |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | INSERT | A-DOOR | Door | IfcDoor | warning | NON_STANDARD_BLOCK | Block 'DOOR_900' is not defined in the active standard. |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | INSERT | A-DOOR | Door | IfcDoor | warning | BIM_MISSING_LEVEL | BIM element has no assigned level. |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | INSERT | A-DOOR | Door | IfcDoor | info | BIM_MISSING_MATERIAL | BIM element has no assigned material. |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | INSERT | A-DOOR | Door | IfcDoor | warning | BIM_MISSING_REQUIRED_PROPERTY | Missing required BIM property: level |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | INSERT | A-DOOR | Door | IfcDoor | info | OPENBIM_GUID_ASSIGNED | IFC GUID was missing; ADF entity id was used as fallback. |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | INSERT | A-DOOR | Door | IfcDoor | warning | OPENBIM_MISSING_SPATIAL_CONTAINER | OpenBIM entity has no spatial container or level assignment. |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | INSERT | A-DOOR | Door | IfcDoor | warning | OPENBIM_MISSING_PSET_PROPERTY | Missing OpenBIM property set value: level |
| `473b6ea9-f366-4168-b3ad-69726c38f64f` | INSERT | A-DOOR | Door | IfcDoor | warning | OPENBIM_MISSING_PSET_PROPERTY | Missing OpenBIM property set value: material |
| `0d4ca13a-154e-4a7a-a82d-a7e52394ce15` | TEXT | A-TEXT | Text | IfcAnnotation | info | OPENBIM_GUID_ASSIGNED | IFC GUID was missing; ADF entity id was used as fallback. |
| `0d4ca13a-154e-4a7a-a82d-a7e52394ce15` | TEXT | A-TEXT | Text | IfcAnnotation | warning | OPENBIM_MISSING_SPATIAL_CONTAINER | OpenBIM entity has no spatial container or level assignment. |
| `e603cd90-2fd6-48d9-818e-20b6cf6bdabe` | LINE | BAD-LAYER | Unknown |  | warning | UNKNOWN_LAYER | Layer 'BAD-LAYER' is not defined in the active standard. |
| `e603cd90-2fd6-48d9-818e-20b6cf6bdabe` | LINE | BAD-LAYER | Unknown |  | warning | UNKNOWN_CATEGORY | Entity could not be classified into an architectural/BIM category. |
| `e603cd90-2fd6-48d9-818e-20b6cf6bdabe` | LINE | BAD-LAYER | Unknown |  | error | ZERO_LENGTH | Geometry length is zero or almost zero. |
| `e603cd90-2fd6-48d9-818e-20b6cf6bdabe` | LINE | BAD-LAYER | Unknown |  | warning | BIM_UNMAPPED_ENTITY | Entity could not be mapped to a BIM/IFC class. |
