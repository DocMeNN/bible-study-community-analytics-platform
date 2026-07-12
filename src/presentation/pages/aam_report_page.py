# src/presentation/pages/aam_report_page.py

"""
AAM Report Page

Purpose
-------
Displays AI-assisted ministry leadership reports.

Responsibilities
----------------
- Render AI leadership reports.
- Generate executive ministry summaries.
- Display strategic recommendations.
- Delegate AI execution to presentation components.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics.
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
from src.presentation.components import metric_cards
from src.presentation.components.ai import ai_panel
from src.presentation.viewmodels.ai_viewmodel import AIViewModel

# ============================================================================
# AAM Report Page
# ============================================================================


def render() -> None:
    """
    Render the AAM report page.
    """

    context.initialize()

    st.title("🧠 AI Ministry Report")

    if not context.has_session():
        st.info(
            "Load a session before generating an AI ministry report.",
        )
        return

    session = context.current_session()

    if session is None:
        st.error(
            "Unable to retrieve the active session.",
        )
        return

    dashboard = context.dashboard_service()

    expected = context.expected_attendees()

    dashboard_summary = dashboard.dashboard_summary(
        session,
        expected,
    )

    attendance = dashboard.attendance_summary(
        session,
        expected,
    )

    activity = dashboard.activity_summary(
        session,
    )

    viewmodel = AIViewModel(
        controller=context.ai_controller(),
    )

    report = viewmodel.build_executive_report(
        session=session,
        dashboard_summary=dashboard_summary,
        attendance=attendance,
        activity=activity,
    )

    metric_cards.render_section_header(
        "AI Ministry Leadership Report",
        ("Generate an AI-assisted report suitable " "for ministry leadership."),
    )

    ai_panel.render(
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
