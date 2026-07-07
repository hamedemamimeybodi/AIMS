# AIMS Foundation v0.1.0 Release Notes

## Added

- Executable DXF to ADF parser.
- ADF dataclass model.
- ACE validation engine skeleton.
- SQLite storage provider.
- Markdown and JSON reports.
- CLI validate command.
- Geometry helper functions.
- Topology and fixer skeletons.
- Plugin SDK contracts.
- Tests and CI workflow.

## Smoke Test

```powershell
python -m apps.cli.main validate examples/simple_site.dxf --db build/aims.sqlite --report build/report.md --json build/report.json
```
