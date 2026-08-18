from __future__ import annotations

import streamlit as st

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


def render() -> None:
    context.initialize()

    st.title("👥 Attendance")

    if not context.has_session_collection():
        st.info(
            "No sessions loaded.\n\nPlease load a WhatsApp chat from the Home page.",
        )
        return

    scope = context.ensure_presentation_scope()

    if scope is None:
        st.error("Unable to establish the active Presentation Scope.")
        return

    dashboard_viewmodel = context.dashboard_viewmodel()

    scope_data = dashboard_viewmodel.scope_dashboard_data(
        sessions=context.scope_sessions(),
        expected_attendees=context.expected_attendees(),
    )

    session = scope_data["scope_session"]
    attendance = scope_data["attendance"]

    scope_label = scope.period.value.capitalize()

    metric_cards.render_section_header(
        "Presentation Scope",
        (
            f"{scope_label} attendance scope: "
            f"{scope.start_date} → {scope.end_date} "
            f"({scope.session_count} Daily Session(s))."
        ),
    )

    st.caption(
        (
            f"Active scope: {scope_label} | "
            f"{scope.start_date} → {scope.end_date} | "
            f"{scope.session_count} Daily Session(s)"
        ),
    )

    st.divider()

    overview.render(
        attendance,
    )

    st.divider()

    distribution.render(
        attendance,
    )

    st.divider()

    metric_cards.render_section_header(
        "Scope Attendance",
        (
            f"Aggregated attendance information for the active "
            f"{scope_label.lower()} scope."
        ),
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
        ),
    )

    st.divider()

    left_column, right_column = st.columns(
        [3, 1],
    )

    with left_column:
        st.caption(
            (
                f"Scope: {scope_label} | "
                f"{scope.start_date} → {scope.end_date} | "
                f"Daily Sessions: {scope.session_count} | "
                f"Expected: {context.expected_attendees()} | "
                f"Unique Participants: {session.attendee_count}"
            ),
        )

    with right_column:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()
