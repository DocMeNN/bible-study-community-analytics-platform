# src/presentation/pages/settings_page.py

"""
Settings Page

Purpose
-------
Provides application configuration controls.

Responsibilities
----------------
- Render settings UI.
- Display AI configuration information.
- Display provider information.
- Display model information.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No provider communication.
- No infrastructure access.
"""

from __future__ import annotations

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.config.ai_config import load_ai_config
from src.presentation.components import metric_cards
from src.presentation.components.ai import provider_selector

# ============================================================================
# Settings Page
# ============================================================================


def render() -> None:
    """
    Render the Settings page.
    """

    st.title("⚙️ Settings")

    # =====================================================================
    # AI Configuration
    # =====================================================================

    metric_cards.render_section_header(
        "AI Configuration",
        "Current AI subsystem settings.",
    )

    config = load_ai_config()

    left_column, right_column = st.columns(2)

    with left_column:
        st.metric(
            "Provider",
            config.provider.value.upper(),
        )

        st.metric(
            "Model",
            config.model,
        )

    with right_column:
        st.metric(
            "Temperature",
            str(config.temperature),
        )

        st.metric(
            "Max Tokens",
            str(config.max_tokens),
        )

    st.divider()

    # =====================================================================
    # Provider Selection
    # =====================================================================

    metric_cards.render_section_header(
        "Provider Selection",
        "Available AI providers for this deployment.",
    )

    selected_provider = provider_selector.render(
        default=config.provider,
        disabled=True,
    )

    provider_selector.caption(
        selected_provider,
    )

    st.info(
        (
            "Runtime provider switching is not yet enabled.\n\n"
            "The active provider is determined by the "
            "application configuration."
        )
    )

    st.divider()

    # =====================================================================
    # Environment Information
    # =====================================================================

    metric_cards.render_section_header(
        "Environment",
        "AI runtime information.",
    )

    st.write(f"**Provider:** {config.provider.value}")

    st.write(f"**Model:** {config.model}")

    st.write(f"**Timeout:** {config.timeout} seconds")

    st.write(f"**Temperature:** {config.temperature}")

    st.write(f"**Max Tokens:** {config.max_tokens}")

    st.divider()

    # =====================================================================
    # Future Features
    # =====================================================================

    metric_cards.render_section_header(
        "Upcoming Features",
        "Planned configuration enhancements.",
    )

    st.info(
        "Planned enhancements:\n\n"
        "• Runtime provider switching\n"
        "• Ollama availability checks\n"
        "• API key management\n"
        "• Connection testing\n"
        "• Model selection\n"
        "• Offline AI status monitoring"
    )
