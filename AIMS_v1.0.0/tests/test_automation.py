from pathlib import Path

from packages.aims_automation.healthcheck import check_project_health
from packages.aims_automation.release_manifest import build_release_manifest, write_release_manifest


def test_healthcheck_current_project():
    health = check_project_health(Path.cwd())
    assert health.checked_paths >= 10
    assert health.ok
    assert health.score >= 90


def test_release_manifest_builds():
    manifest = build_release_manifest(Path.cwd(), version="0.9.0-test")
    assert manifest.version == "0.9.0-test"
    assert manifest.file_count > 0
    assert "README.md" in manifest.sha256


def test_release_manifest_writes(tmp_path):
    manifest = write_release_manifest(Path.cwd(), out=tmp_path / "manifest.json", version="0.9.0-test")
    assert manifest.file_count > 0
    assert (tmp_path / "manifest.json").exists()
