from __future__ import annotations

from collections import Counter
from typing import Any, cast

import streamlit as st

from src.presentation import context
from src.presentation.components.ai import ministry_ai_panel
from src.presentation.components.common import (
    charts,
    metric_cards,
    tables,
)
from src.presentation.utils import formatters


def render() -> None:
    context.initialize()

    st.title("📊 Dashboard")

    if not context.has_session_collection():
        st.info(
            "No sessions loaded.\n\nPlease import a WhatsApp chat from the Home page.",
        )
        return

    scope = context.ensure_presentation_scope()

    if scope is None:
        st.error("Unable to establish the active Presentation Scope.")
        return

    viewmodel = context.dashboard_viewmodel()

    dashboard_data = viewmodel.scope_dashboard_data(
        sessions=context.scope_sessions(),
        expected_attendees=context.expected_attendees(),
    )

    session = dashboard_data["scope_session"]

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

    scope_label = scope.period.value.capitalize()

    metric_cards.render_section_header(
        "Presentation Scope",
        (
            f"{scope_label} scope: "
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

    metric_cards.render_section_header(
        "Overview",
        f"Key performance indicators for the active {scope_label.lower()} scope.",
    )

    metric_cards.render_metric_row(
        formatters.dashboard_metrics(summary),
    )

    st.divider()

    try:
        metric_cards.render_section_header(
            "AI Ministry Intelligence",
            f"Generate AI intelligence for the active {scope_label.lower()} scope.",
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
            title="Scope Summary",
            button_label="✨ Generate Scope Summary",
            callback=context.ai_controller().generate_session_summary,
            callback_kwargs={
                "session_information": session_information,
                "attendance_summary": attendance_summary,
                "activity_summary": activity_summary,
            },
            result_key="dashboard_scope_summary",
            button_key="dashboard_generate_scope_summary",
            help_text=(
                f"Generate an AI summary of the active "
                f"{scope_label.lower()} presentation scope."
            ),
            empty_message=(
                f"Click 'Generate Scope Summary' to create an "
                f"AI-powered overview of the active "
                f"{scope_label.lower()} scope."
            ),
        )

    except Exception as exc:
        st.error(
            "Unable to load the AI Ministry Intelligence panel.",
        )
        st.exception(exc)

    metric_cards.render_section_header(
        "Attendance Analytics",
        f"Attendance classifications for the active {scope_label.lower()} scope.",
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
        title=f"{scope_label} Attendance Distribution",
    )

    tables.render_dataframe(
        attendance_dataframe,
    )

    st.divider()

    metric_cards.render_section_header(
        "Activity Analytics",
        f"Activity classifications for the active {scope_label.lower()} scope.",
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
        "Session Overview",
        (
            f"Aggregated overview for the active {scope_label.lower()} "
            f"presentation scope."
        ),
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
        ),
    )

    st.divider()

    metric_cards.render_section_header(
        "Session Highlights",
        f"Important milestones from the active {scope_label.lower()} scope.",
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
                f"{scope.start_date} → {scope.end_date} | "
                f"Daily Sessions: {scope.session_count} | "
                f"Unique Participants: {session.attendee_count} | "
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
