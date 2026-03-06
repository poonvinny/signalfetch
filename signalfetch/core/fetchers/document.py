"""DocumentFetcher — base class for PDF and document retrieval.

Used by the funds/ module for downloading and parsing PDF filings, prospectuses,
and other structured documents from sources like SEC EDGAR. LLM-assisted
extraction (via core/llm/) is typically applied after raw text is extracted here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import httpx


class DocumentFetcher(ABC):
    """Base class for retrieving and extracting text from PDF/document sources.

    Subclass this for document-based data sources (e.g. EDGAR fund filings,
    prospectuses). Handles downloading raw bytes via HTTP and delegating to a
    PDF parser (pypdf) for text extraction. The extracted text is then passed
    to an LLMProvider for structured data extraction.

    Intended usage pattern:
        class EDGARDocumentFetcher(DocumentFetcher):
            async def fetch_document(self, cik, accession_number):
                raw_bytes = await self._download(url)
                text = self._extract_text(raw_bytes)
                return text
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "DocumentFetcher":
        self._client = httpx.AsyncClient(follow_redirects=True)
        return self

    async def __aexit__(self, *_: object) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    @abstractmethod
    async def fetch_document(self, **kwargs: object) -> str:
        """Download and extract text from a document.

        Args:
            **kwargs: Source-specific locators (URLs, filing IDs, etc.)

        Returns:
            Extracted plain text content of the document, ready for LLM processing.
        """
        ...
