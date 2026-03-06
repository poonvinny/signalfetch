"""Claude LLM provider — the default SignalFetch LLM backend.

Uses the Anthropic Python SDK. Requires ANTHROPIC_API_KEY to be set in the
environment. To swap providers, implement LLMProvider and pass your instance
to the relevant agent.
"""

from __future__ import annotations

import os
from typing import Any, TypeVar

from pydantic import BaseModel

from signalfetch.core.llm.base import LLMProvider

T = TypeVar("T", bound=BaseModel)

_DEFAULT_MODEL = "claude-sonnet-4-6"


class ClaudeProvider(LLMProvider):
    """LLM provider backed by Anthropic's Claude API.

    This is the default provider. It reads ANTHROPIC_API_KEY from the environment.

    Args:
        model: Claude model ID to use. Defaults to claude-sonnet-4-6.
        api_key: Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var.
    """

    def __init__(
        self,
        model: str = _DEFAULT_MODEL,
        api_key: str | None = None,
    ) -> None:
        self._model = model
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

    async def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a free-text completion using Claude.

        Args:
            prompt: The input prompt.
            **kwargs: Passed through to the Anthropic messages.create() call
                      (e.g. max_tokens, temperature).

        Returns:
            The text content of Claude's response.
        """
        raise NotImplementedError("ClaudeProvider.complete() not yet implemented")

    async def structured(self, prompt: str, schema: type[T], **kwargs: Any) -> T:
        """Extract structured data from a prompt using Claude's tool use.

        Converts `schema` into a tool definition, calls Claude with tool_choice=required,
        and parses the returned tool input back into a validated Pydantic instance.

        Args:
            prompt: The extraction prompt (typically document text + instructions).
            schema: Pydantic model defining the expected output.
            **kwargs: Passed through to the Anthropic messages.create() call.

        Returns:
            A validated instance of `schema`.
        """
        raise NotImplementedError("ClaudeProvider.structured() not yet implemented")
