# tests/application/services/test_multi_session_analytics_service.py

"""
Multi-Session Analytics Service Tests

Purpose
-------
Verify application-level analytics coordination across multiple
Daily Session aggregates.

Coverage
--------
- Empty session collections.
- Single-session analytics.
- Multiple-session analytics.
- Chronological date boundaries.
- Unique participant aggregation.
- Case-insensitive participant deduplication.
- Done event aggregation.
- Activity event aggregation.
- Iterable input support.
- Session ordering independence.

Architectural Rules
-------------------
- Daily Session remains the atomic Domain aggregate.
- The service coordinates analytics across selected sessions.
- The service does not perform Presentation-layer grouping.
- The service does not own Streamlit state.
- The service does not replace the Session domain model.

Author
------
OYBS Attendance Dashboard

Created
-------
July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================

from datetime import date, datetime

# ============================================================================
# Local Imports
# ============================================================================

from src.application.dto.multi_session_analytics_result import (
    MultiSessionAnalyticsResult,
)
from src.application.services.multi_session_analytics_service import (
    MultiSessionAnalyticsService,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
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


def attendance_event(
    *,
    attendee: str = "Alice",
    minute: int = 0,
    line_number: int = 1,
) -> AttendanceEvent:
    """
    Create a valid AttendanceEvent for testing.
    """

    return AttendanceEvent(
        attendee=attendee,
        source_message=message(
            sender=attendee,
            content="Participation",
            minute=minute,
            line_number=line_number,
        ),
    )


def done_event(
    *,
    attendee: str = "Alice",
    minute: int = 0,
    line_number: int = 1,
) -> DoneEvent:
    """
    Create a valid DoneEvent for testing.
    """

    return DoneEvent(
        attendee=attendee,
        source_message=message(
            sender=attendee,
            content="Done",
            minute=minute,
            line_number=line_number,
        ),
    )


def activity_event(
    *,
    activity_type: ActivityType = ActivityType.INSIGHT,
    minute: int = 0,
    line_number: int = 1,
) -> ActivityEvent:
    """
    Create a valid ActivityEvent for testing.
    """

    return ActivityEvent(
        activity_type=activity_type,
        source_message=message(
            content="Activity",
            minute=minute,
            line_number=line_number,
        ),
    )


def session(
    *,
    session_date: date,
    attendance_events: tuple[AttendanceEvent, ...] = (),
    done_events: tuple[DoneEvent, ...] = (),
    activity_events: tuple[ActivityEvent, ...] = (),
) -> Session:
    """
    Create a Session with the requested domain events.
    """

    return Session(
        session_date=session_date,
        attendance_events=attendance_events,
        done_events=done_events,
        activity_events=activity_events,
    )


# ============================================================================
# Service Construction
# ============================================================================


class TestMultiSessionAnalyticsServiceConstruction:
    """
    Test MultiSessionAnalyticsService construction.
    """

    def test_service_can_be_constructed(self) -> None:
        """
        The service can be instantiated.
        """

        service = MultiSessionAnalyticsService()

        assert isinstance(
            service,
            MultiSessionAnalyticsService,
        )


# ============================================================================
# Empty Input
# ============================================================================


class TestEmptyInput:
    """
    Test analytics for empty input.
    """

    def test_empty_sessions_return_empty_result(self) -> None:
        """
        Empty input produces zero-valued analytics.
        """

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (),
        )

        assert isinstance(
            result,
            MultiSessionAnalyticsResult,
        )

        assert result.session_count == 0
        assert result.start_date is None
        assert result.end_date is None
        assert result.total_participants == 0
        assert result.total_done_events == 0
        assert result.total_activity_events == 0


# ============================================================================
# Single Session Analytics
# ============================================================================


class TestSingleSessionAnalytics:
    """
    Test analytics across one Daily Session.
    """

    def test_single_session_count_is_one(self) -> None:
        """
        One Daily Session produces a session count of one.
        """

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                session(
                    session_date=date(
                        2026,
                        7,
                        23,
                    ),
                ),
            ),
        )

        assert result.session_count == 1

    def test_single_session_date_boundaries_are_identical(self) -> None:
        """
        A single session has identical start and end dates.
        """

        session_date = date(
            2026,
            7,
            23,
        )

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                session(
                    session_date=session_date,
                ),
            ),
        )

        assert result.start_date == session_date
        assert result.end_date == session_date


# ============================================================================
# Multiple Session Analytics
# ============================================================================


class TestMultipleSessionAnalytics:
    """
    Test analytics across multiple Daily Sessions.
    """

    def test_multiple_sessions_are_counted(self) -> None:
        """
        The result counts all selected sessions.
        """

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                session(
                    session_date=date(
                        2026,
                        7,
                        23,
                    ),
                ),
                session(
                    session_date=date(
                        2026,
                        7,
                        24,
                    ),
                ),
                session(
                    session_date=date(
                        2026,
                        7,
                        25,
                    ),
                ),
            ),
        )

        assert result.session_count == 3

    def test_date_boundaries_cover_earliest_and_latest_sessions(self) -> None:
        """
        Date boundaries represent the earliest and latest session dates.
        """

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                session(
                    session_date=date(
                        2026,
                        7,
                        24,
                    ),
                ),
                session(
                    session_date=date(
                        2026,
                        7,
                        23,
                    ),
                ),
                session(
                    session_date=date(
                        2026,
                        7,
                        25,
                    ),
                ),
            ),
        )

        assert result.start_date == date(
            2026,
            7,
            23,
        )

        assert result.end_date == date(
            2026,
            7,
            25,
        )


# ============================================================================
# Participant Aggregation
# ============================================================================


class TestParticipantAggregation:
    """
    Test unique participant aggregation across sessions.
    """

    def test_participants_are_aggregated_across_sessions(self) -> None:
        """
        Participants from all sessions are combined.
        """

        first_session = session(
            session_date=date(
                2026,
                7,
                23,
            ),
            attendance_events=(
                attendance_event(
                    attendee="Alice",
                ),
                attendance_event(
                    attendee="Bob",
                    minute=1,
                    line_number=2,
                ),
            ),
        )

        second_session = session(
            session_date=date(
                2026,
                7,
                24,
            ),
            attendance_events=(
                attendance_event(
                    attendee="Carol",
                ),
            ),
        )

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                first_session,
                second_session,
            ),
        )

        assert result.total_participants == 3

    def test_duplicate_participants_are_counted_once(self) -> None:
        """
        A participant appearing in multiple sessions is counted once.
        """

        first_session = session(
            session_date=date(
                2026,
                7,
                23,
            ),
            attendance_events=(
                attendance_event(
                    attendee="Alice",
                ),
            ),
        )

        second_session = session(
            session_date=date(
                2026,
                7,
                24,
            ),
            attendance_events=(
                attendance_event(
                    attendee="Alice",
                ),
            ),
        )

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                first_session,
                second_session,
            ),
        )

        assert result.total_participants == 1

    def test_participant_deduplication_is_case_insensitive(self) -> None:
        """
        Participant names differing only by case are counted once.
        """

        first_session = session(
            session_date=date(
                2026,
                7,
                23,
            ),
            attendance_events=(
                attendance_event(
                    attendee="Alice",
                ),
            ),
        )

        second_session = session(
            session_date=date(
                2026,
                7,
                24,
            ),
            attendance_events=(
                attendance_event(
                    attendee="alice",
                ),
            ),
        )

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                first_session,
                second_session,
            ),
        )

        assert result.total_participants == 1


# ============================================================================
# Done Event Aggregation
# ============================================================================


class TestDoneEventAggregation:
    """
    Test Done event aggregation across sessions.
    """

    def test_done_events_are_summed_across_sessions(self) -> None:
        """
        Total Done events include events from every session.
        """

        first_session = session(
            session_date=date(
                2026,
                7,
                23,
            ),
            done_events=(
                done_event(
                    attendee="Alice",
                ),
                done_event(
                    attendee="Bob",
                    minute=1,
                    line_number=2,
                ),
            ),
        )

        second_session = session(
            session_date=date(
                2026,
                7,
                24,
            ),
            done_events=(
                done_event(
                    attendee="Carol",
                ),
            ),
        )

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                first_session,
                second_session,
            ),
        )

        assert result.total_done_events == 3


# ============================================================================
# Activity Event Aggregation
# ============================================================================


class TestActivityEventAggregation:
    """
    Test activity event aggregation across sessions.
    """

    def test_activity_events_are_summed_across_sessions(self) -> None:
        """
        Total activity events include events from every session.
        """

        first_session = session(
            session_date=date(
                2026,
                7,
                23,
            ),
            activity_events=(
                activity_event(
                    activity_type=ActivityType.INSIGHT,
                ),
                activity_event(
                    activity_type=ActivityType.DISCUSSION,
                    minute=1,
                    line_number=2,
                ),
            ),
        )

        second_session = session(
            session_date=date(
                2026,
                7,
                24,
            ),
            activity_events=(
                activity_event(
                    activity_type=ActivityType.PRAYER_SESSION,
                ),
            ),
        )

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                first_session,
                second_session,
            ),
        )

        assert result.total_activity_events == 3


# ============================================================================
# Iterable Input
# ============================================================================


class TestIterableInput:
    """
    Test support for general iterables.
    """

    def test_generator_input_is_supported(self) -> None:
        """
        The service accepts a generator of sessions.
        """

        sessions = (
            session(
                session_date=date(
                    2026,
                    7,
                    23,
                ),
            ),
            session(
                session_date=date(
                    2026,
                    7,
                    24,
                ),
            ),
        )

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                item
                for item in sessions
            ),
        )

        assert result.session_count == 2


# ============================================================================
# Ordering Independence
# ============================================================================


class TestOrderingIndependence:
    """
    Test that input ordering does not affect analytics boundaries.
    """

    def test_unsorted_sessions_are_ordered_for_date_boundaries(self) -> None:
        """
        Sessions are sorted chronologically before boundary calculation.
        """

        service = MultiSessionAnalyticsService()

        result = service.analyze(
            (
                session(
                    session_date=date(
                        2026,
                        7,
                        25,
                    ),
                ),
                session(
                    session_date=date(
                        2026,
                        7,
                        23,
                    ),
                ),
                session(
                    session_date=date(
                        2026,
                        7,
                        24,
                    ),
                ),
            ),
        )

        assert result.start_date == date(
            2026,
            7,
            23,
        )

        assert result.end_date == date(
            2026,
            7,
            25,
        )