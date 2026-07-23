# src/application/dto/dashboard_result.py

"""
Dashboard Application Result DTO

Purpose:
    Represents dashboard-ready results returned by the
    Application Layer.

Architecture:
    Application Layer - Data Transfer Objects

Responsibilities:
    - Carry dashboard metrics between Application and Presentation layers.
    - Provide a stable, typed application-level result structure.
    - Prevent raw dictionaries from becoming the public application contract.

Rules:
    - No business logic.
    - No pandas.
    - No Streamlit.
    - No infrastructure dependencies.
    - No AI dependencies.

Author:
    Me

Created:
    July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from dataclasses import dataclass
from datetime import date, datetime
from typing import TYPE_CHECKING

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.enums.activity_type import ActivityType
from src.domain.enums.attendance_type import AttendanceType

if TYPE_CHECKING:
    from src.domain.models.done_event import DoneEvent


@dataclass(frozen=True, slots=True)
class DashboardResult:
    """
    Immutable application-level dashboard result.

    Represents the aggregate metrics required by the
    Presentation Layer for dashboard display.
    """

    session_date: date
    attendance_count: int
    attendance_rate: float
    done_count: int
    activity_count: int
    attendance_events: int
    participants: int
    first_done: DoneEvent | None
    first_activity: datetime | None
    last_activity: datetime | None
    duration: object | None
    attendance_types: dict[AttendanceType, int]
    activity_types: dict[ActivityType, int]

    @property
    def has_attendance(self) -> bool:
        """
        Return True when attendance exists.
        """

        return self.attendance_count > 0

    @property
    def has_activities(self) -> bool:
        """
        Return True when activities exist.
        """

        return self.activity_count > 0

    @property
    def is_empty(self) -> bool:
        """
        Return True when the dashboard contains no events.
        """

        return (
            self.attendance_count == 0
            and self.activity_count == 0
            and self.done_count == 0
        )

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"session_date={self.session_date!r}, "
            f"attendance_count={self.attendance_count}, "
            f"activity_count={self.activity_count}, "
            f"done_count={self.done_count})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()
