from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any

from packages.aims_core.adf import ADFDocument

from .base import PluginContext, PluginResult, attach_plugin_issue
from .registry import PluginRegistry


@dataclass
class PluginRunSummary:
    enabled_plugins: int = 0
    executed_plugins: int = 0
    failed_plugins: int = 0
    total_issues: int = 0
    results: list[PluginResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        if self.executed_plugins == 0:
            return 100
        penalty = min(100, self.failed_plugins * 20 + self.total_issues * 4)
        return max(0, 100 - penalty)


def _instantiate(path: str):
    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls()


def load_plugins_from_config(config: dict[str, Any] | None) -> PluginRegistry:
    registry = PluginRegistry()
    config = config or {}
    for item in config.get("plugins", []):
        if not item.get("enabled", True):
            continue
        plugin = _instantiate(item["path"])
        registry.register(plugin)
    return registry


def run_plugins(document: ADFDocument, config: dict[str, Any] | None = None, annotate: bool = True) -> PluginRunSummary:
    config = config or {}
    registry = load_plugins_from_config(config)
    summary = PluginRunSummary(enabled_plugins=len(registry.list()))

    plugin_options = {item.get("name"): item for item in config.get("plugins", []) if item.get("name")}

    for name in registry.list():
        plugin = registry.get(name)
        context = PluginContext(standard=config, options=plugin_options.get(name, {}))
        try:
            result = plugin.run(document, context)
        except Exception as exc:  # defensive plugin boundary
            result = PluginResult(
                plugin_name=name,
                version=getattr(plugin, "version", "unknown"),
                status="failed",
                issues=[],
                metrics={"error": str(exc)},
            )
        summary.executed_plugins += 1
        if result.status == "failed":
            summary.failed_plugins += 1
        summary.total_issues += len(result.issues)
        if annotate:
            for issue in result.issues:
                if issue.plugin is None:
                    issue.plugin = name
                attach_plugin_issue(document, issue)
        summary.results.append(result)
    return summary
