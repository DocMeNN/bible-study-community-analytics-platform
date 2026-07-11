# src/application/ai/request_builder.py

"""
AI Request Builder

Purpose:
    Builds AIRequest objects for the AI subsystem.

Architecture:
    Application Layer

Dependencies:
    Configuration Layer
    Domain Layer

Notes:
    This builder centralizes AIRequest construction so that
    application services do not instantiate AIRequest directly.
    Future enhancements (system prompts, tools, JSON mode,
    multimodal inputs, etc.) can be introduced here without
    changing AIService.

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.config.ai_config import AIConfig
from src.domain.ai.models import AIRequest


class AIRequestBuilder:
    """
    Builds AIRequest instances.
    """

    def __init__(
        self,
        config: AIConfig,
    ) -> None:
        """
        Initialize the request builder.

        Parameters
        ----------
        config:
            AI configuration.
        """

        self._temperature = config.temperature
        self._max_tokens = config.max_tokens

    def build(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AIRequest:
        """
        Build an AIRequest.

        Parameters
        ----------
        prompt:
            Rendered prompt.

        system_prompt:
            Optional system prompt.

        temperature:
            Optional temperature override.

        max_tokens:
            Optional maximum token override.

        Returns
        -------
        AIRequest
            Configured AI request.
        """

        return AIRequest(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=(temperature if temperature is not None else self._temperature),
            max_tokens=(max_tokens if max_tokens is not None else self._max_tokens),
        )
