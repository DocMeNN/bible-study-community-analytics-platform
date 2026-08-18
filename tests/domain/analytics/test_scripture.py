# tests/domain/analytics/test_scripture.py

"""
Tests for Domain Scripture Analytics.
"""

from datetime import datetime

from src.domain.analytics.scripture import (
    count_scripture_dates,
    count_scripture_events,
    first_scripture_event,
    get_scripture_events,
    get_scripture_events_by_date,
    has_scripture_reading_on_date,
    last_scripture_event,
    scripture_dates,
    scripture_summary,
)
from src.domain.models.message import Message
from src.domain.models.scripture_event import ScriptureEvent

# ============================================================================
# Test Helpers
# ============================================================================


def build_scripture_event(
    *,
    sender: str,
    line_number: int,
    year: int = 2026,
    month: int = 7,
    day: int = 22,
    hour: int = 10,
    minute: int = 0,
) -> ScriptureEvent:
    """Build a test Scripture Reading event."""

    message = Message(
        timestamp=datetime(
            year,
            month,
            day,
            hour,
            minute,
        ),
        sender=sender,
        content="SCRIPTURE READING",
        line_number=line_number,
    )

    return ScriptureEvent(
        source_message=message,
    )


# ============================================================================
# Retrieval
# ============================================================================


def test_get_scripture_events_returns_events_chronologically() -> None:
    """Scripture events should be ordered by timestamp."""

    late = build_scripture_event(
        sender="Late",
        line_number=2,
        hour=12,
    )

    early = build_scripture_event(
        sender="Early",
        line_number=1,
        hour=8,
    )

    result = get_scripture_events(
        (
            late,
            early,
        )
    )

    assert result == (
        early,
        late,
    )


def test_get_scripture_events_by_date_returns_matching_events() -> None:
    """Only events occurring on the requested date should be returned."""

    target = build_scripture_event(
        sender="Target",
        line_number=1,
        day=22,
    )

    other = build_scripture_event(
        sender="Other",
        line_number=2,
        day=23,
    )

    result = get_scripture_events_by_date(
        (
            target,
            other,
        ),
        target.event_date,
    )

    assert result == (target,)


# ============================================================================
# Counts
# ============================================================================


def test_count_scripture_events_returns_total_event_count() -> None:
    """Scripture event count should include every event."""

    events = (
        build_scripture_event(
            sender="Alice",
            line_number=1,
        ),
        build_scripture_event(
            sender="Bob",
            line_number=2,
        ),
        build_scripture_event(
            sender="Charlie",
            line_number=3,
        ),
    )

    assert count_scripture_events(events) == 3


def test_count_scripture_events_returns_zero_for_empty_input() -> None:
    """Empty input should return zero Scripture events."""

    assert count_scripture_events([]) == 0


def test_count_scripture_dates_counts_unique_dates() -> None:
    """Repeated events on one date should count as one date."""

    events = (
        build_scripture_event(
            sender="Alice",
            line_number=1,
            day=22,
        ),
        build_scripture_event(
            sender="Bob",
            line_number=2,
            day=22,
        ),
        build_scripture_event(
            sender="Charlie",
            line_number=3,
            day=23,
        ),
    )

    assert count_scripture_dates(events) == 2


# ============================================================================
# Timeline
# ============================================================================


def test_first_scripture_event_returns_earliest_event() -> None:
    """The first Scripture event should be the earliest event."""

    first = build_scripture_event(
        sender="First",
        line_number=1,
        hour=8,
    )

    second = build_scripture_event(
        sender="Second",
        line_number=2,
        hour=12,
    )

    assert (
        first_scripture_event(
            (
                second,
                first,
            )
        )
        == first
    )


def test_last_scripture_event_returns_latest_event() -> None:
    """The last Scripture event should be the latest event."""

    first = build_scripture_event(
        sender="First",
        line_number=1,
        hour=8,
    )

    last = build_scripture_event(
        sender="Last",
        line_number=2,
        hour=12,
    )

    assert (
        last_scripture_event(
            (
                first,
                last,
            )
        )
        == last
    )


def test_first_and_last_scripture_event_return_none_for_empty_input() -> None:
    """Empty input should return no first or last event."""

    assert first_scripture_event([]) is None
    assert last_scripture_event([]) is None


# ============================================================================
# Date Utilities
# ============================================================================


def test_scripture_dates_returns_unique_dates_chronologically() -> None:
    """Scripture dates should be unique and chronologically ordered."""

    events = (
        build_scripture_event(
            sender="Later",
            line_number=3,
            day=24,
        ),
        build_scripture_event(
            sender="Earlier",
            line_number=1,
            day=22,
        ),
        build_scripture_event(
            sender="Same Day",
            line_number=2,
            day=22,
        ),
        build_scripture_event(
            sender="Middle",
            line_number=4,
            day=23,
        ),
    )

    result = scripture_dates(events)

    assert result == (
        events[1].event_date,
        events[3].event_date,
        events[0].event_date,
    )


def test_has_scripture_reading_on_date_returns_true_for_matching_date() -> None:
    """A matching Scripture event should return True."""

    event = build_scripture_event(
        sender="Alice",
        line_number=1,
        day=22,
    )

    assert (
        has_scripture_reading_on_date(
            (event,),
            event.event_date,
        )
        is True
    )


def test_has_scripture_reading_on_date_returns_false_without_match() -> None:
    """No matching Scripture event should return False."""

    event = build_scripture_event(
        sender="Alice",
        line_number=1,
        day=22,
    )

    assert (
        has_scripture_reading_on_date(
            (event,),
            event.event_date.replace(
                day=23,
            ),
        )
        is False
    )


# ============================================================================
# Summary
# ============================================================================


def test_scripture_summary_returns_complete_summary() -> None:
    """Scripture summary should contain all expected analytics."""

    first = build_scripture_event(
        sender="First",
        line_number=1,
        day=22,
        hour=8,
    )

    second = build_scripture_event(
        sender="Second",
        line_number=2,
        day=23,
        hour=10,
    )

    result = scripture_summary(
        (
            second,
            first,
        )
    )

    assert result["scripture_event_count"] == 2
    assert result["scripture_date_count"] == 2
    assert result["first_scripture_event"] == first
    assert result["last_scripture_event"] == second
    assert result["scripture_dates"] == (
        first.event_date,
        second.event_date,
    )


def test_scripture_summary_returns_empty_summary_for_empty_input() -> None:
    """Empty input should produce an empty Scripture summary."""

    result = scripture_summary([])

    assert result == {
        "scripture_event_count": 0,
        "scripture_date_count": 0,
        "first_scripture_event": None,
        "last_scripture_event": None,
        "scripture_dates": (),
    }
