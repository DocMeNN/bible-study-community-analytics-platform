# tests/domain/models/test_scripture_event.py

"""
Tests for the ScriptureEvent domain model.
"""

from datetime import datetime

import pytest

from src.domain.models.message import Message
from src.domain.models.scripture_event import ScriptureEvent


@pytest.fixture
def source_message() -> Message:
    """Return a valid Scripture Reading source message."""
    return Message(
        timestamp=datetime(2026, 7, 22, 8, 30),
        sender="Alice",
        content="SCRIPTURES READING",
        line_number=42,
    )


@pytest.fixture
def scripture_event(
    source_message: Message,
) -> ScriptureEvent:
    """Return a valid ScriptureEvent."""
    return ScriptureEvent(
        source_message=source_message,
    )


def test_creates_valid_scripture_event(
    scripture_event: ScriptureEvent,
) -> None:
    """A valid ScriptureEvent should be created."""
    assert isinstance(scripture_event, ScriptureEvent)


def test_invalid_source_message_is_rejected() -> None:
    """A non-Message source should raise TypeError."""
    with pytest.raises(TypeError):
        ScriptureEvent(
            source_message="invalid",  # type: ignore[arg-type]
        )


def test_timestamp_comes_from_source_message(
    scripture_event: ScriptureEvent,
    source_message: Message,
) -> None:
    """The event timestamp should come from its source message."""
    assert scripture_event.timestamp == source_message.timestamp


def test_date_and_time_properties(
    scripture_event: ScriptureEvent,
) -> None:
    """Date and time should be derived from the source message."""
    assert (
        scripture_event.event_date
        == datetime(
            2026,
            7,
            22,
        ).date()
    )

    assert (
        scripture_event.event_time
        == datetime(
            2026,
            7,
            22,
            8,
            30,
        ).time()
    )


def test_source_metadata_is_exposed(
    scripture_event: ScriptureEvent,
) -> None:
    """Source metadata should be available through the event."""
    assert scripture_event.sender == "Alice"
    assert scripture_event.message_text == "SCRIPTURES READING"
    assert scripture_event.line_number == 42


def test_activity_classification(
    scripture_event: ScriptureEvent,
) -> None:
    """The event should identify itself as Scripture Reading."""
    assert scripture_event.activity_name == "Scripture Reading"
    assert scripture_event.is_scripture_reading is True


def test_events_compare_chronologically(
    source_message: Message,
) -> None:
    """Scripture events should compare chronologically."""
    earlier = ScriptureEvent(
        source_message=source_message,
    )

    later_message = Message(
        timestamp=datetime(2026, 7, 22, 9, 30),
        sender="Alice",
        content="SCRIPTURES READING",
        line_number=43,
    )

    later = ScriptureEvent(
        source_message=later_message,
    )

    assert earlier.occurred_before(later) is True
    assert later.occurred_after(earlier) is True


def test_events_can_be_compared_by_date(
    source_message: Message,
) -> None:
    """Scripture events should identify same-date events."""
    same_date_message = Message(
        timestamp=datetime(2026, 7, 22, 12, 0),
        sender="Bob",
        content="SCRIPTURES READING",
        line_number=43,
    )

    event_one = ScriptureEvent(
        source_message=source_message,
    )

    event_two = ScriptureEvent(
        source_message=same_date_message,
    )

    assert event_one.occurred_on_same_date(event_two) is True


def test_events_on_different_dates_are_not_same_date(
    source_message: Message,
) -> None:
    """Events on different dates should not match."""
    next_day_message = Message(
        timestamp=datetime(2026, 7, 23, 8, 30),
        sender="Bob",
        content="SCRIPTURES READING",
        line_number=43,
    )

    event_one = ScriptureEvent(
        source_message=source_message,
    )

    event_two = ScriptureEvent(
        source_message=next_day_message,
    )

    assert event_one.occurred_on_same_date(event_two) is False


def test_to_dict_returns_event_data(
    scripture_event: ScriptureEvent,
) -> None:
    """The event should serialize to a dictionary."""
    result = scripture_event.to_dict()

    assert result == {
        "activity_name": "Scripture Reading",
        "timestamp": datetime(2026, 7, 22, 8, 30),
        "event_date": datetime(2026, 7, 22).date(),
        "sender": "Alice",
        "message": "SCRIPTURES READING",
        "line_number": 42,
    }


def test_scripture_event_is_immutable(
    scripture_event: ScriptureEvent,
) -> None:
    """ScriptureEvent should be immutable."""
    with pytest.raises(AttributeError):
        scripture_event.source_message = None  # type: ignore[assignment]
