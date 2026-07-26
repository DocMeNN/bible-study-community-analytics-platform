# tests/application/builders/test_multi_session_builder.py

"""
Multi-Session Builder Tests

Purpose
-------
Verify multi-session detection and construction orchestration.

Coverage
--------
- Builder construction.
- SessionBuilder dependency injection.
- First Scripture Reading session detection.
- 18-hour session boundary.
- Sub-18-hour Scripture Reading markers.
- Messages before the first session marker.
- Chronological ordering.
- Multiple Session construction.
- Empty input.
- Invalid message validation.
- SessionBuilder delegation.
- Accessors and dunder methods.

Rules
-----
- Test MultiSessionBuilder orchestration only.
- Do not duplicate SessionBuilder tests.
- Do not duplicate SessionCollection tests.
- Do not test Domain analytics.
- Do not test infrastructure parsing.

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
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

# ============================================================================
# Local Imports
# ============================================================================
from src.application.builders.multi_session_builder import (
    MultiSessionBuilder,
)
from src.application.builders.session_builder import SessionBuilder
from src.domain.models.message import Message
from src.domain.models.session import Session
from src.domain.models.session_collection import SessionCollection

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def builder() -> MultiSessionBuilder:
    """Return a default MultiSessionBuilder."""

    return MultiSessionBuilder()


@pytest.fixture
def session_builder() -> Mock:
    """Return an injected SessionBuilder mock."""

    return Mock(
        spec=SessionBuilder,
    )


def make_message(
    timestamp: datetime,
    content: str,
    sender: str = "Alice",
) -> Message:
    """Create a representative Message."""

    return Message(
        timestamp=timestamp,
        sender=sender,
        content=content,
        line_number=1,
    )


# ============================================================================
# Construction
# ============================================================================


class TestMultiSessionBuilderConstruction:
    """Test MultiSessionBuilder construction."""

    def test_default_construction(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """Default construction creates a SessionBuilder."""

        assert isinstance(
            builder.session_builder,
            SessionBuilder,
        )

    def test_dependency_injection_preserves_session_builder(
        self,
        session_builder: Mock,
    ) -> None:
        """Injected SessionBuilder is preserved."""

        service = MultiSessionBuilder(
            session_builder=session_builder,
        )

        assert service.session_builder is session_builder


# ============================================================================
# Session Detection
# ============================================================================


class TestSessionDetection:
    """Test Scripture Reading session detection."""

    def test_first_scripture_reading_starts_first_session(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """The first Scripture Reading marker starts the first session."""

        messages = (
            make_message(
                datetime(
                    2026,
                    7,
                    23,
                    8,
                    0,
                ),
                "SCRIPTURE READING",
            ),
            make_message(
                datetime(
                    2026,
                    7,
                    23,
                    9,
                    0,
                ),
                "Done",
            ),
        )

        result = builder._group_messages(
            messages,
        )

        assert len(result) == 1
        assert len(result[0]) == 2

    def test_scripture_reading_before_18_hours_does_not_start_new_session(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """A marker before the 18-hour gap remains in the same session."""

        start = datetime(
            2026,
            7,
            23,
            8,
            0,
        )

        messages = (
            make_message(
                start,
                "SCRIPTURE READING",
            ),
            make_message(
                start + timedelta(hours=10),
                "SCRIPTURE READING",
            ),
            make_message(
                start + timedelta(hours=11),
                "Done",
            ),
        )

        result = builder._group_messages(
            messages,
        )

        assert len(result) == 1
        assert len(result[0]) == 3

    def test_scripture_reading_exactly_18_hours_later_starts_new_session(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """A marker exactly 18 hours later starts a new session."""

        start = datetime(
            2026,
            7,
            23,
            8,
            0,
        )

        messages = (
            make_message(
                start,
                "SCRIPTURE READING",
            ),
            make_message(
                start + timedelta(hours=17),
                "Done",
            ),
            make_message(
                start + timedelta(hours=18),
                "SCRIPTURE READING",
            ),
            make_message(
                start + timedelta(hours=19),
                "Done",
            ),
        )

        result = builder._group_messages(
            messages,
        )

        assert len(result) == 2
        assert len(result[0]) == 2
        assert len(result[1]) == 2

    def test_scripture_reading_after_18_hours_starts_new_session(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """A marker after 18 hours starts a new session."""

        start = datetime(
            2026,
            7,
            23,
            8,
            0,
        )

        messages = (
            make_message(
                start,
                "SCRIPTURE READING",
            ),
            make_message(
                start + timedelta(hours=19),
                "SCRIPTURE READING",
            ),
        )

        result = builder._group_messages(
            messages,
        )

        assert len(result) == 2

    def test_messages_before_first_session_marker_are_excluded(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """Messages before the first Scripture Reading are excluded."""

        messages = (
            make_message(
                datetime(
                    2026,
                    7,
                    23,
                    6,
                    0,
                ),
                "Good morning",
            ),
            make_message(
                datetime(
                    2026,
                    7,
                    23,
                    8,
                    0,
                ),
                "SCRIPTURE READING",
            ),
            make_message(
                datetime(
                    2026,
                    7,
                    23,
                    9,
                    0,
                ),
                "Done",
            ),
        )

        result = builder._group_messages(
            messages,
        )

        assert len(result) == 1
        assert len(result[0]) == 2
        assert result[0][0].content == "SCRIPTURE READING"

    def test_multiple_sessions_are_detected(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """Multiple daily session boundaries are detected."""

        first = datetime(
            2026,
            7,
            23,
            8,
            0,
        )

        messages = (
            make_message(
                first,
                "SCRIPTURE READING",
            ),
            make_message(
                first + timedelta(hours=1),
                "Done",
            ),
            make_message(
                first + timedelta(hours=20),
                "SCRIPTURE READING",
            ),
            make_message(
                first + timedelta(hours=21),
                "Done",
            ),
            make_message(
                first + timedelta(hours=40),
                "SCRIPTURE READING",
            ),
            make_message(
                first + timedelta(hours=41),
                "Done",
            ),
        )

        result = builder._group_messages(
            messages,
        )

        assert len(result) == 3


# ============================================================================
# Ordering
# ============================================================================


class TestMessageOrdering:
    """Test chronological ordering."""

    def test_messages_are_sorted_before_grouping(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """Messages are ordered chronologically."""

        first = make_message(
            datetime(
                2026,
                7,
                23,
                8,
                0,
            ),
            "SCRIPTURE READING",
        )

        second = make_message(
            datetime(
                2026,
                7,
                23,
                9,
                0,
            ),
            "Done",
        )

        result = builder._validate_messages(
            (
                second,
                first,
            ),
        )

        assert result == (
            first,
            second,
        )


# ============================================================================
# Public Build Workflow
# ============================================================================


class TestBuildWorkflow:
    """Test complete multi-session build workflow."""

    def test_build_returns_session_collection(
        self,
        session_builder: Mock,
    ) -> None:
        """build returns a SessionCollection."""

        session_builder.build.side_effect = (
            lambda session_date, messages: Session(
                session_date=session_date,
            )
        )

        builder = MultiSessionBuilder(
            session_builder=session_builder,
        )

        messages = (
            make_message(
                datetime(
                    2026,
                    7,
                    23,
                    8,
                    0,
                ),
                "SCRIPTURE READING",
            ),
            make_message(
                datetime(
                    2026,
                    7,
                    24,
                    8,
                    0,
                ),
                "SCRIPTURE READING",
            ),
        )

        result = builder.build(
            messages,
        )

        assert isinstance(
            result,
            SessionCollection,
        )

        assert result.count == 2

    def test_build_delegates_each_session_to_session_builder(
        self,
        session_builder: Mock,
    ) -> None:
        """Each detected group is delegated to SessionBuilder."""

        session_builder.build.side_effect = (
            lambda session_date, messages: Session(
                session_date=session_date,
            )
        )

        builder = MultiSessionBuilder(
            session_builder=session_builder,
        )

        first = datetime(
            2026,
            7,
            23,
            8,
            0,
        )

        messages = (
            make_message(
                first,
                "SCRIPTURE READING",
            ),
            make_message(
                first + timedelta(hours=20),
                "SCRIPTURE READING",
            ),
        )

        result = builder.build(
            messages,
        )

        assert result.count == 2

        assert session_builder.build.call_count == 2

        first_call = session_builder.build.call_args_list[0]
        second_call = session_builder.build.call_args_list[1]

        assert first_call.kwargs["session_date"] == first.date()
        assert second_call.kwargs["session_date"] == (
            first + timedelta(hours=20)
        ).date()

    def test_empty_input_returns_empty_collection(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """Empty input produces an empty SessionCollection."""

        result = builder.build(
            (),
        )

        assert isinstance(
            result,
            SessionCollection,
        )

        assert result.is_empty

    def test_session_dates_are_chronological(
        self,
        session_builder: Mock,
    ) -> None:
        """Built sessions are returned chronologically."""

        session_builder.build.side_effect = (
            lambda session_date, messages: Session(
                session_date=session_date,
            )
        )

        builder = MultiSessionBuilder(
            session_builder=session_builder,
        )

        messages = (
            make_message(
                datetime(
                    2026,
                    7,
                    24,
                    8,
                    0,
                ),
                "SCRIPTURE READING",
            ),
            make_message(
                datetime(
                    2026,
                    7,
                    23,
                    8,
                    0,
                ),
                "SCRIPTURE READING",
            ),
        )

        result = builder.build(
            messages,
        )

        assert result.session_dates == (
            result.session_dates[0],
            result.session_dates[1],
        )

        assert result.session_dates[0] < result.session_dates[1]


# ============================================================================
# Validation
# ============================================================================


class TestValidation:
    """Test input validation."""

    def test_non_message_input_raises_type_error(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """Non-Message values are rejected."""

        with pytest.raises(
            TypeError,
            match="messages must contain only Message instances",
        ):
            builder.build(
                (
                    "not a message",
                ),
            )


# ============================================================================
# Session Marker
# ============================================================================


class TestSessionMarker:
    """Test session marker detection."""

    def test_session_marker_matching_is_case_insensitive(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """Session marker matching is case-insensitive."""

        message = make_message(
            datetime(
                2026,
                7,
                23,
                8,
                0,
            ),
            "scripture reading",
        )

        assert builder._is_session_start(
            message,
        )


# ============================================================================
# Dunder Methods
# ============================================================================


class TestDunderMethods:
    """Test MultiSessionBuilder dunder methods."""

    def test_repr_contains_class_name(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """repr contains the class name."""

        assert "MultiSessionBuilder" in repr(
            builder,
        )

    def test_str_matches_repr(
        self,
        builder: MultiSessionBuilder,
    ) -> None:
        """str and repr return the same representation."""

        assert str(
            builder,
        ) == repr(
            builder,
        )
