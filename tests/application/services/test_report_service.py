# tests/application/services/test_report_service.py

"""
Report Service Application Tests

Purpose:
    Verify the application-level ReportService.

Coverage:
    - Service initialization.
    - Dependency injection.
    - Session construction delegation.
    - Complete ReportResult construction.
    - Individual report sections.
    - Convenience methods.
    - Service accessors.
    - String representations.

Rules:
    - Tests must use current Application and Domain contracts.
    - ReportService must return ReportResult for complete reports.
    - ReportService must delegate calculations to its services.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from datetime import date, datetime

# ============================================================================
# Third-Party Imports
# ============================================================================
# ============================================================================
# Local Imports
# ============================================================================
from src.application.dto.report_result import ReportResult
from src.application.services.activity_service import ActivityService
from src.application.services.attendance_service import AttendanceService
from src.application.services.dashboard_service import DashboardService
from src.application.services.report_service import ReportService
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Test Helpers
# ============================================================================


def message(
    *,
    sender: str = "Alice",
    content: str = "Message",
    minute: int = 0,
    line_number: int = 1,
) -> Message:
    """
    Create a valid Message for testing.
    """

    return Message(
        timestamp=datetime(
            2026,
            7,
            23,
            8,
            minute,
        ),
        sender=sender,
        content=content,
        line_number=line_number,
    )


def empty_session() -> Session:
    """
    Create an empty Session for testing.
    """

    return Session(
        session_date=date(
            2026,
            7,
            23,
        ),
    )


def populated_session() -> Session:
    """
    Build a Session containing a representative message.
    """

    return Session(
        session_date=date(
            2026,
            7,
            23,
        ),
        messages=(
            message(
                sender="Alice",
                content="Study message",
            ),
        ),
    )


# ============================================================================
# Test Doubles
# ============================================================================


class RecordingAttendanceService:
    """
    Test double for AttendanceService delegation.
    """

    def __init__(self) -> None:
        self.build_session_calls: list[dict[str, object]] = []
        self.has_attendance_calls: list[Session] = []

    def build_session(
        self,
        *,
        session_date: date,
        messages: object,
    ) -> Session:
        """
        Record session construction.
        """

        self.build_session_calls.append(
            {
                "session_date": session_date,
                "messages": messages,
            }
        )

        return empty_session()

    def has_attendance(
        self,
        session: Session,
    ) -> bool:
        """
        Record attendance lookup.
        """

        self.has_attendance_calls.append(
            session,
        )

        return True


class RecordingActivityService:
    """
    Test double for ActivityService delegation.
    """

    def __init__(self) -> None:
        self.has_activities_calls: list[Session] = []

    def has_activities(
        self,
        session: Session,
    ) -> bool:
        """
        Record activity lookup.
        """

        self.has_activities_calls.append(
            session,
        )

        return True


class RecordingDashboardService:
    """
    Test double for DashboardService delegation.
    """

    def __init__(self) -> None:
        self.session_summary_calls: list[Session] = []
        self.dashboard_summary_calls: list[tuple[Session, int]] = []
        self.attendance_summary_calls: list[tuple[Session, int]] = []
        self.activity_summary_calls: list[Session] = []

    def session_summary(
        self,
        session: Session,
    ) -> dict[str, object]:
        """
        Record session summary request.
        """

        self.session_summary_calls.append(
            session,
        )

        return {
            "section": "session",
        }

    def dashboard_summary(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Record dashboard summary request.
        """

        self.dashboard_summary_calls.append(
            (
                session,
                expected_attendees,
            )
        )

        return {
            "section": "dashboard",
        }

    def attendance_summary(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Record attendance summary request.
        """

        self.attendance_summary_calls.append(
            (
                session,
                expected_attendees,
            )
        )

        return {
            "section": "attendance",
        }

    def activity_summary(
        self,
        session: Session,
    ) -> dict[str, object]:
        """
        Record activity summary request.
        """

        self.activity_summary_calls.append(
            session,
        )

        return {
            "section": "activity",
        }


# ============================================================================
# Initialization
# ============================================================================


class TestReportServiceInitialization:
    """
    Test ReportService initialization.
    """

    def test_default_services_are_created(self) -> None:
        """
        Default dependencies are created when none are supplied.
        """

        service = ReportService()

        assert isinstance(
            service.attendance_service,
            AttendanceService,
        )

        assert isinstance(
            service.activity_service,
            ActivityService,
        )

        assert isinstance(
            service.dashboard_service,
            DashboardService,
        )

    def test_supplied_attendance_service_is_preserved(self) -> None:
        """
        Supplied AttendanceService is preserved.
        """

        attendance_service = RecordingAttendanceService()

        service = ReportService(
            attendance_service=attendance_service,
        )

        assert service.attendance_service is attendance_service

    def test_supplied_activity_service_is_preserved(self) -> None:
        """
        Supplied ActivityService is preserved.
        """

        activity_service = RecordingActivityService()

        service = ReportService(
            activity_service=activity_service,
        )

        assert service.activity_service is activity_service

    def test_supplied_dashboard_service_is_preserved(self) -> None:
        """
        Supplied DashboardService is preserved.
        """

        dashboard_service = RecordingDashboardService()

        service = ReportService(
            dashboard_service=dashboard_service,
        )

        assert service.dashboard_service is dashboard_service


# ============================================================================
# Session Construction
# ============================================================================


class TestSessionConstruction:
    """
    Test session construction delegation.
    """

    def test_build_session_delegates_to_attendance_service(self) -> None:
        """
        Session construction delegates to AttendanceService.
        """

        attendance_service = RecordingAttendanceService()

        service = ReportService(
            attendance_service=attendance_service,
        )

        session_date = date(
            2026,
            7,
            23,
        )

        messages = (
            message(
                line_number=1,
            ),
        )

        result = service.build_session(
            session_date=session_date,
            messages=messages,
        )

        assert isinstance(
            result,
            Session,
        )

        assert len(
            attendance_service.build_session_calls,
        ) == 1

        assert attendance_service.build_session_calls[0][
            "session_date"
        ] == session_date

        assert attendance_service.build_session_calls[0][
            "messages"
        ] is messages


# ============================================================================
# Complete Report
# ============================================================================


class TestReportData:
    """
    Test complete ReportResult construction.
    """

    def test_report_data_returns_report_result(self) -> None:
        """
        Complete report data is returned as ReportResult.
        """

        dashboard_service = RecordingDashboardService()

        service = ReportService(
            dashboard_service=dashboard_service,
        )

        session = empty_session()

        result = service.report_data(
            session,
            expected_attendees=10,
        )

        assert isinstance(
            result,
            ReportResult,
        )

    def test_report_data_contains_all_report_sections(self) -> None:
        """
        Complete report data contains all four sections.
        """

        dashboard_service = RecordingDashboardService()

        service = ReportService(
            dashboard_service=dashboard_service,
        )

        result = service.report_data(
            empty_session(),
            expected_attendees=10,
        )

        assert result.session == {
            "section": "session",
        }

        assert result.dashboard == {
            "section": "dashboard",
        }

        assert result.attendance == {
            "section": "attendance",
        }

        assert result.activity == {
            "section": "activity",
        }

    def test_report_data_delegates_to_all_dashboard_sections(self) -> None:
        """
        Complete report construction requests all dashboard sections.
        """

        dashboard_service = RecordingDashboardService()

        service = ReportService(
            dashboard_service=dashboard_service,
        )

        session = empty_session()

        service.report_data(
            session,
            expected_attendees=10,
        )

        assert dashboard_service.session_summary_calls == [
            session,
        ]

        assert dashboard_service.dashboard_summary_calls == [
            (
                session,
                10,
            ),
        ]

        assert dashboard_service.attendance_summary_calls == [
            (
                session,
                10,
            ),
        ]

        assert dashboard_service.activity_summary_calls == [
            session,
        ]


# ============================================================================
# Individual Sections
# ============================================================================


class TestReportSections:
    """
    Test individual report section methods.
    """

    def test_session_section_returns_session_summary(self) -> None:
        """
        Session section delegates to DashboardService.
        """

        dashboard_service = RecordingDashboardService()

        service = ReportService(
            dashboard_service=dashboard_service,
        )

        session = empty_session()

        result = service.session_section(
            session,
        )

        assert result == {
            "section": "session",
        }

        assert dashboard_service.session_summary_calls == [
            session,
        ]

    def test_dashboard_section_returns_dashboard_summary(self) -> None:
        """
        Dashboard section delegates to DashboardService.
        """

        dashboard_service = RecordingDashboardService()

        service = ReportService(
            dashboard_service=dashboard_service,
        )

        session = empty_session()

        result = service.dashboard_section(
            session,
            expected_attendees=20,
        )

        assert result == {
            "section": "dashboard",
        }

        assert dashboard_service.dashboard_summary_calls == [
            (
                session,
                20,
            ),
        ]

    def test_attendance_section_returns_attendance_summary(self) -> None:
        """
        Attendance section delegates to DashboardService.
        """

        dashboard_service = RecordingDashboardService()

        service = ReportService(
            dashboard_service=dashboard_service,
        )

        session = empty_session()

        result = service.attendance_section(
            session,
            expected_attendees=15,
        )

        assert result == {
            "section": "attendance",
        }

        assert dashboard_service.attendance_summary_calls == [
            (
                session,
                15,
            ),
        ]

    def test_activity_section_returns_activity_summary(self) -> None:
        """
        Activity section delegates to DashboardService.
        """

        dashboard_service = RecordingDashboardService()

        service = ReportService(
            dashboard_service=dashboard_service,
        )

        session = empty_session()

        result = service.activity_section(
            session,
        )

        assert result == {
            "section": "activity",
        }

        assert dashboard_service.activity_summary_calls == [
            session,
        ]


# ============================================================================
# Convenience Methods
# ============================================================================


class TestConvenienceMethods:
    """
    Test convenience methods.
    """

    def test_has_attendance_delegates_to_attendance_service(self) -> None:
        """
        Attendance existence delegates to AttendanceService.
        """

        attendance_service = RecordingAttendanceService()

        service = ReportService(
            attendance_service=attendance_service,
        )

        session = empty_session()

        assert service.has_attendance(
            session,
        ) is True

        assert attendance_service.has_attendance_calls == [
            session,
        ]

    def test_has_activities_delegates_to_activity_service(self) -> None:
        """
        Activity existence delegates to ActivityService.
        """

        activity_service = RecordingActivityService()

        service = ReportService(
            activity_service=activity_service,
        )

        session = empty_session()

        assert service.has_activities(
            session,
        ) is True

        assert activity_service.has_activities_calls == [
            session,
        ]

    def test_is_empty_returns_session_state(self) -> None:
        """
        is_empty returns the Session aggregate state.
        """

        service = ReportService()

        session = empty_session()

        assert service.is_empty(
            session,
        ) is True


# ============================================================================
# Representations
# ============================================================================


class TestReportServiceRepresentations:
    """
    Test service string representations.
    """

    def test_repr_contains_service_name(self) -> None:
        """
        repr identifies the ReportService.
        """

        service = ReportService()

        result = repr(
            service,
        )

        assert "ReportService" in result

    def test_repr_contains_dependency_names(self) -> None:
        """
        repr identifies the coordinated services.
        """

        service = ReportService()

        result = repr(
            service,
        )

        assert "AttendanceService" in result
        assert "ActivityService" in result
        assert "DashboardService" in result

    def test_str_matches_repr(self) -> None:
        """
        str returns the official representation.
        """

        service = ReportService()

        assert str(
            service,
        ) == repr(
            service,
        )
