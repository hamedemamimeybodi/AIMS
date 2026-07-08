from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass
class ReleaseManifest:
    version: str
    root: str
    file_count: int
    total_bytes: int
    sha256: Dict[str, str]


def iter_release_files(root: Path, ignored_parts: Iterable[str] | None = None) -> List[Path]:
    ignored = set(ignored_parts or {".git", ".pytest_cache", "__pycache__", "reports"})
    files: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in ignored for part in p.parts):
            continue
        files.append(p)
    return sorted(files)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_release_manifest(root: str | Path = ".", version: str = "0.9.0") -> ReleaseManifest:
    base = Path(root)
    files = iter_release_files(base)
    checksums = {str(p.relative_to(base)).replace("\\", "/"): sha256_file(p) for p in files}
    total = sum(p.stat().st_size for p in files)
    return ReleaseManifest(version=version, root=str(base), file_count=len(files), total_bytes=total, sha256=checksums)


def write_release_manifest(root: str | Path = ".", out: str | Path = "reports/release_manifest.json", version: str = "0.9.0") -> ReleaseManifest:
    base = Path(root)
    manifest = build_release_manifest(base, version=version)
    out_path = base / out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(asdict(manifest), indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest
