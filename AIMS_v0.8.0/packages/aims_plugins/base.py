from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from packages.aims_core.adf import ADFDocument, ValidationIssue


@dataclass
class PluginIssue:
    code: str
    severity: str
    message: str
    entity_id: str | None = None
    plugin: str | None = None


@dataclass
class PluginResult:
    plugin_name: str
    version: str = "0.1.0"
    status: str = "passed"
    checked_entities: int = 0
    issues: list[PluginIssue] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    @property
    def issue_count(self) -> int:
        return len(self.issues)


@dataclass
class PluginContext:
    standard: dict[str, Any] = field(default_factory=dict)
    options: dict[str, Any] = field(default_factory=dict)


class AIMSPlugin(Protocol):
    name: str
    version: str
    description: str

    def run(self, document: ADFDocument, context: PluginContext) -> PluginResult:
        ...


def attach_plugin_issue(document: ADFDocument, issue: PluginIssue) -> None:
    if not issue.entity_id:
        return
    for entity in document.entities:
        if entity.id == issue.entity_id:
            entity.issues.append(
                ValidationIssue(
                    code=issue.code,
                    severity=issue.severity,
                    message=f"[{issue.plugin}] {issue.message}" if issue.plugin else issue.message,
                )
            )
            return
