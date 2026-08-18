# src/presentation/streamlit_app.py

"""
Attendance Dashboard Application

Purpose
-------
Application entry point for the OYBS WhatsApp Attendance Dashboard.

Responsibilities
----------------
- Configure the Streamlit application.
- Initialize the Presentation Context.
- Render the application header.
- Render the unified session navigation control.
- Route navigation to the selected page.
- Handle unexpected application-level exceptions.

Architectural Rules
-------------------
This module intentionally remains thin.

It must:
- Configure the Presentation layer.
- Delegate navigation.
- Delegate session selection.
- Delegate page rendering.

It must not:
- Perform business logic.
- Access Infrastructure directly.
- Perform analytics.
- Parse data.
- Build Session aggregates.

Unified Session Presentation
----------------------------
The active SessionCollection is loaded once into the Presentation Context.

The unified session selector is rendered once at the application level.

Pages consume the currently selected Session through the
Presentation Context.

Presentation flow:

SessionCollection
        ↓
Presentation Scope
        ↓
Session Group
        ↓
Daily Session
        ↓
Selected Session
        ↓
Selected Page
        ↓
Analytics

Dependency Flow
---------------
Presentation
        ↓
Application
        ↓
Domain
        ↑
Infrastructure
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
import traceback

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st
from dotenv import load_dotenv

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation import context, navigation, theme
from src.presentation.components.common import session_selector

# ============================================================================
# Application Entry Point
# ============================================================================


def main() -> None:
    """
    Launch the Streamlit application.
    """

    load_dotenv()

    theme.configure_page()

    context.initialize()

    theme.render_application_header()

    if context.has_session_collection():
        session_selector.render()

        st.divider()

    page_renderer = navigation.get_selected_page()

    page_renderer()


# ============================================================================
# Direct Execution Support
# ============================================================================


def run() -> None:
    """
    Execute the application with error handling.
    """

    try:
        main()

    except Exception:
        st.error(
            "An unexpected application error occurred.",
        )

        with st.expander(
            "Technical Details",
        ):
            st.code(
                traceback.format_exc(),
            )


# ============================================================================
# Bootstrap
# ============================================================================


if __name__ == "__main__":
    run()
