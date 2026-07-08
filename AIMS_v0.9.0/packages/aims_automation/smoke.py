from __future__ import annotations

from pathlib import Path

from .healthcheck import ProjectHealth, check_project_health
from .release_manifest import ReleaseManifest, write_release_manifest


def run_smoke(root: str | Path = ".", version: str = "0.9.0") -> tuple[ProjectHealth, ReleaseManifest]:
    health = check_project_health(root)
    manifest = write_release_manifest(root, version=version)
    return health, manifest
