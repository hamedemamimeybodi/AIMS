# Release Checklist

Before tagging or pushing a release, run:

```bash
python -m aims.cli validate --version 1.0.0
python -m aims.cli release-check --version 1.0.0
pytest
```

## Manual checks

- [ ] README version is correct
- [ ] pyproject version is correct
- [ ] CI workflow exists
- [ ] docs are present
- [ ] example DXF exists
- [ ] reports directory exists
- [ ] tests pass
- [ ] release manifest generated
- [ ] package zip created

## Suggested Git commands

```bash
git add .
git commit -m "release: prepare AIMS v1.0.0 professional release candidate"
git tag v1.0.0
git push origin main --tags
```
