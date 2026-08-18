# src/presentation/components/common/session_selector.py

"""
Hierarchical Session Selector

Presentation flow
-----------------

SessionCollection
        ↓
Grouping Configuration
        ↓
Session Group
        ↓
Selected Daily Session
        ↓
PresentationScope (managed by Context)

Responsibilities
----------------
- Render Presentation Scope selection.
- Apply GroupingConfiguration.
- Resolve SessionGroup.
- Resolve Daily Session.
- Delegate PresentationScope management to Context.

Architectural Rules
-------------------
- No business logic.
- No analytics.
- No parsing.
- No infrastructure access.
- No PresentationScope construction.

ADR-003
-------
The Presentation layer maintains exactly one active
PresentationScope.

Context owns PresentationScope lifecycle.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date

import streamlit as st

from src.domain.models.session import Session
from src.presentation import context
from src.presentation.grouping.grouping_configuration import (
    GroupingConfiguration,
)
from src.presentation.grouping.grouping_types import GroupingPeriod
from src.presentation.models.session_group import SessionGroup

# ============================================================================
# Constants
# ============================================================================

SCOPE_SELECTOR_KEY = "presentation_scope_selector"

GROUP_SELECTOR_KEY = "session_group_selector"


# ============================================================================
# Labels
# ============================================================================

_SCOPE_LABELS: dict[GroupingPeriod, str] = {
    GroupingPeriod.DAY: "Daily",
    GroupingPeriod.WEEK: "Weekly",
    GroupingPeriod.MONTH: "Monthly",
    GroupingPeriod.FIRST_HALF: "First Half of Year",
    GroupingPeriod.SECOND_HALF: "Last Half of Year",
    GroupingPeriod.YEAR: "Yearly",
}


# ============================================================================
# Helpers
# ============================================================================


def _scope_options() -> tuple[GroupingPeriod, ...]:
    """
    Return supported Presentation Scope options.
    """

    return tuple(_SCOPE_LABELS.keys())


def _scope_label(
    period: GroupingPeriod,
) -> str:
    """
    Return display label.
    """

    return _SCOPE_LABELS[period]


def _group_label(
    group: SessionGroup,
) -> str:
    """
    Return readable SessionGroup label.
    """

    return f"{group.start_date} – {group.end_date}"


def _current_scope_index(
    options: Sequence[GroupingPeriod],
) -> int:
    """
    Return the current grouping period index.
    """

    configuration = context.grouping_configuration()

    if configuration.period in options:
        return options.index(
            configuration.period,
        )

    return 0


def _apply_scope_selection(
    selected_period: GroupingPeriod,
) -> bool:
    """
    Apply Presentation Scope selection.

    Returns True when the grouping period changed.
    """

    current_configuration = context.grouping_configuration()

    if current_configuration.period == selected_period:
        return False

    context.set_grouping_configuration(
        GroupingConfiguration(
            period=selected_period,
            week_start_day=(current_configuration.week_start_day),
        ),
    )

    return True


def _current_group_index(
    groups: Sequence[SessionGroup],
    current_date: date | None,
) -> int:
    """
    Return the SessionGroup containing the
    current Daily Session.
    """

    if current_date is None:
        return 0

    for index, group in enumerate(groups):
        if (
            group.get_session(
                current_date,
            )
            is not None
        ):
            return index

    return 0


def _select_group(
    groups: tuple[SessionGroup, ...],
    current_date: date | None,
) -> SessionGroup:
    """
    Render SessionGroup selector.
    """

    labels = [_group_label(group) for group in groups]

    selected_index = _current_group_index(
        groups,
        current_date,
    )

    selected_label = st.selectbox(
        "Select Session Group",
        options=labels,
        index=selected_index,
        key=GROUP_SELECTOR_KEY,
        help=("Choose the presentation group containing the Daily Session."),
    )

    return groups[
        labels.index(
            selected_label,
        )
    ]


def _resolve_session(
    group: SessionGroup,
    current_date: date | None,
) -> Session | None:
    """
    Resolve the active Daily Session.
    """

    if not group.sessions:
        return None

    if current_date is not None:
        session = group.get_session(
            current_date,
        )

        if session is not None:
            return session

    return group.sessions[0]


def _persist_selected_session(
    selected_session: Session | None,
) -> None:
    """
    Persist the selected Daily Session.

    ADR-003:

    Context owns PresentationScope.

    Updating the selected Daily Session causes
    Context to rebuild the active
    PresentationScope automatically.
    """

    if selected_session is None:
        return

    if context.selected_session_date() != selected_session.session_date:
        context.set_selected_session(
            selected_session.session_date,
        )


# ============================================================================
# Public API
# ============================================================================


def render() -> Session | None:
    """
    Render hierarchical Session selection.

    Flow

    Session Collection
            ↓
    Presentation Scope
            ↓
    Session Group
            ↓
    Daily Session

    Context automatically rebuilds the active
    PresentationScope whenever the selected
    Daily Session changes.
    """

    session_collection = context.current_session_collection()

    if session_collection is None:
        return None

    if session_collection.is_empty:
        return None

    scope_options = _scope_options()

    selected_period = st.selectbox(
        "Presentation Scope",
        options=scope_options,
        index=_current_scope_index(
            scope_options,
        ),
        format_func=_scope_label,
        key=SCOPE_SELECTOR_KEY,
        help=("Choose how Daily Sessions are grouped for presentation."),
    )

    scope_changed = _apply_scope_selection(
        selected_period,
    )

    groups = tuple(
        context.grouped_sessions(),
    )

    if not groups:
        return None

    current_session = context.current_session()

    current_date = current_session.session_date if current_session is not None else None

    if scope_changed:
        st.session_state.pop(
            GROUP_SELECTOR_KEY,
            None,
        )

    selected_group = _select_group(
        groups,
        current_date,
    )

    selected_session = _resolve_session(
        selected_group,
        current_date,
    )

    _persist_selected_session(
        selected_session,
    )

    return selected_session


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "render",
]
