# src/presentation/viewmodels/report_viewmodel.py

"""
Report ViewModel

Purpose
-------
Coordinates report presentation workflows by consuming the
Application Layer ReportService and adapting ReportResult
for Presentation Layer consumption.

Responsibilities
----------------
- Delegate report workflows to ReportService.
- Consume the typed ReportResult application contract.
- Expose presentation-ready report data.
- Adapt application results for report presentation components.

Architectural Rules
-------------------
- Presentation layer only.
- No business logic.
- No analytics calculations.
- No Streamlit.
- No PDF generation.
- No Excel generation.
- No file I/O.
- No direct Domain analytics.
- No infrastructure dependencies.
- No direct data parsing.

Architecture
------------
Reports Page
        |
        v
ReportViewModel
        |
        v
ReportService
        |
        v
ReportResult
        |
        v
Presentation Components

The ViewModel is an adapter between the Application Layer
contract and Presentation Layer consumption.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable
from datetime import date
from typing import Any

# ============================================================================
# Local Imports
# ============================================================================
from src.application.dto.report_result import ReportResult
from src.application.services.report_service import ReportService
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Report ViewModel
# ============================================================================


class ReportViewModel:
    """
    Presentation ViewModel for report workflows.

    Coordinates the ReportService and adapts the resulting
    ReportResult for Presentation Layer consumption.

    The ViewModel does not calculate report analytics.
    All calculations remain delegated to the Application
    and Domain layers.
    """

    def __init__(
        self,
        report_service: ReportService | None = None,
    ) -> None:
        """
        Initialize the ReportViewModel.

        Parameters
        ----------
        report_service:
            Optional ReportService dependency.

            When omitted, a default ReportService is created.
        """

        self._report_service = (
            report_service if report_service is not None else ReportService()
        )

    # =========================================================================
    # Session Construction
    # =========================================================================

    def build_session(
        self,
        *,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build a Session through the Application Layer.

        Session construction remains delegated to
        ReportService.
        """

        return self._report_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # =========================================================================
    # Report Result
    # =========================================================================

    def get_report(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> ReportResult:
        """
        Return the typed application report result.

        The ViewModel delegates report construction
        to the ReportService.
        """

        return self._report_service.report_data(
            session=session,
            expected_attendees=expected_attendees,
        )

    # =========================================================================
    # Presentation Adapter
    # =========================================================================

    def to_presentation_data(
        self,
        result: ReportResult,
    ) -> dict[str, Any]:
        """
        Adapt ReportResult for Presentation components.

        This method performs structural presentation adaptation only.

        It does not:
            - calculate report analytics;
            - apply business rules;
            - generate files;
            - modify the application result.
        """

        return result.to_dict()

    # =========================================================================
    # Presentation Workflow
    # =========================================================================

    def report_data(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return presentation-ready report data.

        The workflow is:

            Session
                |
                v
            ReportService
                |
                v
            ReportResult
                |
                v
            Presentation Mapping
        """

        result = self.get_report(
            session=session,
            expected_attendees=expected_attendees,
        )

        return self.to_presentation_data(
            result,
        )

    # =========================================================================
    # Individual Sections
    # =========================================================================

    def session_section(
        self,
        *,
        session: Session,
    ) -> dict[str, object]:
        """
        Return the session report section.
        """

        return self._report_service.session_section(
            session,
        )

    def dashboard_section(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return the dashboard report section.
        """

        return self._report_service.dashboard_section(
            session,
            expected_attendees,
        )

    def attendance_section(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return the attendance report section.
        """

        return self._report_service.attendance_section(
            session,
            expected_attendees,
        )

    def activity_section(
        self,
        *,
        session: Session,
    ) -> dict[str, object]:
        """
        Return the activity report section.
        """

        return self._report_service.activity_section(
            session,
        )

    # =========================================================================
    # State
    # =========================================================================

    def has_attendance(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when attendance exists.
        """

        return self._report_service.has_attendance(
            session,
        )

    def has_activities(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when activities exist.
        """

        return self._report_service.has_activities(
            session,
        )

    def is_empty(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when the Session contains no events.
        """

        return self._report_service.is_empty(
            session,
        )

    # =========================================================================
    # Service Access
    # =========================================================================

    @property
    def report_service(self) -> ReportService:
        """
        Return the underlying ReportService.
        """

        return self._report_service

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"report_service="
            f"{self.report_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "ReportViewModel",
]
