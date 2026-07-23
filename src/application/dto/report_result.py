# src/application/dto/report_result.py

"""
Report Result DTO

Purpose:
    Represents application-level report data prepared for
    presentation and report generation.

Architecture:
    Application Layer - Data Transfer Object

Responsibilities:
    - Carry complete report data between application and presentation layers.
    - Group session, dashboard, attendance and activity results.
    - Provide a stable application-facing result structure.
    - Remain immutable.

Rules:
    - No business logic.
    - No pandas.
    - No Streamlit.
    - No file I/O.
    - No report generation.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from dataclasses import dataclass
from typing import Any

# ============================================================================
# Report Result
# ============================================================================


@dataclass(frozen=True, slots=True)
class ReportResult:
    """
    Immutable report result.

    A ReportResult groups the complete set of report-ready
    application data into four logical sections:

        - session
        - dashboard
        - attendance
        - activity

    The DTO carries data only. It performs no calculations
    and contains no business rules.
    """

    session: dict[str, Any]
    dashboard: dict[str, Any]
    attendance: dict[str, Any]
    activity: dict[str, Any]

    # =========================================================================
    # State
    # =========================================================================

    @property
    def has_session(self) -> bool:
        """
        Return True if session data exists.
        """

        return bool(self.session)

    @property
    def has_dashboard(self) -> bool:
        """
        Return True if dashboard data exists.
        """

        return bool(self.dashboard)

    @property
    def has_attendance(self) -> bool:
        """
        Return True if attendance data exists.
        """

        return bool(self.attendance)

    @property
    def has_activity(self) -> bool:
        """
        Return True if activity data exists.
        """

        return bool(self.activity)

    @property
    def is_empty(self) -> bool:
        """
        Return True if all report sections are empty.
        """

        return not any(
            (
                self.session,
                self.dashboard,
                self.attendance,
                self.activity,
            )
        )

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict[str, dict[str, Any]]:
        """
        Return the complete report as a dictionary.
        """

        return {
            "session": self.session,
            "dashboard": self.dashboard,
            "attendance": self.attendance,
            "activity": self.activity,
        }

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"session={self.session!r}, "
            f"dashboard={self.dashboard!r}, "
            f"attendance={self.attendance!r}, "
            f"activity={self.activity!r})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()
