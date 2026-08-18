from __future__ import annotations

from collections import Counter
from typing import Any, cast

import streamlit as st

from src.presentation import context
from src.presentation.components.common import (
    charts,
    metric_cards,
    tables,
)
from src.presentation.utils import formatters


def render() -> None:
    context.initialize()

    st.title("?? Activity")

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
    summary = cast(
        dict[str, Any],
        scope_data["dashboard"],
    )
    activity = cast(
        dict[str, Any],
        scope_data["activity"],
    )

    scope_label = scope.period.value.capitalize()

    metric_cards.render_section_header(
        "Presentation Scope",
        (
            f"{scope_label} activity scope: "
            f"{scope.start_date} ? {scope.end_date} "
            f"({scope.session_count} Daily Session(s))."
        ),
    )

    st.caption(
        (
            f"Active scope: {scope_label} | "
            f"{scope.start_date} ? {scope.end_date} | "
            f"{scope.session_count} Daily Session(s)"
        ),
    )

    st.divider()

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

    metric_cards.render_section_header(
        "Activity Overview",
        f"Activity statistics for the active {scope_label.lower()} scope.",
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

    metric_cards.render_section_header(
        "Activity Distribution",
        (
            f"Distribution of recorded activities for the active "
            f"{scope_label.lower()} scope."
        ),
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
        title=f"{scope_label} Activity Distribution",
    )

    tables.render_dataframe(
        activity_dataframe,
    )

    st.divider()

    metric_cards.render_section_header(
        "Scope Activity",
        (
            f"Aggregated activity information for the active "
            f"{scope_label.lower()} scope."
        ),
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
        ),
    )

    st.divider()

    metric_cards.render_section_header(
        "Scope Highlights",
        f"Important milestones during the active {scope_label.lower()} scope.",
    )

    tables.render_table(
        formatters.highlight_records(
            session=session,
            summary=summary,
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
                f"{scope.start_date} ? {scope.end_date} | "
                f"Daily Sessions: {scope.session_count} | "
                f"Activities: {session.activity_count} | "
                f"Done Events: {session.done_count}"
            ),
        )

    with right_column:
        if st.button(
            "?? Refresh",
            use_container_width=True,
        ):
            st.rerun()

