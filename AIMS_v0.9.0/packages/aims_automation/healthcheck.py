from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List


@dataclass
class ProjectHealth:
    root: str
    checked_paths: int
    missing_paths: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.missing_paths

    @property
    def score(self) -> int:
        if self.checked_paths == 0:
            return 0
        present = self.checked_paths - len(self.missing_paths)
        base = round((present / self.checked_paths) * 100)
        penalty = min(20, len(self.warnings) * 2)
        return max(0, base - penalty)


def default_required_paths() -> List[str]:
    return [
        "aims/cli.py",
        "packages/aims_parser/dxf_parser.py",
        "packages/aims_core/adf.py",
        "packages/aims_geometry/validation.py",
        "packages/aims_database/sqlite_store.py",
        "packages/aims_report/markdown_report.py",
        "packages/aims_bim/readiness.py",
        "packages/aims_gis/geojson_export.py",
        "packages/aims_rules/engine.py",
        "packages/aims_plugins/loader.py",
        "packages/aims_openbim/ifc_export.py",
        "standards/architectural_layers.yaml",
        "standards/bim/ifc_mapping.yaml",
        "standards/gis/gis_readiness.yaml",
        "standards/rules/architectural_qaqc.yaml",
        "standards/plugins/plugin_manifest.yaml",
        "standards/openbim/openbim.yaml",
        "examples/simple_site.dxf",
        "README.md",
        "pyproject.toml",
        "requirements.txt",
    ]


def check_project_health(root: str | Path = ".", required_paths: Iterable[str] | None = None) -> ProjectHealth:
    base = Path(root)
    paths = list(required_paths or default_required_paths())
    missing = [p for p in paths if not (base / p).exists()]
    warnings: List[str] = []

    reports_dir = base / "reports"
    if not reports_dir.exists():
        warnings.append("reports directory is missing; audit output will create it when possible")

    workflow = base / ".github" / "workflows" / "ci.yml"
    if not workflow.exists():
        warnings.append("GitHub Actions workflow is missing")

    return ProjectHealth(root=str(base), checked_paths=len(paths), missing_paths=missing, warnings=warnings)
