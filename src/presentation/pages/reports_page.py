"""
Reports Page

Presentation-scope-aware reporting.
"""

from __future__ import annotations

from typing import Any, cast

import streamlit as st

from src.presentation import context
from src.presentation.components.ai import ministry_ai_panel
from src.presentation.components.common import (
    metric_cards,
    tables,
)
from src.presentation.utils import formatters


def render() -> None:
    """Render the Reports page for the active Presentation Scope."""

    context.initialize()

    st.title("📄 Reports")

    if not context.has_session_collection():
        st.info(
            "No sessions loaded.\n\n"
            "Please load a WhatsApp chat from the Home page.",
        )
        return

    scope = context.ensure_presentation_scope()

    if scope is None:
        st.error(
            "Unable to establish the active Presentation Scope.",
        )
        return

    dashboard_viewmodel = context.dashboard_viewmodel()

    scope_data = dashboard_viewmodel.scope_dashboard_data(
        sessions=context.scope_sessions(),
        expected_attendees=context.expected_attendees(),
    )

    session = scope_data["scope_session"]

    if session is None:
        st.error(
            "Unable to build the active Presentation Scope report.",
        )
        return

    summary = cast(
        dict[str, Any],
        scope_data["dashboard"],
    )

    attendance = scope_data["attendance"]
    activity = scope_data["activity"]

    scope_label = scope.period.value.capitalize()

    # ========================================================================
    # Presentation Scope
    # ========================================================================

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

    # ========================================================================
    # Report Overview
    # ========================================================================

    metric_cards.render_section_header(
        "Report Overview",
        (
            f"Aggregated report statistics for the active "
            f"{scope_label.lower()} scope."
        ),
    )

    metric_cards.render_metric_row(
        formatters.dashboard_metrics(
            summary,
        ),
    )

    st.divider()

    # ========================================================================
    # Scope Summary
    # ========================================================================

    metric_cards.render_section_header(
        "Scope Summary",
        (
            f"Aggregated information for the active "
            f"{scope_label.lower()} presentation scope."
        ),
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
        ),
    )

    st.divider()

    # ========================================================================
    # Scope Highlights
    # ========================================================================

    metric_cards.render_section_header(
        "Scope Highlights",
        (
            f"Important milestones from the active "
            f"{scope_label.lower()} scope."
        ),
    )

    tables.render_table(
        formatters.highlight_records(
            session=session,
            summary=summary,
        ),
    )

    st.divider()

    # ========================================================================
    # AI Executive Report
    # ========================================================================

    try:
        ai_viewmodel = context.ai_viewmodel()

        report = ai_viewmodel.build_executive_report(
            session=session,
            dashboard_summary=summary,
            attendance=attendance,
            activity=activity,
        )

        metric_cards.render_section_header(
            "AI Executive Report",
            (
                f"Generate an executive report for the active "
                f"{scope_label.lower()} presentation scope."
            ),
        )

        ministry_ai_panel.render(
            title=f"{scope_label} Executive Summary",
            button_label="✨ Generate Executive Summary",
            callback=context.ai_controller().generate_executive_summary,
            callback_kwargs={
                "report": report,
            },
            result_key="executive_scope_summary",
            button_key="generate_executive_scope_summary",
            help_text=(
                f"Generate an AI-powered executive report for the "
                f"active {scope_label.lower()} scope."
            ),
            empty_message=(
                "Click 'Generate Executive Summary' "
                "to create an AI-powered leadership report."
            ),
        )

    except Exception as exc:
        st.error(
            "Unable to load the AI Executive Report.",
        )
        st.exception(exc)

    st.divider()

    # ========================================================================
    # Footer
    # ========================================================================

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
