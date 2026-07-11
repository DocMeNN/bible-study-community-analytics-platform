# src/application/ai/response_engine.py

"""
Response Engine

Purpose:
    Coordinates AI response parsing and validation.

Architecture:
    Application Layer

Dependencies:
    ResponseParser
    ResponseValidator
    Domain Layer

Notes:
    The ResponseEngine serves as the single entry point for
    processing provider-agnostic AI responses. It delegates
    parsing and validation to dedicated components and returns
    normalized text suitable for application consumption.

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.application.ai.response_parser import ResponseParser
from src.application.ai.response_validator import ResponseValidator
from src.domain.ai.models import AIResponse


class ResponseEngine:
    """
    Coordinates AI response processing.
    """

    def __init__(
        self,
        parser: ResponseParser,
        validator: ResponseValidator,
    ) -> None:
        """
        Initialize the response engine.

        Parameters
        ----------
        parser:
            Response parser.

        validator:
            Response validator.
        """

        self._parser = parser
        self._validator = validator

    def process(
        self,
        response: AIResponse,
    ) -> str:
        """
        Process an AI response.

        Processing pipeline
        -------------------
        1. Parse the provider response.
        2. Validate the parsed content.
        3. Return normalized text.

        Parameters
        ----------
        response:
            Provider-agnostic AI response.

        Returns
        -------
        str
            Parsed and validated response text.
        """

        parsed = self._parser.parse(
            response=response,
        )

        self._validator.validate(
            response=parsed,
        )

        return parsed
