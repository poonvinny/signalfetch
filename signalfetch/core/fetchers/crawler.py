"""CrawlerFetcher — base class for sources with no public API.

Used when a data source publishes data only via HTML pages or file downloads
without a structured API. Provides async HTTP capabilities and patterns for
HTML parsing, pagination, and polite crawling (rate limiting, robots.txt).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import httpx


class CrawlerFetcher(ABC):
    """Base class for scraping data from web sources without a public API.

    Subclass this for HTML-based or file-download data sources. Provides a
    managed `httpx.AsyncClient` with a browser-like User-Agent. Subclasses
    should implement `crawl()` with source-specific page traversal logic.

    Intended usage pattern:
        class EurostatCrawler(CrawlerFetcher):
            async def crawl(self, dataset_code):
                # fetch HTML, parse tables, yield rows
                ...
    """

    _default_headers = {
        "User-Agent": "SignalFetch/0.1 (https://github.com/signalfetch/signalfetch; research bot)",
    }

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "CrawlerFetcher":
        self._client = httpx.AsyncClient(headers=self._default_headers, follow_redirects=True)
        return self

    async def __aexit__(self, *_: object) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    @abstractmethod
    async def crawl(self, **kwargs: object) -> object:
        """Crawl the source and return raw extracted data.

        Args:
            **kwargs: Source-specific parameters (URLs, dataset codes, etc.)

        Returns:
            Raw extracted content; callers map to DataPoint instances.
        """
        ...
