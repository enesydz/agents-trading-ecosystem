"""Allow-listed agent tools with explicit paper/live boundaries."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

ToolHandler = Callable[..., Awaitable[dict[str, Any]]]


@dataclass(frozen=True)
class ToolSpec:
    """Registered tool metadata and execution handler."""

    name: str
    description: str
    handler: ToolHandler
    paper_only: bool = True


class ToolRegistry:
    """Registry that rejects unknown tools and live execution by default."""

    def __init__(self, allow_live: bool = False) -> None:
        self._allow_live = allow_live
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"Tool already registered: {spec.name}")
        self._tools[spec.name] = spec

    async def call(self, name: str, **arguments: Any) -> dict[str, Any]:
        spec = self._tools.get(name)
        if spec is None:
            raise KeyError(f"Unknown tool: {name}")
        if not spec.paper_only and not self._allow_live:
            raise PermissionError("Live tools are disabled")
        return await spec.handler(**arguments)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))
