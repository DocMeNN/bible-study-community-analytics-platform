# tests/application/services/test_activity_service.py

"""
Activity Service Application Tests

Purpose:
    Verify the application-level activity service.

Coverage:
    - Service initialization.
    - Session construction delegation.
    - Activity event access.
    - Activity counting.
    - Activity type filtering.
    - First and last activity lookup.
    - Convenience methods.
    - Builder access.
    - String representations.

Rules:
    - Tests must use the current Domain model contracts.
    - Tests must not invent ActivityType values.
    - Prayer activity is represented by PRAYER_SESSION.
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
from src.application.builders.session_builder import SessionBuilder
from src.application.services.activity_service import ActivityService
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
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


def activity_event(
    *,
    sender: str = "Alice",
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
            sender=sender,
            content="Activity",
            minute=minute,
            line_number=line_number,
        ),
    )


def session_with_activities(
    *events: ActivityEvent,
) -> Session:
    """
    Build a Session containing activity events.
    """

    return Session(
        session_date=date(
            2026,
            7,
            23,
        ),
        activity_events=tuple(events),
    )


# ============================================================================
# Test Doubles
# ============================================================================


class RecordingSessionBuilder:
    """
    Test double for SessionBuilder delegation.
    """

    name = "RecordingSessionBuilder"

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self.calls: list[dict[str, object]] = []

    def build(
        self,
        *,
        session_date: date,
        messages: object,
    ) -> Session:
        """
        Record the build call and return the configured session.
        """

        self.calls.append(
            {
                "session_date": session_date,
                "messages": messages,
            }
        )

        return self.session


# ============================================================================
# ActivityService Initialization
# ============================================================================


class TestActivityServiceInitialization:
    """
    Test service initialization and builder access.
    """

    def test_default_builder_is_created(self) -> None:
        """
        The service creates a SessionBuilder when none is supplied.
        """

        service = ActivityService()

        assert isinstance(
            service.builder,
            SessionBuilder,
        )

    def test_supplied_builder_is_preserved(self) -> None:
        """
        A supplied builder is used by the service.
        """

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            ),
        )

        builder = RecordingSessionBuilder(
            session,
        )

        service = ActivityService(
            session_builder=builder,
        )

        assert service.builder is builder


# ============================================================================
# Session Construction
# ============================================================================


class TestSessionConstruction:
    """
    Test SessionBuilder orchestration.
    """

    def test_build_session_delegates_to_builder(self) -> None:
        """
        build_session delegates session construction to the builder.
        """

        expected_session = Session(
            session_date=date(
                2026,
                7,
                23,
            ),
        )

        builder = RecordingSessionBuilder(
            expected_session,
        )

        service = ActivityService(
            session_builder=builder,
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

        assert result is expected_session
        assert len(builder.calls) == 1
        assert builder.calls[0]["session_date"] == session_date
        assert builder.calls[0]["messages"] is messages


# ============================================================================
# Activity Events
# ============================================================================


class TestActivityEvents:
    """
    Test activity event access and counting.
    """

    def test_activity_events_returns_session_events(self) -> None:
        """
        All activity events are returned.
        """

        first = activity_event(
            sender="Alice",
            minute=1,
            line_number=1,
        )

        second = activity_event(
            sender="Bob",
            minute=2,
            line_number=2,
        )

        session = session_with_activities(
            first,
            second,
        )

        service = ActivityService()

        assert service.activity_events(
            session,
        ) == (
            first,
            second,
        )

    def test_activity_count_returns_number_of_events(self) -> None:
        """
        Activity count returns the total number of activity events.
        """

        session = session_with_activities(
            activity_event(
                line_number=1,
            ),
            activity_event(
                sender="Bob",
                minute=1,
                line_number=2,
            ),
            activity_event(
                sender="Carol",
                minute=2,
                line_number=3,
            ),
        )

        service = ActivityService()

        assert service.activity_count(
            session,
        ) == 3

    def test_activity_count_returns_zero_for_empty_session(self) -> None:
        """
        Empty sessions have zero activity events.
        """

        service = ActivityService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            ),
        )

        assert service.activity_count(
            session,
        ) == 0


# ============================================================================
# Activity Counts
# ============================================================================


class TestActivityCounts:
    """
    Test activity classification counts.
    """

    def test_activity_counts_group_events_by_type(self) -> None:
        """
        Activity events are counted by ActivityType.
        """

        session = session_with_activities(
            activity_event(
                activity_type=ActivityType.INSIGHT,
                line_number=1,
            ),
            activity_event(
                activity_type=ActivityType.INSIGHT,
                minute=1,
                line_number=2,
            ),
            activity_event(
                activity_type=ActivityType.PRAYER_SESSION,
                minute=2,
                line_number=3,
            ),
        )

        service = ActivityService()

        assert service.activity_counts(
            session,
        ) == {
            ActivityType.INSIGHT: 2,
            ActivityType.PRAYER_SESSION: 1,
        }

    def test_empty_activity_returns_empty_counts(self) -> None:
        """
        No activity events produce empty counts.
        """

        service = ActivityService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            ),
        )

        assert service.activity_counts(
            session,
        ) == {}


# ============================================================================
# Activity Boundaries
# ============================================================================


class TestActivityBoundaries:
    """
    Test first and last activity lookup.
    """

    def test_first_activity_returns_earliest_event(self) -> None:
        """
        The earliest activity event is returned.
        """

        first = activity_event(
            sender="Alice",
            minute=1,
            line_number=1,
        )

        second = activity_event(
            sender="Bob",
            minute=2,
            line_number=2,
        )

        session = session_with_activities(
            second,
            first,
        )

        service = ActivityService()

        assert service.first_activity(
            session,
        ) is first

    def test_first_activity_returns_none_when_no_events_exist(self) -> None:
        """
        No activity events produce None.
        """

        service = ActivityService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            ),
        )

        assert service.first_activity(
            session,
        ) is None

    def test_last_activity_returns_latest_event(self) -> None:
        """
        The latest activity event is returned.
        """

        first = activity_event(
            sender="Alice",
            minute=1,
            line_number=1,
        )

        last = activity_event(
            sender="Bob",
            minute=2,
            line_number=2,
        )

        session = session_with_activities(
            first,
            last,
        )

        service = ActivityService()

        assert service.last_activity(
            session,
        ) is last

    def test_last_activity_returns_none_when_no_events_exist(self) -> None:
        """
        No activity events produce None.
        """

        service = ActivityService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            ),
        )

        assert service.last_activity(
            session,
        ) is None


# ============================================================================
# Activity Lookup
# ============================================================================


class TestActivityLookup:
    """
    Test activity type filtering.
    """

    def test_activity_events_by_type_returns_matching_events(self) -> None:
        """
        Only events of the requested type are returned.
        """

        insight = activity_event(
            activity_type=ActivityType.INSIGHT,
            line_number=1,
        )

        prayer_session = activity_event(
            activity_type=ActivityType.PRAYER_SESSION,
            minute=1,
            line_number=2,
        )

        session = session_with_activities(
            insight,
            prayer_session,
        )

        service = ActivityService()

        assert service.activity_events_by_type(
            session,
            ActivityType.INSIGHT,
        ) == (
            insight,
        )

    def test_activity_events_by_type_returns_empty_tuple_when_no_match(
        self,
    ) -> None:
        """
        No matching activity type produces an empty tuple.
        """

        session = session_with_activities(
            activity_event(
                activity_type=ActivityType.INSIGHT,
            ),
        )

        service = ActivityService()

        assert service.activity_events_by_type(
            session,
            ActivityType.PRAYER_SESSION,
        ) == ()

    def test_has_activity_returns_true_when_type_exists(self) -> None:
        """
        has_activity returns True for an existing activity type.
        """

        session = session_with_activities(
            activity_event(
                activity_type=ActivityType.INSIGHT,
            ),
        )

        service = ActivityService()

        assert service.has_activity(
            session,
            ActivityType.INSIGHT,
        ) is True

    def test_has_activity_returns_false_when_type_does_not_exist(
        self,
    ) -> None:
        """
        has_activity returns False for a missing activity type.
        """

        session = session_with_activities(
            activity_event(
                activity_type=ActivityType.INSIGHT,
            ),
        )

        service = ActivityService()

        assert service.has_activity(
            session,
            ActivityType.PRAYER_SESSION,
        ) is False


# ============================================================================
# Convenience Methods
# ============================================================================


class TestConvenienceMethods:
    """
    Test service convenience methods.
    """

    def test_has_activities_returns_true_when_activities_exist(self) -> None:
        """
        has_activities returns True when activities exist.
        """

        session = session_with_activities(
            activity_event(),
        )

        service = ActivityService()

        assert service.has_activities(
            session,
        ) is True

    def test_has_activities_returns_false_for_empty_session(self) -> None:
        """
        has_activities returns False for an empty session.
        """

        service = ActivityService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            ),
        )

        assert service.has_activities(
            session,
        ) is False

    def test_is_empty_returns_true_for_empty_session(self) -> None:
        """
        Empty sessions are identified correctly.
        """

        service = ActivityService()

        session = Session(
            session_date=date(
                2026,
                7,
                23,
            ),
        )

        assert service.is_empty(
            session,
        ) is True

    def test_is_empty_returns_false_for_non_empty_session(self) -> None:
        """
        Sessions containing activities are not empty.
        """

        session = session_with_activities(
            activity_event(),
        )

        service = ActivityService()

        assert service.is_empty(
            session,
        ) is False


# ============================================================================
# Representations
# ============================================================================


class TestActivityServiceRepresentations:
    """
    Test service string representations.
    """

    def test_repr_contains_service_name_and_builder_name(self) -> None:
        """
        repr identifies the service and its builder.
        """

        service = ActivityService()

        result = repr(
            service,
        )

        assert "ActivityService" in result
        assert "SessionBuilder" in result

    def test_str_matches_repr(self) -> None:
        """
        str returns the official representation.
        """

        service = ActivityService()

        assert str(
            service,
        ) == repr(
            service,
        )
