# src/application/services/multi_session_analytics_service.py

"""
Multi-Session Analytics Service

Purpose
-------
Coordinate analytics across multiple Daily Session aggregates.

Architectural Responsibility
----------------------------
The service receives a collection of Daily Sessions selected by the
Presentation scope and coordinates analytics across them.

The service does not:

- perform Presentation-layer grouping;
- own Streamlit state;
- replace the Daily Session domain model;
- move business rules into the Presentation layer.

The architectural flow is:

Selected SessionGroup
        ↓
SessionGroup.sessions
        ↓
MultiSessionAnalyticsService
        ↓
MultiSessionAnalyticsResult
"""

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

    Daily Session remains the atomic Domain aggregate. This service provides
    the application-level coordination boundary for a selected multi-session
    Presentation scope.
    """

    def analyze(
        self,
        sessions: Iterable[Session],
    ) -> MultiSessionAnalyticsResult:
        """
        Analyze a collection of Daily Sessions.

        Parameters
        ----------
        sessions:
            Iterable containing the Daily Sessions included in the selected
            Presentation scope.

        Returns
        -------
        MultiSessionAnalyticsResult
            Typed application-layer analytics result.
        """

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

        total_done_events = sum(
            len(session.done_events)
            for session in ordered_sessions
        )

        total_activity_events = sum(
            len(session.activity_events)
            for session in ordered_sessions
        )

        return MultiSessionAnalyticsResult(
            session_count=len(ordered_sessions),
            start_date=self._session_date(ordered_sessions[0]),
            end_date=self._session_date(ordered_sessions[-1]),
            total_participants=len(participants),
            total_done_events=total_done_events,
            total_activity_events=total_activity_events,
        )

    @staticmethod
    def _session_date(session: Session) -> date:
        """
        Return the date associated with a Daily Session.
        """

        return session.session_date