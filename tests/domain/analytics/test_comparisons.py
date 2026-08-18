# tests/domain/analytics/test_comparisons.py

"""
Tests for Domain Comparison Analytics.
"""

from datetime import date, datetime

import pytest

from src.domain.analytics.comparisons import (
    attendance_declined,
    attendance_improved,
    attendance_unchanged,
    best_session,
    compare_attendance,
    compare_expected_attendance,
    compare_present_count,
    compare_sessions,
    worst_session,
)
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.attendance_summary import AttendanceSummary
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Fixtures
# ============================================================================


def build_summary(
    *,
    session_date: date,
    present_count: int,
    expected_attendees: int = 10,
) -> AttendanceSummary:
    """
    Build an AttendanceSummary with the requested
    number of unique participants.
    """

    attendance_events = tuple(
        AttendanceEvent(
            attendee=f"Member {index}",
            source_message=Message(
                timestamp=datetime(
                    session_date.year,
                    session_date.month,
                    session_date.day,
                    10,
                    index,
                ),
                sender=f"Member {index}",
                content="Participation",
                line_number=index,
            ),
        )
        for index in range(1, present_count + 1)
    )

    session = Session(
        session_date=session_date,
        attendance_events=attendance_events,
    )

    return AttendanceSummary(
        session=session,
        expected_attendees=expected_attendees,
    )


@pytest.fixture
def first_summary() -> AttendanceSummary:
    """Return the first attendance summary."""

    return build_summary(
        session_date=date(2026, 7, 21),
        present_count=5,
    )


@pytest.fixture
def second_summary() -> AttendanceSummary:
    """Return the second attendance summary."""

    return build_summary(
        session_date=date(2026, 7, 22),
        present_count=8,
    )


# ============================================================================
# Attendance Comparison
# ============================================================================


def test_compare_attendance_returns_percentage_point_difference(
    first_summary: AttendanceSummary,
    second_summary: AttendanceSummary,
) -> None:
    """Attendance comparison should return percentage-point difference."""

    assert (
        compare_attendance(
            first_summary,
            second_summary,
        )
        == 30.0
    )


def test_compare_attendance_returns_negative_difference_on_decline(
    first_summary: AttendanceSummary,
) -> None:
    """Attendance comparison should return negative difference on decline."""

    lower_summary = build_summary(
        session_date=date(2026, 7, 22),
        present_count=3,
    )

    assert (
        compare_attendance(
            first_summary,
            lower_summary,
        )
        == -20.0
    )


def test_compare_attendance_returns_zero_when_unchanged(
    first_summary: AttendanceSummary,
) -> None:
    """Attendance comparison should return zero when unchanged."""

    same_summary = build_summary(
        session_date=date(2026, 7, 22),
        present_count=5,
    )

    assert (
        compare_attendance(
            first_summary,
            same_summary,
        )
        == 0.0
    )


# ============================================================================
# Attendance Classification
# ============================================================================


def test_attendance_improved(
    first_summary: AttendanceSummary,
    second_summary: AttendanceSummary,
) -> None:
    """Improvement should be detected."""

    assert attendance_improved(
        first_summary,
        second_summary,
    )


def test_attendance_declined(
    first_summary: AttendanceSummary,
) -> None:
    """Decline should be detected."""

    lower_summary = build_summary(
        session_date=date(2026, 7, 22),
        present_count=3,
    )

    assert attendance_declined(
        first_summary,
        lower_summary,
    )


def test_attendance_unchanged(
    first_summary: AttendanceSummary,
) -> None:
    """Unchanged attendance should be detected."""

    same_summary = build_summary(
        session_date=date(2026, 7, 22),
        present_count=5,
    )

    assert attendance_unchanged(
        first_summary,
        same_summary,
    )


# ============================================================================
# Best and Worst Sessions
# ============================================================================


def test_best_session_returns_highest_participation(
    first_summary: AttendanceSummary,
    second_summary: AttendanceSummary,
) -> None:
    """Best session should have the highest participation."""

    result = best_session(
        (
            first_summary,
            second_summary,
        )
    )

    assert result is second_summary


def test_worst_session_returns_lowest_participation(
    first_summary: AttendanceSummary,
    second_summary: AttendanceSummary,
) -> None:
    """Worst session should have the lowest participation."""

    result = worst_session(
        (
            first_summary,
            second_summary,
        )
    )

    assert result is first_summary


def test_best_and_worst_session_return_none_for_empty_input() -> None:
    """Empty input should return no best or worst session."""

    assert best_session([]) is None
    assert worst_session([]) is None


# ============================================================================
# Expected Attendance Comparison
# ============================================================================


def test_compare_expected_attendance(
    first_summary: AttendanceSummary,
) -> None:
    """Expected attendee difference should be returned."""

    second_summary = build_summary(
        session_date=date(2026, 7, 22),
        present_count=5,
        expected_attendees=15,
    )

    assert (
        compare_expected_attendance(
            first_summary,
            second_summary,
        )
        == 5
    )


# ============================================================================
# Present Count Comparison
# ============================================================================


def test_compare_present_count(
    first_summary: AttendanceSummary,
    second_summary: AttendanceSummary,
) -> None:
    """Present participant difference should be returned."""

    assert (
        compare_present_count(
            first_summary,
            second_summary,
        )
        == 3
    )


# ============================================================================
# Composite Comparison
# ============================================================================


def test_compare_sessions_returns_complete_comparison(
    first_summary: AttendanceSummary,
    second_summary: AttendanceSummary,
) -> None:
    """Complete session comparison should contain expected values."""

    result = compare_sessions(
        first_summary,
        second_summary,
    )

    assert result == {
        "first_session_date": date(2026, 7, 21),
        "second_session_date": date(2026, 7, 22),
        "attendance_difference": 30.0,
        "attendance_improved": True,
        "attendance_declined": False,
        "attendance_unchanged": False,
        "expected_attendees_difference": 0,
        "present_count_difference": 3,
    }


def test_compare_sessions_detects_decline(
    first_summary: AttendanceSummary,
) -> None:
    """Complete comparison should detect declining participation."""

    lower_summary = build_summary(
        session_date=date(2026, 7, 22),
        present_count=3,
    )

    result = compare_sessions(
        first_summary,
        lower_summary,
    )

    assert result["attendance_difference"] == -20.0
    assert result["attendance_improved"] is False
    assert result["attendance_declined"] is True
    assert result["attendance_unchanged"] is False


def test_compare_sessions_detects_unchanged_attendance(
    first_summary: AttendanceSummary,
) -> None:
    """Complete comparison should detect unchanged participation."""

    same_summary = build_summary(
        session_date=date(2026, 7, 22),
        present_count=5,
    )

    result = compare_sessions(
        first_summary,
        same_summary,
    )

    assert result["attendance_difference"] == 0.0
    assert result["attendance_improved"] is False
    assert result["attendance_declined"] is False
    assert result["attendance_unchanged"] is True


# ============================================================================
# Iterable Support
# ============================================================================


def test_best_session_supports_generator_input(
    first_summary: AttendanceSummary,
    second_summary: AttendanceSummary,
) -> None:
    """Best session should support generator input."""

    summaries = (
        summary
        for summary in (
            first_summary,
            second_summary,
        )
    )

    assert best_session(summaries) is second_summary


def test_worst_session_supports_generator_input(
    first_summary: AttendanceSummary,
    second_summary: AttendanceSummary,
) -> None:
    """Worst session should support generator input."""

    summaries = (
        summary
        for summary in (
            first_summary,
            second_summary,
        )
    )

    assert worst_session(summaries) is first_summary
