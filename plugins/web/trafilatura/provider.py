"""Local URL extraction via ``httpx`` (fetch) + ``trafilatura`` (readability).

Free, no API key, no external service — fetches the URL directly from this
machine and pulls the main article/body content out of the raw HTML with
``trafilatura``. Does not execute JavaScript, so it won't work well on
client-side-rendered (SPA) pages — fine for most articles, docs, and blog
posts, which is the common case for "read this URL and summarize it."

Both ``httpx`` and ``trafilatura`` are optional deps (installed via
``uv pip install --python /opt/hermes/.venv/bin/python3 httpx trafilatura``);
``is_available()`` reflects whether both are importable.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from agent.web_search_provider import WebSearchProvider

logger = logging.getLogger(__name__)

_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


class TrafilaturaWebExtractProvider(WebSearchProvider):
    """Local httpx-fetch + trafilatura-extract provider. Extract-only."""

    @property
    def name(self) -> str:
        return "trafilatura"

    @property
    def display_name(self) -> str:
        return "Local extract (httpx + trafilatura)"

    def is_available(self) -> bool:
        """Return True when both ``httpx`` and ``trafilatura`` are importable.

        Must NOT perform network I/O — runs at tool-registration time and on
        every ``hermes tools`` paint.
        """
        try:
            import httpx  # noqa: F401
            import trafilatura  # noqa: F401

            return True
        except ImportError:
            return False

    def supports_search(self) -> bool:
        return False

    def supports_extract(self) -> bool:
        return True

    def extract(self, urls: List[str], **kwargs: Any) -> Any:
        """Fetch each URL directly and extract readable content with trafilatura."""
        try:
            import httpx
        except ImportError:
            return [
                {"url": u, "error": "httpx package is not installed"} for u in urls
            ]
        try:
            import trafilatura
        except ImportError:
            return [
                {"url": u, "error": "trafilatura package is not installed"}
                for u in urls
            ]

        results = []
        with httpx.Client(
            headers={"User-Agent": _USER_AGENT},
            timeout=20.0,
            follow_redirects=True,
        ) as client:
            for url in urls:
                try:
                    resp = client.get(url)
                    resp.raise_for_status()
                    body = resp.text
                    content_type = resp.headers.get("content-type", "")
                except Exception as exc:  # noqa: BLE001 — surface as per-URL error
                    logger.warning("trafilatura fetch error for %s: %s", url, exc)
                    results.append({"url": url, "error": f"fetch failed: {exc}"})
                    continue

                # trafilatura expects HTML; plain-text/Markdown bodies (raw
                # GitHub files, .txt/.md endpoints, etc.) parse to nothing
                # extractable, so pass those straight through as content.
                is_plain_text = "text/html" not in content_type and not body.lstrip().startswith(
                    ("<!DOCTYPE", "<html", "<?xml")
                )

                if is_plain_text:
                    results.append(
                        {
                            "url": url,
                            "title": "",
                            "content": body,
                            "raw_content": body,
                            "metadata": {"content_type": content_type},
                        }
                    )
                    continue

                try:
                    extracted = trafilatura.bare_extraction(
                        body, url=url, with_metadata=True, as_dict=True
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.warning("trafilatura extract error for %s: %s", url, exc)
                    results.append({"url": url, "error": f"extract failed: {exc}"})
                    continue

                if not extracted or not extracted.get("text"):
                    results.append(
                        {
                            "url": url,
                            "error": "trafilatura found no extractable article content "
                            "(may be a JS-rendered page — this provider does not "
                            "execute JavaScript)",
                        }
                    )
                    continue

                results.append(
                    {
                        "url": url,
                        "title": str(extracted.get("title") or ""),
                        "content": str(extracted.get("text") or ""),
                        "raw_content": body,
                        "metadata": {
                            "author": extracted.get("author"),
                            "date": extracted.get("date"),
                            "description": extracted.get("description"),
                            "sitename": extracted.get("sitename"),
                        },
                    }
                )

        logger.info("trafilatura extract: %d/%d URLs succeeded", sum(1 for r in results if "error" not in r), len(urls))
        return results

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "Local extract (httpx + trafilatura)",
            "badge": "free · no key · extract only",
            "tag": "Fetches the URL directly from this machine and pulls out "
            "readable content locally — no JS execution, no external API.",
            "env_vars": [],
        }
