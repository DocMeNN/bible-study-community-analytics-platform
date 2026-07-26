# src/application/builders/multi_session_builder.py

"""
Multi-Session Builder

Purpose
-------
Builds multiple Session aggregates from a complete collection of
validated Message objects.

Responsibilities
----------------
- Validate supplied messages.
- Detect Scripture Reading session boundaries.
- Group messages into individual sessions.
- Delegate each session to SessionBuilder.
- Return a SessionCollection.

Session Detection Rule
----------------------
A new Daily Session begins when:

- a Scripture Reading marker is detected; and
- it occurs at least 18 hours after the previous Scripture Reading marker.

The first Scripture Reading marker always begins the first session.

Rules
-----
- No pandas.
- No Streamlit.
- No file I/O.
- No infrastructure parsing.
- No analytics.
- No UI code.

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
from datetime import datetime, timedelta

# ============================================================================
# Local Imports
# ============================================================================
from src.application.builders.session_builder import SessionBuilder
from src.domain.constants.keywords import SESSION_START_KEYWORDS
from src.domain.models.message import Message
from src.domain.models.session_collection import SessionCollection

# ============================================================================
# Multi-Session Builder
# ============================================================================


class MultiSessionBuilder:
    """
    Build multiple Session aggregates from validated messages.
    """

    SESSION_GAP = timedelta(
        hours=18,
    )

    def __init__(
        self,
        session_builder: SessionBuilder | None = None,
    ) -> None:
        """
        Initialize the MultiSessionBuilder.
        """

        self._session_builder = (
            session_builder
            if session_builder is not None
            else SessionBuilder()
        )

    # =========================================================================
    # Public Builder
    # =========================================================================

    def build(
        self,
        messages: Iterable[Message],
    ) -> SessionCollection:
        """
        Build a collection of detected Sessions.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_groups = self._group_messages(
            ordered_messages,
        )

        sessions = tuple(
            self._session_builder.build(
                session_date=group[0].timestamp.date(),
                messages=group,
            )
            for group in session_groups
        )

        return SessionCollection(
            sessions=sessions,
        )

    # =========================================================================
    # Session Detection
    # =========================================================================

    def _group_messages(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[tuple[Message, ...], ...]:
        """
        Group messages into detected sessions.
        """

        groups: list[list[Message]] = []
        current_group: list[Message] = []
        previous_scripture_timestamp: datetime | None = None

        for message in messages:

            if self._is_new_session(
                message,
                previous_scripture_timestamp,
            ):

                if current_group:
                    groups.append(
                        current_group,
                    )

                current_group = []

                previous_scripture_timestamp = (
                    message.timestamp
                )

            if current_group:
                current_group.append(
                    message,
                )

            elif self._is_session_start(
                message,
            ):
                current_group.append(
                    message,
                )

        if current_group:
            groups.append(
                current_group,
            )

        return tuple(
            tuple(group)
            for group in groups
        )

    def _is_new_session(
        self,
        message: Message,
        previous_scripture_timestamp: datetime | None,
    ) -> bool:
        """
        Return True if the message begins a new session.
        """

        if not self._is_session_start(
            message,
        ):
            return False

        if previous_scripture_timestamp is None:
            return True

        return (
            message.timestamp
            - previous_scripture_timestamp
        ) >= self.SESSION_GAP

    # =========================================================================
    # Session Marker
    # =========================================================================

    def _is_session_start(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message contains a Scripture Reading marker.
        """

        normalized = message.content.casefold()

        return bool(
            any(
                keyword.casefold() in normalized
                for keyword in SESSION_START_KEYWORDS
            )
        )

    # =========================================================================
    # Validation
    # =========================================================================

    def _validate_messages(
        self,
        messages: Iterable[Message],
    ) -> tuple[Message, ...]:
        """
        Validate and chronologically order messages.
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
    # Accessors
    # =========================================================================

    @property
    def session_builder(
        self,
    ) -> SessionBuilder:
        """
        Return the SessionBuilder.
        """

        return self._session_builder

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
            f"{self.__class__.__name__}("
            f"session_builder="
            f"{self.session_builder.name})"
        )

    def __str__(
        self,
    ) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()
