# src/presentation/pages/analytics_page.py

"""
Analytics Page

Purpose
-------
Displays Multi-Session Analytics across selected Daily Sessions.

Responsibilities
----------------
- Consume the selected SessionCollection from Presentation Context.
- Delegate multi-session analytics to DashboardViewModel.
- Render reusable analytics presentation components.
- Display scope-based aggregated analytics.

Architectural Rules
-------------------
- Presentation layer only.
- No business logic.
- No analytics calculations.
- No infrastructure access.
- No direct Domain processing.
- No Streamlit session manipulation outside Presentation.

Architecture
------------
Analytics Page
        |
        v
DashboardViewModel
        |
        v
MultiSessionAnalyticsService
        |
        v
MultiSessionOverview (Presentation DTO)
        |
        v
Analytics Components
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
from src.presentation.components.analytics import (
    overview,
    scope_summary,
)
from src.presentation.dto.multi_session_overview import (
    MultiSessionOverview,
)

# ============================================================================
# Analytics Page
# ============================================================================


def render() -> None:
    """
    Render the Multi-Session Analytics page.
    """

    context.initialize()

    st.title("📈 Multi-Session Analytics")

    if not context.has_session_collection():
        st.info(
            "No sessions loaded.\n\nPlease import a WhatsApp chat from the Home page.",
        )

        return

    session_collection = context.current_session_collection()

    if session_collection is None:
        st.error(
            "Unable to retrieve the session collection.",
        )

        return

    viewmodel = context.dashboard_viewmodel()

    presentation_data = viewmodel.multi_session_presentation_data(
        sessions=session_collection.sessions,
    )

    overview_data = presentation_data["overview"]

    if not isinstance(
        overview_data,
        MultiSessionOverview,
    ):
        raise TypeError(
            "Expected MultiSessionOverview from DashboardViewModel.",
        )

    # =====================================================================
    # Scope Summary
    # =====================================================================

    scope_summary.render_scope_summary(
        overview_data,
    )

    st.divider()

    # =====================================================================
    # Overview Metrics
    # =====================================================================

    overview.render_overview(
        overview_data,
    )

    st.divider()

    # =====================================================================
    # Placeholder
    # =====================================================================

    st.subheader("Analytics Expansion")

    st.info(
        "Trend analysis, attendance patterns, activity rankings, "
        "distribution charts, engagement analytics, and comparative "
        "reporting will be integrated in subsequent CP-017 milestones.",
    )


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "render",
]
