from __future__ import annotations

from collections.abc import Iterable
from datetime import date
from typing import Any

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


class DashboardViewModel:
    """
    Presentation ViewModel for dashboard workflows.

    Provides both Daily Session and Presentation Scope analytics.

    Daily Session remains the atomic Domain aggregate.

    When the active Presentation Scope contains multiple Daily Sessions,
    scope analytics are calculated against an application-layer aggregate
    projection containing all Daily Sessions in that scope.
    """

    def __init__(
        self,
        dashboard_service: DashboardService | None = None,
        multi_session_analytics_service: (
            MultiSessionAnalyticsService | None
        ) = None,
    ) -> None:
        self._dashboard_service = (
            dashboard_service
            if dashboard_service is not None
            else DashboardService()
        )

        self._multi_session_analytics_service = (
            multi_session_analytics_service
            if multi_session_analytics_service is not None
            else MultiSessionAnalyticsService()
        )

    def build_session(
        self,
        *,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        return self._dashboard_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    def get_dashboard(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
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
    # Presentation Scope Analytics
    # =========================================================================

    def scope_session(
        self,
        *,
        sessions: Iterable[Session],
    ) -> Session:
        """
        Return the analysis Session for the active Presentation Scope.
        """

        return self._multi_session_analytics_service.aggregate_session(
            sessions,
        )

    def scope_analytics(
        self,
        *,
        sessions: Iterable[Session],
    ) -> MultiSessionAnalyticsResult:
        """
        Return multi-session analytics for the Presentation Scope.
        """

        return self._multi_session_analytics_service.analyze(
            sessions,
        )

    def scope_dashboard_data(
        self,
        *,
        sessions: Iterable[Session],
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return complete dashboard/attendance/activity analytics for
        every Daily Session contained in the active Presentation Scope.
        """

        scope_session = self.scope_session(
            sessions=sessions,
        )

        analytics = self.scope_analytics(
            sessions=sessions,
        )

        data = self.to_presentation_data(
            session=scope_session,
            expected_attendees=expected_attendees,
        )

        data["scope_session"] = scope_session
        data["scope_analytics"] = analytics

        return data

    def multi_session_summary(
        self,
        *,
        sessions: Iterable[Session],
    ) -> MultiSessionAnalyticsResult:
        return self._multi_session_analytics_service.analyze(
            sessions=sessions,
        )

    def multi_session_presentation_data(
        self,
        *,
        sessions: Iterable[Session],
    ) -> dict[str, Any]:
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

    def session_summary(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        return self._dashboard_service.session_summary(
            session,
        )

    def dashboard_summary(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
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
        return self._dashboard_service.attendance_summary(
            session,
            expected_attendees,
        )

    def activity_summary(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        return self._dashboard_service.activity_summary(
            session,
        )

    def has_attendance(
        self,
        *,
        session: Session,
    ) -> bool:
        return self._dashboard_service.has_attendance(
            session,
        )

    def has_activities(
        self,
        *,
        session: Session,
    ) -> bool:
        return self._dashboard_service.has_activities(
            session,
        )

    def is_empty(
        self,
        *,
        session: Session,
    ) -> bool:
        return self._dashboard_service.is_empty(
            session,
        )

    @property
    def dashboard_service(self) -> DashboardService:
        return self._dashboard_service

    @property
    def multi_session_analytics_service(
        self,
    ) -> MultiSessionAnalyticsService:
        return self._multi_session_analytics_service

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"dashboard_service="
            f"{self.dashboard_service.__class__.__name__}, "
            f"multi_session_analytics_service="
            f"{self.multi_session_analytics_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        return self.__repr__()


__all__ = [
    "DashboardViewModel",
]
