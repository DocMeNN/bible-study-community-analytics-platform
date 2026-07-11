# src/application/ai/prompt_engine.py

"""
Prompt Engine

Purpose:
    Coordinates prompt retrieval, validation, and rendering.

Architecture:
    Application Layer

Dependencies:
    PromptRegistry
    PromptRenderer
    Domain Layer

Notes:
    This class is the public entry point for rendering AI prompt
    templates. It delegates retrieval, validation, and rendering
    to dedicated components.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from typing import Any

# Local application imports
from src.application.ai.prompt_registry import PromptRegistry
from src.application.ai.prompt_renderer import PromptRenderer
from src.domain.ai.prompts import PromptTemplate


class PromptEngine:
    """
    Coordinates AI prompt rendering.
    """

    def __init__(
        self,
        registry: PromptRegistry,
        renderer: PromptRenderer,
    ) -> None:
        """
        Initialize the prompt engine.

        Parameters
        ----------
        registry:
            Prompt registry.

        renderer:
            Prompt renderer.
        """

        self._registry = registry
        self._renderer = renderer

    def render(
        self,
        prompt: PromptTemplate,
        variables: dict[str, Any],
    ) -> str:
        """
        Render a prompt template.

        Parameters
        ----------
        prompt:
            Prompt template identifier.

        variables:
            Template variables.

        Returns
        -------
        str
            Fully rendered prompt.
        """

        template = self._registry.get(prompt)

        self._registry.validate(
            template=template,
            variables=variables,
        )

        return self._renderer.render(
            template=template,
            variables=variables,
        )

    def available_prompts(
        self,
    ) -> list[PromptTemplate]:
        """
        Return all registered prompt templates.

        Returns
        -------
        list[PromptTemplate]
            Available prompt identifiers.
        """

        return self._registry.list_prompts()
