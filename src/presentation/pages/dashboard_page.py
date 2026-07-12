# src/presentation/pages/dashboard_page.py

"""
Dashboard Page

Purpose
-------
Displays the primary dashboard for a meeting session.

Responsibilities
----------------
- Display dashboard metrics.
- Display attendance analytics.
- Display activity analytics.
- Display session overview.
- Display AI-powered ministry insights.
- Delegate rendering to reusable presentation components.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics.
- No infrastructure access.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections import Counter
from typing import Any, cast

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation import context
from src.presentation.components import (
    charts,
    metric_cards,
    tables,
)
from src.presentation.components.ai import ai_panel
from src.presentation.utils import formatters
from src.presentation.viewmodels.ai_viewmodel import AIViewModel

# ============================================================================
# Dashboard Page
# ============================================================================


def render() -> None:
    """
    Render the dashboard page.
    """

    context.initialize()

    st.title("📊 Dashboard")

    if not context.has_session():
        st.info(
            "No session loaded.\n\n"
            "Please load a WhatsApp session from the Home page."
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

    summary = dashboard.dashboard_summary(
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

    # =====================================================================
    # Overview
    # =====================================================================

    metric_cards.render_section_header(
        "Overview",
        "Key performance indicators for this session.",
    )

    metric_cards.render_metric_row(
        formatters.dashboard_metrics(
            summary,
        ),
    )

    st.divider()

    # =====================================================================
    # AI Ministry Intelligence
    # =====================================================================

    metric_cards.render_section_header(
        "AI Ministry Intelligence",
        ("Generate an AI-powered summary of the current " "meeting session."),
    )

    viewmodel = AIViewModel(
        controller=context.ai_controller(),
    )

    session_information = viewmodel.build_session_information(
        session=session,
    )

    attendance_summary = viewmodel.build_attendance_summary(
        attendance=attendance,
    )

    activity_summary = viewmodel.build_activity_summary(
        activity=activity,
    )

    ai_panel.render(
        title="Session Summary",
        button_label="✨ Generate Session Summary",
        callback=context.ai_controller().generate_session_summary,
        callback_kwargs={
            "session_information": session_information,
            "attendance_summary": attendance_summary,
            "activity_summary": activity_summary,
        },
        result_key="dashboard_session_summary",
        button_key="dashboard_generate_summary",
        help_text="Generate an AI summary of this ministry session.",
        empty_message=(
            "Click 'Generate Session Summary' to create "
            "an AI-powered overview of this meeting."
        ),
    )

    st.divider()

    # =====================================================================
    # Attendance Analytics
    # =====================================================================

    metric_cards.render_section_header(
        "Attendance Analytics",
        "Attendance classifications for the current session.",
    )

    attendance_counts = cast(
        Counter[Any],
        attendance["attendance_types"],
    )

    attendance_dataframe = formatters.counter_to_dataframe(
        attendance_counts,
    )

    charts.render_bar_chart(
        attendance_dataframe,
        x="Category",
        y="Count",
        title="Attendance Distribution",
    )

    tables.render_dataframe(
        attendance_dataframe,
    )

    st.divider()

    # =====================================================================
    # Activity Analytics
    # =====================================================================

    metric_cards.render_section_header(
        "Activity Analytics",
        "Activity classifications recorded during the session.",
    )

    activity_counts = cast(
        Counter[Any],
        activity["activity_types"],
    )

    activity_dataframe = formatters.counter_to_dataframe(
        activity_counts,
    )

    charts.render_bar_chart(
        activity_dataframe,
        x="Category",
        y="Count",
        title="Activity Distribution",
    )

    tables.render_dataframe(
        activity_dataframe,
    )

    st.divider()

    # =====================================================================
    # Session Overview
    # =====================================================================

    metric_cards.render_section_header(
        "Session Overview",
        "General information for the current session.",
    )

    session_dataframe = formatters.session_summary(
        session,
    )

    tables.render_dataframe(
        session_dataframe,
    )

    st.divider()

    # =====================================================================
    # Session Highlights
    # =====================================================================

    metric_cards.render_section_header(
        "Session Highlights",
        "Important milestones from the session timeline.",
    )

    highlight_records = formatters.highlight_records(
        session=session,
        summary=summary,
    )

    tables.render_table(
        highlight_records,
    )

    st.divider()

    # =====================================================================
    # Footer
    # =====================================================================

    left_column, right_column = st.columns([3, 1])

    with left_column:
        st.caption(
            (
                f"Session Date: {session.session_date} | "
                f"Unique Attendees: {session.attendee_count} | "
                f"Attendance Events: {session.attendance_count} | "
                f"Done Events: {session.done_count} | "
                f"Activity Events: {session.activity_count}"
            )
        )

    with right_column:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()
