from __future__ import annotations

from typing import Protocol

from packages.aims_domain import ADFDocument


class ParserPlugin(Protocol):
    def supports(self, path: str) -> bool: ...
    def parse(self, path: str) -> ADFDocument: ...


class ExporterPlugin(Protocol):
    def export(self, document: ADFDocument, path: str) -> None: ...
