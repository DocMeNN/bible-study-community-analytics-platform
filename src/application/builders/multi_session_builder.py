# src/application/builders/multi_session_builder.py

"""
Multi-Session Builder

Purpose
-------
Builds multiple Session aggregates from validated Message objects.

Responsibilities
----------------
- Validate supplied messages.
- Delegate session detection to SessionBuilder.
- Build SessionCollection objects.
- Expose session-grouping helpers for application tests.

Rules
-----
- Application orchestration only.
- Session detection logic lives inside SessionBuilder.
- No duplicated business rules.
- No pandas.
- No Streamlit.
- No infrastructure parsing.
- No analytics.
"""

from __future__ import annotations

from collections.abc import Iterable

from src.application.builders.session_builder import SessionBuilder
from src.domain.models.message import Message
from src.domain.models.session import Session
from src.domain.models.session_collection import SessionCollection
from src.domain.services.session_detector import SessionDetector


class MultiSessionBuilder:
    """
    Builds a SessionCollection from validated messages.
    """

    def __init__(
        self,
        *,
        session_detector: SessionDetector | None = None,
        session_builder: SessionBuilder | None = None,
    ) -> None:
        self._session_detector = (
            session_detector if session_detector is not None else SessionDetector()
        )

        self._session_builder = (
            session_builder if session_builder is not None else SessionBuilder()
        )

    # =========================================================================
    # Public Builder
    # =========================================================================

    def build(
        self,
        messages: Iterable[Message],
    ) -> SessionCollection:
        """
        Build every detected Daily Session.
        """

        validated_messages = self._validate_messages(messages)

        grouped_messages = self._group_messages(validated_messages)

        sessions: tuple[Session, ...] = tuple(
            self._session_builder.build(
                session_date=session_messages[0].timestamp.date(),
                messages=session_messages,
            )
            for session_messages in grouped_messages
            if session_messages
        )

        return SessionCollection(
            sessions=sessions,
        )

    # =========================================================================
    # Compatibility Helpers
    # =========================================================================

    def _group_messages(
        self,
        messages: Iterable[Message],
    ) -> tuple[tuple[Message, ...], ...]:
        """
        Group messages into detected sessions.

        Groups include the Scripture Reading marker because the
        application tests assert against the raw grouped messages.
        """

        validated = self._validate_messages(messages)

        groups: list[list[Message]] = []
        current_group: list[Message] = []

        previous_marker: Message | None = None
        session_started = False

        for message in validated:

            if self._is_session_start(message):

                if not session_started:
                    session_started = True
                    current_group = [message]
                    previous_marker = message
                    continue

                assert previous_marker is not None

                if (
                    message.timestamp - previous_marker.timestamp
                    >= self.session_detector.minimum_session_gap
                ):
                    groups.append(current_group)
                    current_group = [message]
                    previous_marker = message
                    continue

            if session_started:
                current_group.append(message)

        if current_group:
            groups.append(current_group)

        return tuple(
            tuple(group)
            for group in groups
        )

    def _is_session_start(
        self,
        message: Message,
    ) -> bool:
        """
        Return True when a message is a session boundary.
        """

        return self._session_builder._is_session_start(message)  # noqa: SLF001

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

        validated = tuple(messages)

        for message in validated:
            if not isinstance(message, Message):
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
    def session_detector(
        self,
    ) -> SessionDetector:
        return self._session_detector

    @property
    def session_builder(
        self,
    ) -> SessionBuilder:
        return self._session_builder

    # =========================================================================
    # Metadata
    # =========================================================================

    @property
    def name(
        self,
    ) -> str:
        return self.__class__.__name__

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}("
            f"session_detector={self.session_detector.name}, "
            f"session_builder={self.session_builder.name})"
        )

    def __str__(
        self,
    ) -> str:
        return self.__repr__()
