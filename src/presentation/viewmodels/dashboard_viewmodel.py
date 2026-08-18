# src/presentation/viewmodels/dashboard_viewmodel.py

"""
Dashboard ViewModel

Purpose
-------
Coordinates dashboard presentation workflows by consuming
Application Layer services and adapting application results
for Presentation Layer consumption.

Responsibilities
----------------
- Delegate single-session workflows to DashboardService.
- Delegate multi-session analytics to MultiSessionAnalyticsService.
- Build Session aggregates through the Application Layer.
- Expose presentation-ready data.
- Adapt application results for Presentation components.

Architectural Rules
-------------------
- Presentation layer only.
- No business logic.
- No analytics calculations.
- No Streamlit.
- No direct Domain analytics.
- No infrastructure dependencies.
- No direct data parsing.

Architecture
------------
                    Dashboard Page
                           |
                           v
                 DashboardViewModel
                    /           \
                   /             \
                  v               v
        DashboardService   MultiSessionAnalyticsService
                  |               |
                  v               v
          Single Session     Multiple Sessions
                  \\               /
                   \\             /
                    v           v
               Presentation Components

The ViewModel is an adapter between the Application Layer
and the Presentation Layer.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable
from datetime import date
from typing import Any

# ============================================================================
# Local Imports
# ============================================================================
from src.application.dto.multi_session_analytics_result import (
    MultiSessionAnalyticsResult,
)
from src.application.services.dashboard_service import DashboardService
from src.application.services.multi_session_analytics_service import (
    MultiSessionAnalyticsService,
)
from src.domain.models.message import Message
from src.domain.models.session import Session
from src.presentation.dto.multi_session_overview import (
    MultiSessionOverview,
)

# ============================================================================
# Dashboard ViewModel
# ============================================================================


class DashboardViewModel:
    """
    Presentation ViewModel for dashboard workflows.

    Coordinates Application Layer services and adapts
    application data for Presentation Layer consumption.

    The ViewModel performs structural adaptation only.

    It does not:

    - calculate analytics;
    - apply business rules;
    - parse messages;
    - modify Session aggregates.
    """

    def __init__(
        self,
        dashboard_service: DashboardService | None = None,
        multi_session_analytics_service: MultiSessionAnalyticsService | None = None,
    ) -> None:
        """
        Initialize the DashboardViewModel.

        Parameters
        ----------
        dashboard_service:
            Optional DashboardService dependency.

        multi_session_analytics_service:
            Optional MultiSessionAnalyticsService dependency.
        """

        self._dashboard_service = (
            dashboard_service if dashboard_service is not None else DashboardService()
        )

        self._multi_session_analytics_service = (
            multi_session_analytics_service
            if multi_session_analytics_service is not None
            else MultiSessionAnalyticsService()
        )

    # =========================================================================
    # Session Construction
    # =========================================================================

    def build_session(
        self,
        *,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build a Session through the Application Layer.
        """

        return self._dashboard_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # =========================================================================
    # Single-Session Dashboard
    # =========================================================================

    def get_dashboard(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return complete dashboard data for a single Daily Session.
        """

        return self.to_presentation_data(
            session=session,
            expected_attendees=expected_attendees,
        )

    def to_presentation_data(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Adapt single-session application results for Presentation components.

        Performs structural adaptation only.
        """

        return {
            "session": self._dashboard_service.session_summary(
                session,
            ),
            "dashboard": self._dashboard_service.dashboard_summary(
                session,
                expected_attendees,
            ),
            "attendance": self._dashboard_service.attendance_summary(
                session,
                expected_attendees,
            ),
            "activity": self._dashboard_service.activity_summary(
                session,
            ),
        }

    # =========================================================================
    # Multi-Session Dashboard
    # =========================================================================

    def multi_session_summary(
        self,
        *,
        sessions: Iterable[Session],
    ) -> MultiSessionAnalyticsResult:
        """
        Return application analytics for multiple Daily Sessions.

        The ViewModel delegates all analytics calculations to the
        MultiSessionAnalyticsService.
        """

        return self._multi_session_analytics_service.analyze(
            sessions=sessions,
        )

    def multi_session_presentation_data(
        self,
        *,
        sessions: Iterable[Session],
    ) -> dict[str, Any]:
        """
        Return presentation-ready multi-session data.

        Performs structural adaptation only.
        """

        analytics = self.multi_session_summary(
            sessions=sessions,
        )

        overview = MultiSessionOverview(
            session_count=analytics.session_count,
            start_date=analytics.start_date,
            end_date=analytics.end_date,
            participant_count=analytics.total_participants,
            done_events=analytics.total_done_events,
            activity_events=analytics.total_activity_events,
        )

        return {
            "overview": overview,
        }

    # =========================================================================
    # Individual Sections
    # =========================================================================

    def session_summary(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        """
        Return presentation-ready session summary.
        """

        return self._dashboard_service.session_summary(
            session,
        )

    def dashboard_summary(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return presentation-ready dashboard summary.
        """

        return self._dashboard_service.dashboard_summary(
            session,
            expected_attendees,
        )

    def attendance_summary(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return presentation-ready attendance summary.
        """

        return self._dashboard_service.attendance_summary(
            session,
            expected_attendees,
        )

    def activity_summary(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        """
        Return presentation-ready activity summary.
        """

        return self._dashboard_service.activity_summary(
            session,
        )

    # =========================================================================
    # State
    # =========================================================================

    def has_attendance(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when attendance exists.
        """

        return self._dashboard_service.has_attendance(
            session,
        )

    def has_activities(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when activity data exists.
        """

        return self._dashboard_service.has_activities(
            session,
        )

    def is_empty(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when the Session contains no events.
        """

        return self._dashboard_service.is_empty(
            session,
        )

    # =========================================================================
    # Service Access
    # =========================================================================

    @property
    def dashboard_service(self) -> DashboardService:
        """
        Return the DashboardService.
        """

        return self._dashboard_service

    @property
    def multi_session_analytics_service(
        self,
    ) -> MultiSessionAnalyticsService:
        """
        Return the MultiSessionAnalyticsService.
        """

        return self._multi_session_analytics_service

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"dashboard_service="
            f"{self.dashboard_service.__class__.__name__}, "
            f"multi_session_analytics_service="
            f"{self.multi_session_analytics_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        """
        Return self.__repr__().
        """

        return self.__repr__()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "DashboardViewModel",
]
