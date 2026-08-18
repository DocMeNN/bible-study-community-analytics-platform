# tests/domain/models/test_done_event.py

"""
Tests for the DoneEvent domain model.
"""

from datetime import datetime

import pytest

from src.domain.models.done_event import DoneEvent
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
def done_event(
    source_message: Message,
) -> DoneEvent:
    """Return a valid Done event."""
    return DoneEvent(
        attendee="Alice",
        source_message=source_message,
    )


def test_creates_valid_done_event(
    done_event: DoneEvent,
) -> None:
    """A valid Done acknowledgement should be created."""
    assert done_event.attendee == "Alice"


def test_attendee_name_is_trimmed(
    source_message: Message,
) -> None:
    """Whitespace around the attendee name should be removed."""
    event = DoneEvent(
        attendee="  Alice  ",
        source_message=source_message,
    )

    assert event.attendee == "Alice"


def test_empty_attendee_is_rejected(
    source_message: Message,
) -> None:
    """An empty attendee name should raise ValueError."""
    with pytest.raises(ValueError):
        DoneEvent(
            attendee="   ",
            source_message=source_message,
        )


def test_invalid_source_message_is_rejected() -> None:
    """A non-Message source should raise TypeError."""
    with pytest.raises(TypeError):
        DoneEvent(
            attendee="Alice",
            source_message="invalid",  # type: ignore[arg-type]
        )


def test_timestamp_comes_from_source_message(
    done_event: DoneEvent,
    source_message: Message,
) -> None:
    """The event timestamp should come from its source message."""
    assert done_event.timestamp == source_message.timestamp


def test_date_and_time_properties(
    done_event: DoneEvent,
) -> None:
    """Date and time should be derived from the source message."""
    assert done_event.event_date == datetime(2026, 7, 22).date()
    assert (
        done_event.event_time
        == datetime(
            2026,
            7,
            22,
            8,
            30,
        ).time()
    )


def test_source_metadata_is_exposed(
    done_event: DoneEvent,
) -> None:
    """Source metadata should be available through the event."""
    assert done_event.sender == "Alice"
    assert done_event.line_number == 42
    assert done_event.attendee_name == "Alice"
    assert done_event.message_text == "Done"


def test_event_comparison(
    source_message: Message,
) -> None:
    """Done events should compare chronologically."""
    earlier = DoneEvent(
        attendee="Alice",
        source_message=source_message,
    )

    later_message = Message(
        timestamp=datetime(2026, 7, 22, 9, 30),
        sender="Alice",
        content="Done",
        line_number=43,
    )

    later = DoneEvent(
        attendee="Alice",
        source_message=later_message,
    )

    assert earlier.occurred_before(later) is True
    assert later.occurred_after(earlier) is True


def test_same_attendee_is_case_insensitive(
    source_message: Message,
) -> None:
    """Attendee comparison should ignore case."""
    first = DoneEvent(
        attendee="Alice",
        source_message=source_message,
    )

    second = DoneEvent(
        attendee="alice",
        source_message=source_message,
    )

    assert first.same_attendee(second) is True


def test_to_dict_returns_event_data(
    done_event: DoneEvent,
) -> None:
    """The event should serialize to a dictionary."""
    result = done_event.to_dict()

    assert result == {
        "attendee": "Alice",
        "timestamp": datetime(2026, 7, 22, 8, 30),
        "sender": "Alice",
        "line_number": 42,
        "message": "Done",
    }


def test_done_event_is_immutable(
    done_event: DoneEvent,
) -> None:
    """DoneEvent should be immutable."""
    with pytest.raises(AttributeError):
        done_event.attendee = "Bob"  # type: ignore[misc]
