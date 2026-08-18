# src/presentation/components/ai/ministry_ai_panel.py

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

import traceback

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
    empty_message: str = "No AI result has been generated yet.",
) -> None:
    """
    Render a reusable AI interaction panel.
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
                # ==========================================================
                # DIAGNOSTIC
                # ==========================================================

                st.write("### Callback")
                st.code(repr(callback), language="text")

                st.write("### Callback Module")
                st.code(
                    getattr(callback, "__module__", "UNKNOWN"),
                    language="text",
                )

                st.write("### Callback Qualname")
                st.code(
                    getattr(callback, "__qualname__", "UNKNOWN"),
                    language="text",
                )

                st.write("### Callback Arguments")
                st.json(callback_kwargs)

                result = callback(
                    **callback_kwargs,
                )

                st.write("### Returned Result Type")
                st.code(type(result).__name__, language="text")

                st.write("### Returned Result Preview")
                st.code(str(result)[:1000], language="text")

                st.session_state[result_key] = result

        except Exception as exc:
            st.error("🔍 AI Exception Captured")

            st.write("### Exception Type")
            st.code(
                type(exc).__name__,
                language="text",
            )

            st.write("### Exception")
            st.code(
                str(exc),
                language="text",
            )

            st.write("### Full Traceback")
            st.code(
                traceback.format_exc(),
                language="text",
            )

            st.exception(exc)

            ai_error.render(
                message="Unable to complete the AI request.",
                exception=exc,
                show_details=True,
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
    """

    st.session_state[result_key] = ""


def has_result(
    result_key: str,
) -> bool:
    """
    Return True if an AI result exists.
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
