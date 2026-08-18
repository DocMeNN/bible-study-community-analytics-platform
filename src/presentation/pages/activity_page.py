# src/presentation/pages/activity_page.py

"""
Activity Page

Purpose
-------
Displays activity analytics for the selected ministry session.

Responsibilities
----------------
- Coordinate activity presentation workflows.
- Consume the globally selected Session through Presentation Context.
- Display activity KPIs.
- Display activity distribution.
- Display session activity summary.
- Delegate activity workflows to ActivityViewModel.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
- No infrastructure access.
- Do not render the unified session selector locally.
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
from src.presentation.components.common import (
    charts,
    metric_cards,
    tables,
)
from src.presentation.utils import formatters

# ============================================================================
# Activity Page
# ============================================================================


def render() -> None:
    """
    Render the Activity page.
    """

    context.initialize()

    st.title("📈 Activity")

    if not context.has_session_collection():
        st.info(
            "No sessions loaded.\n\nPlease load a WhatsApp chat from the Home page.",
        )

        return

    session = context.current_session()

    if session is None:
        st.info(
            "No session is currently selected.",
        )

        return

    activity_viewmodel = context.activity_viewmodel()

    activity = activity_viewmodel.activity_data(
        session=session,
    )

    dashboard_viewmodel = context.dashboard_viewmodel()

    summary = dashboard_viewmodel.dashboard_summary(
        session=session,
        expected_attendees=(context.expected_attendees()),
    )

    # =========================================================================
    # Typed Values
    # =========================================================================

    activity_count = cast(
        int,
        summary["activity_count"],
    )

    done_count = cast(
        int,
        summary["done_count"],
    )

    attendance_count = cast(
        int,
        summary["attendance_count"],
    )

    attendance_rate = cast(
        float,
        summary["attendance_rate"],
    )

    # =========================================================================
    # Activity Overview
    # =========================================================================

    metric_cards.render_section_header(
        "Activity Overview",
        "Activity statistics for the current session.",
    )

    metric_cards.render_metric_row(
        [
            (
                "Activities",
                activity_count,
                None,
                "Total recorded activities",
            ),
            (
                "Done",
                done_count,
                None,
                "Done acknowledgements",
            ),
            (
                "Attendees",
                attendance_count,
                None,
                "Unique attendees",
            ),
            (
                "Attendance %",
                formatters.percentage(
                    attendance_rate,
                ),
                None,
                "Attendance rate",
            ),
        ],
    )

    st.divider()

    # =========================================================================
    # Activity Distribution
    # =========================================================================

    metric_cards.render_section_header(
        "Activity Distribution",
        "Distribution of recorded activities.",
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

    # =========================================================================
    # Session Summary
    # =========================================================================

    metric_cards.render_section_header(
        "Session Activity",
        "General activity information for this meeting.",
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
        ),
    )

    st.divider()

    # =========================================================================
    # Session Highlights
    # =========================================================================

    metric_cards.render_section_header(
        "Session Highlights",
        "Important milestones during the session.",
    )

    tables.render_table(
        formatters.highlight_records(
            session=session,
            summary=summary,
        ),
    )

    st.divider()

    # =========================================================================
    # Footer
    # =========================================================================

    left_column, right_column = st.columns(
        [3, 1],
    )

    with left_column:
        st.caption(
            (
                f"Session Date: {session.session_date} | "
                f"Activities: {session.activity_count} | "
                f"Done Events: {session.done_count}"
            ),
        )

    with right_column:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()
