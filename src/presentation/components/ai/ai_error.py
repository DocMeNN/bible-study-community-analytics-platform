# src/presentation/components/ai/ai_error.py

"""
AI Error Component

Purpose
-------
Provides a reusable error presentation component for AI operations.

Responsibilities
----------------
- Display AI-related errors consistently.
- Present user-friendly guidance.
- Keep AI error rendering centralized.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No provider communication.
- No exception recovery.
"""

from __future__ import annotations

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Public Functions
# ============================================================================


def render(
    message: str,
    *,
    exception: Exception | None = None,
    show_details: bool = False,
) -> None:
    """
    Render an AI error message.

    Parameters
    ----------
    message:
        User-friendly error message.

    exception:
        Optional underlying exception.

    show_details:
        Display technical details when available.
    """

    st.error(
        f"🤖 AI Error\n\n{message}",
        icon="⚠️",
    )

    if show_details and exception is not None:
        with st.expander(
            "Technical Details",
            expanded=False,
        ):
            st.code(
                str(exception),
                language="text",
            )


def provider_unavailable() -> None:
    """
    Display a provider unavailable message.
    """

    render(
        (
            "The configured AI provider is currently unavailable. "
            "Please verify your provider configuration and try again."
        ),
    )


def invalid_response() -> None:
    """
    Display an invalid AI response message.
    """

    render(
        ("The AI provider returned an invalid response. " "Please retry your request."),
    )


def configuration_error() -> None:
    """
    Display an AI configuration error.
    """

    render(
        (
            "AI configuration is incomplete or invalid. "
            "Please review the application settings."
        ),
    )


__all__ = [
    "render",
    "provider_unavailable",
    "invalid_response",
    "configuration_error",
]
