# tests/domain/analytics/test_activity.py

"""
Tests for Domain Activity Analytics.
"""

from datetime import datetime

import pytest

from src.domain.analytics.activity import (
    activity_names,
    activity_summary,
    activity_value_counts,
    count_activity_events,
    count_activity_types,
    count_unique_activity_types,
    first_activity_event,
    first_activity_name,
    first_activity_type,
    get_activity_events,
    get_events_by_type,
    has_activity,
    last_activity_event,
    last_activity_name,
    last_activity_type,
    unique_activity_names,
    unique_activity_types,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.message import Message


@pytest.fixture
def events() -> tuple[ActivityEvent, ...]:
    """Return sample activity events."""
    return (
        ActivityEvent(
            activity_type=ActivityType.INSIGHT,
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 8, 30),
                sender="Alice",
                content="My insight",
                line_number=3,
            ),
        ),
        ActivityEvent(
            activity_type=ActivityType.SCRIPTURE_READING,
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 8, 0),
                sender="Admin",
                content="SCRIPTURES READING",
                line_number=1,
            ),
        ),
        ActivityEvent(
            activity_type=ActivityType.DONE,
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 8, 15),
                sender="Bob",
                content="Done",
                line_number=2,
            ),
        ),
        ActivityEvent(
            activity_type=ActivityType.INSIGHT,
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 9, 0),
                sender="Charlie",
                content="Another insight",
                line_number=4,
            ),
        ),
    )


def test_events_are_sorted_chronologically(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Events should be returned in chronological order."""
    result = get_activity_events(events)

    assert [event.activity_type for event in result] == [
        ActivityType.SCRIPTURE_READING,
        ActivityType.DONE,
        ActivityType.INSIGHT,
        ActivityType.INSIGHT,
    ]


def test_get_events_by_type_returns_matching_events(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Events should be filtered by activity type."""
    result = get_events_by_type(
        events,
        ActivityType.INSIGHT,
    )

    assert len(result) == 2
    assert all(event.activity_type is ActivityType.INSIGHT for event in result)


def test_count_activity_events(
    events: tuple[ActivityEvent, ...],
) -> None:
    """All activity events should be counted."""
    assert count_activity_events(events) == 4


def test_count_activity_types(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Activity events should be counted by type."""
    counts = count_activity_types(events)

    assert counts[ActivityType.INSIGHT] == 2
    assert counts[ActivityType.SCRIPTURE_READING] == 1
    assert counts[ActivityType.DONE] == 1


def test_activity_value_counts_matches_type_counts(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Activity value counts should group events by type."""
    assert activity_value_counts(events) == count_activity_types(events)


def test_count_unique_activity_types(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Unique activity types should be counted."""
    assert count_unique_activity_types(events) == 3


def test_first_and_last_activity_events(
    events: tuple[ActivityEvent, ...],
) -> None:
    """First and last activities should be identified chronologically."""
    assert first_activity_event(events).activity_type is ActivityType.SCRIPTURE_READING

    assert last_activity_event(events).activity_type is ActivityType.INSIGHT


def test_empty_events_return_none() -> None:
    """Empty activity collections should have no first or last event."""
    assert first_activity_event([]) is None
    assert last_activity_event([]) is None
    assert first_activity_type([]) is None
    assert last_activity_type([]) is None
    assert first_activity_name([]) is None
    assert last_activity_name([]) is None


@pytest.mark.parametrize(
    "activity_type",
    [
        ActivityType.SCRIPTURE_READING,
        ActivityType.INSIGHT,
        ActivityType.DONE,
    ],
)
def test_has_activity(
    events: tuple[ActivityEvent, ...],
    activity_type: ActivityType,
) -> None:
    """Existing activity types should be detected."""
    assert has_activity(events, activity_type) is True


def test_missing_activity_is_not_detected(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Missing activity types should not be detected."""
    assert (
        has_activity(
            events,
            ActivityType.PRAYER_SESSION,
        )
        is False
    )


def test_activity_names_preserve_chronological_order(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Activity names should follow chronological event order."""
    assert activity_names(events) == (
        "Scripture Reading",
        "Done",
        "Insight",
        "Insight",
    )


def test_unique_activity_types_preserve_first_seen_order(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Unique activity types should preserve chronological first-seen order."""
    assert unique_activity_types(events) == (
        ActivityType.SCRIPTURE_READING,
        ActivityType.DONE,
        ActivityType.INSIGHT,
    )


def test_unique_activity_names_preserve_first_seen_order(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Unique activity names should preserve first-seen order."""
    assert unique_activity_names(events) == (
        "Scripture Reading",
        "Done",
        "Insight",
    )


def test_first_and_last_activity_types(
    events: tuple[ActivityEvent, ...],
) -> None:
    """First and last activity types should be identified."""
    assert first_activity_type(events) is ActivityType.SCRIPTURE_READING

    assert last_activity_type(events) is ActivityType.INSIGHT


def test_first_and_last_activity_names(
    events: tuple[ActivityEvent, ...],
) -> None:
    """First and last activity names should be identified."""
    assert first_activity_name(events) == "Scripture Reading"
    assert last_activity_name(events) == "Insight"


def test_activity_summary(
    events: tuple[ActivityEvent, ...],
) -> None:
    """Activity summary should contain expected values."""
    summary = activity_summary(events)

    assert summary["activity_count"] == 4
    assert summary["unique_activity_count"] == 3
    assert summary["unique_activity_types"] == (
        ActivityType.SCRIPTURE_READING,
        ActivityType.DONE,
        ActivityType.INSIGHT,
    )

    assert summary["first_activity"].activity_type is (ActivityType.SCRIPTURE_READING)

    assert summary["last_activity"].activity_type is (ActivityType.INSIGHT)


def test_generator_input_is_supported() -> None:
    """Analytics should support iterable inputs."""
    messages = (
        Message(
            timestamp=datetime(2026, 7, 22, 8, 0),
            sender="Admin",
            content="SCRIPTURES READING",
            line_number=1,
        ),
        Message(
            timestamp=datetime(2026, 7, 22, 8, 1),
            sender="Alice",
            content="Done",
            line_number=2,
        ),
    )

    generator = (
        ActivityEvent(
            activity_type=(
                ActivityType.SCRIPTURE_READING
                if message.content == "SCRIPTURES READING"
                else ActivityType.DONE
            ),
            source_message=message,
        )
        for message in messages
    )

    assert count_activity_events(generator) == 2
