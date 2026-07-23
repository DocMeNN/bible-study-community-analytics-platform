# src/application/services/dashboard_service.py

"""
Dashboard Application Service

Purpose:
    Provides dashboard-ready application use cases by orchestrating
    attendance and activity services.

Responsibilities:
    - Build Session aggregates.
    - Coordinate attendance metrics.
    - Coordinate activity metrics.
    - Provide dashboard-ready data.
    - Remain free of business logic.

Rules:
    - No pandas.
    - No Streamlit.
    - No plotting.
    - No reporting.
    - No business rules.

Notes:
    - Delegates business calculations to Domain services.
    - Delegates Session construction to AttendanceService.
    - Acts as the primary service consumed by the Presentation layer.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable
from datetime import date

# ============================================================================
# Local Imports
# ============================================================================
from src.application.services.activity_service import ActivityService
from src.application.services.attendance_service import AttendanceService
from src.domain.models.message import Message
from src.domain.models.session import Session


class DashboardService:
    """
    Application service for dashboard workflows.

    Coordinates application services required to assemble
    dashboard-ready session information.
    """

    def __init__(
        self,
        attendance_service: AttendanceService | None = None,
        activity_service: ActivityService | None = None,
    ) -> None:
        """
        Initialize dashboard service.
        """

        self._attendance_service = (
            attendance_service
            if attendance_service is not None
            else AttendanceService()
        )

        self._activity_service = (
            activity_service
            if activity_service is not None
            else ActivityService()
        )

    # ------------------------------------------------------------------
    # Session
    # ------------------------------------------------------------------

    def build_session(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build a Session aggregate.
        """

        return self._attendance_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # ------------------------------------------------------------------
    # Dashboard Summary
    # ------------------------------------------------------------------

    def dashboard_summary(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return dashboard-ready metrics.
        """

        return {
            "session_date": session.session_date,
            "attendance_count": session.attendee_count,
            "attendance_rate": self._attendance_service.attendance_rate(
                session,
                expected_attendees,
            ),
            "done_count": session.done_count,
            "activity_count": session.activity_count,
            "attendance_events": session.attendance_count,
            "participants": session.attendee_count,
            "first_done": session.first_done,
            "first_activity": session.first_activity,
            "last_activity": session.last_activity,
            "duration": session.duration,
        }

    # ------------------------------------------------------------------
    # Attendance
    # ------------------------------------------------------------------

    def attendance_summary(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return attendance metrics.
        """

        return {
            "attendees": self._attendance_service.attendees(
                session,
            ),
            "participants": self._attendance_service.participant_count(
                session,
            ),
            "attendance_count": self._attendance_service.attendance_count(
                session,
            ),
            "attendance_rate": self._attendance_service.attendance_rate(
                session,
                expected_attendees,
            ),
            "attendance_types": self._attendance_service.attendance_counts(
                session,
            ),
        }

    # ------------------------------------------------------------------
    # Activity
    # ------------------------------------------------------------------

    def activity_summary(
        self,
        session: Session,
    ) -> dict[str, object]:
        """
        Return activity metrics.
        """

        return {
            "activity_count": self._activity_service.activity_count(
                session,
            ),
            "activity_types": self._activity_service.activity_counts(
                session,
            ),
            "first_activity": self._activity_service.first_activity(
                session,
            ),
            "last_activity": self._activity_service.last_activity(
                session,
            ),
        }

    # ------------------------------------------------------------------
    # Session Summary
    # ------------------------------------------------------------------

    def session_summary(
        self,
        session: Session,
    ) -> dict[str, object]:
        """
        Return session information.
        """

        return {
            "session_date": session.session_date,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "duration": session.duration,
            "participants": session.attendee_count,
            "attendance_events": session.attendance_count,
            "done_events": session.done_count,
            "activity_events": session.activity_count,
            "total_events": session.total_events,
        }

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def has_attendance(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if attendance exists.
        """

        return session.has_attendance

    def has_activities(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if activities exist.
        """

        return session.has_activities

    def is_empty(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if the session has no events.
        """

        return session.is_empty

    # ------------------------------------------------------------------
    # Service Accessors
    # ------------------------------------------------------------------

    @property
    def attendance_service(self) -> AttendanceService:
        """
        Return the AttendanceService.
        """

        return self._attendance_service

    @property
    def activity_service(self) -> ActivityService:
        """
        Return the ActivityService.
        """

        return self._activity_service

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"attendance_service="
            f"{self.attendance_service.__class__.__name__}, "
            f"activity_service="
            f"{self.activity_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()
