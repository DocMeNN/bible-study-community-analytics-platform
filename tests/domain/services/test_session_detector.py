# tests/domain/services/test_session_detector.py

"""
Session Detector Domain Tests

Purpose
-------
Verify Scripture Reading session-boundary detection.

Coverage
--------
- Empty input.
- Generator input.
- Message validation.
- Chronological ordering.
- First Scripture Reading detection.
- 18-hour minimum session gap.
- Markers inside the 18-hour window.
- Multiple session detection.
- Message grouping.
- Session marker preservation.
- Detector metadata.

Author
------
OYBS Attendance Dashboard
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from datetime import datetime, timedelta

import pytest

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.message import Message
from src.domain.services.session_detector import (
    MINIMUM_SESSION_GAP,
    SessionDetector,
)

# ============================================================================
# Test Helpers
# ============================================================================


def make_message(
    *,
    content: str,
    sender: str = "Alice",
    timestamp: datetime,
    line_number: int,
) -> Message:
    """
    Create a valid Message for testing.
    """

    return Message(
        timestamp=timestamp,
        sender=sender,
        content=content,
        line_number=line_number,
    )


def scripture_message(
    *,
    timestamp: datetime,
    line_number: int,
    content: str = "SCRIPTURE READING",
) -> Message:
    """
    Create a Scripture Reading marker message.
    """

    return make_message(
        content=content,
        timestamp=timestamp,
        line_number=line_number,
    )


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def detector() -> SessionDetector:
    """
    Return a SessionDetector instance.
    """

    return SessionDetector()


# ============================================================================
# Construction
# ============================================================================


class TestSessionDetectorConstruction:
    """
    Test detector construction and metadata.
    """

    def test_can_be_instantiated(
        self,
    ) -> None:
        """
        SessionDetector can be instantiated.
        """

        detector = SessionDetector()

        assert isinstance(
            detector,
            SessionDetector,
        )

    def test_name_returns_class_name(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        name returns the official class name.
        """

        assert detector.name == "SessionDetector"

    def test_minimum_session_gap_is_18_hours(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        The minimum session gap is 18 hours.
        """

        assert detector.minimum_session_gap == timedelta(
            hours=18,
        )

        assert detector.minimum_session_gap == (MINIMUM_SESSION_GAP)

    def test_repr_returns_official_representation(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        repr returns the expected representation.
        """

        assert repr(detector) == ("SessionDetector(minimum_session_gap=18:00:00)")

    def test_str_matches_repr(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        str returns the same representation as repr.
        """

        assert str(detector) == repr(
            detector,
        )


# ============================================================================
# Validation
# ============================================================================


class TestSessionDetectorValidation:
    """
    Test input validation.
    """

    def test_empty_input_returns_no_sessions(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Empty input produces no sessions.
        """

        result = detector.detect(
            [],
        )

        assert result == ()

    def test_accepts_generator_input(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Generator input is supported.
        """

        messages = (
            message
            for message in [
                scripture_message(
                    timestamp=datetime(
                        2026,
                        7,
                        1,
                        8,
                        0,
                    ),
                    line_number=1,
                ),
            ]
        )

        result = detector.detect(
            messages,
        )

        assert len(result) == 1

    def test_rejects_non_message_items(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Non-Message items are rejected.
        """

        with pytest.raises(
            TypeError,
            match="messages must contain only Message instances",
        ):
            detector.detect(
                [
                    "not a message",
                ],
            )

    def test_no_scripture_marker_returns_no_sessions(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Messages without a Scripture Reading marker
        produce no sessions.
        """

        result = detector.detect(
            [
                make_message(
                    content="Insight",
                    timestamp=datetime(
                        2026,
                        7,
                        1,
                        8,
                        0,
                    ),
                    line_number=1,
                ),
            ],
        )

        assert result == ()


# ============================================================================
# Chronological Ordering
# ============================================================================


class TestChronologicalOrdering:
    """
    Test chronological message ordering.
    """

    def test_messages_are_sorted_before_detection(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Messages are ordered chronologically before detection.
        """

        second_session = scripture_message(
            timestamp=datetime(
                2026,
                7,
                2,
                8,
                0,
            ),
            line_number=3,
        )

        first_session = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        result = detector.detect(
            [
                second_session,
                first_session,
            ],
        )

        assert len(result) == 2

        assert result[0][0] is first_session
        assert result[1][0] is second_session


# ============================================================================
# Session Boundary Detection
# ============================================================================


class TestSessionBoundaryDetection:
    """
    Test Scripture Reading session-boundary detection.
    """

    def test_first_scripture_marker_starts_first_session(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        The first Scripture Reading marker starts a session.
        """

        marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        result = detector.detect(
            [
                marker,
            ],
        )

        assert len(result) == 1
        assert result[0] == (marker,)

    def test_marker_within_18_hours_does_not_start_new_session(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        A Scripture Reading marker less than 18 hours
        after the previous marker belongs to the current session.
        """

        first_marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        second_marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                2,
                1,
                59,
            ),
            line_number=3,
        )

        result = detector.detect(
            [
                first_marker,
                second_marker,
            ],
        )

        assert len(result) == 1

        assert result[0] == (
            first_marker,
            second_marker,
        )

    def test_marker_exactly_18_hours_after_previous_starts_new_session(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        A Scripture Reading marker exactly 18 hours
        after the previous marker starts a new session.
        """

        first_marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        second_marker = scripture_message(
            timestamp=(
                first_marker.timestamp
                + timedelta(
                    hours=18,
                )
            ),
            line_number=3,
        )

        result = detector.detect(
            [
                first_marker,
                second_marker,
            ],
        )

        assert len(result) == 2

    def test_marker_more_than_18_hours_after_previous_starts_new_session(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        A Scripture Reading marker more than 18 hours
        after the previous marker starts a new session.
        """

        first_marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        second_marker = scripture_message(
            timestamp=(
                first_marker.timestamp
                + timedelta(
                    hours=24,
                )
            ),
            line_number=3,
        )

        result = detector.detect(
            [
                first_marker,
                second_marker,
            ],
        )

        assert len(result) == 2

    def test_scripture_marker_matching_is_case_insensitive(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Scripture Reading marker matching is case-insensitive.
        """

        result = detector.detect(
            [
                scripture_message(
                    content="scripture reading",
                    timestamp=datetime(
                        2026,
                        7,
                        1,
                        8,
                        0,
                    ),
                    line_number=1,
                ),
            ],
        )

        assert len(result) == 1


# ============================================================================
# Session Grouping
# ============================================================================


class TestSessionGrouping:
    """
    Test messages are assigned to the correct detected session.
    """

    def test_messages_between_markers_belong_to_first_session(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Messages between session markers belong to the
        preceding session.
        """

        first_marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        first_message = make_message(
            content="First session message",
            timestamp=datetime(
                2026,
                7,
                1,
                9,
                0,
            ),
            line_number=2,
        )

        second_marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                2,
                8,
                0,
            ),
            line_number=3,
        )

        result = detector.detect(
            [
                first_marker,
                first_message,
                second_marker,
            ],
        )

        assert len(result) == 2

        assert result[0] == (
            first_marker,
            first_message,
        )

        assert result[1] == (second_marker,)

    def test_multiple_sessions_are_detected(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Multiple valid Scripture Reading boundaries
        produce multiple sessions.
        """

        messages = [
            scripture_message(
                timestamp=datetime(
                    2026,
                    7,
                    1,
                    8,
                    0,
                ),
                line_number=1,
            ),
            make_message(
                content="Session 1",
                timestamp=datetime(
                    2026,
                    7,
                    1,
                    9,
                    0,
                ),
                line_number=2,
            ),
            scripture_message(
                timestamp=datetime(
                    2026,
                    7,
                    2,
                    8,
                    0,
                ),
                line_number=3,
            ),
            make_message(
                content="Session 2",
                timestamp=datetime(
                    2026,
                    7,
                    2,
                    9,
                    0,
                ),
                line_number=4,
            ),
            scripture_message(
                timestamp=datetime(
                    2026,
                    7,
                    3,
                    8,
                    0,
                ),
                line_number=5,
            ),
            make_message(
                content="Session 3",
                timestamp=datetime(
                    2026,
                    7,
                    3,
                    9,
                    0,
                ),
                line_number=6,
            ),
        ]

        result = detector.detect(
            messages,
        )

        assert len(result) == 3

        assert result[0][1].content == "Session 1"
        assert result[1][1].content == "Session 2"
        assert result[2][1].content == "Session 3"

    def test_messages_before_first_marker_are_excluded(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        Messages before the first Scripture Reading marker
        are excluded from all sessions.
        """

        before = make_message(
            content="Before session",
            timestamp=datetime(
                2026,
                7,
                1,
                7,
                0,
            ),
            line_number=1,
        )

        marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=2,
        )

        result = detector.detect(
            [
                before,
                marker,
            ],
        )

        assert len(result) == 1

        assert result[0] == (marker,)

    def test_session_marker_is_preserved_in_group(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        The Scripture Reading marker remains in the detected
        session group for SessionBuilder processing.
        """

        marker = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        result = detector.detect(
            [
                marker,
            ],
        )

        assert result[0][0] is marker


# ============================================================================
# Session Gap Behaviour
# ============================================================================


class TestSessionGapBehaviour:
    """
    Test boundary behaviour around the 18-hour threshold.
    """

    def test_gap_just_below_18_hours_is_same_session(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        A gap of 17 hours and 59 minutes is not a new session.
        """

        first = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        second = scripture_message(
            timestamp=(
                first.timestamp
                + timedelta(
                    hours=17,
                    minutes=59,
                )
            ),
            line_number=2,
        )

        result = detector.detect(
            [
                first,
                second,
            ],
        )

        assert len(result) == 1

    def test_gap_of_18_hours_is_new_session(
        self,
        detector: SessionDetector,
    ) -> None:
        """
        A gap of exactly 18 hours is a new session.
        """

        first = scripture_message(
            timestamp=datetime(
                2026,
                7,
                1,
                8,
                0,
            ),
            line_number=1,
        )

        second = scripture_message(
            timestamp=(first.timestamp + MINIMUM_SESSION_GAP),
            line_number=2,
        )

        result = detector.detect(
            [
                first,
                second,
            ],
        )

        assert len(result) == 2
