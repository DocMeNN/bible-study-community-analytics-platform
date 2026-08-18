# tests/domain/analytics/test_leaderboards.py

"""
Tests for Domain Leaderboard Analytics.
"""

from datetime import datetime

from src.domain.analytics.leaderboards import (
    participant_rank,
    rank_activities,
    rank_participation,
    rank_total_participation,
    top_members,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.message import Message

# ============================================================================
# Test Helpers
# ============================================================================


def build_message(
    *,
    sender: str,
    content: str,
    line_number: int,
) -> Message:
    """Build a test message."""

    return Message(
        timestamp=datetime(
            2026,
            7,
            22,
            10,
            line_number,
        ),
        sender=sender,
        content=content,
        line_number=line_number,
    )


def build_attendance_event(
    *,
    attendee: str,
    line_number: int,
) -> AttendanceEvent:
    """Build a test attendance event."""

    return AttendanceEvent(
        attendee=attendee,
        source_message=build_message(
            sender=attendee,
            content="Participation",
            line_number=line_number,
        ),
    )


def build_activity_event(
    *,
    sender: str,
    line_number: int,
) -> ActivityEvent:
    """Build a test activity event."""

    return ActivityEvent(
        activity_type=ActivityType.INSIGHT,
        source_message=build_message(
            sender=sender,
            content="Activity",
            line_number=line_number,
        ),
    )


# ============================================================================
# Participation Rankings
# ============================================================================


def test_rank_participation_counts_events() -> None:
    """Members should be ranked by attendance event frequency."""

    events = (
        build_attendance_event(
            attendee="Alice",
            line_number=1,
        ),
        build_attendance_event(
            attendee="Bob",
            line_number=2,
        ),
        build_attendance_event(
            attendee="Alice",
            line_number=3,
        ),
        build_attendance_event(
            attendee="Alice",
            line_number=4,
        ),
        build_attendance_event(
            attendee="Bob",
            line_number=5,
        ),
    )

    result = rank_participation(events)

    assert result == (
        ("Alice", 3),
        ("Bob", 2),
    )


def test_rank_participation_returns_empty_for_empty_input() -> None:
    """Empty attendance input should return empty rankings."""

    assert rank_participation([]) == ()


# ============================================================================
# Activity Rankings
# ============================================================================


def test_rank_activities_counts_activity_events() -> None:
    """Members should be ranked by activity event frequency."""

    events = (
        build_activity_event(
            sender="Alice",
            line_number=1,
        ),
        build_activity_event(
            sender="Bob",
            line_number=2,
        ),
        build_activity_event(
            sender="Alice",
            line_number=3,
        ),
    )

    result = rank_activities(events)

    assert result == (
        ("Alice", 2),
        ("Bob", 1),
    )


def test_rank_activities_returns_empty_for_empty_input() -> None:
    """Empty activity input should return empty rankings."""

    assert rank_activities([]) == ()


# ============================================================================
# Combined Participation Rankings
# ============================================================================


def test_rank_total_participation_combines_attendance_and_activity() -> None:
    """Total rankings should combine attendance and activity events."""

    attendance_events = (
        build_attendance_event(
            attendee="Alice",
            line_number=1,
        ),
        build_attendance_event(
            attendee="Bob",
            line_number=2,
        ),
    )

    activity_events = (
        build_activity_event(
            sender="Alice",
            line_number=3,
        ),
        build_activity_event(
            sender="Alice",
            line_number=4,
        ),
        build_activity_event(
            sender="Bob",
            line_number=5,
        ),
    )

    result = rank_total_participation(
        attendance_events,
        activity_events,
    )

    assert result == (
        ("Alice", 3),
        ("Bob", 2),
    )


def test_rank_total_participation_returns_empty_for_empty_input() -> None:
    """Empty attendance and activity inputs should return empty rankings."""

    assert (
        rank_total_participation(
            [],
            [],
        )
        == ()
    )


# ============================================================================
# Top Members
# ============================================================================


def test_top_members_returns_requested_limit() -> None:
    """Top members should respect the requested limit."""

    rankings = (
        ("Alice", 10),
        ("Bob", 8),
        ("Charlie", 6),
    )

    assert top_members(
        rankings,
        limit=2,
    ) == (
        ("Alice", 10),
        ("Bob", 8),
    )


def test_top_members_returns_all_when_limit_exceeds_size() -> None:
    """A large limit should return all available rankings."""

    rankings = (
        ("Alice", 10),
        ("Bob", 8),
    )

    assert (
        top_members(
            rankings,
            limit=10,
        )
        == rankings
    )


def test_top_members_with_zero_limit_returns_empty() -> None:
    """A zero limit should return no members."""

    rankings = (
        ("Alice", 10),
        ("Bob", 8),
    )

    assert (
        top_members(
            rankings,
            limit=0,
        )
        == ()
    )


def test_top_members_rejects_negative_limit() -> None:
    """Negative limits should be rejected."""

    rankings = (("Alice", 10),)

    try:
        top_members(
            rankings,
            limit=-1,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError for negative limit.",
        )


# ============================================================================
# Participant Rank
# ============================================================================


def test_participant_rank_returns_one_based_position() -> None:
    """Participant rank should start at position one."""

    rankings = (
        ("Alice", 10),
        ("Bob", 8),
        ("Charlie", 6),
    )

    assert (
        participant_rank(
            "Bob",
            rankings,
        )
        == 2
    )


def test_participant_rank_is_case_insensitive() -> None:
    """Participant lookup should ignore case."""

    rankings = (
        ("Alice", 10),
        ("Bob", 8),
    )

    assert (
        participant_rank(
            "alice",
            rankings,
        )
        == 1
    )


def test_participant_rank_returns_none_for_unknown_participant() -> None:
    """Unknown participants should have no ranking."""

    rankings = (
        ("Alice", 10),
        ("Bob", 8),
    )

    assert (
        participant_rank(
            "Charlie",
            rankings,
        )
        is None
    )


def test_participant_rank_supports_generator_input() -> None:
    """Participant ranking should support iterable input."""

    rankings = (
        ("Alice", 10),
        ("Bob", 8),
    )

    ranking_generator = (ranking for ranking in rankings)

    assert (
        participant_rank(
            "Bob",
            ranking_generator,
        )
        == 2
    )
