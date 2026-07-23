# tests/application/dto/test_attendance_result.py

"""
AttendanceResult DTO Tests

Purpose:
    Verify the immutable application-level attendance result DTO.

Coverage:
    - Construction.
    - Field storage.
    - Immutability.
    - Attendance state.
    - Done event state.
    - Representation methods.

Rules:
    - Test DTO behaviour only.
    - Do not test AttendanceService.
    - Do not test Domain analytics.
    - Do not test Session construction.

Author:
    Me

Created:
    July 2026
"""

from __future__ import annotations

from datetime import datetime

import pytest

from src.application.dto.attendance_result import AttendanceResult
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.message import Message

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def attendance_message() -> Message:
    """Return a representative attendance source message."""

    return Message(
        sender="Me",
        content="Done",
        timestamp=datetime(
            2026,
            7,
            23,
            8,
            0,
        ),
        line_number=1,
    )


@pytest.fixture
def done_message() -> Message:
    """Return a representative Done source message."""

    return Message(
        sender="Me",
        content="Done",
        timestamp=datetime(
            2026,
            7,
            23,
            8,
            5,
        ),
        line_number=2,
    )


@pytest.fixture
def attendance_event(
    attendance_message: Message,
) -> AttendanceEvent:
    """Return a representative attendance event."""

    return AttendanceEvent(
        attendee="Me",
        source_message=attendance_message,
    )


@pytest.fixture
def done_event(
    done_message: Message,
) -> DoneEvent:
    """Return a representative Done event."""

    return DoneEvent(
        attendee="Me",
        source_message=done_message,
    )


@pytest.fixture
def result(
    attendance_event: AttendanceEvent,
    done_event: DoneEvent,
) -> AttendanceResult:
    """Return a representative attendance result."""

    return AttendanceResult(
        attendees=("Me", "John"),
        participants=2,
        attendance_count=2,
        attendance_rate=80.0,
        attendance_types={
            AttendanceType.PRESENT: 2,
        },
        attendance_events=(attendance_event,),
        done_events=(done_event,),
        done_count=1,
        first_done=done_event,
    )


# ============================================================================
# Construction
# ============================================================================


class TestAttendanceResultConstruction:
    """Test AttendanceResult construction."""

    def test_result_can_be_constructed(
        self,
        result: AttendanceResult,
    ) -> None:
        """AttendanceResult can be constructed."""

        assert isinstance(
            result,
            AttendanceResult,
        )

    def test_fields_are_stored(
        self,
        result: AttendanceResult,
    ) -> None:
        """AttendanceResult stores supplied values."""

        assert result.attendees == ("Me", "John")
        assert result.participants == 2
        assert result.attendance_count == 2
        assert result.attendance_rate == 80.0
        assert result.done_count == 1


# ============================================================================
# State Properties
# ============================================================================


class TestAttendanceResultState:
    """Test attendance result state properties."""

    def test_has_attendance_returns_true_when_attendance_exists(
        self,
        result: AttendanceResult,
    ) -> None:
        """has_attendance returns True when attendance exists."""

        assert result.has_attendance is True

    def test_has_done_events_returns_true_when_done_events_exist(
        self,
        result: AttendanceResult,
    ) -> None:
        """has_done_events returns True when Done events exist."""

        assert result.has_done_events is True

    def test_has_attendance_returns_false_when_empty(self) -> None:
        """has_attendance returns False without attendance."""

        result = AttendanceResult(
            attendees=(),
            participants=0,
            attendance_count=0,
            attendance_rate=0.0,
            attendance_types={},
            attendance_events=(),
            done_events=(),
            done_count=0,
            first_done=None,
        )

        assert result.has_attendance is False

    def test_has_done_events_returns_false_when_empty(self) -> None:
        """has_done_events returns False without Done events."""

        result = AttendanceResult(
            attendees=(),
            participants=0,
            attendance_count=0,
            attendance_rate=0.0,
            attendance_types={},
            attendance_events=(),
            done_events=(),
            done_count=0,
            first_done=None,
        )

        assert result.has_done_events is False


# ============================================================================
# Immutability
# ============================================================================


class TestAttendanceResultImmutability:
    """Test AttendanceResult immutability."""

    def test_result_is_immutable(
        self,
        result: AttendanceResult,
    ) -> None:
        """AttendanceResult fields cannot be reassigned."""

        with pytest.raises(
            AttributeError,
        ):
            result.participants = 10  # type: ignore[misc]


# ============================================================================
# Representation
# ============================================================================


class TestAttendanceResultRepresentation:
    """Test AttendanceResult representations."""

    def test_repr_contains_class_name(
        self,
        result: AttendanceResult,
    ) -> None:
        """repr contains the class name."""

        assert "AttendanceResult" in repr(result)

    def test_str_matches_repr(
        self,
        result: AttendanceResult,
    ) -> None:
        """str returns the official representation."""

        assert str(result) == repr(result)
