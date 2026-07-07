# AIMS Foundation v0.1.0 - 30 Day Implementation Pack

This pack converts the 30-day AIMS Foundation plan into an executable repository patch.

## Target Pipeline

```text
DXF -> ADF -> ACE -> SQLite -> Markdown/JSON Report
```

## Included Sprints

| Sprint | Area | Included |
|---|---|---|
| F1 | DXF Parser | Tokenizer, reader, parser |
| F2 | ACE | Rule engine skeleton |
| F3 | SQLite | Storage schema and writer |
| F4 | Reports | Markdown and JSON reports |
| F5 | Geometry | Basic geometry helpers |
| F6 | Topology | Basic topology placeholder |
| F7 | Auto Fix | Fix plan skeleton |
| F8 | Plugin SDK | Plugin contracts |
| F9 | Benchmark | Benchmark runner skeleton |
| F10 | Release | Release checklist and CLI smoke test |

## First Command

```powershell
python -m apps.cli.main validate examples/simple_site.dxf --db build/aims.sqlite --report build/report.md --json build/report.json
```

## Suggested Commit

```powershell
git add .
git commit -m "feat(foundation): implement AIMS v0.1 executable pipeline"
git push
```
