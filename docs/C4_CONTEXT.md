# C4 Context

```mermaid
flowchart TD
    User[Engineer / Reviewer] --> AIMS[AIMS Platform]
    CAD[CAD Systems] --> AIMS
    GIS[GIS Systems] --> AIMS
    AIMS --> Reports[Validation Reports]
    AIMS --> Storage[(SQLite / Future Stores)]
    AIMS --> Exports[GeoJSON / Future Outputs]
```
