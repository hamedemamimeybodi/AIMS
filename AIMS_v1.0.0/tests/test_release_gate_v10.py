from pathlib import Path

from packages.aims_automation.release_check import run_release_gate
from packages.aims_automation.release_manifest import build_release_manifest


def test_release_gate_passes_project_root():
    root = Path(__file__).resolve().parents[1]
    gate = run_release_gate(root, version="1.0.0")
    assert gate.passed is True
    assert gate.score >= 90
    assert any("pyproject version matches" in item for item in gate.checks)


def test_release_manifest_uses_v100():
    root = Path(__file__).resolve().parents[1]
    manifest = build_release_manifest(root, version="1.0.0")
    assert manifest.version == "1.0.0"
    assert manifest.file_count > 20
    assert "pyproject.toml" in manifest.sha256
