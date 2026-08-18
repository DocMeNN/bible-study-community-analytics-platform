# tests/domain/analytics/test_statistics.py

"""
Tests for Domain Statistics Analytics.
"""

from datetime import date, datetime

from src.domain.analytics.statistics import (
    average_attendance,
    full_attendance_sessions,
    highest_attendance,
    lowest_attendance,
    sessions_with_quorum,
    total_absent,
    total_activities,
    total_attendance_events,
    total_expected_attendees,
    total_present,
)
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.attendance_summary import AttendanceSummary
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Test Helpers
# ============================================================================


def build_message(
    *,
    sender: str,
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
        content="Participation",
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
            line_number=line_number,
        ),
    )


def build_summary(
    *,
    session_date: date,
    expected_attendees: int,
    attendees: tuple[str, ...],
) -> AttendanceSummary:
    """Build an attendance summary."""

    attendance_events = tuple(
        build_attendance_event(
            attendee=attendee,
            line_number=index,
        )
        for index, attendee in enumerate(
            attendees,
            start=1,
        )
    )

    session = Session(
        session_date=session_date,
        attendance_events=attendance_events,
    )

    return AttendanceSummary(
        session=session,
        expected_attendees=expected_attendees,
    )


# ============================================================================
# Average Attendance
# ============================================================================


def test_average_attendance_returns_average_percentage() -> None:
    """Average attendance should be calculated across summaries."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie", "David"),
        ),
    )

    assert average_attendance(summaries) == 30.0


def test_average_attendance_returns_zero_for_empty_input() -> None:
    """Average attendance should be zero for empty input."""

    assert average_attendance([]) == 0.0


def test_average_attendance_supports_generator_input() -> None:
    """Average attendance should support iterable generators."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie", "David"),
        ),
    )

    summary_generator = (summary for summary in summaries)

    assert average_attendance(summary_generator) == 30.0


# ============================================================================
# Highest and Lowest Attendance
# ============================================================================


def test_highest_attendance_returns_highest_percentage() -> None:
    """Highest attendance should return the best-performing session."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie", "David", "Eve"),
        ),
    )

    result = highest_attendance(summaries)

    assert result is summaries[1]


def test_highest_attendance_returns_none_for_empty_input() -> None:
    """Highest attendance should return None for empty input."""

    assert highest_attendance([]) is None


def test_lowest_attendance_returns_lowest_percentage() -> None:
    """Lowest attendance should return the weakest-performing session."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie", "David", "Eve"),
        ),
    )

    result = lowest_attendance(summaries)

    assert result is summaries[0]


def test_lowest_attendance_returns_none_for_empty_input() -> None:
    """Lowest attendance should return None for empty input."""

    assert lowest_attendance([]) is None


# ============================================================================
# Attendance Totals
# ============================================================================


def test_total_expected_attendees_sums_expected_population() -> None:
    """Expected attendees should be summed across summaries."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=15,
            attendees=("Alice", "Bob", "Charlie"),
        ),
    )

    assert total_expected_attendees(summaries) == 25


def test_total_expected_attendees_returns_zero_for_empty_input() -> None:
    """Empty input should produce zero expected attendees."""

    assert total_expected_attendees([]) == 0


def test_total_present_sums_present_attendees() -> None:
    """Present attendees should be summed across summaries."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie"),
        ),
    )

    assert total_present(summaries) == 5


def test_total_present_returns_zero_for_empty_input() -> None:
    """Empty input should produce zero present attendees."""

    assert total_present([]) == 0


def test_total_absent_sums_absent_attendees() -> None:
    """Absent attendees should be summed across summaries."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie"),
        ),
    )

    assert total_absent(summaries) == 15


def test_total_absent_returns_zero_for_empty_input() -> None:
    """Empty input should produce zero absent attendees."""

    assert total_absent([]) == 0


# ============================================================================
# Event Totals
# ============================================================================


def test_total_attendance_events_sums_attendance_events() -> None:
    """Attendance event counts should be summed across summaries."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie"),
        ),
    )

    assert total_attendance_events(summaries) == 5


def test_total_attendance_events_returns_zero_for_empty_input() -> None:
    """Empty input should produce zero attendance events."""

    assert total_attendance_events([]) == 0


def test_total_activities_sums_activity_events() -> None:
    """Activity event counts should be summed across summaries."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie"),
        ),
    )

    assert total_activities(summaries) == 0


def test_total_activities_returns_zero_for_empty_input() -> None:
    """Empty input should produce zero activities."""

    assert total_activities([]) == 0


# ============================================================================
# Session Classification
# ============================================================================


def test_sessions_with_quorum_returns_sessions_reaching_fifty_percent() -> None:
    """Quorum should include sessions with at least 50% participation."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob", "Charlie", "David", "Eve"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
    )

    result = sessions_with_quorum(summaries)

    assert result == (summaries[0],)


def test_sessions_with_quorum_returns_empty_when_none_qualify() -> None:
    """No-quorum input should return an empty tuple."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
    )

    assert sessions_with_quorum(summaries) == ()


def test_full_attendance_sessions_returns_fully_attended_sessions() -> None:
    """Full attendance should include sessions with all expected members."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=3,
            attendees=("Alice", "Bob", "Charlie"),
        ),
        build_summary(
            session_date=date(2026, 7, 21),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
    )

    result = full_attendance_sessions(summaries)

    assert result == (summaries[0],)


def test_full_attendance_sessions_returns_empty_when_none_are_full() -> None:
    """No fully attended sessions should return an empty tuple."""

    summaries = (
        build_summary(
            session_date=date(2026, 7, 20),
            expected_attendees=10,
            attendees=("Alice", "Bob"),
        ),
    )

    assert full_attendance_sessions(summaries) == ()
