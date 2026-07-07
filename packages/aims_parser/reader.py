from __future__ import annotations

from pathlib import Path

from .tokenizer import DXFToken, tokenize_lines


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def read_lines(path: str | Path) -> list[str]:
    return read_text(path).splitlines()


def read_tokens(path: str | Path) -> list[DXFToken]:
    return tokenize_lines(read_lines(path))
