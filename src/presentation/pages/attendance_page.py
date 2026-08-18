# src/presentation/pages/attendance_page.py

"""
Attendance Page

Purpose
-------
Displays attendance analytics for the selected ministry session.

Responsibilities
----------------
- Coordinate the AttendanceViewModel.
- Consume the globally selected Session through Presentation Context.
- Display attendance session summary.
- Coordinate attendance presentation components.
- Display the attendance page footer.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
- No direct Application Service orchestration.
- Consume Application results through the Presentation ViewModel.
- Do not render the session selector locally.

Session Selection
-----------------
The unified session selector is rendered once by the application shell.

This page consumes the selected Session through:

    context.current_session()
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
from src.presentation.components.attendance import (
    distribution,
    overview,
)
from src.presentation.components.common import (
    metric_cards,
    tables,
)
from src.presentation.utils import formatters

# ============================================================================
# Attendance Page
# ============================================================================


def render() -> None:
    """
    Render the Attendance page.
    """

    context.initialize()

    st.title("👥 Attendance")

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

    attendance_viewmodel = context.attendance_viewmodel()

    attendance = attendance_viewmodel.attendance_data(
        session=session,
        expected_attendees=(context.expected_attendees()),
    )

    # =========================================================================
    # Attendance Overview
    # =========================================================================

    overview.render(
        attendance,
    )

    st.divider()

    # =========================================================================
    # Attendance Distribution
    # =========================================================================

    distribution.render(
        attendance,
    )

    st.divider()

    # =========================================================================
    # Session Summary
    # =========================================================================

    metric_cards.render_section_header(
        "Session Attendance",
        "Attendance information for this meeting.",
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
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
                f"Expected: {context.expected_attendees()} | "
                f"Present: {session.attendee_count}"
            ),
        )

    with right_column:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()
