# ARL Rule Language Draft

ARL means **AIMS Rule Language**.

The first implementation may use JSON/YAML. A compact DSL may come later.

## Draft DSL

```text
RULE ACS-3001
TARGET Boundary
WHEN closed == false
THEN ERROR
MESSAGE "Boundary must be closed."
FIX CloseIfGapBelowTolerance
```

## Safety Levels

- automatic
- semi_automatic
- manual
