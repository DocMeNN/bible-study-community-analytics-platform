# tests/domain/analytics/test_done.py

"""
Tests for Domain Done Analytics.
"""

from datetime import date, datetime

import pytest

from src.domain.analytics.done import (
    count_done_by_member,
    count_done_events,
    count_done_for_member,
    done_count_by_date,
    done_count_by_member_for_period,
    done_count_by_period,
    done_summary,
    get_done_events,
    get_done_events_between,
    get_done_events_for_member,
    get_done_events_on_date,
    rank_members_by_done_count,
    top_done_members,
    unique_done_member_count,
)
from src.domain.models.done_event import DoneEvent
from src.domain.models.message import Message


@pytest.fixture
def events() -> tuple[DoneEvent, ...]:
    """Return sample Done acknowledgement events."""
    return (
        DoneEvent(
            attendee="Alice",
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 8, 30),
                sender="Alice",
                content="Done",
                line_number=3,
            ),
        ),
        DoneEvent(
            attendee="Bob",
            source_message=Message(
                timestamp=datetime(2026, 7, 21, 8, 15),
                sender="Bob",
                content="Done",
                line_number=2,
            ),
        ),
        DoneEvent(
            attendee="alice",
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 9, 0),
                sender="Alice",
                content="Done",
                line_number=4,
            ),
        ),
        DoneEvent(
            attendee="Charlie",
            source_message=Message(
                timestamp=datetime(2026, 7, 23, 10, 0),
                sender="Charlie",
                content="Done",
                line_number=5,
            ),
        ),
    )


def test_done_events_are_sorted_chronologically(
    events: tuple[DoneEvent, ...],
) -> None:
    """Done events should be returned chronologically."""
    result = get_done_events(events)

    assert [event.attendee for event in result] == [
        "Bob",
        "Alice",
        "alice",
        "Charlie",
    ]


def test_get_done_events_for_member_is_case_insensitive(
    events: tuple[DoneEvent, ...],
) -> None:
    """Member lookup should be case-insensitive."""
    result = get_done_events_for_member(events, "ALICE")

    assert len(result) == 2
    assert [event.attendee for event in result] == [
        "Alice",
        "alice",
    ]


def test_get_done_events_between_is_inclusive(
    events: tuple[DoneEvent, ...],
) -> None:
    """Datetime range boundaries should be inclusive."""
    result = get_done_events_between(
        events,
        datetime(2026, 7, 22, 8, 30),
        datetime(2026, 7, 22, 9, 0),
    )

    assert len(result) == 2


def test_get_done_events_on_date(
    events: tuple[DoneEvent, ...],
) -> None:
    """Events should be filtered by calendar date."""
    result = get_done_events_on_date(
        events,
        date(2026, 7, 22),
    )

    assert len(result) == 2


def test_count_done_events(
    events: tuple[DoneEvent, ...],
) -> None:
    """Every Done acknowledgement should be counted."""
    assert count_done_events(events) == 4


def test_count_done_for_member(
    events: tuple[DoneEvent, ...],
) -> None:
    """All acknowledgements from a member should be counted."""
    assert count_done_for_member(events, "alice") == 2
    assert count_done_for_member(events, "nobody") == 0


def test_count_done_by_member(
    events: tuple[DoneEvent, ...],
) -> None:
    """Counts should be grouped case-insensitively by member."""
    counts = count_done_by_member(events)

    assert counts["Alice"] == 2
    assert counts["Bob"] == 1
    assert counts["Charlie"] == 1
    assert len(counts) == 3


def test_unique_done_member_count(
    events: tuple[DoneEvent, ...],
) -> None:
    """Unique members should be counted."""
    assert unique_done_member_count(events) == 3


def test_rank_members_by_done_count(
    events: tuple[DoneEvent, ...],
) -> None:
    """Members should be ranked by count."""
    assert rank_members_by_done_count(events) == (
        ("Alice", 2),
        ("Bob", 1),
        ("Charlie", 1),
    )


def test_equal_counts_are_sorted_alphabetically(
    events: tuple[DoneEvent, ...],
) -> None:
    """Equal counts should be ordered alphabetically."""
    result = rank_members_by_done_count(events)

    assert result[1:] == (
        ("Bob", 1),
        ("Charlie", 1),
    )


def test_top_done_members(
    events: tuple[DoneEvent, ...],
) -> None:
    """Top members should respect the requested limit."""
    assert top_done_members(events, limit=2) == (
        ("Alice", 2),
        ("Bob", 1),
    )


def test_top_done_members_rejects_invalid_limit(
    events: tuple[DoneEvent, ...],
) -> None:
    """A non-positive limit should be rejected."""
    with pytest.raises(ValueError):
        top_done_members(events, limit=0)


def test_done_count_by_date(
    events: tuple[DoneEvent, ...],
) -> None:
    """Done acknowledgements should be counted by date."""
    counts = done_count_by_date(events)

    assert counts[date(2026, 7, 21)] == 1
    assert counts[date(2026, 7, 22)] == 2
    assert counts[date(2026, 7, 23)] == 1


def test_done_count_by_period(
    events: tuple[DoneEvent, ...],
) -> None:
    """Done acknowledgements should be counted within an inclusive period."""
    assert (
        done_count_by_period(
            events,
            date(2026, 7, 22),
            date(2026, 7, 22),
        )
        == 2
    )


def test_done_count_by_period_rejects_invalid_range(
    events: tuple[DoneEvent, ...],
) -> None:
    """Invalid date ranges should be rejected."""
    with pytest.raises(ValueError):
        done_count_by_period(
            events,
            date(2026, 7, 23),
            date(2026, 7, 21),
        )


def test_done_count_by_member_for_period(
    events: tuple[DoneEvent, ...],
) -> None:
    """Period member counts should include only events in the period."""
    counts = done_count_by_member_for_period(
        events,
        date(2026, 7, 22),
        date(2026, 7, 22),
    )

    assert counts["Alice"] == 2
    assert len(counts) == 1


def test_done_count_by_member_for_period_rejects_invalid_range(
    events: tuple[DoneEvent, ...],
) -> None:
    """Invalid period ranges should be rejected."""
    with pytest.raises(ValueError):
        done_count_by_member_for_period(
            events,
            date(2026, 7, 23),
            date(2026, 7, 21),
        )


def test_done_summary(
    events: tuple[DoneEvent, ...],
) -> None:
    """Done summary should contain expected analytics."""
    summary = done_summary(events)

    assert summary["done_count"] == 4
    assert summary["unique_member_count"] == 3
    assert summary["done_by_member"]["Alice"] == 2
    assert summary["done_by_date"][date(2026, 7, 22)] == 2
    assert summary["first_done"].attendee == "Bob"
    assert summary["last_done"].attendee == "Charlie"


def test_empty_events_return_empty_results() -> None:
    """Empty Done collections should return empty analytics."""
    assert get_done_events([]) == ()
    assert count_done_events([]) == 0
    assert count_done_by_member([]) == {}
    assert unique_done_member_count([]) == 0
    assert rank_members_by_done_count([]) == ()
    assert top_done_members([]) == ()
    assert done_count_by_date({}) == {}
    assert done_summary([])["first_done"] is None
    assert done_summary([])["last_done"] is None


def test_generator_input_is_supported() -> None:
    """Analytics should support iterable inputs."""
    messages = (
        Message(
            timestamp=datetime(2026, 7, 22, 8, 0),
            sender="Alice",
            content="Done",
            line_number=1,
        ),
        Message(
            timestamp=datetime(2026, 7, 22, 8, 1),
            sender="Bob",
            content="Done",
            line_number=2,
        ),
    )

    generator = (
        DoneEvent(
            attendee=message.sender,
            source_message=message,
        )
        for message in messages
    )

    assert count_done_events(generator) == 2
