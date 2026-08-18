# tests/domain/models/test_activity_event.py

"""
Tests for the ActivityEvent domain model.
"""

from datetime import datetime

import pytest

from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.message import Message


@pytest.fixture
def source_message() -> Message:
    """Return a valid source message."""
    return Message(
        timestamp=datetime(2026, 7, 22, 8, 30),
        sender="Alice",
        content="Insight from today's reading",
        line_number=42,
    )


@pytest.fixture
def activity_event(
    source_message: Message,
) -> ActivityEvent:
    """Return a valid activity event."""
    return ActivityEvent(
        activity_type=ActivityType.INSIGHT,
        source_message=source_message,
    )


def test_creates_valid_activity_event(
    activity_event: ActivityEvent,
) -> None:
    """A valid activity event should be created."""
    assert activity_event.activity_type is ActivityType.INSIGHT


def test_invalid_activity_type_is_rejected(
    source_message: Message,
) -> None:
    """A non-ActivityType value should raise TypeError."""
    with pytest.raises(TypeError):
        ActivityEvent(
            activity_type="Insight",  # type: ignore[arg-type]
            source_message=source_message,
        )


def test_invalid_source_message_is_rejected() -> None:
    """A non-Message source should raise TypeError."""
    with pytest.raises(TypeError):
        ActivityEvent(
            activity_type=ActivityType.INSIGHT,
            source_message="invalid",  # type: ignore[arg-type]
        )


def test_timestamp_comes_from_source_message(
    activity_event: ActivityEvent,
    source_message: Message,
) -> None:
    """The event timestamp should come from its source message."""
    assert activity_event.timestamp == source_message.timestamp


def test_date_and_time_properties(
    activity_event: ActivityEvent,
) -> None:
    """Date and time should be derived from the source message."""
    assert activity_event.event_date == datetime(2026, 7, 22).date()
    assert (
        activity_event.event_time
        == datetime(
            2026,
            7,
            22,
            8,
            30,
        ).time()
    )


def test_source_metadata_is_exposed(
    activity_event: ActivityEvent,
) -> None:
    """Source metadata should be available through the event."""
    assert activity_event.sender == "Alice"
    assert activity_event.line_number == 42


@pytest.mark.parametrize(
    "activity_type, property_name",
    [
        (
            ActivityType.SCRIPTURE_READING,
            "is_scripture_reading",
        ),
        (
            ActivityType.INSIGHT,
            "is_insight",
        ),
        (
            ActivityType.DISCUSSION,
            "is_discussion",
        ),
        (
            ActivityType.ANNOUNCEMENT,
            "is_announcement",
        ),
        (
            ActivityType.DONE,
            "is_done",
        ),
        (
            ActivityType.PRAYER_SESSION,
            "is_prayer_session",
        ),
    ],
)
def test_activity_classification_properties(
    source_message: Message,
    activity_type: ActivityType,
    property_name: str,
) -> None:
    """Each classification property should identify its own activity."""
    event = ActivityEvent(
        activity_type=activity_type,
        source_message=source_message,
    )

    assert getattr(event, property_name) is True


def test_activity_name_returns_enum_value(
    activity_event: ActivityEvent,
) -> None:
    """The activity name should return the human-readable enum value."""
    assert activity_event.activity_name == "Insight"


def test_occurred_before_and_after(
    source_message: Message,
) -> None:
    """Events should compare chronologically."""
    earlier = ActivityEvent(
        activity_type=ActivityType.INSIGHT,
        source_message=source_message,
    )

    later_message = Message(
        timestamp=datetime(2026, 7, 22, 9, 30),
        sender="Alice",
        content="Another insight",
        line_number=43,
    )

    later = ActivityEvent(
        activity_type=ActivityType.DISCUSSION,
        source_message=later_message,
    )

    assert earlier.occurred_before(later) is True
    assert later.occurred_after(earlier) is True


def test_to_dict_returns_event_data(
    activity_event: ActivityEvent,
) -> None:
    """The event should serialize to a dictionary."""
    result = activity_event.to_dict()

    assert result == {
        "activity_type": "Insight",
        "timestamp": datetime(2026, 7, 22, 8, 30),
        "sender": "Alice",
        "line_number": 42,
    }


def test_activity_event_is_immutable(
    activity_event: ActivityEvent,
) -> None:
    """ActivityEvent should be immutable."""
    with pytest.raises(AttributeError):
        activity_event.activity_type = ActivityType.DONE  # type: ignore[misc]
