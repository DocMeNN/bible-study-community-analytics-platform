# tests/domain/models/test_attendance_event.py

"""
Tests for the AttendanceEvent domain model.
"""

from datetime import datetime

import pytest

from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.message import Message


@pytest.fixture
def source_message() -> Message:
    """Return a valid source message."""
    return Message(
        timestamp=datetime(2026, 7, 22, 8, 30),
        sender="Alice",
        content="Done",
        line_number=42,
    )


@pytest.fixture
def attendance_event(
    source_message: Message,
) -> AttendanceEvent:
    """Return a valid attendance event."""
    return AttendanceEvent(
        attendee="Alice",
        source_message=source_message,
    )


def test_creates_valid_attendance_event(
    attendance_event: AttendanceEvent,
) -> None:
    """A valid participation event should be created."""
    assert attendance_event.attendee == "Alice"


def test_attendee_name_is_trimmed(
    source_message: Message,
) -> None:
    """Whitespace around the attendee name should be removed."""
    event = AttendanceEvent(
        attendee="  Alice  ",
        source_message=source_message,
    )

    assert event.attendee == "Alice"


def test_empty_attendee_is_rejected(
    source_message: Message,
) -> None:
    """An empty attendee name should raise ValueError."""
    with pytest.raises(ValueError):
        AttendanceEvent(
            attendee="   ",
            source_message=source_message,
        )


def test_invalid_source_message_is_rejected() -> None:
    """A non-Message source should raise TypeError."""
    with pytest.raises(TypeError):
        AttendanceEvent(
            attendee="Alice",
            source_message="invalid",  # type: ignore[arg-type]
        )


def test_timestamp_comes_from_source_message(
    attendance_event: AttendanceEvent,
    source_message: Message,
) -> None:
    """The event timestamp should come from its source message."""
    assert attendance_event.timestamp == source_message.timestamp


def test_date_and_time_properties(
    attendance_event: AttendanceEvent,
) -> None:
    """Date and time should be derived from the source message."""
    assert attendance_event.event_date == datetime(2026, 7, 22).date()
    assert (
        attendance_event.event_time
        == datetime(
            2026,
            7,
            22,
            8,
            30,
        ).time()
    )


def test_source_metadata_is_exposed(
    attendance_event: AttendanceEvent,
) -> None:
    """Source metadata should be available through the event."""
    assert attendance_event.line_number == 42
    assert attendance_event.sender == "Alice"
    assert attendance_event.attendee_name == "Alice"


def test_participation_is_present(
    attendance_event: AttendanceEvent,
) -> None:
    """Every AttendanceEvent represents present participation."""
    assert attendance_event.is_present is True


def test_absence_and_lateness_are_not_represented(
    attendance_event: AttendanceEvent,
) -> None:
    """Absence and lateness are not represented by the event."""
    assert attendance_event.is_absent is False
    assert attendance_event.is_late is False


def test_event_comparison(
    source_message: Message,
) -> None:
    """Events should compare chronologically."""
    earlier = AttendanceEvent(
        attendee="Alice",
        source_message=source_message,
    )

    later_message = Message(
        timestamp=datetime(2026, 7, 22, 9, 30),
        sender="Alice",
        content="Done",
        line_number=43,
    )

    later = AttendanceEvent(
        attendee="Alice",
        source_message=later_message,
    )

    assert earlier.occurred_before(later) is True
    assert later.occurred_after(earlier) is True


def test_same_attendee_is_case_insensitive(
    source_message: Message,
) -> None:
    """Attendee comparison should ignore case."""
    first = AttendanceEvent(
        attendee="Alice",
        source_message=source_message,
    )

    second = AttendanceEvent(
        attendee="alice",
        source_message=source_message,
    )

    assert first.same_attendee(second) is True


def test_to_dict_returns_event_data(
    attendance_event: AttendanceEvent,
) -> None:
    """The event should serialize to a dictionary."""
    result = attendance_event.to_dict()

    assert result == {
        "attendee": "Alice",
        "timestamp": datetime(2026, 7, 22, 8, 30),
        "sender": "Alice",
        "line_number": 42,
    }


def test_attendance_event_is_immutable(
    attendance_event: AttendanceEvent,
) -> None:
    """AttendanceEvent should be immutable."""
    with pytest.raises(AttributeError):
        attendance_event.attendee = "Bob"  # type: ignore[misc]
