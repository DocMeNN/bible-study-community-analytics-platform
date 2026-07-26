# src/presentation/pages/reports_page.py

"""
Reports Page

Purpose
-------
Displays reporting and AI executive reporting for the selected session.

Responsibilities
----------------
- Coordinate report presentation workflows.
- Consume the selected Session through the shared Session Selector.
- Display report metrics.
- Display session summary.
- Display AI executive report generation.
- Display export roadmap.
- Delegate report workflows to ReportViewModel.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
- No report generation.
- No file I/O.
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
from src.presentation.components.common import (
    metric_cards,
    session_selector,
    tables,
)
from src.presentation.utils import formatters

# ============================================================================
# Reports Page
# ============================================================================


def render() -> None:
    """
    Render the Reports page.
    """

    context.initialize()

    st.title("📄 Reports")

    if not context.has_session_collection():
        st.info(
            "No sessions loaded.\n\n"
            "Please load a WhatsApp chat from the Home page.",
        )
        return

    session = session_selector.render()

    if session is None:
        st.info(
            "No session is currently selected.",
        )
        return

    expected_attendees = context.expected_attendees()

    report_viewmodel = context.report_viewmodel()

    report_data = report_viewmodel.report_data(
        session=session,
        expected_attendees=expected_attendees,
    )

    summary = report_data["dashboard"]

    # ========================================================================
    # Report Overview
    # ========================================================================

    metric_cards.render_section_header(
        "Report Overview",
        "Summary statistics included in this report.",
    )

    metric_cards.render_metric_row(
        formatters.dashboard_metrics(
            summary,
        ),
    )

    st.divider()

    # ========================================================================
    # Session Summary
    # ========================================================================

    metric_cards.render_section_header(
        "Session Summary",
        "General information for the current meeting.",
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
        ),
    )

    st.divider()

    # ========================================================================
    # Session Highlights
    # ========================================================================

    metric_cards.render_section_header(
        "Session Highlights",
        "Important milestones from this meeting.",
    )

    tables.render_table(
        formatters.highlight_records(
            session=session,
            summary=summary,
        ),
    )

    st.divider()

    # ========================================================================
    # AI Executive Summary
    # ========================================================================

    ai_viewmodel = context.ai_viewmodel()

    report = ai_viewmodel.build_executive_report(
        session=session,
        dashboard_summary=report_data["dashboard"],
        attendance=report_data["attendance"],
        activity=report_data["activity"],
    )

    metric_cards.render_section_header(
        "AI Executive Report",
        "Generate an executive summary for ministry leadership.",
    )

    ministry_ai_panel.render(
        title="Executive Summary",
        button_label="✨ Generate Executive Summary",
        callback=context.ai_controller().generate_executive_summary,
        callback_kwargs={
            "report": report,
        },
        result_key="executive_summary",
        button_key="generate_executive_summary",
        help_text="Generate an executive report from the current session.",
        empty_message=(
            "Click 'Generate Executive Summary' "
            "to create an AI-powered leadership report."
        ),
    )

    st.divider()

    # ========================================================================
    # Export
    # ========================================================================

    metric_cards.render_section_header(
        "Export",
        "Export functionality planned for the next checkpoint.",
    )

    st.info(
        "Planned export formats:\n\n"
        "• PDF Ministry Report\n"
        "• Excel Workbook\n"
        "• CSV Export\n"
        "• AI Executive Summary\n"
        "• Printable Ministry Report",
    )

    st.divider()

    # ========================================================================
    # Footer
    # ========================================================================

    left_column, right_column = st.columns([3, 1])

    with left_column:
        st.caption(
            (
                f"Session Date: {session.session_date} | "
                f"Attendance: {summary['attendance_count']} | "
                f"Activities: {summary['activity_count']}"
            ),
        )

    with right_column:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()
