# tests/application/dto/test_report_result.py

"""
Report Result DTO Tests

Purpose:
    Verify the immutable ReportResult data transfer object.

Coverage:
    - Construction.
    - Field storage.
    - Section state.
    - Empty state.
    - Dictionary serialization.
    - Immutability.
    - Representation.

Rules:
    - Test DTO behaviour only.
    - Do not test business logic.
    - Do not test application services.

Author:
    Me

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from src.application.dto.report_result import ReportResult

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def session_data() -> dict[str, object]:
    """Return representative session data."""

    return {
        "session_date": "2026-07-23",
        "participants": 10,
    }


@pytest.fixture
def dashboard_data() -> dict[str, object]:
    """Return representative dashboard data."""

    return {
        "attendance_count": 10,
        "activity_count": 25,
    }


@pytest.fixture
def attendance_data() -> dict[str, object]:
    """Return representative attendance data."""

    return {
        "attendees": ("Me", "Member 2"),
        "attendance_count": 2,
    }


@pytest.fixture
def activity_data() -> dict[str, object]:
    """Return representative activity data."""

    return {
        "activity_count": 25,
        "activity_types": {},
    }


@pytest.fixture
def result(
    session_data: dict[str, object],
    dashboard_data: dict[str, object],
    attendance_data: dict[str, object],
    activity_data: dict[str, object],
) -> ReportResult:
    """Return a representative ReportResult."""

    return ReportResult(
        session=session_data,
        dashboard=dashboard_data,
        attendance=attendance_data,
        activity=activity_data,
    )


# ============================================================================
# Construction
# ============================================================================


class TestReportResultConstruction:
    """Test ReportResult construction."""

    def test_result_can_be_constructed(
        self,
        result: ReportResult,
    ) -> None:
        """ReportResult can be constructed."""

        assert isinstance(
            result,
            ReportResult,
        )

    def test_fields_are_stored(
        self,
        result: ReportResult,
        session_data: dict[str, object],
        dashboard_data: dict[str, object],
        attendance_data: dict[str, object],
        activity_data: dict[str, object],
    ) -> None:
        """All report sections are stored."""

        assert result.session == session_data
        assert result.dashboard == dashboard_data
        assert result.attendance == attendance_data
        assert result.activity == activity_data


# ============================================================================
# State
# ============================================================================


class TestReportResultState:
    """Test ReportResult state properties."""

    def test_has_session_returns_true_when_session_exists(
        self,
        result: ReportResult,
    ) -> None:
        """has_session returns True when session data exists."""

        assert result.has_session is True

    def test_has_dashboard_returns_true_when_dashboard_exists(
        self,
        result: ReportResult,
    ) -> None:
        """has_dashboard returns True when dashboard data exists."""

        assert result.has_dashboard is True

    def test_has_attendance_returns_true_when_attendance_exists(
        self,
        result: ReportResult,
    ) -> None:
        """has_attendance returns True when attendance data exists."""

        assert result.has_attendance is True

    def test_has_activity_returns_true_when_activity_exists(
        self,
        result: ReportResult,
    ) -> None:
        """has_activity returns True when activity data exists."""

        assert result.has_activity is True

    def test_empty_result_is_empty(
        self,
    ) -> None:
        """An empty result reports an empty state."""

        result = ReportResult(
            session={},
            dashboard={},
            attendance={},
            activity={},
        )

        assert result.is_empty is True

    def test_populated_result_is_not_empty(
        self,
        result: ReportResult,
    ) -> None:
        """A populated result reports a non-empty state."""

        assert result.is_empty is False


# ============================================================================
# Serialization
# ============================================================================


class TestReportResultSerialization:
    """Test ReportResult serialization."""

    def test_to_dict_returns_all_sections(
        self,
        result: ReportResult,
    ) -> None:
        """to_dict returns all report sections."""

        data = result.to_dict()

        assert data == {
            "session": result.session,
            "dashboard": result.dashboard,
            "attendance": result.attendance,
            "activity": result.activity,
        }


# ============================================================================
# Immutability
# ============================================================================


class TestReportResultImmutability:
    """Test ReportResult immutability."""

    def test_result_is_immutable(
        self,
        result: ReportResult,
    ) -> None:
        """ReportResult fields cannot be reassigned."""

        with pytest.raises(FrozenInstanceError):
            result.session = {}


# ============================================================================
# Representation
# ============================================================================


class TestReportResultRepresentation:
    """Test ReportResult representations."""

    def test_repr_contains_class_name(
        self,
        result: ReportResult,
    ) -> None:
        """repr contains the class name."""

        assert "ReportResult" in repr(result)

    def test_str_matches_repr(
        self,
        result: ReportResult,
    ) -> None:
        """str matches repr."""

        assert str(result) == repr(result)
