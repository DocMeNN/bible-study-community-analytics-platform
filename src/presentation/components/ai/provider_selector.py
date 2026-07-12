# src/presentation/components/ai/provider_selector.py

"""
Provider Selector Component

Purpose
-------
Provides a reusable selector for choosing the active AI provider.

Responsibilities
----------------
- Display supported AI providers.
- Return the selected provider.
- Keep provider selection UI consistent.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No provider initialization.
- No configuration persistence.
"""

from __future__ import annotations

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.config.ai_config import AIProvider

# ============================================================================
# Public Functions
# ============================================================================


def render(
    *,
    label: str = "AI Provider",
    key: str | None = None,
    default: AIProvider = AIProvider.OLLAMA,
    disabled: bool = False,
    help_text: str | None = ("Select the AI provider used for this request."),
) -> AIProvider:
    """
    Render an AI provider selector.

    Parameters
    ----------
    label:
        Display label.

    key:
        Optional Streamlit widget key.

    default:
        Default selected provider.

    disabled:
        Disable the selector.

    help_text:
        Tooltip shown on hover.

    Returns
    -------
    AIProvider
        Selected provider.
    """

    providers = list(AIProvider)

    index = providers.index(default)

    selected = st.selectbox(
        label,
        options=providers,
        index=index,
        key=key,
        disabled=disabled,
        help=help_text,
        format_func=lambda provider: provider.value.capitalize(),
    )

    return selected


def caption(provider: AIProvider) -> None:
    """
    Display the currently selected provider.

    Parameters
    ----------
    provider:
        Active AI provider.
    """

    st.caption(f"Current Provider: **{provider.value.capitalize()}**")


__all__ = [
    "render",
    "caption",
]
