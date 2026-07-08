from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from .healthcheck import check_project_health


@dataclass
class ReleaseGate:
    version: str
    root: str
    passed: bool
    score: int
    checks: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def _read_pyproject_version(root: Path) -> str | None:
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return None
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    return data.get("project", {}).get("version")


def run_release_gate(root: str | Path = ".", version: str = "1.0.0") -> ReleaseGate:
    base = Path(root)
    failures: List[str] = []
    warnings: List[str] = []
    checks: List[str] = []

    health = check_project_health(base)
    checks.append(f"project health score: {health.score}/100")
    failures.extend(f"missing required path: {p}" for p in health.missing_paths)
    warnings.extend(health.warnings)

    pyproject_version = _read_pyproject_version(base)
    if pyproject_version == version:
        checks.append(f"pyproject version matches {version}")
    else:
        failures.append(f"pyproject version mismatch: expected {version}, got {pyproject_version}")

    expected_docs = [
        "docs/v1.0.0-release.md",
        "docs/INSTALL.md",
        "docs/USER_GUIDE.md",
        "docs/RELEASE_CHECKLIST.md",
    ]
    for rel in expected_docs:
        if (base / rel).exists():
            checks.append(f"doc present: {rel}")
        else:
            failures.append(f"missing release doc: {rel}")

    workflow = base / ".github" / "workflows" / "ci.yml"
    if workflow.exists():
        checks.append("CI workflow present")
    else:
        failures.append("CI workflow missing")

    score = max(0, 100 - len(failures) * 12 - len(warnings) * 2)
    return ReleaseGate(
        version=version,
        root=str(base),
        passed=not failures,
        score=score,
        checks=checks,
        failures=failures,
        warnings=warnings,
    )
