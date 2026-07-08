from __future__ import annotations

from typing import Any, Dict


def normalize_standard(standard: Dict[str, Any] | None) -> Dict[str, Any]:
    standard = standard or {}
    standard.setdefault("layers", {})
    standard.setdefault("blocks", {})
    standard.setdefault("text_styles", {})
    standard.setdefault("rules", {})
    return standard
