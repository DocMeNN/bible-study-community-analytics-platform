# src/presentation/components/ai/ai_result.py

"""
AI Result Component

Purpose
-------
Displays AI-generated output in a consistent, reusable format.

Responsibilities
----------------
- Render AI-generated text.
- Provide copy-friendly presentation.
- Optionally display metadata.
- Provide a reusable container for AI responses.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No AI provider communication.
- No response parsing.
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
    result: str,
    *,
    title: str = "AI Result",
    height: int = 260,
    border: bool = True,
) -> None:
    """
    Render an AI-generated result.

    Parameters
    ----------
    result:
        AI-generated text.

    title:
        Section title.

    height:
        Display height for the text area.

    border:
        Display inside a bordered container.
    """

    container = st.container(border=border)

    with container:
        st.subheader(title)

        st.text_area(
            label="",
            value=result,
            height=height,
            disabled=True,
            label_visibility="collapsed",
        )


def empty(
    message: str = ("Generate an AI response to view the result."),
) -> None:
    """
    Display an empty-state placeholder.
    """

    st.info(
        message,
        icon="🤖",
    )


def metadata(
    *,
    provider: str,
    model: str,
) -> None:
    """
    Display AI metadata.

    Parameters
    ----------
    provider:
        AI provider name.

    model:
        Model used.
    """

    left, right = st.columns(2)

    with left:
        st.caption(f"Provider: **{provider}**")

    with right:
        st.caption(f"Model: **{model}**")


__all__ = [
    "render",
    "empty",
    "metadata",
]
