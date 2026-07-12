# src/presentation/context.py

"""
Presentation Context

Purpose
-------
Provides a centralized state manager for the Presentation layer.

Responsibilities
----------------
- Manage Streamlit session state.
- Store the active Session aggregate.
- Provide access to application services.
- Provide access to presentation controllers.
- Provide access to presentation view models.
- Store presentation configuration values.
- Act as the bridge between the UI and the Application layer.

Architectural Rules
-------------------
- No business logic.
- No analytics.
- No parsing.
- No Infrastructure access outside object composition.
- No Domain calculations.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
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
from src.presentation.controllers.ai_controller import AIController
from src.presentation.viewmodels.ai_viewmodel import AIViewModel

# ============================================================================
# Session State Keys
# ============================================================================

_SESSION_KEY: Final = "current_session"
_EXPECTED_ATTENDEES_KEY: Final = "expected_attendees"

_ATTENDANCE_SERVICE_KEY: Final = "attendance_service"
_ACTIVITY_SERVICE_KEY: Final = "activity_service"
_DASHBOARD_SERVICE_KEY: Final = "dashboard_service"
_REPORT_SERVICE_KEY: Final = "report_service"
_IMPORT_SERVICE_KEY: Final = "import_service"

_AI_SERVICE_KEY: Final = "ai_service"
_AI_CONTROLLER_KEY: Final = "ai_controller"
_AI_VIEWMODEL_KEY: Final = "ai_viewmodel"

# ============================================================================
# Initialization
# ============================================================================


def initialize() -> None:
    """
    Initialize the presentation context.

    Safe to call multiple times.
    """

    state = st.session_state

    state.setdefault(
        _SESSION_KEY,
        None,
    )

    state.setdefault(
        _EXPECTED_ATTENDEES_KEY,
        0,
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
        ImportService(
            dashboard_service=cast(
                DashboardService,
                state[_DASHBOARD_SERVICE_KEY],
            ),
        ),
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


# ============================================================================
# Session
# ============================================================================


def set_session(session: Session) -> None:
    """
    Store the active Session.
    """

    st.session_state[_SESSION_KEY] = session


def current_session() -> Session | None:
    """
    Return the active Session.
    """

    return cast(
        Session | None,
        st.session_state[_SESSION_KEY],
    )


def has_session() -> bool:
    """
    Return True when a Session is loaded.
    """

    return current_session() is not None


def clear_session() -> None:
    """
    Remove the active Session.
    """

    st.session_state[_SESSION_KEY] = None


def set_expected_attendees(value: int) -> None:
    """
    Store the expected attendee count.
    """

    st.session_state[_EXPECTED_ATTENDEES_KEY] = value


def expected_attendees() -> int:
    """
    Return the configured expected attendee count.
    """

    return cast(
        int,
        st.session_state[_EXPECTED_ATTENDEES_KEY],
    )


# ============================================================================
# Services
# ============================================================================


def attendance_service() -> AttendanceService:
    """
    Return the AttendanceService.
    """

    return cast(
        AttendanceService,
        st.session_state[_ATTENDANCE_SERVICE_KEY],
    )


def activity_service() -> ActivityService:
    """
    Return the ActivityService.
    """

    return cast(
        ActivityService,
        st.session_state[_ACTIVITY_SERVICE_KEY],
    )


def dashboard_service() -> DashboardService:
    """
    Return the DashboardService.
    """

    return cast(
        DashboardService,
        st.session_state[_DASHBOARD_SERVICE_KEY],
    )


def report_service() -> ReportService:
    """
    Return the ReportService.
    """

    return cast(
        ReportService,
        st.session_state[_REPORT_SERVICE_KEY],
    )


def import_service() -> ImportService:
    """
    Return the ImportService.
    """

    return cast(
        ImportService,
        st.session_state[_IMPORT_SERVICE_KEY],
    )


def ai_service() -> AIService:
    """
    Return the shared AIService.
    """

    return cast(
        AIService,
        st.session_state[_AI_SERVICE_KEY],
    )


# ============================================================================
# Controllers
# ============================================================================


def ai_controller() -> AIController:
    """
    Return the AIController.
    """

    return cast(
        AIController,
        st.session_state[_AI_CONTROLLER_KEY],
    )


# ============================================================================
# View Models
# ============================================================================


def ai_viewmodel() -> AIViewModel:
    """
    Return the shared AIViewModel.
    """

    return cast(
        AIViewModel,
        st.session_state[_AI_VIEWMODEL_KEY],
    )


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "initialize",
    "set_session",
    "current_session",
    "has_session",
    "clear_session",
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
]
