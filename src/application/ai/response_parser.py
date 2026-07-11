# src/application/ai/response_parser.py

"""
Response Parser

Purpose:
    Parses AI responses into normalized application text.

Architecture:
    Application Layer

Dependencies:
    Domain Layer

Notes:
    The ResponseParser converts provider-agnostic AIResponse
    objects into normalized text suitable for downstream
    processing.

    Future enhancements may include:

    - Markdown parsing
    - JSON parsing
    - Structured output extraction
    - Citation extraction
    - Tool/function call parsing

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.domain.ai.models import AIResponse


class ResponseParser:
    """
    Parses AI responses.

    Responsibilities
    ----------------
    - Normalize whitespace.
    - Return clean response text.
    - Provide a single parsing entry point for all providers.
    """

    def parse(
        self,
        response: AIResponse,
    ) -> str:
        """
        Parse an AI response.

        Parameters
        ----------
        response:
            AI response returned by a provider.

        Returns
        -------
        str
            Normalized response text.
        """

        return self._normalize(
            response.content,
        )

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:
        """
        Normalize response text.

        Operations
        ----------
        - Strip leading whitespace.
        - Strip trailing whitespace.
        - Normalize line endings.

        Parameters
        ----------
        text:
            Raw response text.

        Returns
        -------
        str
            Normalized text.
        """

        return text.replace("\r\n", "\n").replace("\r", "\n").strip()
