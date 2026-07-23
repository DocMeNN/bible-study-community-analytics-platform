# src/application/services/attendance_service.py

"""
Attendance Application Service

Purpose:
    Provides application-level attendance use cases by orchestrating
    Session construction and Domain attendance analytics.

Responsibilities:
    - Build Session aggregates.
    - Expose attendance-related application workflows.
    - Coordinate attendance analytics.
    - Coordinate Done acknowledgement analytics.
    - Produce typed AttendanceResult DTOs.
    - Remain free of business logic.

Rules:
    - No pandas.
    - No Streamlit.
    - No plotting.
    - No reporting.
    - No infrastructure parsing.
    - No business rules.

Notes:
    - Business rules remain inside the Domain layer.
    - This service coordinates Domain components only.
    - Attendance is based on participation.
    - Missing members cannot be calculated because no member registry
      exists for the attendance population.
    - Application results are exposed through AttendanceResult.

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
from src.application.builders.session_builder import SessionBuilder
from src.application.dto.attendance_result import AttendanceResult
from src.domain.analytics.done import count_done_events
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.member import Member
from src.domain.models.message import Message
from src.domain.models.session import Session


class AttendanceService:
    """
    Application service for attendance workflows.

    Coordinates Session creation and delegates
    attendance-related behaviour to Domain models
    and Domain analytics.
    """

    def __init__(
        self,
        session_builder: SessionBuilder | None = None,
    ) -> None:
        """
        Initialize attendance service.
        """

        self._session_builder = (
            session_builder
            if session_builder is not None
            else SessionBuilder()
        )

    # =========================================================================
    # Session Construction
    # =========================================================================

    def build_session(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build immutable Session aggregate.
        """

        return self._session_builder.build(
            session_date=session_date,
            messages=messages,
        )

    # =========================================================================
    # Attendance Events
    # =========================================================================

    def attendance_events(
        self,
        session: Session,
    ) -> tuple[AttendanceEvent, ...]:
        """
        Return attendance events from session.
        """

        return session.attendance_events

    def attendees(
        self,
        session: Session,
    ) -> tuple[str, ...]:
        """
        Return unique participating attendees.

        Session-level attendance is participation-based.
        """

        return session.unique_attendees

    def attendance_count(
        self,
        session: Session,
    ) -> int:
        """
        Return unique participant attendance count.
        """

        return len(
            self.attendees(
                session,
            )
        )

    def attendance_rate(
        self,
        session: Session,
        expected_attendees: int,
    ) -> float:
        """
        Calculate attendance percentage against an
        externally supplied expected participant count.

        Attendance rate is calculated as:

            observed participants
            ---------------------
            expected participants

        The expected participant count must come from
        an external known population because a WhatsApp
        export cannot identify silent members.
        """

        if expected_attendees < 0:
            raise ValueError(
                "expected_attendees cannot be negative.",
            )

        if expected_attendees == 0:
            return 0.0

        return (
            self.attendance_count(
                session,
            )
            / expected_attendees
        ) * 100.0

    def member_attendance_rate(
        self,
        member: Member,
        session: Session,
    ) -> float:
        """
        Calculate whether a known member participated
        in the supplied session.

        This service method provides a session-level
        participation result for a known member.

        The result is:

            100.0
                Member participated.

            0.0
                Member did not participate.
        """

        member_name = member.name.casefold()

        for attendee in self.attendees(
            session,
        ):
            if attendee.casefold() == member_name:
                return 100.0

        return 0.0

    def attendance_counts(
        self,
        session: Session,
    ) -> dict[AttendanceType, int]:
        """
        Count attendance classifications.

        The current attendance domain contains only
        PRESENT participation events.
        """

        present_count = self.attendance_count(
            session,
        )

        if present_count == 0:
            return {}

        return {
            AttendanceType.PRESENT: present_count,
        }

    # =========================================================================
    # Done Events
    # =========================================================================

    def done_events(
        self,
        session: Session,
    ) -> tuple[DoneEvent, ...]:
        """
        Return Done acknowledgement events.
        """

        return session.done_events

    def done_count(
        self,
        session: Session,
    ) -> int:
        """
        Return total Done acknowledgement count.
        """

        return count_done_events(
            session.done_events,
        )

    def first_done(
        self,
        session: Session,
    ) -> DoneEvent | None:
        """
        Return the first Done acknowledgement event.

        Done events are already chronologically ordered
        by the Session aggregate.
        """

        if not session.done_events:
            return None

        return session.done_events[0]

    # =========================================================================
    # Participant Information
    # =========================================================================

    def participant_count(
        self,
        session: Session,
    ) -> int:
        """
        Return number of unique observed participants.

        This represents observed participants only.
        No missing-member calculation is performed.
        """

        return len(
            session.unique_attendees,
        )

    def participants(
        self,
        session: Session,
    ) -> tuple[str, ...]:
        """
        Return observed participants.
        """

        return session.unique_attendees

    # =========================================================================
    # Application Result
    # =========================================================================

    def attendance_result(
        self,
        session: Session,
        expected_attendees: int,
    ) -> AttendanceResult:
        """
        Return the complete attendance application result.

        This method assembles attendance-related information
        into the typed AttendanceResult DTO.

        The service remains responsible for orchestration only.
        Business calculations continue to be delegated to
        the Domain model and Domain analytics.
        """

        return AttendanceResult(
            attendees=self.attendees(
                session,
            ),
            participants=self.participant_count(
                session,
            ),
            attendance_count=self.attendance_count(
                session,
            ),
            attendance_rate=self.attendance_rate(
                session,
                expected_attendees,
            ),
            attendance_types=self.attendance_counts(
                session,
            ),
            attendance_events=self.attendance_events(
                session,
            ),
            done_events=self.done_events(
                session,
            ),
            done_count=self.done_count(
                session,
            ),
            first_done=self.first_done(
                session,
            ),
        )

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def has_attendance(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if attendance exists.
        """

        return session.has_attendance

    def has_done_events(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if Done events exist.
        """

        return session.has_done_events

    def is_empty(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if session contains no events.
        """

        return session.is_empty

    # =========================================================================
    # Builder Access
    # =========================================================================

    @property
    def builder(self) -> SessionBuilder:
        """
        Return the SessionBuilder.
        """

        return self._session_builder

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"builder={self.builder.name})"
        )

    def __str__(self) -> str:
        """
        Return readable representation.
        """

        return self.__repr__()
