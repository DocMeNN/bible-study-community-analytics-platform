# tests/application/services/test_dashboard_service.py

"""
Dashboard Service Tests

Tests the application-level DashboardService orchestration.
"""

from __future__ import annotations

from datetime import date, datetime

import pytest

from src.application.services.activity_service import ActivityService
from src.application.services.attendance_service import AttendanceService
from src.application.services.dashboard_service import DashboardService
from src.domain.enums.activity_type import ActivityType
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def session_date() -> date:
    """Return a test session date."""
    return date(2026, 7, 23)


@pytest.fixture
def messages() -> list[Message]:
    """Return representative study messages."""

    return [
        Message(
            timestamp=datetime(2026, 7, 23, 8, 0),
            sender="System",
            content="SCRIPTURE READING",
            line_number=1,
        ),
        Message(
            timestamp=datetime(2026, 7, 23, 8, 1),
            sender="Alice",
            content="Insight from today's reading",
            line_number=2,
        ),
        Message(
            timestamp=datetime(2026, 7, 23, 8, 2),
            sender="Bob",
            content="Done",
            line_number=3,
        ),
        Message(
            timestamp=datetime(2026, 7, 23, 8, 3),
            sender="Alice",
            content="Discussion about the passage",
            line_number=4,
        ),
    ]


@pytest.fixture
def service() -> DashboardService:
    """Return a DashboardService instance."""
    return DashboardService()


@pytest.fixture
def session(
    service: DashboardService,
    session_date: date,
    messages: list[Message],
) -> Session:
    """Build and return a test session."""

    return service.build_session(
        session_date=session_date,
        messages=messages,
    )


# ============================================================================
# Initialization
# ============================================================================


class TestDashboardServiceInitialization:
    """Test DashboardService initialization."""

    def test_creates_default_services(
        self,
        service: DashboardService,
    ) -> None:
        """Default application services are created."""

        assert isinstance(
            service.attendance_service,
            AttendanceService,
        )

        assert isinstance(
            service.activity_service,
            ActivityService,
        )

    def test_accepts_injected_services(self) -> None:
        """Custom application services are preserved."""

        attendance_service = AttendanceService()
        activity_service = ActivityService()

        service = DashboardService(
            attendance_service=attendance_service,
            activity_service=activity_service,
        )

        assert service.attendance_service is attendance_service
        assert service.activity_service is activity_service


# ============================================================================
# Session Construction
# ============================================================================


class TestSessionConstruction:
    """Test Session construction."""

    def test_build_session(
        self,
        service: DashboardService,
        session_date: date,
        messages: list[Message],
    ) -> None:
        """DashboardService builds a Session aggregate."""

        result = service.build_session(
            session_date=session_date,
            messages=messages,
        )

        assert isinstance(result, Session)
        assert result.session_date == session_date

    def test_build_session_delegates_to_attendance_service(
        self,
        service: DashboardService,
        session_date: date,
        messages: list[Message],
    ) -> None:
        """Session construction is delegated to AttendanceService."""

        result = service.build_session(
            session_date=session_date,
            messages=messages,
        )

        expected = service.attendance_service.build_session(
            session_date=session_date,
            messages=messages,
        )

        assert result == expected


# ============================================================================
# Dashboard Summary
# ============================================================================


class TestDashboardSummary:
    """Test dashboard summary generation."""

    def test_returns_expected_keys(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Dashboard summary contains expected metrics."""

        result = service.dashboard_summary(
            session=session,
            expected_attendees=10,
        )

        expected_keys = {
            "session_date",
            "attendance_count",
            "attendance_rate",
            "done_count",
            "activity_count",
            "attendance_events",
            "participants",
            "first_done",
            "first_activity",
            "last_activity",
            "duration",
        }

        assert set(result) == expected_keys

    def test_returns_session_date(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Summary contains the session date."""

        result = service.dashboard_summary(
            session=session,
            expected_attendees=10,
        )

        assert result["session_date"] == session.session_date

    def test_returns_participant_count(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Summary contains the unique participant count."""

        result = service.dashboard_summary(
            session=session,
            expected_attendees=10,
        )

        assert result["participants"] == session.attendee_count

    def test_returns_attendance_rate(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Summary contains the calculated attendance rate."""

        result = service.dashboard_summary(
            session=session,
            expected_attendees=10,
        )

        assert result["attendance_rate"] == 20.0

    def test_returns_done_count(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Summary contains the Done event count."""

        result = service.dashboard_summary(
            session=session,
            expected_attendees=10,
        )

        assert result["done_count"] == session.done_count

    def test_returns_activity_count(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Summary contains the activity count."""

        result = service.dashboard_summary(
            session=session,
            expected_attendees=10,
        )

        assert result["activity_count"] == session.activity_count


# ============================================================================
# Attendance Summary
# ============================================================================


class TestAttendanceSummary:
    """Test attendance summary generation."""

    def test_returns_expected_keys(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Attendance summary contains expected metrics."""

        result = service.attendance_summary(
            session=session,
            expected_attendees=10,
        )

        expected_keys = {
            "attendees",
            "participants",
            "attendance_count",
            "attendance_rate",
            "attendance_types",
        }

        assert set(result) == expected_keys

    def test_returns_attendees(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Attendance summary returns observed attendees."""

        result = service.attendance_summary(
            session=session,
            expected_attendees=10,
        )

        assert result["attendees"] == session.unique_attendees

    def test_returns_attendance_count(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Attendance summary returns unique attendance count."""

        result = service.attendance_summary(
            session=session,
            expected_attendees=10,
        )

        assert result["attendance_count"] == session.attendee_count

    def test_returns_attendance_rate(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Attendance summary returns attendance rate."""

        result = service.attendance_summary(
            session=session,
            expected_attendees=10,
        )

        assert result["attendance_rate"] == 20.0


# ============================================================================
# Activity Summary
# ============================================================================


class TestActivitySummary:
    """Test activity summary generation."""

    def test_returns_expected_keys(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Activity summary contains expected metrics."""

        result = service.activity_summary(
            session,
        )

        expected_keys = {
            "activity_count",
            "activity_types",
            "first_activity",
            "last_activity",
        }

        assert set(result) == expected_keys

    def test_returns_activity_count(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Activity summary returns activity count."""

        result = service.activity_summary(
            session,
        )

        assert result["activity_count"] == session.activity_count

    def test_returns_activity_types(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Activity summary returns activity type counts."""

        result = service.activity_summary(
            session,
        )

        activity_types = result["activity_types"]

        assert activity_types[ActivityType.INSIGHT] == 1
        assert activity_types[ActivityType.DISCUSSION] == 1


# ============================================================================
# Session Summary
# ============================================================================


class TestSessionSummary:
    """Test session summary generation."""

    def test_returns_expected_keys(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Session summary contains expected metrics."""

        result = service.session_summary(
            session,
        )

        expected_keys = {
            "session_date",
            "start_time",
            "end_time",
            "duration",
            "participants",
            "attendance_events",
            "done_events",
            "activity_events",
            "total_events",
        }

        assert set(result) == expected_keys

    def test_returns_session_metrics(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """Session summary returns aggregate metrics."""

        result = service.session_summary(
            session,
        )

        assert result["session_date"] == session.session_date
        assert result["participants"] == session.attendee_count
        assert result["attendance_events"] == session.attendance_count
        assert result["done_events"] == session.done_count
        assert result["activity_events"] == session.activity_count
        assert result["total_events"] == session.total_events


# ============================================================================
# Convenience Methods
# ============================================================================


class TestConvenienceMethods:
    """Test DashboardService convenience methods."""

    def test_has_attendance_returns_true(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """has_attendance returns True when attendance exists."""

        assert service.has_attendance(session) is True

    def test_has_activities_returns_true(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """has_activities returns True when activities exist."""

        assert service.has_activities(session) is True

    def test_is_empty_returns_false(
        self,
        service: DashboardService,
        session: Session,
    ) -> None:
        """is_empty returns False for a populated session."""

        assert service.is_empty(session) is False

    def test_empty_session_reports_no_events(
        self,
        service: DashboardService,
        session_date: date,
    ) -> None:
        """Empty sessions report no events."""

        empty_session = Session(
            session_date=session_date,
        )

        assert service.has_attendance(empty_session) is False
        assert service.has_activities(empty_session) is False
        assert service.is_empty(empty_session) is True


# ============================================================================
# Representations
# ============================================================================


class TestRepresentations:
    """Test DashboardService representations."""

    def test_repr_contains_service_name(
        self,
        service: DashboardService,
    ) -> None:
        """repr contains the class name."""

        result = repr(service)

        assert "DashboardService" in result

    def test_str_matches_repr(
        self,
        service: DashboardService,
    ) -> None:
        """str returns the official representation."""

        assert str(service) == repr(service)
