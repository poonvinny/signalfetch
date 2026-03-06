"""APIFetcher — base class for structured REST API sources.

Used by macro/ agents (BLS, IMF, World Bank, OECD, Eurostat) that expose
JSON REST endpoints. Provides a shared async HTTP client and common patterns
for authentication, pagination, and rate limiting.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import httpx


class APIFetcher(ABC):
    """Base class for fetching data from structured JSON REST APIs.

    Subclass this for each API-backed data source. Provides a managed
    `httpx.AsyncClient` for async HTTP requests. Subclasses should define
    `base_url` and implement `_build_request` / `_parse_response` as needed.

    Intended usage pattern:
        class BLSFetcher(APIFetcher):
            base_url = "https://api.bls.gov/publicAPI/v2"

            async def get(self, series_ids, start_year, end_year):
                ...
    """

    base_url: str

    def __init__(self, api_key: str | None = None) -> None:
        """
        Args:
            api_key: Optional API key for authenticated sources (e.g. BLS registration key).
        """
        self._api_key = api_key
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "APIFetcher":
        self._client = httpx.AsyncClient(base_url=self.base_url)
        return self

    async def __aexit__(self, *_: object) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    @abstractmethod
    async def get(self, **kwargs: object) -> object:
        """Perform a source-specific data retrieval.

        Args:
            **kwargs: Source-specific parameters.

        Returns:
            Raw parsed response (dict or list); callers are responsible for
            mapping to DataPoint instances.
        """
        ...
