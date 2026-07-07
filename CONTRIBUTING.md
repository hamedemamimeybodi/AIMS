# Contributing to AIMS

## Contribution Rules

1. Major features require an RFC.
2. Architecture changes require an ADR.
3. Rule changes require tests.
4. Documentation must change with behavior.
5. Parsers must not contain business validation logic.

## Commit Convention

Use conventional commits:

```text
feat:
fix:
docs:
spec:
test:
refactor:
ci:
build:
```

Examples:

```text
feat(parser): add ASCII DXF LINE support
spec(acs): add ACS-3001 closed polyline
docs(architecture): explain ADF pipeline
```

## Definition of Done

A contribution is not done until:

- Code or documentation is complete.
- Tests are added where applicable.
- CHANGELOG is updated.
- Relevant ADR/RFC/spec is updated.
