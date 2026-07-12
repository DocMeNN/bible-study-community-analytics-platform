# src/presentation/components/ai/ai_button.py

"""
AI Button Component

Purpose
-------
Provides a reusable Streamlit button for invoking AI-powered
features throughout the application.

Responsibilities
----------------
- Render a consistently styled AI action button.
- Provide a common interface for AI actions.
- Keep presentation logic reusable across pages.

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
    label: str = "✨ Generate with AI",
    *,
    key: str | None = None,
    help_text: str | None = None,
    disabled: bool = False,
    use_container_width: bool = True,
    icon: str = "✨",
) -> bool:
    """
    Render a reusable AI action button.

    Parameters
    ----------
    label:
        Button label.

    key:
        Optional unique Streamlit key.

    help_text:
        Tooltip shown on hover.

    disabled:
        Disable the button.

    use_container_width:
        Whether the button fills the available width.

    icon:
        Button icon.

    Returns
    -------
    bool
        True when the button is clicked.
    """

    return st.button(
        label,
        key=key,
        help=help_text,
        disabled=disabled,
        use_container_width=use_container_width,
        icon=icon,
        type="primary",
    )


__all__ = [
    "render",
]
