# tests/application/builders/test_session_builder.py

"""
Session Builder Application Tests

Purpose
-------
Verify the orchestration behaviour of the SessionBuilder.

Coverage
--------
- Message validation.
- Chronological ordering.
- Session-start detection.
- Session message extraction.
- Attendance event construction.
- Done event construction.
- Activity event construction.
- Prayer session state handling.
- Session aggregate construction.
- Public builder utilities.
- Builder metadata.

Testing Principle
-----------------
These tests verify application-layer orchestration.

Domain business rules are not reimplemented here.
The SessionBuilder is tested for correctly coordinating
validated Message objects and Domain event models.

Author
------
OYBS Attendance Dashboard
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from datetime import date, datetime, timedelta

import pytest

# ============================================================================
# Local Imports
# ============================================================================
from src.application.builders.session_builder import SessionBuilder
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Test Helpers
# ============================================================================


def make_message(
    *,
    content: str,
    sender: str = "Alice",
    timestamp: datetime | None = None,
    line_number: int = 1,
) -> Message:
    """
    Create a valid Message for testing.
    """

    return Message(
        timestamp=timestamp
        or datetime(
            2026,
            7,
            23,
            8,
            0,
        ),
        sender=sender,
        content=content,
        line_number=line_number,
    )


def session_start_message(
    *,
    timestamp: datetime | None = None,
    line_number: int = 1,
) -> Message:
    """
    Create a standard session-start message.
    """

    return make_message(
        content="SCRIPTURE READING",
        timestamp=timestamp,
        line_number=line_number,
    )


def study_message(
    *,
    content: str,
    sender: str = "Alice",
    minutes_after_start: int = 1,
    line_number: int = 2,
) -> Message:
    """
    Create a message occurring after the session-start marker.
    """

    return make_message(
        content=content,
        sender=sender,
        timestamp=datetime(
            2026,
            7,
            23,
            8,
            0,
        )
        + timedelta(
            minutes=minutes_after_start,
        ),
        line_number=line_number,
    )


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def builder() -> SessionBuilder:
    """
    Return a SessionBuilder instance.
    """

    return SessionBuilder()


@pytest.fixture
def session_date() -> date:
    """
    Return a standard session date.
    """

    return date(
        2026,
        7,
        23,
    )


# ============================================================================
# Construction
# ============================================================================


class TestSessionBuilderConstruction:
    """
    Test SessionBuilder construction and metadata.
    """

    def test_can_be_instantiated(self) -> None:
        """
        SessionBuilder can be instantiated.
        """

        builder = SessionBuilder()

        assert isinstance(
            builder,
            SessionBuilder,
        )

    def test_name_returns_class_name(
        self,
        builder: SessionBuilder,
    ) -> None:
        """
        name returns the official class name.
        """

        assert builder.name == "SessionBuilder"

    def test_repr_returns_official_representation(
        self,
        builder: SessionBuilder,
    ) -> None:
        """
        repr returns the expected representation.
        """

        assert repr(builder) == "SessionBuilder()"

    def test_str_matches_repr(
        self,
        builder: SessionBuilder,
    ) -> None:
        """
        str returns the same representation as repr.
        """

        assert str(builder) == "SessionBuilder()"


# ============================================================================
# Message Validation
# ============================================================================


class TestMessageValidation:
    """
    Test message validation and ordering.
    """

    def test_accepts_empty_iterable(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        An empty iterable produces an empty Session.
        """

        result = builder.build(
            session_date=session_date,
            messages=[],
        )

        assert isinstance(
            result,
            Session,
        )

        assert result.is_empty

    def test_accepts_generator_input(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Iterable input may be a generator.
        """

        messages = (
            message
            for message in [
                session_start_message(),
                study_message(
                    content="Insight",
                ),
            ]
        )

        result = builder.build(
            session_date=session_date,
            messages=messages,
        )

        assert result.attendance_count == 1

    def test_rejects_non_message_items(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Non-Message items are rejected.
        """

        with pytest.raises(
            TypeError,
            match="messages must contain only Message instances",
        ):
            builder.build(
                session_date=session_date,
                messages=[
                    "not a message",
                ],
            )

    def test_sorts_messages_chronologically(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Messages are sorted by timestamp before processing.
        """

        start = session_start_message(
            timestamp=datetime(
                2026,
                7,
                23,
                8,
                0,
            ),
            line_number=1,
        )

        late_message = make_message(
            content="Late message",
            sender="Bob",
            timestamp=datetime(
                2026,
                7,
                23,
                9,
                0,
            ),
            line_number=3,
        )

        early_message = make_message(
            content="Early message",
            sender="Alice",
            timestamp=datetime(
                2026,
                7,
                23,
                8,
                30,
            ),
            line_number=2,
        )

        result = builder.build(
            session_date=session_date,
            messages=[
                late_message,
                start,
                early_message,
            ],
        )

        assert result.attendees == (
            "Alice",
            "Bob",
        )

        assert result.first_attendance is not None

        assert result.first_attendance.attendee == "Alice"

    def test_preserves_equal_timestamp_messages(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Messages with equal timestamps remain valid.
        """

        timestamp = datetime(
            2026,
            7,
            23,
            8,
            0,
        )

        start = session_start_message(
            timestamp=timestamp,
            line_number=1,
        )

        first = make_message(
            content="First",
            sender="Alice",
            timestamp=timestamp,
            line_number=2,
        )

        second = make_message(
            content="Second",
            sender="Bob",
            timestamp=timestamp,
            line_number=3,
        )

        result = builder.build(
            session_date=session_date,
            messages=[
                start,
                first,
                second,
            ],
        )

        assert result.attendance_count == 2


# ============================================================================
# Session Extraction
# ============================================================================


class TestSessionExtraction:
    """
    Test session-start detection and message extraction.
    """

    def test_messages_before_session_start_are_excluded(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Messages before the first session-start marker are excluded.
        """

        before = make_message(
            content="Before session",
            sender="Before",
            timestamp=datetime(
                2026,
                7,
                23,
                7,
                0,
            ),
            line_number=1,
        )

        start = session_start_message(
            timestamp=datetime(
                2026,
                7,
                23,
                8,
                0,
            ),
            line_number=2,
        )

        after = study_message(
            content="After session",
            sender="After",
            minutes_after_start=1,
            line_number=3,
        )

        result = builder.build(
            session_date=session_date,
            messages=[
                before,
                start,
                after,
            ],
        )

        assert result.attendees == (
            "After",
        )

    def test_session_start_marker_is_excluded(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        The session-start marker itself is not converted into events.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
            ],
        )

        assert result.attendance_count == 0
        assert result.done_count == 0
        assert result.activity_count == 0

    def test_messages_after_session_start_are_included(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Messages after the session-start marker are included.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Message one",
                    sender="Alice",
                ),
                study_message(
                    content="Message two",
                    sender="Bob",
                    minutes_after_start=2,
                ),
            ],
        )

        assert result.attendance_count == 2

    def test_no_session_start_produces_empty_session(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Messages without a session-start marker are excluded.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                make_message(
                    content="No marker",
                ),
            ],
        )

        assert result.is_empty

    def test_multiple_session_start_markers_do_not_reset_extraction(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Once a session begins, later start markers remain in the
        extracted message stream according to current orchestration.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(
                    line_number=1,
                ),
                study_message(
                    content="First message",
                    sender="Alice",
                    line_number=2,
                ),
                make_message(
                    content="SCRIPTURE READING",
                    timestamp=datetime(
                        2026,
                        7,
                        23,
                        8,
                        3,
                    ),
                    line_number=3,
                ),
            ],
        )

        assert result.attendance_count == 2


# ============================================================================
# Attendance Events
# ============================================================================


class TestAttendanceEvents:
    """
    Test AttendanceEvent construction.
    """

    def test_every_session_message_becomes_attendance_event(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Every message after the session start becomes an
        AttendanceEvent.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Insight",
                    sender="Alice",
                ),
                study_message(
                    content="Done",
                    sender="Bob",
                    minutes_after_start=2,
                ),
            ],
        )

        assert result.attendance_count == 2

        assert all(
            isinstance(
                event,
                AttendanceEvent,
            )
            for event in result.attendance_events
        )

    def test_attendance_event_preserves_sender(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        AttendanceEvent attendee is taken from the Message sender.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Insight",
                    sender="Alice",
                ),
            ],
        )

        assert result.attendance_events[0].attendee == "Alice"

    def test_attendance_event_preserves_source_message(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        AttendanceEvent preserves its originating Message.
        """

        message = study_message(
            content="Insight",
            sender="Alice",
        )

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                message,
            ],
        )

        assert result.attendance_events[0].source_message is message

    def test_build_attendance_events_utility(
        self,
        builder: SessionBuilder,
    ) -> None:
        """
        Public attendance utility builds attendance events.
        """

        result = builder.build_attendance_events(
            [
                session_start_message(),
                study_message(
                    content="Insight",
                ),
            ]
        )

        assert len(result) == 1

        assert isinstance(
            result[0],
            AttendanceEvent,
        )


# ============================================================================
# Done Events
# ============================================================================


class TestDoneEvents:
    """
    Test DoneEvent construction.
    """

    def test_done_message_creates_done_event(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        A valid Done acknowledgement creates a DoneEvent.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Done",
                    sender="Alice",
                ),
            ],
        )

        assert result.done_count == 1

        assert isinstance(
            result.done_events[0],
            DoneEvent,
        )

    def test_done_matching_is_case_insensitive(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Done matching is case-insensitive.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="DONE",
                ),
                study_message(
                    content="done",
                    sender="Bob",
                    minutes_after_start=2,
                ),
            ],
        )

        assert result.done_count == 2

    def test_multiple_done_messages_are_preserved(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Multiple Done acknowledgements are preserved.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Done",
                    sender="Alice",
                ),
                study_message(
                    content="Done",
                    sender="Alice",
                    minutes_after_start=2,
                ),
            ],
        )

        assert result.done_count == 2

        assert result.done_attendees == (
            "Alice",
            "Alice",
        )

    def test_non_done_messages_are_excluded_from_done_events(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Non-Done messages do not produce DoneEvents.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Insight",
                ),
            ],
        )

        assert result.done_count == 0

    def test_build_done_events_utility(
        self,
        builder: SessionBuilder,
    ) -> None:
        """
        Public Done utility builds DoneEvents.
        """

        result = builder.build_done_events(
            [
                session_start_message(),
                study_message(
                    content="Done",
                ),
            ]
        )

        assert len(result) == 1

        assert isinstance(
            result[0],
            DoneEvent,
        )


# ============================================================================
# Activity Events
# ============================================================================


class TestActivityEvents:
    """
    Test ActivityEvent construction.
    """

    @pytest.mark.parametrize(
        (
            "content",
            "expected_type",
        ),
        [
            (
                "Scripture Reading",
                ActivityType.SCRIPTURE_READING,
            ),
            (
                "Insight",
                ActivityType.INSIGHT,
            ),
            (
                "Discussion",
                ActivityType.DISCUSSION,
            ),
            (
                "Announcement",
                ActivityType.ANNOUNCEMENT,
            ),
            (
                "Done",
                ActivityType.DONE,
            ),
        ],
    )
    def test_supported_activity_is_classified(
        self,
        builder: SessionBuilder,
        session_date: date,
        content: str,
        expected_type: ActivityType,
    ) -> None:
        """
        Supported activities are converted to ActivityEvents.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content=content,
                ),
            ],
        )

        assert result.activity_count == 1

        assert result.activity_events[0].activity_type is expected_type

    def test_unclassified_message_is_handled_by_domain_policy(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Activity classification remains delegated to the Domain Policy.

        The SessionBuilder does not independently decide whether
        arbitrary content is supported or unsupported.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Random unsupported content",
                ),
            ],
        )

        assert result.activity_count == 1

        assert isinstance(
            result.activity_events[0],
            ActivityEvent,
        )

    def test_activity_event_preserves_source_message(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        ActivityEvent preserves its originating Message.
        """

        message = study_message(
            content="Insight",
        )

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                message,
            ],
        )

        assert result.activity_events[0].source_message is message

    def test_prayer_session_is_opened_and_classified(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        An opening prayer marker activates Prayer Session
        classification for subsequent supported messages.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Opening Prayer",
                ),
                study_message(
                    content="Prayer Session",
                    minutes_after_start=2,
                ),
            ],
        )

        assert any(
            event.activity_type is ActivityType.PRAYER_SESSION
            for event in result.activity_events
        )

    def test_prayer_session_closing_marker_closes_prayer_state(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Prayer activity classification remains active through the
        closing marker because the builder updates the prayer state
        after classification.

        The closing marker then closes the state for subsequent messages.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Opening Prayer",
                ),
                study_message(
                    content="Prayer Session",
                    minutes_after_start=2,
                ),
                study_message(
                    content="Closing Prayer",
                    minutes_after_start=3,
                ),
            ],
        )

        prayer_events = tuple(
            event
            for event in result.activity_events
            if event.activity_type is ActivityType.PRAYER_SESSION
        )

        assert len(prayer_events) == 3

    def test_build_activity_events_utility(
        self,
        builder: SessionBuilder,
    ) -> None:
        """
        Public activity utility builds ActivityEvents.
        """

        result = builder.build_activity_events(
            [
                session_start_message(),
                study_message(
                    content="Insight",
                ),
            ]
        )

        assert len(result) == 1

        assert isinstance(
            result[0],
            ActivityEvent,
        )


# ============================================================================
# Session Aggregate
# ============================================================================


class TestSessionAggregate:
    """
    Test final Session aggregate construction.
    """

    def test_build_returns_session(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        build returns a Session aggregate.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Insight",
                ),
            ],
        )

        assert isinstance(
            result,
            Session,
        )

    def test_preserves_session_date(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        The supplied session date is preserved.
        """

        result = builder.build(
            session_date=session_date,
            messages=[],
        )

        assert result.session_date == session_date

    def test_builds_all_event_collections(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        A mixed message stream produces the expected event collections.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Insight",
                    sender="Alice",
                ),
                study_message(
                    content="Done",
                    sender="Bob",
                    minutes_after_start=2,
                ),
            ],
        )

        assert result.attendance_count == 2
        assert result.done_count == 1
        assert result.activity_count >= 1

    def test_event_collections_are_tuples(
        self,
        builder: SessionBuilder,
        session_date: date,
    ) -> None:
        """
        Session event collections are immutable tuples.
        """

        result = builder.build(
            session_date=session_date,
            messages=[
                session_start_message(),
                study_message(
                    content="Insight",
                ),
            ],
        )

        assert isinstance(
            result.attendance_events,
            tuple,
        )

        assert isinstance(
            result.done_events,
            tuple,
        )

        assert isinstance(
            result.activity_events,
            tuple,
        )
