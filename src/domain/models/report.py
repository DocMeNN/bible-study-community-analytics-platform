# src/domain/models/report.py

"""
Report Domain Model

Purpose:
    Represents the final business report generated from a meeting
    session.

Responsibilities:
    - Aggregate session information.
    - Aggregate attendance summary.
    - Provide report metadata.
    - Remain technology independent.

Notes:
    - Immutable.
    - Contains no UI, pandas or infrastructure dependencies.
    - Serves as the canonical report object for all exporters.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from src.domain.enums.report_type import ReportType

from .attendance_summary import AttendanceSummary


@dataclass(frozen=True, slots=True)
class Report:
    """
    Immutable domain report.
    """

    title: str
    report_type: ReportType
    summary: AttendanceSummary
    generated_at: datetime

    def __post_init__(self) -> None:
        """Validate report."""

        title = self.title.strip()

        if not title:
            raise ValueError("title cannot be empty.")

        if not isinstance(self.report_type, ReportType):
            raise TypeError("report_type must be a ReportType.")

        if not isinstance(self.summary, AttendanceSummary):
            raise TypeError("summary must be an AttendanceSummary.")

        if not isinstance(self.generated_at, datetime):
            raise TypeError("generated_at must be a datetime.")

        object.__setattr__(self, "title", title)

    # ------------------------------------------------------------------
    # Derived Properties
    # ------------------------------------------------------------------

    @property
    def session_date(self) -> date:
        """Return session date."""
        return self.summary.session_date

    @property
    def attendance_percentage(self) -> float:
        """Return attendance percentage."""
        return self.summary.attendance_percentage

    @property
    def present_count(self) -> int:
        """Return members present."""
        return self.summary.present_count

    @property
    def absent_count(self) -> int:
        """Return members absent."""
        return self.summary.absent_count

    @property
    def expected_attendees(self) -> int:
        """Return expected attendees."""
        return self.summary.expected_attendees

    @property
    def first_attendee(self) -> str | None:
        """Return first attendee."""
        return self.summary.first_attendee

    @property
    def duration(self):
        """Return session duration."""
        return self.summary.duration

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "title": self.title,
            "report_type": self.report_type.value,
            "generated_at": self.generated_at.isoformat(),
            "session_date": self.session_date.isoformat(),
            "present_count": self.present_count,
            "absent_count": self.absent_count,
            "expected_attendees": self.expected_attendees,
            "attendance_percentage": self.attendance_percentage,
            "first_attendee": self.first_attendee,
            "duration": str(self.duration),
        }

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Return readable representation."""

        return f"{self.title} ({self.attendance_percentage:.2f}% attendance)"
