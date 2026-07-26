# src/presentation/components/common/session_selector.py

"""
Hierarchical Session Selector

Presentation flow
-----------------
Grouping Period
        ?
Session Group
        ?
Daily Session
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.session import Session
from src.presentation import context

# ============================================================================
# Constants
# ============================================================================

GROUP_SELECTOR_KEY = "session_group_selector"
SESSION_SELECTOR_KEY = "shared_session_selector"

# ============================================================================
# Helpers
# ============================================================================


def _group_label(group: object) -> str:
    """
    Return a readable label for a SessionGroup.

    The grouping model owns the actual group boundaries.
    """

    start_date = getattr(
        group,
        "start_date",
    )

    end_date = getattr(
        group,
        "end_date",
    )

    return f"{start_date} – {end_date}"


def _group_sessions(group: object) -> tuple[Session, ...]:
    """
    Return the Daily Sessions contained in a SessionGroup.
    """

    sessions = getattr(
        group,
        "sessions",
    )

    return tuple(sessions)


# ============================================================================
# Public API
# ============================================================================


def render() -> Session | None:
    """
    Render hierarchical Session selection.

    The user first selects a presentation group, then a
    Daily Session within that group.
    """

    session_collection = (
        context.current_session_collection()
    )

    if session_collection is None:
        return None

    if session_collection.is_empty:
        return None

    groups = tuple(
        context.grouped_sessions(),
    )

    if not groups:
        return None

    group_labels = [
        _group_label(group)
        for group in groups
    ]

    current_session = context.current_session()

    current_date = (
        current_session.session_date
        if current_session is not None
        else None
    )

    selected_group_index = 0

    for index, group in enumerate(groups):

        group_dates = {
            session.session_date
            for session in _group_sessions(group)
        }

        if current_date in group_dates:

            selected_group_index = index
            break

    selected_group_label = st.selectbox(
        "Select Week",
        options=group_labels,
        index=selected_group_index,
        key=GROUP_SELECTOR_KEY,
        help=(
            "Select the study week containing "
            "the Daily Session to analyse."
        ),
    )

    selected_group = groups[
        group_labels.index(
            selected_group_label,
        )
    ]

    group_sessions = _group_sessions(
        selected_group,
    )

    session_dates = [
        session.session_date
        for session in group_sessions
    ]

    if current_date not in session_dates:

        current_date = session_dates[0]

        context.set_selected_session(
            current_date,
        )

    selected_session_date = st.selectbox(
        "Select Daily Session",
        options=session_dates,
        index=session_dates.index(
            current_date,
        ),
        format_func=str,
        key=SESSION_SELECTOR_KEY,
        help=(
            "Select the Daily Session to display "
            "throughout the application."
        ),
    )

    if selected_session_date != (
        context.selected_session_date()
    ):

        context.set_selected_session(
            selected_session_date,
        )

    return context.current_session()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "render",
]
