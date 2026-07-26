# src/presentation/pages/ministry_ai_page.py

"""
AI Ministry Report Page

Purpose
-------
Displays AI-assisted ministry leadership reports.

Responsibilities
----------------
- Render AI leadership reports.
- Generate executive ministry summaries.
- Display strategic recommendations.
- Delegate report data preparation to AIViewModel.
- Delegate AI execution to presentation components.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
- No AI provider communication.
"""

from __future__ import annotations

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation import context
from src.presentation.components.ai import ministry_ai_panel
from src.presentation.components.common import metric_cards

# ============================================================================
# AI Ministry Report Page
# ============================================================================


def render() -> None:
    """
    Render the AI Ministry Report page.
    """

    context.initialize()

    st.title("🧠 AI Ministry Report")

    if not context.has_session_collection():
        st.info(
            "Load a session before generating an AI ministry report.",
        )
        return

    session_collection = context.current_session_collection()

    if session_collection is None:
        st.error(
            "Unable to retrieve the active session collection.",
        )
        return

    session = session_collection.first_session

    if session is None:
        st.info(
            "The loaded session collection contains no sessions.",
        )
        return

    dashboard_viewmodel = context.dashboard_viewmodel()

    report_data = dashboard_viewmodel.get_dashboard(
        session=session,
        expected_attendees=context.expected_attendees(),
    )

    ai_viewmodel = context.ai_viewmodel()

    report = ai_viewmodel.build_executive_report(
        session=session,
        dashboard_summary=report_data["dashboard"],
        attendance=report_data["attendance"],
        activity=report_data["activity"],
    )

    metric_cards.render_section_header(
        "AI Ministry Leadership Report",
        "Generate an AI-assisted report suitable for ministry leadership.",
    )

    ministry_ai_panel.render(
        title="Leadership Report",
        button_label="✨ Generate Ministry Report",
        callback=context.ai_controller().generate_executive_summary,
        callback_kwargs={
            "report": report,
        },
        result_key="aam_leadership_report",
        button_key="generate_aam_report",
        help_text="Generate an AI-powered ministry leadership report.",
        empty_message="No ministry leadership report has been generated yet.",
    )
