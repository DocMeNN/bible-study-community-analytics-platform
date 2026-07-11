# src/application/ai/prompt_registry.py

"""
Prompt Registry

Purpose:
    Provides access to registered prompt templates and validates
    template variables before rendering.

Architecture:
    Application Layer

Dependencies:
    Domain Layer

Notes:
    Prompt templates are defined in the Domain layer. This registry
    acts as an application-facing adapter over those templates.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from string import Formatter
from typing import Any

# Local application imports
from src.domain.ai.exceptions import (
    PromptNotFoundError,
    PromptValidationError,
)
from src.domain.ai.prompts import PROMPTS, PromptTemplate


class PromptRegistry:
    """
    Registry for AI prompt templates.
    """

    def __init__(self) -> None:
        """
        Initialize the registry.
        """
        self._formatter = Formatter()

    def get(
        self,
        prompt_id: PromptTemplate,
    ) -> str:
        """
        Retrieve a prompt template.

        Parameters
        ----------
        prompt_id:
            Prompt template identifier.

        Returns
        -------
        str
            Prompt template.

        Raises
        ------
        PromptNotFoundError
            If the prompt template is unavailable.
        """

        try:
            return PROMPTS[prompt_id]

        except KeyError as exc:
            raise PromptNotFoundError(f"Unknown prompt template: {prompt_id}") from exc

    def list_prompts(
        self,
    ) -> list[PromptTemplate]:
        """
        Return all available prompt templates.
        """

        return sorted(PROMPTS.keys())

    def extract_variables(
        self,
        template: str,
    ) -> set[str]:
        """
        Extract template variables.

        Parameters
        ----------
        template:
            Prompt template.

        Returns
        -------
        set[str]
            Placeholder names.
        """

        variables: set[str] = set()

        for _, field_name, _, _ in self._formatter.parse(template):
            if field_name:
                variables.add(field_name)

        return variables

    def validate(
        self,
        template: str,
        variables: dict[str, Any],
    ) -> None:
        """
        Validate supplied template variables.

        Parameters
        ----------
        template:
            Prompt template.

        variables:
            Variables supplied by the caller.

        Raises
        ------
        PromptValidationError
            If variables are missing, unexpected, or invalid.
        """

        expected = self.extract_variables(template)
        supplied = set(variables.keys())

        missing = expected - supplied

        if missing:
            raise PromptValidationError(
                "Missing variables: " + ", ".join(sorted(missing))
            )

        unexpected = supplied - expected

        if unexpected:
            raise PromptValidationError(
                "Unexpected variables: " + ", ".join(sorted(unexpected))
            )

        for name, value in variables.items():
            if value is None:
                raise PromptValidationError(f"Variable '{name}' cannot be None.")

            if isinstance(value, str) and not value.strip():
                raise PromptValidationError(f"Variable '{name}' cannot be empty.")
