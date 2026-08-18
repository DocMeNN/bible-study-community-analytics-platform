# src/presentation/components/analytics/overview.py

"""
Multi-Session Analytics Overview Component

Purpose
-------
Render presentation metrics for a MultiSessionOverview.

Responsibilities
----------------
- Render presentation-only metrics.
- Display the selected date range.
- Display summary metric cards.
- Contain no business logic.
- Contain no analytics calculations.

Architectural Rules
-------------------
- Presentation layer only.
- No Domain dependencies.
- No Application services.
- No analytics calculations.
- No Streamlit session state.
"""

from __future__ import annotations

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation.dto.multi_session_overview import MultiSessionOverview

# ============================================================================
# Public Functions
# ============================================================================


def render_overview(
    overview: MultiSessionOverview,
) -> None:
    """
    Render the multi-session overview.

    Parameters
    ----------
    overview:
        Presentation DTO containing aggregated multi-session metrics.
    """

    st.subheader("Multi-Session Overview")

    if overview.start_date is not None and overview.end_date is not None:
        st.caption((f"{overview.start_date:%d %b %Y} - {overview.end_date:%d %b %Y}"))

    sessions_column, participants_column, activity_column = st.columns(3)

    with sessions_column:
        st.metric(
            label="Sessions",
            value=overview.session_count,
        )

        st.metric(
            label="Participants",
            value=overview.participant_count,
        )

    with participants_column:
        st.metric(
            label="Done Events",
            value=overview.done_events,
        )

    with activity_column:
        st.metric(
            label="Activity Events",
            value=overview.activity_events,
        )


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "render_overview",
]
