# src/application/dto/attendance_result.py

"""
Attendance Application Result DTO

Purpose:
    Represents attendance-related results returned by the
    Application Layer.

Architecture:
    Application Layer - Data Transfer Objects

Responsibilities:
    - Carry attendance results between Application and Presentation layers.
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
from typing import TYPE_CHECKING

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.enums.attendance_type import AttendanceType

if TYPE_CHECKING:
    from src.domain.models.attendance_event import AttendanceEvent
    from src.domain.models.done_event import DoneEvent


@dataclass(frozen=True, slots=True)
class AttendanceResult:
    """
    Immutable application-level attendance result.

    Represents attendance and Done acknowledgement information
    produced by application services.
    """

    attendees: tuple[str, ...]
    participants: int
    attendance_count: int
    attendance_rate: float
    attendance_types: dict[AttendanceType, int]
    attendance_events: tuple[AttendanceEvent, ...]
    done_events: tuple[DoneEvent, ...]
    done_count: int
    first_done: DoneEvent | None

    @property
    def has_attendance(self) -> bool:
        """
        Return True when attendance exists.
        """

        return self.attendance_count > 0

    @property
    def has_done_events(self) -> bool:
        """
        Return True when Done events exist.
        """

        return self.done_count > 0

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"participants={self.participants}, "
            f"attendance_count={self.attendance_count}, "
            f"attendance_rate={self.attendance_rate}, "
            f"done_count={self.done_count})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()
