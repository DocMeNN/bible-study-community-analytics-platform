# src/presentation/components/ai/summary_card.py

"""
AI Summary Card Component

Purpose
-------
Provides a reusable card for displaying AI-generated summaries.

Responsibilities
----------------
- Display a titled AI summary.
- Optionally show provider/model metadata.
- Support bordered, reusable presentation across dashboard pages.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No AI provider communication.
- No application orchestration.
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
    *,
    title: str,
    summary: str,
    provider: str | None = None,
    model: str | None = None,
    border: bool = True,
) -> None:
    """
    Render an AI summary card.

    Parameters
    ----------
    title:
        Card title.

    summary:
        AI-generated summary.

    provider:
        Optional AI provider name.

    model:
        Optional model name.

    border:
        Display within a bordered container.
    """

    container = st.container(border=border)

    with container:
        st.subheader(title)

        if provider is not None or model is not None:
            left, right = st.columns(2)

            with left:
                if provider is not None:
                    st.caption(f"Provider: **{provider}**")

            with right:
                if model is not None:
                    st.caption(f"Model: **{model}**")

            st.divider()

        st.markdown(summary)


def empty(
    *,
    title: str = "AI Summary",
    message: str = ("No AI summary has been generated yet."),
) -> None:
    """
    Render an empty summary card.

    Parameters
    ----------
    title:
        Card title.

    message:
        Placeholder message.
    """

    container = st.container(border=True)

    with container:
        st.subheader(title)
        st.info(message, icon="🤖")


def error(
    *,
    title: str = "AI Summary",
    message: str = ("Unable to generate an AI summary."),
) -> None:
    """
    Render an error summary card.

    Parameters
    ----------
    title:
        Card title.

    message:
        Error message.
    """

    container = st.container(border=True)

    with container:
        st.subheader(title)
        st.error(message, icon="⚠️")


__all__ = [
    "render",
    "empty",
    "error",
]
