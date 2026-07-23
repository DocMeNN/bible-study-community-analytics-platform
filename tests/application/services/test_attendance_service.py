# tests/application/services/test_attendance_service.py

"""
AttendanceService Application Service Tests

Purpose:
    Verify AttendanceService orchestration, attendance calculations,
    Done acknowledgement handling, participant information, convenience
    methods, application result DTO construction, and representations.

Author:
    Me
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from datetime import date, datetime

# ============================================================================
# Third-Party Imports
# ============================================================================
import pytest

# ============================================================================
# Local Imports
# ============================================================================
from src.application.builders.session_builder import SessionBuilder
from src.application.dto.attendance_result import AttendanceResult
from src.application.services.attendance_service import AttendanceService
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.member import Member
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Test Helpers
# ============================================================================


def message(
    *,
    sender: str = "Alice",
    content: str = "Message",
    minute: int = 0,
    line_number: int = 1,
) -> Message:
    """
    Create a valid Message for testing.
    """

    return Message(
        timestamp=datetime(
            2026,
            7,
            23,
            8,
            minute,
        ),
        sender=sender,
        content=content,
        line_number=line_number,
    )


def attendance_event(
    *,
    attendee: str = "Alice",
    minute: int = 0,
    line_number: int = 1,
) -> AttendanceEvent:
    """
    Create a valid AttendanceEvent for testing.
    """

    source = message(
        sender=attendee,
        content="Participation",
        minute=minute,
        line_number=line_number,
    )

    return AttendanceEvent(
        attendee=attendee,
        source_message=source,
    )


def done_event(
    *,
    attendee: str = "Alice",
    minute: int = 0,
    line_number: int = 1,
) -> DoneEvent:
    """
    Create a valid DoneEvent for testing.
    """

    source = message(
        sender=attendee,
        content="Done",
        minute=minute,
        line_number=line_number,
    )

    return DoneEvent(
        attendee=attendee,
        source_message=source,
    )


def session_with_attendance(
    *events: AttendanceEvent,
) -> Session:
    """
    Build a Session containing attendance events.
    """

    return Session(
        session_date=date(
            2026,
            7,
            23,
        ),
        attendance_events=tuple(events),
    )


def session_with_done_events(
    *events: DoneEvent,
) -> Session:
    """
    Build a Session containing Done events.
    """

    return Session(
        session_date=date(
            2026,
            7,
            23,
        ),
        done_events=tuple(events),
    )


# ============================================================================
# Test Doubles
# ============================================================================


class RecordingSessionBuilder:
    """
    Test double for SessionBuilder delegation.
    """

    name = "RecordingSessionBuilder"

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self.calls: list[dict[str, object]] = []

    def build(
        self,
        *,
        session_date: date,
        messages: object,
    ) -> Session:
        """
        Record the build call and return the configured session.
        """

        self.calls.append(
            {
                "session_date": session_date,
                "messages": messages,
            }
        )

        return self.session


# ============================================================================
# AttendanceService Initialization
# ============================================================================


class TestAttendanceServiceInitialization:
    """
    Test service initialization and builder access.
    """

    def test_default_builder_is_created(self) -> None:
        """
        The service creates a SessionBuilder when none is supplied.
        """

        service = AttendanceService()

        assert isinstance(
            service.builder,
            SessionBuilder,
        )

    def test_supplied_builder_is_preserved(self) -> None:
        """
        A supplied builder is used by the service.
        """

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        builder = RecordingSessionBuilder(
            session,
        )

        service = AttendanceService(
            session_builder=builder,
        )

        assert service.builder is builder


# ============================================================================
# Session Construction
# ============================================================================


class TestSessionConstruction:
    """
    Test SessionBuilder orchestration.
    """

    def test_build_session_delegates_to_builder(self) -> None:
        """
        build_session delegates session construction to the builder.
        """

        expected_session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        builder = RecordingSessionBuilder(
            expected_session,
        )

        service = AttendanceService(
            session_builder=builder,
        )

        session_date = date(
            2026,
            7,
            23,
        )

        messages = (
            message(
                line_number=1,
            ),
        )

        result = service.build_session(
            session_date=session_date,
            messages=messages,
        )

        assert result is expected_session
        assert len(builder.calls) == 1
        assert builder.calls[0]["session_date"] == session_date
        assert builder.calls[0]["messages"] is messages


# ============================================================================
# Attendance Events
# ============================================================================


class TestAttendanceEvents:
    """
    Test attendance event access and participant calculations.
    """

    def test_attendance_events_returns_session_events(self) -> None:
        """
        Attendance events are returned from the Session aggregate.
        """

        first = attendance_event(
            attendee="Alice",
            minute=1,
            line_number=1,
        )

        second = attendance_event(
            attendee="Bob",
            minute=2,
            line_number=2,
        )

        session = session_with_attendance(
            first,
            second,
        )

        service = AttendanceService()

        assert service.attendance_events(
            session,
        ) == (
            first,
            second,
        )

    def test_attendees_returns_unique_participants(self) -> None:
        """
        Attendees are unique while preserving domain ordering.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
                line_number=1,
            ),
            attendance_event(
                attendee="alice",
                minute=1,
                line_number=2,
            ),
            attendance_event(
                attendee="Bob",
                minute=2,
                line_number=3,
            ),
        )

        service = AttendanceService()

        assert service.attendees(
            session,
        ) == (
            "Alice",
            "Bob",
        )

    def test_attendance_count_returns_unique_participant_count(self) -> None:
        """
        Attendance count represents unique observed participants.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
                line_number=1,
            ),
            attendance_event(
                attendee="Alice",
                minute=1,
                line_number=2,
            ),
            attendance_event(
                attendee="Bob",
                minute=2,
                line_number=3,
            ),
        )

        service = AttendanceService()

        assert service.attendance_count(
            session,
        ) == 2

    def test_attendance_count_is_zero_for_empty_session(self) -> None:
        """
        Empty sessions have zero observed participants.
        """

        service = AttendanceService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        assert service.attendance_count(
            session,
        ) == 0


# ============================================================================
# Attendance Rate
# ============================================================================


class TestAttendanceRate:
    """
    Test attendance percentage calculations.
    """

    def test_attendance_rate_is_calculated_against_expected_population(
        self,
    ) -> None:
        """
        Attendance rate is observed participants divided by expected members.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
                line_number=1,
            ),
            attendance_event(
                attendee="Bob",
                minute=1,
                line_number=2,
            ),
        )

        service = AttendanceService()

        result = service.attendance_rate(
            session,
            expected_attendees=4,
        )

        assert result == 50.0

    def test_attendance_rate_returns_zero_for_zero_expected_attendees(
        self,
    ) -> None:
        """
        Zero expected participants produce a zero rate.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
            ),
        )

        service = AttendanceService()

        assert service.attendance_rate(
            session,
            expected_attendees=0,
        ) == 0.0

    def test_negative_expected_attendees_raise_value_error(self) -> None:
        """
        Negative expected participant counts are invalid.
        """

        service = AttendanceService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        with pytest.raises(
            ValueError,
            match="expected_attendees cannot be negative",
        ):
            service.attendance_rate(
                session,
                expected_attendees=-1,
            )


# ============================================================================
# Member Attendance Rate
# ============================================================================


class TestMemberAttendanceRate:
    """
    Test known-member participation calculations.
    """

    def test_member_who_participated_has_full_rate(self) -> None:
        """
        A known member who participated receives 100 percent.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
            ),
        )

        service = AttendanceService()

        member = Member(
            name="Alice",
        )

        assert service.member_attendance_rate(
            member,
            session,
        ) == 100.0

    def test_member_matching_is_case_insensitive(self) -> None:
        """
        Member matching is case-insensitive.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
            ),
        )

        service = AttendanceService()

        member = Member(
            name="alice",
        )

        assert service.member_attendance_rate(
            member,
            session,
        ) == 100.0

    def test_member_who_did_not_participate_has_zero_rate(self) -> None:
        """
        A known member who did not participate receives zero percent.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
            ),
        )

        service = AttendanceService()

        member = Member(
            name="Bob",
        )

        assert service.member_attendance_rate(
            member,
            session,
        ) == 0.0


# ============================================================================
# Attendance Classification
# ============================================================================


class TestAttendanceCounts:
    """
    Test attendance classification counts.
    """

    def test_present_count_is_returned_as_present(self) -> None:
        """
        Current attendance classification contains PRESENT participation.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
            ),
            attendance_event(
                attendee="Bob",
                minute=1,
                line_number=2,
            ),
        )

        service = AttendanceService()

        assert service.attendance_counts(
            session,
        ) == {
            AttendanceType.PRESENT: 2,
        }

    def test_empty_attendance_returns_empty_mapping(self) -> None:
        """
        No attendance produces no classification counts.
        """

        service = AttendanceService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        assert service.attendance_counts(
            session,
        ) == {}


# ============================================================================
# Done Events
# ============================================================================


class TestDoneEvents:
    """
    Test Done acknowledgement orchestration.
    """

    def test_done_events_returns_session_events(self) -> None:
        """
        Done events are returned from the Session aggregate.
        """

        first = done_event(
            attendee="Alice",
            line_number=1,
        )

        second = done_event(
            attendee="Bob",
            minute=1,
            line_number=2,
        )

        session = session_with_done_events(
            first,
            second,
        )

        service = AttendanceService()

        assert service.done_events(
            session,
        ) == (
            first,
            second,
        )

    def test_done_count_counts_acknowledgement_events(self) -> None:
        """
        Done count counts events rather than unique attendees.
        """

        session = session_with_done_events(
            done_event(
                attendee="Alice",
                line_number=1,
            ),
            done_event(
                attendee="Alice",
                minute=1,
                line_number=2,
            ),
            done_event(
                attendee="Bob",
                minute=2,
                line_number=3,
            ),
        )

        service = AttendanceService()

        assert service.done_count(
            session,
        ) == 3

    def test_first_done_returns_earliest_done_event(self) -> None:
        """
        The first Done event is returned.
        """

        first = done_event(
            attendee="Alice",
            minute=1,
            line_number=1,
        )

        second = done_event(
            attendee="Bob",
            minute=2,
            line_number=2,
        )

        session = session_with_done_events(
            second,
            first,
        )

        service = AttendanceService()

        assert service.first_done(
            session,
        ) is first

    def test_first_done_returns_none_when_no_done_events_exist(self) -> None:
        """
        No Done events produce None.
        """

        service = AttendanceService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        assert service.first_done(
            session,
        ) is None


# ============================================================================
# Participant Information
# ============================================================================


class TestParticipantInformation:
    """
    Test participant convenience methods.
    """

    def test_participant_count_returns_unique_observed_participants(
        self,
    ) -> None:
        """
        Participant count reflects unique observed participants.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
                line_number=1,
            ),
            attendance_event(
                attendee="alice",
                minute=1,
                line_number=2,
            ),
            attendance_event(
                attendee="Bob",
                minute=2,
                line_number=3,
            ),
        )

        service = AttendanceService()

        assert service.participant_count(
            session,
        ) == 2

    def test_participants_returns_observed_participants(self) -> None:
        """
        Participants returns the unique observed participant sequence.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
                line_number=1,
            ),
            attendance_event(
                attendee="Bob",
                minute=1,
                line_number=2,
            ),
        )

        service = AttendanceService()

        assert service.participants(
            session,
        ) == (
            "Alice",
            "Bob",
        )


# ============================================================================
# Application Result
# ============================================================================


class TestAttendanceResult:
    """
    Test typed attendance result construction.
    """

    def test_attendance_result_returns_attendance_result_dto(self) -> None:
        """
        attendance_result returns the typed application DTO.
        """

        session = session_with_attendance(
            attendance_event(
                attendee="Alice",
                line_number=1,
            ),
            attendance_event(
                attendee="Bob",
                minute=1,
                line_number=2,
            ),
        )

        service = AttendanceService()

        result = service.attendance_result(
            session,
            expected_attendees=4,
        )

        assert isinstance(
            result,
            AttendanceResult,
        )

    def test_attendance_result_contains_attendance_data(self) -> None:
        """
        AttendanceResult contains the expected attendance values.
        """

        first = attendance_event(
            attendee="Alice",
            line_number=1,
        )

        second = attendance_event(
            attendee="Bob",
            minute=1,
            line_number=2,
        )

        session = session_with_attendance(
            first,
            second,
        )

        service = AttendanceService()

        result = service.attendance_result(
            session,
            expected_attendees=4,
        )

        assert result.attendees == (
            "Alice",
            "Bob",
        )

        assert result.participants == 2
        assert result.attendance_count == 2
        assert result.attendance_rate == 50.0

        assert result.attendance_types == {
            AttendanceType.PRESENT: 2,
        }

        assert result.attendance_events == (
            first,
            second,
        )

    def test_attendance_result_contains_done_data(self) -> None:
        """
        AttendanceResult contains Done acknowledgement data.
        """

        first = done_event(
            attendee="Alice",
            line_number=1,
        )

        second = done_event(
            attendee="Bob",
            minute=1,
            line_number=2,
        )

        session = session_with_done_events(
            first,
            second,
        )

        service = AttendanceService()

        result = service.attendance_result(
            session,
            expected_attendees=4,
        )

        assert result.done_events == (
            first,
            second,
        )

        assert result.done_count == 2
        assert result.first_done is first

    def test_attendance_result_handles_empty_session(self) -> None:
        """
        Empty sessions produce an empty AttendanceResult.
        """

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        service = AttendanceService()

        result = service.attendance_result(
            session,
            expected_attendees=4,
        )

        assert result.attendees == ()
        assert result.participants == 0
        assert result.attendance_count == 0
        assert result.attendance_rate == 0.0
        assert result.attendance_types == {}
        assert result.attendance_events == ()
        assert result.done_events == ()
        assert result.done_count == 0
        assert result.first_done is None


# ============================================================================
# Convenience Methods
# ============================================================================


class TestConvenienceMethods:
    """
    Test service-level convenience methods.
    """

    def test_has_attendance_returns_true_when_attendance_exists(self) -> None:
        """
        has_attendance returns True when participation exists.
        """

        session = session_with_attendance(
            attendance_event(),
        )

        service = AttendanceService()

        assert service.has_attendance(
            session,
        ) is True

    def test_has_attendance_returns_false_when_no_attendance_exists(
        self,
    ) -> None:
        """
        has_attendance returns False for an empty session.
        """

        service = AttendanceService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        assert service.has_attendance(
            session,
        ) is False

    def test_has_done_events_returns_true_when_done_events_exist(
        self,
    ) -> None:
        """
        has_done_events returns True when Done events exist.
        """

        session = session_with_done_events(
            done_event(),
        )

        service = AttendanceService()

        assert service.has_done_events(
            session,
        ) is True

    def test_has_done_events_returns_false_when_no_done_events_exist(
        self,
    ) -> None:
        """
        has_done_events returns False when no Done events exist.
        """

        service = AttendanceService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        assert service.has_done_events(
            session,
        ) is False

    def test_is_empty_returns_true_for_empty_session(self) -> None:
        """
        Empty sessions are identified correctly.
        """

        service = AttendanceService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            )
        )

        assert service.is_empty(
            session,
        ) is True

    def test_is_empty_returns_false_for_non_empty_session(self) -> None:
        """
        Sessions containing events are not empty.
        """

        session = session_with_attendance(
            attendance_event(),
        )

        service = AttendanceService()

        assert service.is_empty(
            session,
        ) is False


# ============================================================================
# Representations
# ============================================================================


class TestAttendanceServiceRepresentations:
    """
    Test service string representations.
    """

    def test_repr_contains_service_name_and_builder_name(self) -> None:
        """
        repr identifies the service and its builder.
        """

        service = AttendanceService()

        result = repr(
            service,
        )

        assert "AttendanceService" in result
        assert "SessionBuilder" in result

    def test_str_matches_repr(self) -> None:
        """
        str returns the official representation.
        """

        service = AttendanceService()

        assert str(
            service,
        ) == repr(
            service,
        )
