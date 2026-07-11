# src/application/ai/response_validator.py

"""
Response Validator

Purpose:
    Validates parsed AI responses before they are consumed by the
    application.

Architecture:
    Application Layer

Dependencies:
    Domain Layer

Notes:
    The ResponseValidator ensures that parsed AI responses satisfy
    basic application requirements.

    Future enhancements may include:

    - Template-specific validation
    - JSON schema validation
    - Markdown section validation
    - Citation validation
    - Structured output validation

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.domain.ai.exceptions import AIResponseError


class ResponseValidator:
    """
    Validates parsed AI responses.
    """

    def validate(
        self,
        response: str,
    ) -> None:
        """
        Validate a parsed AI response.

        Parameters
        ----------
        response:
            Parsed response text.

        Raises
        ------
        AIResponseError
            If the response is invalid.
        """

        self._validate_not_empty(response)
        self._validate_not_whitespace(response)

    @staticmethod
    def _validate_not_empty(
        response: str,
    ) -> None:
        """
        Ensure the response is not empty.
        """

        if response == "":
            raise AIResponseError("AI response is empty.")

    @staticmethod
    def _validate_not_whitespace(
        response: str,
    ) -> None:
        """
        Ensure the response contains non-whitespace characters.
        """

        if not response.strip():
            raise AIResponseError("AI response contains only whitespace.")

    @staticmethod
    def minimum_length(
        response: str,
        length: int,
    ) -> None:
        """
        Validate a minimum response length.

        Parameters
        ----------
        response:
            Parsed response text.

        length:
            Minimum acceptable length.

        Raises
        ------
        AIResponseError
            If the response is shorter than the required length.
        """

        if len(response.strip()) < length:
            raise AIResponseError(
                f"AI response must contain at least {length} characters."
            )
