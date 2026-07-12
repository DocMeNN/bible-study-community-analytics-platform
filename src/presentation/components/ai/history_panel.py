# src/presentation/components/ai/history_panel.py

"""
AI History Panel

Purpose
-------
Displays previously generated AI results.

Responsibilities
----------------
- Display generated AI outputs.
- Keep AI history organized.
- Provide a reusable presentation component.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No persistence.
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
    history: dict[str, str],
) -> None:
    """
    Render AI history.
    """

    st.subheader("AI History")

    if not history:
        st.info("No AI responses generated during this session.")
        return

    for title, content in history.items():

        with st.expander(title):

            st.markdown(content)


__all__ = [
    "render",
]
