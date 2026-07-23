# tests/application/dto/test_dashboard_result.py

"""
DashboardResult DTO Tests

Purpose:
    Verify the immutable application-level dashboard result DTO.

Coverage:
    - Construction.
    - Field storage.
    - State properties.
    - Immutability.
    - Representation methods.

Rules:
    - Test DTO behaviour only.
    - Do not test DashboardService.
    - Do not test Domain analytics.
    - Do not test Session construction.

Author:
    Me

Created:
    July 2026
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

from src.application.dto.dashboard_result import DashboardResult
from src.domain.enums.attendance_type import AttendanceType

# ============================================================================
# Fixtures
# ============================================================================


def create_result() -> DashboardResult:
    """Return a representative dashboard result."""

    return DashboardResult(
        session_date=date(
            2026,
            7,
            23,
        ),
        attendance_count=5,
        attendance_rate=80.0,
        done_count=5,
        activity_count=12,
        attendance_events=5,
        participants=5,
        first_done=None,
        first_activity=datetime(
            2026,
            7,
            23,
            8,
            0,
        ),
        last_activity=datetime(
            2026,
            7,
            23,
            9,
            0,
        ),
        duration=timedelta(
            hours=1,
        ),
        attendance_types={
            AttendanceType.PRESENT: 5,
        },
        activity_types={},
    )


# ============================================================================
# Construction
# ============================================================================


class TestDashboardResultConstruction:
    """Test DashboardResult construction."""

    def test_result_can_be_constructed(self) -> None:
        """DashboardResult can be constructed."""

        result = create_result()

        assert isinstance(
            result,
            DashboardResult,
        )

    def test_fields_are_stored(self) -> None:
        """DashboardResult stores supplied values."""

        result = create_result()

        assert result.session_date == date(
            2026,
            7,
            23,
        )
        assert result.attendance_count == 5
        assert result.attendance_rate == 80.0
        assert result.done_count == 5
        assert result.activity_count == 12
        assert result.attendance_events == 5
        assert result.participants == 5


# ============================================================================
# State Properties
# ============================================================================


class TestDashboardResultState:
    """Test dashboard result state properties."""

    def test_has_attendance_returns_true_when_attendance_exists(self) -> None:
        """has_attendance returns True when attendance exists."""

        result = create_result()

        assert result.has_attendance is True

    def test_has_activities_returns_true_when_activities_exist(self) -> None:
        """has_activities returns True when activities exist."""

        result = create_result()

        assert result.has_activities is True

    def test_is_empty_returns_false_when_events_exist(self) -> None:
        """is_empty returns False when events exist."""

        result = create_result()

        assert result.is_empty is False

    def test_empty_result_has_correct_state(self) -> None:
        """An empty result reports no events."""

        result = DashboardResult(
            session_date=date(
                2026,
                7,
                23,
            ),
            attendance_count=0,
            attendance_rate=0.0,
            done_count=0,
            activity_count=0,
            attendance_events=0,
            participants=0,
            first_done=None,
            first_activity=None,
            last_activity=None,
            duration=None,
            attendance_types={},
            activity_types={},
        )

        assert result.has_attendance is False
        assert result.has_activities is False
        assert result.is_empty is True


# ============================================================================
# Immutability
# ============================================================================


class TestDashboardResultImmutability:
    """Test DashboardResult immutability."""

    def test_result_is_immutable(self) -> None:
        """DashboardResult fields cannot be reassigned."""

        result = create_result()

        try:
            result.attendance_count = 10  # type: ignore[misc]
        except AttributeError:
            pass
        else:
            raise AssertionError(
                "DashboardResult should be immutable.",
            )


# ============================================================================
# Representation
# ============================================================================


class TestDashboardResultRepresentation:
    """Test DashboardResult representations."""

    def test_repr_contains_class_name(self) -> None:
        """repr contains the class name."""

        result = create_result()

        assert "DashboardResult" in repr(result)

    def test_str_matches_repr(self) -> None:
        """str returns the official representation."""

        result = create_result()

        assert str(result) == repr(result)
