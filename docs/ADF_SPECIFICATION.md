# ADF Specification Draft

ADF means **AIMS Digital Foundation**.

ADF is the internal model used between parsing, validation, storage, reporting, and export.

## Minimum Document Shape

```json
{
  "document": {
    "adf_version": "0.1",
    "source": "sample.dxf"
  },
  "layers": [],
  "features": [],
  "metadata": {},
  "validation": []
}
```

## Design Goals

- Vendor-neutral
- Versioned
- JSON-compatible
- Geometry-aware
- Rule-compatible
- Storage-friendly

## Non-goals

- Replacing full CAD file formats
- Preserving every vendor-specific rendering detail in v0.1
