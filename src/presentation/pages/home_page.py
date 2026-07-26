# src/presentation/pages/home_page.py

"""
Home Page

Purpose
-------
Provides the landing workspace for the OYBS Attendance Dashboard.

Responsibilities
----------------
- Upload WhatsApp chat exports.
- Configure expected attendees.
- Delegate chat importing to ImportService.
- Store the resulting SessionCollection through Presentation Context.
- Provide the shared application-wide Session selector.
- Display imported session collection status.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
- No direct parsing.
- No Infrastructure access.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
import tempfile
from pathlib import Path

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation import context
from src.presentation.components.common import (
    filters,
    session_selector,
    sidebar,
)

# ============================================================================
# Constants
# ============================================================================

APPLICATION_NAME = "OYBS WhatsApp Attendance Dashboard"

# ============================================================================
# Helpers
# ============================================================================


def _render_sidebar() -> None:
    """
    Render the application sidebar.
    """

    sidebar.render_title("Application")

    sidebar.render_info(
        APPLICATION_NAME,
    )

    sidebar.render_divider()

    sidebar.render_section("Status")

    if context.has_session_collection():

        session_collection = (
            context.current_session_collection()
        )

        if session_collection is not None:

            sidebar.render_success(
                f"{session_collection.count} Sessions Loaded",
            )

        else:

            sidebar.render_warning(
                "No Sessions Loaded",
            )

    else:

        sidebar.render_warning(
            "No Sessions Loaded",
        )

    sidebar.render_divider()

    sidebar.render_text(
        f"Expected Attendees: {context.expected_attendees()}",
    )

    selected_session = context.current_session()

    if selected_session is not None:

        sidebar.render_text(
            (
                "Selected Session: "
                f"{selected_session.session_date}"
            ),
        )


def _render_configuration() -> None:
    """
    Render application configuration controls.
    """

    st.subheader("Configuration")

    expected_attendees = filters.render_number_input(
        label="Expected Attendees",
        value=context.expected_attendees(),
        minimum=0,
        maximum=1000,
    )

    context.set_expected_attendees(
        expected_attendees,
    )


def _render_upload() -> None:
    """
    Render the WhatsApp chat upload workflow.
    """

    st.subheader("Upload WhatsApp Chat")

    uploaded_file = st.file_uploader(
        "Select a WhatsApp exported chat (.txt)",
        type=["txt"],
    )

    if uploaded_file is None:
        return

    if not st.button(
        "Build Sessions",
        type="primary",
        use_container_width=True,
    ):
        return

    with st.spinner(
        "Detecting and building sessions...",
    ):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt",
        ) as temp_file:

            temp_file.write(
                uploaded_file.getvalue(),
            )

            temp_path = Path(
                temp_file.name,
            )

        try:

            session_collection = (
                context.import_service().import_chat(
                    temp_path,
                )
            )

            context.set_session_collection(
                session_collection,
            )

            st.success(
                (
                    f"{session_collection.count} "
                    "session(s) successfully loaded."
                ),
            )

            st.rerun()

        except Exception as exc:

            st.error(
                str(exc),
            )

        finally:

            temp_path.unlink(
                missing_ok=True,
            )


def _render_session_status() -> None:
    """
    Render the current SessionCollection status.
    """

    st.subheader("Imported Sessions")

    if not context.has_session_collection():

        st.info(
            "No sessions loaded.",
        )

        return

    session_collection = (
        context.current_session_collection()
    )

    if session_collection is None:
        return

    if session_collection.is_empty:

        st.info(
            (
                "The imported chat did not contain "
                "any detected sessions."
            ),
        )

        return

    first_session = (
        session_collection.first_session
    )

    last_session = (
        session_collection.last_session
    )

    if first_session is None or last_session is None:
        return

    left_column, middle_column, right_column = (
        st.columns(3)
    )

    with left_column:

        st.metric(
            "Sessions",
            session_collection.count,
        )

    with middle_column:

        st.metric(
            "First Session",
            str(session_collection.first_date),
        )

    with right_column:

        st.metric(
            "Last Session",
            str(session_collection.last_date),
        )

    st.divider()

    st.subheader("Active Session")

    session_selector.render()

    selected_session = context.current_session()

    if selected_session is not None:

        st.success(
            (
                "Active session: "
                f"{selected_session.session_date}"
            ),
        )

    st.divider()

    st.subheader("Session Timeline")

    st.dataframe(
        {
            "Session": range(
                1,
                session_collection.count + 1,
            ),
            "Date": [
                session.session_date
                for session in session_collection
            ],
            "Participants": [
                session.attendee_count
                for session in session_collection
            ],
            "Done Events": [
                session.done_count
                for session in session_collection
            ],
            "Activity Events": [
                session.activity_count
                for session in session_collection
            ],
        },
        use_container_width=True,
        hide_index=True,
    )


# ============================================================================
# Public API
# ============================================================================


def render() -> None:
    """
    Render the Home page.
    """

    context.initialize()

    _render_sidebar()

    st.title("🏠 Home")

    st.write(
        """
Welcome to the **OYBS WhatsApp Attendance Dashboard**.

Upload a WhatsApp chat export to begin analysing attendance,
activity and engagement across detected study sessions.
"""
    )

    st.divider()

    _render_configuration()

    st.divider()

    _render_upload()

    st.divider()

    _render_session_status()
