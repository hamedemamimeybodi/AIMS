from __future__ import annotations

from typing import Any

from .base import AIMSPlugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, AIMSPlugin] = {}

    def register(self, plugin: AIMSPlugin) -> None:
        if not getattr(plugin, "name", None):
            raise ValueError("Plugin must define a non-empty name")
        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> AIMSPlugin:
        if name not in self._plugins:
            raise KeyError(f"Plugin not registered: {name}")
        return self._plugins[name]

    def list(self) -> list[str]:
        return sorted(self._plugins.keys())

    def as_metadata(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for name in self.list():
            plugin = self._plugins[name]
            out.append(
                {
                    "name": plugin.name,
                    "version": getattr(plugin, "version", "unknown"),
                    "description": getattr(plugin, "description", ""),
                }
            )
        return out
