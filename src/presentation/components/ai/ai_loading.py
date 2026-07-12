# src/presentation/components/ai/ai_loading.py

"""
AI Loading Component

Purpose
-------
Provides a reusable loading indicator for AI-powered operations.

Responsibilities
----------------
- Display a consistent loading state.
- Provide user feedback while AI processing is in progress.
- Encapsulate the Streamlit spinner component.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No AI provider communication.
- No application orchestration.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterator
from contextlib import contextmanager

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Public Functions
# ============================================================================


@contextmanager
def render(
    message: str = "Generating AI response...",
) -> Iterator[None]:
    """
    Display a reusable AI loading spinner.

    Parameters
    ----------
    message:
        Message displayed while the AI operation is running.

    Yields
    ------
    None
        Control returns to the caller while the spinner is active.
    """

    with st.spinner(message):
        yield


def show_status(
    message: str = "AI is processing your request...",
) -> None:
    """
    Display an informational AI processing message.

    Parameters
    ----------
    message:
        Status message shown to the user.
    """

    st.info(f"🤖 {message}")


__all__ = [
    "render",
    "show_status",
]
