# src/presentation/components/ai/provider_status.py

"""
Provider Status Component

Purpose
-------
Displays the current AI provider status.

Responsibilities
----------------
- Display the active AI provider.
- Display provider availability.
- Keep provider status UI consistent.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No provider initialization.
- No network communication.
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
    provider: AIProvider,
    available: bool = True,
) -> None:
    """
    Render the provider status.

    Parameters
    ----------
    provider:
        Active AI provider.

    available:
        Indicates whether the provider is available.
    """

    if available:
        st.success(f"AI Provider: {provider.value.capitalize()} ✓")
    else:
        st.warning(f"AI Provider: {provider.value.capitalize()} " "(Unavailable)")


def render_badge(
    *,
    provider: AIProvider,
) -> None:
    """
    Render a compact provider badge.

    Parameters
    ----------
    provider:
        Active AI provider.
    """

    st.caption(f"🤖 Provider: {provider.value.capitalize()}")


def render_offline() -> None:
    """
    Render an offline provider message.
    """

    st.info("Offline AI mode is active.")


def render_not_configured() -> None:
    """
    Render a provider configuration warning.
    """

    st.warning("No AI provider has been configured.")


__all__ = [
    "render",
    "render_badge",
    "render_offline",
    "render_not_configured",
]
