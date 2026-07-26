# src/presentation/pages/dashboard_page.py

"""
Dashboard Page

Purpose
-------
Displays the primary dashboard for a selected study session.

Responsibilities
----------------
- Coordinate dashboard presentation workflows.
- Select a Session from the active SessionCollection.
- Persist the selected Session through the shared Session Selector.
- Display dashboard metrics.
- Display attendance analytics.
- Display activity analytics.
- Display session overview.
- Display AI-powered ministry insights.
- Delegate application workflows to DashboardViewModel.
- Delegate rendering to reusable presentation components.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
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
from src.presentation.components.ai import ministry_ai_panel
from src.presentation.components.common import (
    charts,
    metric_cards,
    session_selector,
    tables,
)
from src.presentation.utils import formatters

# ============================================================================
# Dashboard Page
# ============================================================================


def render() -> None:
    """
    Render the Dashboard page.
    """

    context.initialize()

    st.title("📊 Dashboard")

    if not context.has_session_collection():
        st.info(
            "No sessions loaded.\n\n"
            "Please import a WhatsApp chat from the Home page.",
        )
        return

    session = session_selector.render()

    if session is None:
        st.error(
            "Unable to retrieve the selected session.",
        )
        return

    viewmodel = context.dashboard_viewmodel()

    expected_attendees = context.expected_attendees()

    dashboard_data = viewmodel.get_dashboard(
        session=session,
        expected_attendees=expected_attendees,
    )

    summary = cast(
        dict[str, Any],
        dashboard_data["dashboard"],
    )

    attendance = cast(
        dict[str, Any],
        dashboard_data["attendance"],
    )

    activity = cast(
        dict[str, Any],
        dashboard_data["activity"],
    )

    # ========================================================================
    # Overview
    # ========================================================================

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

    # ========================================================================
    # AI Ministry Intelligence
    # ========================================================================

    try:

        metric_cards.render_section_header(
            "AI Ministry Intelligence",
            "Generate an AI-powered summary of the current meeting session.",
        )

        ai_viewmodel = context.ai_viewmodel()

        session_information = ai_viewmodel.build_session_information(
            session=session,
        )

        attendance_summary = ai_viewmodel.build_attendance_summary(
            attendance=attendance,
        )

        activity_summary = ai_viewmodel.build_activity_summary(
            activity=activity,
        )

        ministry_ai_panel.render(
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

    except Exception as exc:

        st.error(
            "Unable to load the AI Ministry Intelligence panel.",
        )

        st.exception(exc)

    # ========================================================================
    # Attendance Analytics
    # ========================================================================

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

    # ========================================================================
    # Activity Analytics
    # ========================================================================

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

    # ========================================================================
    # Session Overview
    # ========================================================================

    metric_cards.render_section_header(
        "Session Overview",
        "General information for the selected session.",
    )

    session_dataframe = formatters.session_summary(
        session,
    )

    tables.render_dataframe(
        session_dataframe,
    )

    st.divider()

    # ========================================================================
    # Session Highlights
    # ========================================================================

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

    # ========================================================================
    # Footer
    # ========================================================================

    left_column, right_column = st.columns([3, 1])

    with left_column:
        st.caption(
            (
                f"Session Date: {session.session_date} | "
                f"Unique Attendees: {session.attendee_count} | "
                f"Attendance Events: {session.attendance_count} | "
                f"Done Events: {session.done_count} | "
                f"Activity Events: {session.activity_count}"
            ),
        )

    with right_column:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()
