# tests/domain/analytics/test_sessions.py

"""
Tests for Domain Session Analytics.
"""

from datetime import date, datetime, timedelta

from src.domain.analytics.sessions import (
    calculate_average_duration,
    calculate_total_duration,
    count_sessions,
    get_earliest_session,
    get_latest_session,
    session_summary,
    total_activity_events,
    total_attendance_events,
    total_unique_attendees,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Test Helpers
# ============================================================================


def build_message(
    *,
    sender: str,
    content: str,
    line_number: int,
    hour: int = 10,
    minute: int = 0,
) -> Message:
    """Build a test message."""

    return Message(
        timestamp=datetime(
            2026,
            7,
            22,
            hour,
            minute,
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
            content="Insight",
            line_number=line_number,
        ),
    )


def build_session(
    *,
    session_date: date,
    attendance: tuple[str, ...] = (),
    activity_senders: tuple[str, ...] = (),
) -> Session:
    """Build a test session."""

    attendance_events = tuple(
        build_attendance_event(
            attendee=attendee,
            line_number=index,
        )
        for index, attendee in enumerate(
            attendance,
            start=1,
        )
    )

    activity_events = tuple(
        build_activity_event(
            sender=sender,
            line_number=100 + index,
        )
        for index, sender in enumerate(
            activity_senders,
            start=1,
        )
    )

    return Session(
        session_date=session_date,
        attendance_events=attendance_events,
        activity_events=activity_events,
    )


def build_session_with_duration(
    *,
    session_date: date,
    start_hour: int,
    start_minute: int,
    end_hour: int,
    end_minute: int,
) -> Session:
    """Build a session with a controlled duration."""

    attendance_events = (
        AttendanceEvent(
            attendee="Alice",
            source_message=build_message(
                sender="Alice",
                content="Start",
                line_number=1,
                hour=start_hour,
                minute=start_minute,
            ),
        ),
        AttendanceEvent(
            attendee="Bob",
            source_message=build_message(
                sender="Bob",
                content="End",
                line_number=2,
                hour=end_hour,
                minute=end_minute,
            ),
        ),
    )

    return Session(
        session_date=session_date,
        attendance_events=attendance_events,
    )


# ============================================================================
# Session Counts
# ============================================================================


def test_count_sessions_returns_total_session_count() -> None:
    """Session count should return the number of sessions."""

    sessions = (
        build_session(session_date=date(2026, 7, 20)),
        build_session(session_date=date(2026, 7, 21)),
        build_session(session_date=date(2026, 7, 22)),
    )

    assert count_sessions(sessions) == 3


def test_count_sessions_returns_zero_for_empty_input() -> None:
    """Empty input should return zero sessions."""

    assert count_sessions([]) == 0


def test_count_sessions_supports_generator_input() -> None:
    """Session counting should support iterable generators."""

    sessions = (
        build_session(session_date=date(2026, 7, 20)),
        build_session(session_date=date(2026, 7, 21)),
    )

    session_generator = (session for session in sessions)

    assert count_sessions(session_generator) == 2


# ============================================================================
# Session Retrieval
# ============================================================================


def test_get_latest_session_returns_latest_by_date() -> None:
    """Latest session should be selected by session date."""

    sessions = (
        build_session(session_date=date(2026, 7, 20)),
        build_session(session_date=date(2026, 7, 22)),
        build_session(session_date=date(2026, 7, 21)),
    )

    result = get_latest_session(sessions)

    assert result is not None
    assert result.session_date == date(2026, 7, 22)


def test_get_latest_session_returns_none_for_empty_input() -> None:
    """Empty input should return no latest session."""

    assert get_latest_session([]) is None


def test_get_earliest_session_returns_earliest_by_date() -> None:
    """Earliest session should be selected by session date."""

    sessions = (
        build_session(session_date=date(2026, 7, 22)),
        build_session(session_date=date(2026, 7, 20)),
        build_session(session_date=date(2026, 7, 21)),
    )

    result = get_earliest_session(sessions)

    assert result is not None
    assert result.session_date == date(2026, 7, 20)


def test_get_earliest_session_returns_none_for_empty_input() -> None:
    """Empty input should return no earliest session."""

    assert get_earliest_session([]) is None


# ============================================================================
# Duration Analytics
# ============================================================================


def test_calculate_average_duration_returns_average_duration() -> None:
    """Average duration should be calculated across all sessions."""

    sessions = (
        build_session_with_duration(
            session_date=date(2026, 7, 20),
            start_hour=10,
            start_minute=0,
            end_hour=11,
            end_minute=0,
        ),
        build_session_with_duration(
            session_date=date(2026, 7, 21),
            start_hour=10,
            start_minute=0,
            end_hour=12,
            end_minute=0,
        ),
    )

    assert calculate_average_duration(sessions) == timedelta(
        hours=1,
        minutes=30,
    )


def test_calculate_average_duration_returns_zero_for_empty_input() -> None:
    """Average duration should be zero for no sessions."""

    assert calculate_average_duration([]) == timedelta(0)


def test_calculate_total_duration_returns_combined_duration() -> None:
    """Total duration should combine all session durations."""

    sessions = (
        build_session_with_duration(
            session_date=date(2026, 7, 20),
            start_hour=10,
            start_minute=0,
            end_hour=11,
            end_minute=0,
        ),
        build_session_with_duration(
            session_date=date(2026, 7, 21),
            start_hour=10,
            start_minute=0,
            end_hour=12,
            end_minute=0,
        ),
    )

    assert calculate_total_duration(sessions) == timedelta(hours=3)


def test_calculate_total_duration_returns_zero_for_empty_input() -> None:
    """Total duration should be zero for no sessions."""

    assert calculate_total_duration([]) == timedelta(0)


# ============================================================================
# Attendance Analytics
# ============================================================================


def test_total_attendance_events_sums_attendance_events() -> None:
    """Attendance events should be summed across sessions."""

    sessions = (
        build_session(
            session_date=date(2026, 7, 20),
            attendance=("Alice", "Bob"),
        ),
        build_session(
            session_date=date(2026, 7, 21),
            attendance=("Alice", "Bob", "Charlie"),
        ),
    )

    assert total_attendance_events(sessions) == 5


def test_total_attendance_events_returns_zero_for_empty_input() -> None:
    """Empty sessions should produce zero attendance events."""

    assert total_attendance_events([]) == 0


def test_total_unique_attendees_sums_unique_attendees_per_session() -> None:
    """
    Unique attendees should be counted independently per session.

    The same participant appearing in multiple sessions contributes
    once to each session's unique attendee count.
    """

    sessions = (
        build_session(
            session_date=date(2026, 7, 20),
            attendance=("Alice", "Bob", "Alice"),
        ),
        build_session(
            session_date=date(2026, 7, 21),
            attendance=("Alice", "Charlie"),
        ),
    )

    assert total_unique_attendees(sessions) == 4


def test_total_unique_attendees_returns_zero_for_empty_input() -> None:
    """Empty sessions should produce zero unique attendees."""

    assert total_unique_attendees([]) == 0


# ============================================================================
# Activity Analytics
# ============================================================================


def test_total_activity_events_sums_activity_events() -> None:
    """Activity events should be summed across sessions."""

    sessions = (
        build_session(
            session_date=date(2026, 7, 20),
            activity_senders=("Alice", "Bob"),
        ),
        build_session(
            session_date=date(2026, 7, 21),
            activity_senders=("Alice", "Charlie", "Bob"),
        ),
    )

    assert total_activity_events(sessions) == 5


def test_total_activity_events_returns_zero_for_empty_input() -> None:
    """Empty sessions should produce zero activity events."""

    assert total_activity_events([]) == 0


# ============================================================================
# Session Summary
# ============================================================================


def test_session_summary_returns_complete_summary() -> None:
    """Session summary should return all aggregate metrics."""

    sessions = (
        build_session_with_duration(
            session_date=date(2026, 7, 20),
            start_hour=10,
            start_minute=0,
            end_hour=11,
            end_minute=0,
        ),
        build_session_with_duration(
            session_date=date(2026, 7, 22),
            start_hour=10,
            start_minute=0,
            end_hour=12,
            end_minute=0,
        ),
    )

    result = session_summary(sessions)

    assert result["session_count"] == 2
    assert result["earliest_session"] == sessions[0]
    assert result["latest_session"] == sessions[1]
    assert result["total_duration"] == timedelta(hours=3)
    assert result["average_duration"] == timedelta(
        hours=1,
        minutes=30,
    )
    assert result["total_attendance_events"] == 4
    assert result["total_activity_events"] == 0


def test_session_summary_returns_empty_summary_for_empty_input() -> None:
    """Empty sessions should produce zero-valued aggregate metrics."""

    result = session_summary([])

    assert result["session_count"] == 0
    assert result["earliest_session"] is None
    assert result["latest_session"] is None
    assert result["total_duration"] == timedelta(0)
    assert result["average_duration"] == timedelta(0)
    assert result["total_attendance_events"] == 0
    assert result["total_activity_events"] == 0
