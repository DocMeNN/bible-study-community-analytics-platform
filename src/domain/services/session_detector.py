# src/domain/services/session_detector.py

"""
Session Detector Domain Service

Purpose
-------
Detect study-session boundaries from Scripture Reading events.

Responsibilities
----------------
- Identify Scripture Reading session markers.
- Order messages chronologically.
- Apply the minimum session-gap rule.
- Group messages into detected study sessions.
- Remain technology independent.

Session Detection Rule
-----------------------
A new study session begins when:

1. A message contains the Scripture Reading marker.
2. The marker occurs at least 18 hours after the
   previous accepted Scripture Reading marker.

Notes
-----
- Pure domain logic.
- No pandas.
- No Streamlit.
- No file I/O.
- No infrastructure dependencies.
- No Session aggregate construction.
- The service detects message groups only.

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
from collections.abc import Iterable
from datetime import timedelta

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.constants.keywords import SESSION_START_KEYWORDS
from src.domain.models.message import Message

# ============================================================================
# Constants
# ============================================================================

MINIMUM_SESSION_GAP = timedelta(
    hours=18,
)

# ============================================================================
# Session Detector
# ============================================================================


class SessionDetector:
    """
    Detect study-session boundaries from validated Messages.
    """

    # =========================================================================
    # Public Detection
    # =========================================================================

    def detect(
        self,
        messages: Iterable[Message],
    ) -> tuple[tuple[Message, ...], ...]:
        """
        Detect and return message groups belonging to separate sessions.
        """

        ordered_messages = self._validate_and_sort_messages(
            messages,
        )

        if not ordered_messages:
            return ()

        session_start_indexes = self._session_start_indexes(
            ordered_messages,
        )

        if not session_start_indexes:
            return ()

        sessions: list[tuple[Message, ...]] = []

        for index, start_index in enumerate(
            session_start_indexes,
        ):
            if index + 1 < len(
                session_start_indexes,
            ):
                end_index = session_start_indexes[index + 1]

            else:
                end_index = len(
                    ordered_messages,
                )

            session_messages = ordered_messages[start_index:end_index]

            sessions.append(
                session_messages,
            )

        return tuple(
            sessions,
        )

    # =========================================================================
    # Session Markers
    # =========================================================================

    def _session_start_indexes(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[int, ...]:
        """
        Return indexes of accepted session-start markers.
        """

        indexes: list[int] = []
        previous_session_start: Message | None = None

        for index, message in enumerate(
            messages,
        ):
            if not self._is_session_start(
                message,
            ):
                continue

            if previous_session_start is None:
                indexes.append(
                    index,
                )

                previous_session_start = message

                continue

            elapsed = message.timestamp - previous_session_start.timestamp

            if elapsed < MINIMUM_SESSION_GAP:
                continue

            indexes.append(
                index,
            )

            previous_session_start = message

        return tuple(
            indexes,
        )

    def _is_session_start(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if a message contains a session-start marker.
        """

        normalized = message.content.casefold()

        return any(
            keyword.casefold() in normalized for keyword in SESSION_START_KEYWORDS
        )

        # =========================================================================

    # Validation
    # =========================================================================

    def _validate_and_sort_messages(
        self,
        messages: Iterable[Message],
    ) -> tuple[Message, ...]:
        """
        Validate and chronologically sort messages.
        """

        validated = tuple(
            messages,
        )

        for message in validated:
            if not isinstance(
                message,
                Message,
            ):
                raise TypeError(
                    "messages must contain only Message instances.",
                )

        return tuple(
            sorted(
                validated,
                key=lambda message: message.timestamp,
            )
        )

    # =========================================================================
    # Metadata
    # =========================================================================

    @property
    def minimum_session_gap(
        self,
    ) -> timedelta:
        """
        Return the minimum time gap between sessions.
        """

        return MINIMUM_SESSION_GAP

    @property
    def name(
        self,
    ) -> str:
        """
        Return the detector name.
        """

        return self.__class__.__name__

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(
        self,
    ) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}(minimum_session_gap={self.minimum_session_gap})"
        )

    def __str__(
        self,
    ) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()
