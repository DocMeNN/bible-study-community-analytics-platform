# src/presentation/pages/reports_page.py

"""
Reports Page

Purpose
-------
Displays reporting functionality.

Responsibilities
----------------
- Display report information.
- Display export options.
- Display AI report generation.
- Delegate AI generation to presentation components.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics.
- No report generation.
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
# Reports Page
# ============================================================================


def render() -> None:
    """
    Render the Reports page.
    """

    context.initialize()

    st.title("📄 Reports")

    if not context.has_session():
        st.info(
            "Load a session before generating reports.",
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
        "Executive Report",
        ("Generate an AI executive summary for " "ministry leadership."),
    )

    ai_panel.render(
        title="Executive Summary",
        button_label="✨ Generate Executive Summary",
        callback=context.ai_controller().generate_executive_summary,
        callback_kwargs={
            "report": report,
        },
        result_key="executive_summary",
        button_key="generate_executive_summary",
        help_text="Generate an executive report from the current session.",
        empty_message="Generate an executive summary to begin.",
    )

    st.divider()

    metric_cards.render_section_header(
        "Export",
        "Report export options coming in CP-009.",
    )

    st.info(
        "Upcoming export formats:\n\n"
        "• PDF Report\n"
        "• Excel Workbook\n"
        "• CSV Export\n"
        "• AI Executive Report"
    )
