# src/presentation/components/ai/ai_panel.py

"""
AI Panel

Purpose
-------
Provides a reusable AI interaction panel for the Presentation layer.

Responsibilities
----------------
- Render AI controls.
- Execute AI requests.
- Display loading state.
- Display AI results.
- Display AI errors.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics.
- No provider communication.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Callable
from typing import Any

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation.components.ai import (
    ai_button,
    ai_error,
    ai_loading,
    ai_result,
)

# ============================================================================
# AI Panel
# ============================================================================


def render(
    *,
    title: str,
    button_label: str,
    callback: Callable[..., str],
    callback_kwargs: dict[str, Any],
    result_key: str,
    button_key: str | None = None,
    help_text: str | None = None,
    empty_message: str = ("No AI result has been generated yet."),
) -> None:
    """
    Render a reusable AI interaction panel.

    Parameters
    ----------
    title:
        Panel title.

    button_label:
        Text displayed on the AI button.

    callback:
        Controller method executed when the
        button is pressed.

    callback_kwargs:
        Keyword arguments supplied to the callback.

    result_key:
        Streamlit session-state key used to
        store the generated result.

    button_key:
        Optional unique Streamlit button key.

    help_text:
        Tooltip shown on hover.

    empty_message:
        Placeholder displayed before the first
        AI request.
    """

    if result_key not in st.session_state:
        st.session_state[result_key] = ""

    st.subheader(title)

    clicked = ai_button.render(
        label=button_label,
        key=button_key,
        help_text=help_text,
    )

    if clicked:

        try:

            with ai_loading.render():

                result = callback(
                    **callback_kwargs,
                )

                st.session_state[result_key] = result

        except Exception as exc:

            ai_error.render(
                message="Unable to complete the AI request.",
                exception=exc,
                show_details=False,
            )

    result = st.session_state[result_key]

    # =====================================================================
    # Result
    # =====================================================================

    if result:

        ai_result.render(
            result=result,
            title="Generated Response",
        )

    else:

        ai_result.empty(
            message=empty_message,
        )


# ============================================================================
# Session State Helpers
# ============================================================================


def clear_result(
    result_key: str,
) -> None:
    """
    Clear a stored AI result.

    Parameters
    ----------
    result_key:
        Session-state key containing the AI result.
    """

    st.session_state[result_key] = ""


def has_result(
    result_key: str,
) -> bool:
    """
    Return True if an AI result exists.

    Parameters
    ----------
    result_key:
        Session-state key containing the AI result.
    """

    return bool(
        st.session_state.get(
            result_key,
            "",
        )
    )


def get_result(
    result_key: str,
) -> str:
    """
    Return a stored AI result.

    Parameters
    ----------
    result_key:
        Session-state key containing the AI result.
    """

    return str(
        st.session_state.get(
            result_key,
            "",
        )
    )


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "render",
    "clear_result",
    "has_result",
    "get_result",
]
