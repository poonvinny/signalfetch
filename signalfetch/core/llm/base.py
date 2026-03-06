"""Abstract LLM provider interface.

All LLM interactions in SignalFetch go through this interface, keeping the framework
LLM-agnostic. Claude is the default implementation (see claude.py), but any provider
can be used by subclassing LLMProvider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):
    """Abstract base class for LLM providers.

    Used exclusively in the funds/ module for structured extraction from
    PDF documents. Macro agents do not require an LLM.

    To use a different LLM, subclass this and pass your provider to the
    relevant agent at construction time.
    """

    @abstractmethod
    async def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a free-text completion for the given prompt.

        Args:
            prompt: The input prompt.
            **kwargs: Provider-specific parameters (model, temperature, max_tokens, etc.)

        Returns:
            The generated text response.
        """
        ...

    @abstractmethod
    async def structured(self, prompt: str, schema: type[T], **kwargs: Any) -> T:
        """Generate a structured response conforming to a Pydantic schema.

        Intended for extracting typed data from unstructured text (e.g. PDF content).
        Implementations should use tool use / function calling or JSON mode where
        available to ensure the response reliably parses into `schema`.

        Args:
            prompt: The input prompt describing the extraction task.
            schema: A Pydantic BaseModel subclass defining the expected output shape.
            **kwargs: Provider-specific parameters.

        Returns:
            A validated instance of `schema`.
        """
        ...
