# src/presentation/context.py

"""
Presentation Context

Purpose
-------
Provides the centralized Presentation state manager for the application.

Responsibilities
----------------
- Manage Streamlit session state.
- Store the active SessionCollection.
- Store the active PresentationScope.
- Store presentation grouping configuration.
- Store the selected Daily Session.
- Compose Presentation-layer services.
- Provide shared ViewModels and Controllers.

Architectural Rules
-------------------
- No business logic.
- No analytics.
- No parsing.
- No Infrastructure access outside object composition.
- No Domain calculations.

ADR-003
-------
The Presentation layer maintains exactly one active
PresentationScope.
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
# Application Services
# ============================================================================
from src.application.services.activity_service import ActivityService
from src.application.services.ai_service import AIService
from src.application.services.attendance_service import AttendanceService
from src.application.services.dashboard_service import DashboardService
from src.application.services.import_service import ImportService
from src.application.services.report_service import ReportService

# ============================================================================
# Configuration
# ============================================================================
from src.config.ai_config import load_ai_config

# ============================================================================
# Domain Models
# ============================================================================
from src.domain.models.session import Session
from src.domain.models.session_collection import SessionCollection

# ============================================================================
# Presentation Controllers
# ============================================================================
from src.presentation.controllers.ai_controller import AIController

# ============================================================================
# Presentation Grouping
# ============================================================================
from src.presentation.grouping.daily_grouping_strategy import (
    DailyGroupingStrategy,
)
from src.presentation.grouping.first_half_grouping_strategy import (
    FirstHalfGroupingStrategy,
)
from src.presentation.grouping.grouping_configuration import (
    GroupingConfiguration,
)
from src.presentation.grouping.grouping_strategy import (
    GroupingStrategy,
)
from src.presentation.grouping.grouping_types import (
    GroupingPeriod,
)
from src.presentation.grouping.monthly_grouping_strategy import (
    MonthlyGroupingStrategy,
)
from src.presentation.grouping.second_half_grouping_strategy import (
    SecondHalfGroupingStrategy,
)
from src.presentation.grouping.session_grouping_service import (
    SessionGroupingService,
)
from src.presentation.grouping.weekly_grouping_strategy import (
    WeeklyGroupingStrategy,
)
from src.presentation.grouping.yearly_grouping_strategy import (
    YearlyGroupingStrategy,
)

# ============================================================================
# Presentation Models
# ============================================================================
from src.presentation.models.presentation_scope import (
    PresentationScope,
)
from src.presentation.models.session_group import (
    SessionGroup,
)

# ============================================================================
# Presentation ViewModels
# ============================================================================
from src.presentation.viewmodels.activity_viewmodel import (
    ActivityViewModel,
)
from src.presentation.viewmodels.ai_viewmodel import (
    AIViewModel,
)
from src.presentation.viewmodels.attendance_viewmodel import (
    AttendanceViewModel,
)
from src.presentation.viewmodels.dashboard_viewmodel import (
    DashboardViewModel,
)
from src.presentation.viewmodels.report_viewmodel import (
    ReportViewModel,
)

# ============================================================================
# Session State Keys
# ============================================================================

_SESSION_COLLECTION_KEY: Final = "session_collection"
_SELECTED_SESSION_DATE_KEY: Final = "selected_session_date"
_ACTIVE_PRESENTATION_SCOPE_KEY: Final = "active_presentation_scope"

_EXPECTED_ATTENDEES_KEY: Final = "expected_attendees"

_GROUPING_CONFIGURATION_KEY: Final = "grouping_configuration"
_GROUPING_SERVICE_KEY: Final = "session_grouping_service"

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
# Internal Builders
# ============================================================================


def _build_grouping_strategy(
    configuration: GroupingConfiguration,
) -> GroupingStrategy:
    """
    Build the Presentation grouping strategy.
    """

    period = configuration.period

    #
    # IMPORTANT
    #
    # Normalize values that may have been restored by
    # Streamlit Session State as plain strings.
    #
    if isinstance(period, str):
        period = GroupingPeriod(period)

    if period == GroupingPeriod.DAY:
        return DailyGroupingStrategy()

    if period == GroupingPeriod.WEEK:
        return WeeklyGroupingStrategy(
            week_start_day=configuration.week_start_day,
        )

    if period == GroupingPeriod.MONTH:
        return MonthlyGroupingStrategy()

    if period == GroupingPeriod.FIRST_HALF:
        return FirstHalfGroupingStrategy()

    if period == GroupingPeriod.SECOND_HALF:
        return SecondHalfGroupingStrategy()

    if period == GroupingPeriod.YEAR:
        return YearlyGroupingStrategy()

    raise ValueError(
        f"Unsupported grouping period: {period}",
    )


def _build_grouping_service(
    configuration: GroupingConfiguration,
) -> SessionGroupingService:
    """
    Build the SessionGroupingService.
    """

    period = configuration.period

    #
    # Normalize restored enum values.
    #
    if isinstance(period, str):
        period = GroupingPeriod(period)

    return SessionGroupingService(
        strategy=_build_grouping_strategy(
            configuration,
        ),
        period=period,
    )


# ============================================================================
# Initialization
# ============================================================================


def initialize() -> None:
    """
    Initialize the Presentation Context.

    Safe to call multiple times.
    """

    state = st.session_state

    # ------------------------------------------------------------------------
    # Core Presentation State
    # ------------------------------------------------------------------------

    state.setdefault(
        _SESSION_COLLECTION_KEY,
        None,
    )

    state.setdefault(
        _SELECTED_SESSION_DATE_KEY,
        None,
    )

    state.setdefault(
        _ACTIVE_PRESENTATION_SCOPE_KEY,
        None,
    )

    state.setdefault(
        _EXPECTED_ATTENDEES_KEY,
        0,
    )

    # ------------------------------------------------------------------------
    # Grouping Configuration
    # ------------------------------------------------------------------------

    configuration = state.get(
        _GROUPING_CONFIGURATION_KEY,
    )

    if not isinstance(
        configuration,
        GroupingConfiguration,
    ):
        configuration = GroupingConfiguration.weekly()

        state[_GROUPING_CONFIGURATION_KEY] = configuration

    state[_GROUPING_SERVICE_KEY] = _build_grouping_service(
        configuration,
    )

    # ------------------------------------------------------------------------
    # Application Services
    # ------------------------------------------------------------------------

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

    # ------------------------------------------------------------------------
    # ViewModels
    # ------------------------------------------------------------------------

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
    """

    st.session_state[_SESSION_COLLECTION_KEY] = session_collection

    if session_collection.has_sessions:
        first_session = session_collection.first_session

        if first_session is not None:
            set_selected_session(
                first_session.session_date,
            )

    else:
        st.session_state[_SELECTED_SESSION_DATE_KEY] = None

        st.session_state[_ACTIVE_PRESENTATION_SCOPE_KEY] = None


def current_session_collection() -> SessionCollection | None:
    """
    Return the active SessionCollection.
    """

    return cast(
        SessionCollection | None,
        st.session_state[_SESSION_COLLECTION_KEY],
    )


def has_session_collection() -> bool:
    """
    Return True when a SessionCollection exists.
    """

    return current_session_collection() is not None


def clear_session_collection() -> None:
    """
    Clear the active SessionCollection.
    """

    st.session_state[_SESSION_COLLECTION_KEY] = None

    st.session_state[_SELECTED_SESSION_DATE_KEY] = None

    st.session_state[_ACTIVE_PRESENTATION_SCOPE_KEY] = None


# ============================================================================
# Grouping Configuration
# ============================================================================


def grouping_service() -> SessionGroupingService:
    """
    Return the active grouping service.
    """

    return cast(
        SessionGroupingService,
        st.session_state[_GROUPING_SERVICE_KEY],
    )


def grouping_configuration() -> GroupingConfiguration:
    """
    Return the active grouping configuration.
    """

    return cast(
        GroupingConfiguration,
        st.session_state[_GROUPING_CONFIGURATION_KEY],
    )


def set_grouping_configuration(
    configuration: GroupingConfiguration,
) -> None:
    """
    Replace the active grouping configuration.
    """

    if not isinstance(
        configuration,
        GroupingConfiguration,
    ):
        raise TypeError(
            "configuration must be a GroupingConfiguration.",
        )

    st.session_state[_GROUPING_CONFIGURATION_KEY] = configuration

    st.session_state[_GROUPING_SERVICE_KEY] = _build_grouping_service(
        configuration,
    )

    st.session_state[_ACTIVE_PRESENTATION_SCOPE_KEY] = None


# ============================================================================
# Grouped Sessions
# ============================================================================


def grouped_sessions() -> tuple[SessionGroup, ...]:
    """
    Return the grouped SessionGroups for the active
    Presentation configuration.
    """

    session_collection = current_session_collection()

    if session_collection is None:
        return ()

    return grouping_service().group(
        session_collection,
    )


# ============================================================================
# Presentation Scope
# ============================================================================


def set_selected_session(
    session_date: date,
) -> None:
    """
    Select the active Daily Session.

    The PresentationScope is rebuilt automatically.
    """

    session_collection = current_session_collection()

    if session_collection is None:
        raise RuntimeError(
            "Cannot select a session without a SessionCollection.",
        )

    session = session_collection.get_session(
        session_date,
    )

    if session is None:
        raise ValueError(
            f"No session exists for date: {session_date}.",
        )

    st.session_state[_SELECTED_SESSION_DATE_KEY] = session_date

    selected_group = None

    for group in grouped_sessions():
        if (
            group.get_session(
                session_date,
            )
            is not None
        ):
            selected_group = group
            break

    if selected_group is None:
        st.session_state[_ACTIVE_PRESENTATION_SCOPE_KEY] = None

        return

    st.session_state[_ACTIVE_PRESENTATION_SCOPE_KEY] = PresentationScope(
        configuration=grouping_configuration(),
        session_group=selected_group,
        session=session,
    )


def selected_session_date() -> date | None:
    """
    Return the selected Daily Session date.
    """

    return cast(
        date | None,
        st.session_state[_SELECTED_SESSION_DATE_KEY],
    )


def current_session() -> Session | None:
    """
    Return the selected Daily Session.
    """

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
    """
    Return True when a Daily Session is selected.
    """

    return current_session() is not None


def presentation_scope() -> PresentationScope | None:
    """
    Return the active PresentationScope.
    """

    return cast(
        PresentationScope | None,
        st.session_state[_ACTIVE_PRESENTATION_SCOPE_KEY],
    )


# ============================================================================
# Presentation Configuration
# ============================================================================


def set_expected_attendees(
    value: int,
) -> None:
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
# Shared Services
# ============================================================================


def attendance_service() -> AttendanceService:
    """
    Return the shared AttendanceService.
    """

    return cast(
        AttendanceService,
        st.session_state[_ATTENDANCE_SERVICE_KEY],
    )


def activity_service() -> ActivityService:
    """
    Return the shared ActivityService.
    """

    return cast(
        ActivityService,
        st.session_state[_ACTIVITY_SERVICE_KEY],
    )


def dashboard_service() -> DashboardService:
    """
    Return the shared DashboardService.
    """

    return cast(
        DashboardService,
        st.session_state[_DASHBOARD_SERVICE_KEY],
    )


def report_service() -> ReportService:
    """
    Return the shared ReportService.
    """

    return cast(
        ReportService,
        st.session_state[_REPORT_SERVICE_KEY],
    )


# ============================================================================
# Remaining Shared Services
# ============================================================================


def import_service() -> ImportService:
    """
    Return the shared ImportService.
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


def ai_controller() -> AIController:
    """
    Return the shared AIController.
    """

    return cast(
        AIController,
        st.session_state[_AI_CONTROLLER_KEY],
    )


# ============================================================================
# ViewModels
# ============================================================================


def ai_viewmodel() -> AIViewModel:
    """
    Return the shared AIViewModel.
    """

    return cast(
        AIViewModel,
        st.session_state[_AI_VIEWMODEL_KEY],
    )


def attendance_viewmodel() -> AttendanceViewModel:
    """
    Return the shared AttendanceViewModel.
    """

    return cast(
        AttendanceViewModel,
        st.session_state[_ATTENDANCE_VIEWMODEL_KEY],
    )


def activity_viewmodel() -> ActivityViewModel:
    """
    Return the shared ActivityViewModel.
    """

    return cast(
        ActivityViewModel,
        st.session_state[_ACTIVITY_VIEWMODEL_KEY],
    )


def dashboard_viewmodel() -> DashboardViewModel:
    """
    Return the shared DashboardViewModel.
    """

    return cast(
        DashboardViewModel,
        st.session_state[_DASHBOARD_VIEWMODEL_KEY],
    )


def report_viewmodel() -> ReportViewModel:
    """
    Return the shared ReportViewModel.
    """

    return cast(
        ReportViewModel,
        st.session_state[_REPORT_VIEWMODEL_KEY],
    )


# ============================================================================
# Public Exports
# ============================================================================

__all__ = [
    # Initialization
    "initialize",
    # Session Collection
    "set_session_collection",
    "current_session_collection",
    "has_session_collection",
    "clear_session_collection",
    # Grouping
    "grouping_configuration",
    "grouping_service",
    "set_grouping_configuration",
    "grouped_sessions",
    # Session Selection
    "set_selected_session",
    "selected_session_date",
    "current_session",
    "has_selected_session",
    # Presentation Scope
    "presentation_scope",
    # Configuration
    "set_expected_attendees",
    "expected_attendees",
    # Services
    "attendance_service",
    "activity_service",
    "dashboard_service",
    "report_service",
    "import_service",
    "ai_service",
    "ai_controller",
    # ViewModels
    "ai_viewmodel",
    "attendance_viewmodel",
    "activity_viewmodel",
    "dashboard_viewmodel",
    "report_viewmodel",
]
