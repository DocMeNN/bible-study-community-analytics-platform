# src/presentation/context.py

"""
Presentation Context

Purpose
-------
Provides a centralized state manager for the Presentation layer.

Responsibilities
----------------
- Manage Streamlit session state.
- Store the active SessionCollection.
- Store presentation grouping state.
- Store the currently selected Session.
- Provide access to application services.
- Provide access to presentation controllers.
- Provide access to presentation ViewModels.
- Store presentation configuration values.

Architectural Rules
-------------------
- No business logic.
- No analytics.
- No parsing.
- No Infrastructure access outside object composition.
- No Domain calculations.

Multi-Level Session Presentation
--------------------------------
The Presentation layer stores the complete imported SessionCollection.

The Presentation layer may group Sessions for navigation.

The Domain remains centered on Daily Session.

The presentation flow is:

SessionCollection
        ↓
Session Grouping
        ↓
Selected Session Group
        ↓
Selected Daily Session
        ↓
Analytics
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from datetime import date
from typing import Final, cast

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.application.services.activity_service import ActivityService
from src.application.services.ai_service import AIService
from src.application.services.attendance_service import AttendanceService
from src.application.services.dashboard_service import DashboardService
from src.application.services.import_service import ImportService
from src.application.services.report_service import ReportService
from src.config.ai_config import load_ai_config
from src.domain.models.session import Session
from src.domain.models.session_collection import SessionCollection
from src.presentation.controllers.ai_controller import AIController
from src.presentation.grouping.grouping_configuration import (
    GroupingConfiguration,
)
from src.presentation.grouping.session_grouping_service import (
    SessionGroupingService,
)
from src.presentation.grouping.weekly_grouping_strategy import (
    WeeklyGroupingStrategy,
)
from src.presentation.viewmodels.activity_viewmodel import ActivityViewModel
from src.presentation.viewmodels.ai_viewmodel import AIViewModel
from src.presentation.viewmodels.attendance_viewmodel import (
    AttendanceViewModel,
)
from src.presentation.viewmodels.dashboard_viewmodel import (
    DashboardViewModel,
)
from src.presentation.viewmodels.report_viewmodel import ReportViewModel

# ============================================================================
# Session State Keys
# ============================================================================

_SESSION_COLLECTION_KEY: Final = "session_collection"
_SELECTED_SESSION_DATE_KEY: Final = "selected_session_date"
_SELECTED_GROUP_KEY: Final = "selected_session_group"
_EXPECTED_ATTENDEES_KEY: Final = "expected_attendees"

_GROUPING_SERVICE_KEY: Final = "session_grouping_service"
_GROUPING_CONFIGURATION_KEY: Final = "grouping_configuration"

_ATTENDANCE_SERVICE_KEY: Final = "attendance_service"
_ACTIVITY_SERVICE_KEY: Final = "activity_service"
_DASHBOARD_SERVICE_KEY: Final = "dashboard_service"
_REPORT_SERVICE_KEY: Final = "report_service"
_IMPORT_SERVICE_KEY: Final = "import_service"

_AI_SERVICE_KEY: Final = "ai_service"
_AI_CONTROLLER_KEY: Final = "ai_controller"

_AI_VIEWMODEL_KEY: Final = "ai_viewmodel"
_ATTENDANCE_VIEWMODEL_KEY: Final = "attendance_viewmodel"
_ACTIVITY_VIEWMODEL_KEY: Final = "activity_viewmodel"
_DASHBOARD_VIEWMODEL_KEY: Final = "dashboard_viewmodel"
_REPORT_VIEWMODEL_KEY: Final = "report_viewmodel"


# ============================================================================
# Initialization
# ============================================================================


def initialize() -> None:
    """
    Initialize the Presentation Context.

    Safe to call multiple times.
    """

    state = st.session_state

    state.setdefault(
        _SESSION_COLLECTION_KEY,
        None,
    )

    state.setdefault(
        _SELECTED_SESSION_DATE_KEY,
        None,
    )

    state.setdefault(
        _SELECTED_GROUP_KEY,
        None,
    )

    state.setdefault(
        _EXPECTED_ATTENDEES_KEY,
        0,
    )

    state.setdefault(
        _GROUPING_CONFIGURATION_KEY,
        GroupingConfiguration.weekly(),
    )

    grouping_configuration = cast(
        GroupingConfiguration,
        state[_GROUPING_CONFIGURATION_KEY],
    )

    state.setdefault(
        _GROUPING_SERVICE_KEY,
        SessionGroupingService(
            strategy=WeeklyGroupingStrategy(
                week_start_day=(
                    grouping_configuration.week_start_day
                ),
            ),
            period=grouping_configuration.period,
        ),
    )

    state.setdefault(
        _ATTENDANCE_SERVICE_KEY,
        AttendanceService(),
    )

    state.setdefault(
        _ACTIVITY_SERVICE_KEY,
        ActivityService(),
    )

    state.setdefault(
        _DASHBOARD_SERVICE_KEY,
        DashboardService(
            attendance_service=cast(
                AttendanceService,
                state[_ATTENDANCE_SERVICE_KEY],
            ),
            activity_service=cast(
                ActivityService,
                state[_ACTIVITY_SERVICE_KEY],
            ),
        ),
    )

    state.setdefault(
        _REPORT_SERVICE_KEY,
        ReportService(
            attendance_service=cast(
                AttendanceService,
                state[_ATTENDANCE_SERVICE_KEY],
            ),
            activity_service=cast(
                ActivityService,
                state[_ACTIVITY_SERVICE_KEY],
            ),
            dashboard_service=cast(
                DashboardService,
                state[_DASHBOARD_SERVICE_KEY],
            ),
        ),
    )

    state.setdefault(
        _IMPORT_SERVICE_KEY,
        ImportService(),
    )

    state.setdefault(
        _AI_SERVICE_KEY,
        AIService(
            config=load_ai_config(),
        ),
    )

    state.setdefault(
        _AI_CONTROLLER_KEY,
        AIController(
            ai_service=cast(
                AIService,
                state[_AI_SERVICE_KEY],
            ),
        ),
    )

    state.setdefault(
        _AI_VIEWMODEL_KEY,
        AIViewModel(
            controller=cast(
                AIController,
                state[_AI_CONTROLLER_KEY],
            ),
        ),
    )

    state.setdefault(
        _ATTENDANCE_VIEWMODEL_KEY,
        AttendanceViewModel(
            attendance_service=cast(
                AttendanceService,
                state[_ATTENDANCE_SERVICE_KEY],
            ),
        ),
    )

    state.setdefault(
        _ACTIVITY_VIEWMODEL_KEY,
        ActivityViewModel(
            activity_service=cast(
                ActivityService,
                state[_ACTIVITY_SERVICE_KEY],
            ),
        ),
    )

    state.setdefault(
        _DASHBOARD_VIEWMODEL_KEY,
        DashboardViewModel(
            dashboard_service=cast(
                DashboardService,
                state[_DASHBOARD_SERVICE_KEY],
            ),
        ),
    )

    state.setdefault(
        _REPORT_VIEWMODEL_KEY,
        ReportViewModel(
            report_service=cast(
                ReportService,
                state[_REPORT_SERVICE_KEY],
            ),
        ),
    )


# ============================================================================
# Session Collection
# ============================================================================


def set_session_collection(
    session_collection: SessionCollection,
) -> None:
    """
    Store the active SessionCollection.

    The first session is selected automatically.
    """

    st.session_state[_SESSION_COLLECTION_KEY] = session_collection

    if session_collection.has_sessions:

        first_session = session_collection.first_session

        if first_session is not None:

            st.session_state[
                _SELECTED_SESSION_DATE_KEY
            ] = first_session.session_date

    else:

        st.session_state[
            _SELECTED_SESSION_DATE_KEY
        ] = None

    st.session_state[
        _SELECTED_GROUP_KEY
    ] = None


def current_session_collection() -> SessionCollection | None:
    """Return the active SessionCollection."""

    return cast(
        SessionCollection | None,
        st.session_state[_SESSION_COLLECTION_KEY],
    )


def has_session_collection() -> bool:
    """Return True when a SessionCollection is loaded."""

    return current_session_collection() is not None


def clear_session_collection() -> None:
    """Remove the active SessionCollection and selection state."""

    st.session_state[_SESSION_COLLECTION_KEY] = None
    st.session_state[_SELECTED_SESSION_DATE_KEY] = None
    st.session_state[_SELECTED_GROUP_KEY] = None


# ============================================================================
# Grouping
# ============================================================================


def grouping_service() -> SessionGroupingService:
    """Return the SessionGroupingService."""

    return cast(
        SessionGroupingService,
        st.session_state[_GROUPING_SERVICE_KEY],
    )


def grouping_configuration() -> GroupingConfiguration:
    """Return the active grouping configuration."""

    return cast(
        GroupingConfiguration,
        st.session_state[_GROUPING_CONFIGURATION_KEY],
    )


def grouped_sessions() -> tuple:
    """
    Return the current presentation grouping.

    Returns
    -------
    tuple
        Presentation session groups.
    """

    session_collection = current_session_collection()

    if session_collection is None:
        return ()

    return grouping_service().group(
        session_collection,
    )


# ============================================================================
# Selected Session
# ============================================================================


def set_selected_session(
    session_date: date,
) -> None:
    """Select a Session by its session date."""

    session_collection = current_session_collection()

    if session_collection is None:
        raise RuntimeError(
            "Cannot select a session without a SessionCollection.",
        )

    if not session_collection.contains_date(
        session_date,
    ):
        raise ValueError(
            f"No session exists for date: {session_date}.",
        )

    st.session_state[
        _SELECTED_SESSION_DATE_KEY
    ] = session_date


def selected_session_date() -> date | None:
    """Return the selected Session date."""

    return cast(
        date | None,
        st.session_state[_SELECTED_SESSION_DATE_KEY],
    )


def current_session() -> Session | None:
    """Return the currently selected Session."""

    session_collection = current_session_collection()

    if session_collection is None:
        return None

    session_date = selected_session_date()

    if session_date is None:
        return None

    return session_collection.get_session(
        session_date,
    )


def has_selected_session() -> bool:
    """Return True when a Session is currently selected."""

    return current_session() is not None


# ============================================================================
# Expected Attendees
# ============================================================================


def set_expected_attendees(
    value: int,
) -> None:
    """Store the expected attendee count."""

    st.session_state[_EXPECTED_ATTENDEES_KEY] = value


def expected_attendees() -> int:
    """Return the configured expected attendee count."""

    return cast(
        int,
        st.session_state[_EXPECTED_ATTENDEES_KEY],
    )


# ============================================================================
# Application Services
# ============================================================================


def attendance_service() -> AttendanceService:
    """Return the AttendanceService."""

    return cast(
        AttendanceService,
        st.session_state[_ATTENDANCE_SERVICE_KEY],
    )


def activity_service() -> ActivityService:
    """Return the ActivityService."""

    return cast(
        ActivityService,
        st.session_state[_ACTIVITY_SERVICE_KEY],
    )


def dashboard_service() -> DashboardService:
    """Return the DashboardService."""

    return cast(
        DashboardService,
        st.session_state[_DASHBOARD_SERVICE_KEY],
    )


def report_service() -> ReportService:
    """Return the ReportService."""

    return cast(
        ReportService,
        st.session_state[_REPORT_SERVICE_KEY],
    )


def import_service() -> ImportService:
    """Return the ImportService."""

    return cast(
        ImportService,
        st.session_state[_IMPORT_SERVICE_KEY],
    )


def ai_service() -> AIService:
    """Return the shared AIService."""

    return cast(
        AIService,
        st.session_state[_AI_SERVICE_KEY],
    )


# ============================================================================
# Controllers
# ============================================================================


def ai_controller() -> AIController:
    """Return the AIController."""

    return cast(
        AIController,
        st.session_state[_AI_CONTROLLER_KEY],
    )


# ============================================================================
# ViewModels
# ============================================================================


def ai_viewmodel() -> AIViewModel:
    """Return the shared AIViewModel."""

    return cast(
        AIViewModel,
        st.session_state[_AI_VIEWMODEL_KEY],
    )


def attendance_viewmodel() -> AttendanceViewModel:
    """Return the shared AttendanceViewModel."""

    return cast(
        AttendanceViewModel,
        st.session_state[_ATTENDANCE_VIEWMODEL_KEY],
    )


def activity_viewmodel() -> ActivityViewModel:
    """Return the shared ActivityViewModel."""

    return cast(
        ActivityViewModel,
        st.session_state[_ACTIVITY_VIEWMODEL_KEY],
    )


def dashboard_viewmodel() -> DashboardViewModel:
    """Return the shared DashboardViewModel."""

    return cast(
        DashboardViewModel,
        st.session_state[_DASHBOARD_VIEWMODEL_KEY],
    )


def report_viewmodel() -> ReportViewModel:
    """Return the shared ReportViewModel."""

    return cast(
        ReportViewModel,
        st.session_state[_REPORT_VIEWMODEL_KEY],
    )


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "initialize",
    "set_session_collection",
    "current_session_collection",
    "has_session_collection",
    "clear_session_collection",
    "grouping_service",
    "grouping_configuration",
    "grouped_sessions",
    "set_selected_session",
    "selected_session_date",
    "current_session",
    "has_selected_session",
    "set_expected_attendees",
    "expected_attendees",
    "attendance_service",
    "activity_service",
    "dashboard_service",
    "report_service",
    "import_service",
    "ai_service",
    "ai_controller",
    "ai_viewmodel",
    "attendance_viewmodel",
    "activity_viewmodel",
    "dashboard_viewmodel",
    "report_viewmodel",
]
