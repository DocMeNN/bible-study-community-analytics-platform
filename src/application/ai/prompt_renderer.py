# src/application/ai/prompt_renderer.py

"""
Prompt Renderer

Purpose:
    Renders prompt templates using supplied variables.

Architecture:
    Application Layer

Dependencies:
    Domain Layer

Notes:
    This module is responsible only for rendering prompt
    templates. It performs no validation and does not know
    how prompts are stored or retrieved.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from string import Formatter
from typing import Any

# Local application imports
from src.domain.ai.exceptions import PromptRenderError


class PromptRenderer:
    """
    Renders prompt templates.
    """

    def __init__(self) -> None:
        """
        Initialize the renderer.
        """
        self._formatter = Formatter()

    def render(
        self,
        template: str,
        variables: dict[str, Any],
    ) -> str:
        """
        Render a prompt template.

        Parameters
        ----------
        template:
            Prompt template.

        variables:
            Template variables.

        Returns
        -------
        str
            Rendered prompt.

        Raises
        ------
        PromptRenderError
            If rendering fails.
        """

        try:
            return self._formatter.vformat(
                template,
                (),
                variables,
            )

        except KeyError as exc:
            raise PromptRenderError(
                f"Missing template variable: {exc.args[0]}"
            ) from exc

        except ValueError as exc:
            raise PromptRenderError(str(exc)) from exc

        except Exception as exc:
            raise PromptRenderError("Unable to render prompt.") from exc

    def extract_variables(
        self,
        template: str,
    ) -> set[str]:
        """
        Extract placeholder names from a template.

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
