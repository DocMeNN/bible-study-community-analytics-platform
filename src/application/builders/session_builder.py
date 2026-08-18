# src/application/builders/session_builder.py

"""
Session Builder

Purpose
-------
Builds immutable Session aggregates from validated Message objects.

Responsibilities
----------------
- Validate input messages.
- Detect multiple study sessions.
- Determine session boundaries from Scripture Reading markers.
- Construct AttendanceEvent objects.
- Construct DoneEvent objects.
- Construct ActivityEvent objects.
- Exclude Scripture Reading announcements from participant activities.
- Assemble immutable Session aggregates.

Rules
-----
- No pandas.
- No Streamlit.
- No analytics.
- No reporting.
- No infrastructure parsing.
- No file I/O.
- Technology independent.

Session Detection Rule
----------------------
A new Daily Session begins when:

1. A Scripture Reading marker is detected.
2. The marker occurs at least 18 hours after the
   previous Scripture Reading marker.

The first Scripture Reading marker always begins
the first detected session.

The Scripture Reading marker itself is excluded from
the resulting Session event collections.

All messages after a session marker belong to that
session until the next valid session marker.

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
from datetime import date, datetime, timedelta

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.constants.keywords import (
    CLOSING_PRAYER_KEYWORDS,
    DONE_KEYWORDS,
    OPENING_PRAYER_KEYWORDS,
    SESSION_START_KEYWORDS,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.message import Message
from src.domain.models.session import Session
from src.domain.policies.activity_policy import (
    classify_activity,
    is_supported_activity,
)

# ============================================================================
# Constants
# ============================================================================

SESSION_MINIMUM_GAP = timedelta(hours=18)

# ============================================================================
# Session Builder
# ============================================================================


class SessionBuilder:
    """
    Build immutable Session aggregates from validated messages.
    """

    # ========================================================================
    # Public Builders
    # ========================================================================

    def build(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build one Session aggregate.

        Preserves the legacy single-session workflow.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_messages = self._session_messages(
            ordered_messages,
        )

        return self._build_session(
            session_date=session_date,
            messages=session_messages,
        )

    def build_sessions(
        self,
        messages: Iterable[Message],
    ) -> tuple[Session, ...]:
        """
        Detect and build every Daily Session.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_groups = self._group_messages_into_sessions(
            ordered_messages,
        )

        return tuple(
            self._build_session(
                session_date=session_messages[0].timestamp.date(),
                messages=session_messages,
            )
            for session_messages in session_groups
            if session_messages
        )

    # ========================================================================
    # Session Construction
    # ========================================================================

    def _build_session(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build one immutable Session aggregate.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        attendance_events = self._build_attendance_events(
            ordered_messages,
        )

        done_events = self._build_done_events(
            ordered_messages,
        )

        activity_events = self._build_activity_events(
            ordered_messages,
        )

        return Session(
            session_date=session_date,
            attendance_events=attendance_events,
            done_events=done_events,
            activity_events=activity_events,
        )

    # ========================================================================
    # Multi-Session Detection
    # ========================================================================

    def _group_messages_into_sessions(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[tuple[Message, ...], ...]:
        """
        Split a chronological message stream into Daily Sessions.

        Scripture Reading markers are treated as boundaries and are
        excluded from the resulting session message collections.
        """

        sessions: list[list[Message]] = []
        current_session: list[Message] = []

        previous_scripture_timestamp: datetime | None = None
        session_started = False

        for message in messages:

            if self._is_session_start(
                message,
            ):
                if not session_started:

                    session_started = True
                    previous_scripture_timestamp = message.timestamp

                    continue

                if (
                    previous_scripture_timestamp is not None
                    and (message.timestamp - previous_scripture_timestamp)
                    >= SESSION_MINIMUM_GAP
                ):

                    if current_session:
                        sessions.append(
                            current_session,
                        )

                    current_session = []

                    previous_scripture_timestamp = message.timestamp

            if session_started:
                current_session.append(
                    message,
                )

        if current_session:
            sessions.append(
                current_session,
            )

        return tuple(tuple(session) for session in sessions)

    # ========================================================================
    # Attendance Construction
    # ========================================================================

    def _build_attendance_events(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[AttendanceEvent, ...]:
        """
        Build AttendanceEvent objects.
        """

        return tuple(
            self._attendance_event(
                message,
            )
            for message in messages
        )

    # ========================================================================
    # Done Construction
    # ========================================================================

    def _build_done_events(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[DoneEvent, ...]:
        """
        Build DoneEvent objects.
        """

        return tuple(
            self._done_event(
                message,
            )
            for message in messages
            if self._is_done_message(
                message,
            )
        )

    # ========================================================================
    # Activity Construction
    # ========================================================================

    def _build_activity_events(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[ActivityEvent, ...]:
        """
        Build ActivityEvent objects.
        """

        activity_events: list[ActivityEvent] = []

        prayer_session_active = False

        for message in messages:

            if self._is_session_start(
                message,
            ):
                continue

            if not is_supported_activity(
                message.content,
                prayer_session_active=prayer_session_active,
            ):
                continue

            activity_type = self._activity_type(
                message,
                prayer_session_active=prayer_session_active,
            )

            if activity_type is None:
                continue

            if activity_type is ActivityType.SCRIPTURE_READING:
                continue

            activity_events.append(
                self._activity_event(
                    message,
                    activity_type,
                )
            )

            if self._is_prayer_session_opening(
                message,
            ):
                prayer_session_active = True

            elif self._is_prayer_session_closing(
                message,
            ):
                prayer_session_active = False

        return tuple(
            activity_events,
        )

    # ========================================================================
    # Activity Classification
    # ========================================================================

    def _activity_type(
        self,
        message: Message,
        *,
        prayer_session_active: bool = False,
    ) -> ActivityType | None:
        """
        Determine the ActivityType represented by a message.
        """

        activity_name = classify_activity(
            message.content,
            prayer_session_active=prayer_session_active,
        )

        activity_mapping: dict[str, ActivityType] = {
            "Scripture Reading": ActivityType.SCRIPTURE_READING,
            "Insight": ActivityType.INSIGHT,
            "Discussion": ActivityType.DISCUSSION,
            "Announcement": ActivityType.ANNOUNCEMENT,
            "Done": ActivityType.DONE,
            "Prayer Session": ActivityType.PRAYER_SESSION,
        }

        return activity_mapping.get(
            activity_name,
        )

    # ========================================================================
    # Prayer Session Boundaries
    # ========================================================================

    def _is_prayer_session_opening(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message opens a prayer session.
        """

        normalized = message.content.strip().casefold()

        return any(
            keyword.casefold() in normalized for keyword in OPENING_PRAYER_KEYWORDS
        )

    def _is_prayer_session_closing(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message closes a prayer session.
        """

        normalized = message.content.strip().casefold()

        return any(
            keyword.casefold() in normalized for keyword in CLOSING_PRAYER_KEYWORDS
        )

    # ========================================================================
    # Keyword Helpers
    # ========================================================================

    def _is_done_message(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message is a Done acknowledgement.
        """

        normalized = message.content.strip().casefold()

        return normalized in {keyword.casefold() for keyword in DONE_KEYWORDS}

    def _is_session_start(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message is a Scripture Reading marker.
        """

        normalized = message.content.strip().casefold()

        return any(
            keyword.casefold() in normalized for keyword in SESSION_START_KEYWORDS
        )

        # ========================================================================

    # Validation
    # ========================================================================

    def _validate_messages(
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

    # ========================================================================
    # Legacy Single-Session Extraction
    # ========================================================================

    def _session_messages(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[Message, ...]:
        """
        Extract messages belonging to the first detected session.

        Preserves backward compatibility for the existing
        single-session workflow.
        """

        session_started = False
        session_messages: list[Message] = []

        for message in messages:

            if not session_started:

                if self._is_session_start(
                    message,
                ):
                    session_started = True

                continue

            session_messages.append(
                message,
            )

        return tuple(
            session_messages,
        )

    # ========================================================================
    # Event Factories
    # ========================================================================

    def _attendance_event(
        self,
        message: Message,
    ) -> AttendanceEvent:
        """
        Create an AttendanceEvent.
        """

        return AttendanceEvent(
            attendee=message.sender,
            source_message=message,
        )

    def _done_event(
        self,
        message: Message,
    ) -> DoneEvent:
        """
        Create a DoneEvent.
        """

        return DoneEvent(
            attendee=message.sender,
            source_message=message,
        )

    def _activity_event(
        self,
        message: Message,
        activity_type: ActivityType,
    ) -> ActivityEvent:
        """
        Create an ActivityEvent.
        """

        return ActivityEvent(
            activity_type=activity_type,
            source_message=message,
        )

    # ========================================================================
    # Public Builder Utilities
    # ========================================================================

    def build_attendance_events(
        self,
        messages: Iterable[Message],
    ) -> tuple[AttendanceEvent, ...]:
        """
        Build attendance events only.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_messages = self._session_messages(
            ordered_messages,
        )

        return self._build_attendance_events(
            session_messages,
        )

    def build_done_events(
        self,
        messages: Iterable[Message],
    ) -> tuple[DoneEvent, ...]:
        """
        Build Done events only.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_messages = self._session_messages(
            ordered_messages,
        )

        return self._build_done_events(
            session_messages,
        )

    def build_activity_events(
        self,
        messages: Iterable[Message],
    ) -> tuple[ActivityEvent, ...]:
        """
        Build activity events only.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_messages = self._session_messages(
            ordered_messages,
        )

        return self._build_activity_events(
            session_messages,
        )

    # ========================================================================
    # Metadata
    # ========================================================================

    @property
    def name(
        self,
    ) -> str:
        """
        Return the builder name.
        """

        return self.__class__.__name__

    # ========================================================================
    # Dunder Methods
    # ========================================================================

    def __repr__(
        self,
    ) -> str:
        """
        Return the official representation.
        """

        return f"{self.__class__.__name__}()"

    def __str__(
        self,
    ) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
