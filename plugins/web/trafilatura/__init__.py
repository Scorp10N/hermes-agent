"""Local URL extraction plugin — bundled, auto-loaded.

Fetches URLs directly with ``httpx`` and extracts readable content with
``trafilatura``. No API key required, but both packages must be installed
(optional deps — gated via :meth:`is_available`).
"""

from __future__ import annotations

from .provider import TrafilaturaWebExtractProvider


def register(ctx) -> None:
    """Register the trafilatura extract provider with the plugin context."""
    ctx.register_web_search_provider(TrafilaturaWebExtractProvider())
