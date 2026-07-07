from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DXFToken:
    code: str
    value: str
    line_no: int


def tokenize_lines(lines: list[str]) -> list[DXFToken]:
    tokens: list[DXFToken] = []
    index = 0
    while index + 1 < len(lines):
        code = lines[index].strip()
        value = lines[index + 1].rstrip("\n\r")
        tokens.append(DXFToken(code=code, value=value, line_no=index + 1))
        index += 2
    return tokens
