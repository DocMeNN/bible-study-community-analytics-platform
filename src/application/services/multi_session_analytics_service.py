from __future__ import annotations

from collections.abc import Iterable
from datetime import date

from src.application.dto.multi_session_analytics_result import (
    MultiSessionAnalyticsResult,
)
from src.domain.models.session import Session


class MultiSessionAnalyticsService:
    """
    Application service for analytics across multiple Daily Sessions.

    Daily Session remains the atomic Domain aggregate.

    This service coordinates Daily Sessions selected by the
    Presentation Scope into one analysis-ready aggregate without
    changing the Domain model or Presentation grouping rules.
    """

    def analyze(
        self,
        sessions: Iterable[Session],
    ) -> MultiSessionAnalyticsResult:
        session_list = tuple(sessions)

        if not session_list:
            return MultiSessionAnalyticsResult(
                session_count=0,
                start_date=None,
                end_date=None,
                total_participants=0,
                total_done_events=0,
                total_activity_events=0,
            )

        ordered_sessions = tuple(
            sorted(
                session_list,
                key=lambda session: session.session_date,
            )
        )

        participants = {
            attendance.attendee.casefold()
            for session in ordered_sessions
            for attendance in session.attendance_events
        }

        return MultiSessionAnalyticsResult(
            session_count=len(ordered_sessions),
            start_date=self._session_date(ordered_sessions[0]),
            end_date=self._session_date(ordered_sessions[-1]),
            total_participants=len(participants),
            total_done_events=sum(
                len(session.done_events)
                for session in ordered_sessions
            ),
            total_activity_events=sum(
                len(session.activity_events)
                for session in ordered_sessions
            ),
        )

    def aggregate_session(
        self,
        sessions: Iterable[Session],
    ) -> Session:
        """
        Build one analysis-ready Session from the Daily Sessions
        contained in the active Presentation Scope.

        Daily Session remains the persisted Domain aggregate.
        The returned Session is an application-layer analytical
        projection used by existing dashboard/attendance/activity
        services.
        """

        session_list = tuple(
            sorted(
                sessions,
                key=lambda session: session.session_date,
            )
        )

        if not session_list:
            raise ValueError(
                "Cannot aggregate an empty session collection.",
            )

        if len(session_list) == 1:
            return session_list[0]

        return Session(
            session_date=session_list[0].session_date,
            attendance_events=tuple(
                event
                for session in session_list
                for event in session.attendance_events
            ),
            done_events=tuple(
                event
                for session in session_list
                for event in session.done_events
            ),
            activity_events=tuple(
                event
                for session in session_list
                for event in session.activity_events
            ),
        )

    @staticmethod
    def _session_date(session: Session) -> date:
        return session.session_date
