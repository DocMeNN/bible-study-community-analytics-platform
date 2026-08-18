# src/domain/analytics/scripture.py

"""
Domain Scripture Analytics

Purpose
-------
Provides business logic for Scripture Reading events.

Responsibilities
----------------
- Retrieve Scripture Reading events.
- Order Scripture Reading events chronologically.
- Count Scripture Reading events.
- Identify first and last Scripture Reading events.
- Retrieve Scripture Reading events by date.
- Provide Scripture Reading timeline utilities.

Notes
-----
- Pure domain analytics.
- No pandas.
- No Streamlit.
- No database access.
- No file I/O.
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
from src.domain.models.scripture_event import ScriptureEvent

# ============================================================================
# Retrieval
# ============================================================================


def get_scripture_events(
    scripture_events: Iterable[ScriptureEvent],
) -> tuple[ScriptureEvent, ...]:
    """
    Return Scripture Reading events ordered chronologically.
    """

    return tuple(
        sorted(
            scripture_events,
            key=lambda event: event.timestamp,
        )
    )


def get_scripture_events_by_date(
    scripture_events: Iterable[ScriptureEvent],
    event_date: date,
) -> tuple[ScriptureEvent, ...]:
    """
    Return Scripture Reading events occurring on a specific date.
    """

    return tuple(
        event
        for event in get_scripture_events(scripture_events)
        if event.event_date == event_date
    )


# ============================================================================
# Counts
# ============================================================================


def count_scripture_events(
    scripture_events: Iterable[ScriptureEvent],
) -> int:
    """
    Return the total number of Scripture Reading events.
    """

    return len(get_scripture_events(scripture_events))


def count_scripture_dates(
    scripture_events: Iterable[ScriptureEvent],
) -> int:
    """
    Return the number of unique dates containing Scripture Reading events.
    """

    return len({event.event_date for event in scripture_events})


# ============================================================================
# Timeline
# ============================================================================


def first_scripture_event(
    scripture_events: Iterable[ScriptureEvent],
) -> ScriptureEvent | None:
    """
    Return the first Scripture Reading event.
    """

    events = get_scripture_events(scripture_events)

    if not events:
        return None

    return events[0]


def last_scripture_event(
    scripture_events: Iterable[ScriptureEvent],
) -> ScriptureEvent | None:
    """
    Return the last Scripture Reading event.
    """

    events = get_scripture_events(scripture_events)

    if not events:
        return None

    return events[-1]


# ============================================================================
# Date Utilities
# ============================================================================


def scripture_dates(
    scripture_events: Iterable[ScriptureEvent],
) -> tuple[date, ...]:
    """
    Return unique Scripture Reading dates in chronological order.
    """

    dates = sorted({event.event_date for event in scripture_events})

    return tuple(dates)


def has_scripture_reading_on_date(
    scripture_events: Iterable[ScriptureEvent],
    event_date: date,
) -> bool:
    """
    Return True if Scripture Reading occurred on the specified date.
    """

    return bool(
        get_scripture_events_by_date(
            scripture_events,
            event_date,
        )
    )


# ============================================================================
# Summary
# ============================================================================


def scripture_summary(
    scripture_events: Iterable[ScriptureEvent],
) -> dict[str, object]:
    """
    Return a summary of Scripture Reading analytics.
    """

    events = get_scripture_events(scripture_events)

    return {
        "scripture_event_count": len(events),
        "scripture_date_count": count_scripture_dates(events),
        "first_scripture_event": first_scripture_event(events),
        "last_scripture_event": last_scripture_event(events),
        "scripture_dates": scripture_dates(events),
    }
