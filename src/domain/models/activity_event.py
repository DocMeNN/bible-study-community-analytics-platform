# src/domain/models/activity_event.py

"""
Activity Event Domain Model

Purpose
-------
Represents a validated activity derived from a message.

Canonical Activity Types
------------------------
- Scripture Reading
- Insight
- Discussion
- Announcement
- Done
- Prayer Session

Prayer Session Boundary Rules
-----------------------------
Opening prayer markers and closing prayer markers are not
independent activity types.

They are boundary markers used to identify a Prayer Session.

A Prayer Session:

    Opening Prayer
        ↓
    Prayer Session
        ↓
    Closing Prayer

If a closing prayer marker is not found, the prayer session
is considered closed automatically when the next session begins.

Domain Context
--------------
This platform analyzes participation in an online Bible Study
community. It is not a church service analytics system.

Therefore, the model does not contain:

- Worship
- Message
- Offering
- Tithe
- Generic church-service categories

Notes
-----
- Immutable.
- Derived from a Message.
- Timestamp is obtained from the source message.
- Contains no UI, pandas, or infrastructure dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time

from src.domain.enums.activity_type import ActivityType

from .message import Message


@dataclass(frozen=True, slots=True)
class ActivityEvent:
    """
    Immutable activity event.

    Attributes
    ----------
    activity_type:
        Canonical type of activity.

    source_message:
        Message that generated this activity event.
    """

    activity_type: ActivityType
    source_message: Message

    def __post_init__(self) -> None:
        """Validate the activity event."""

        if not isinstance(
            self.activity_type,
            ActivityType,
        ):
            raise TypeError(
                "activity_type must be an ActivityType.",
            )

        if not isinstance(
            self.source_message,
            Message,
        ):
            raise TypeError(
                "source_message must be a Message.",
            )

    # =========================================================================
    # Derived Properties
    # =========================================================================

    @property
    def timestamp(self) -> datetime:
        """Return the activity timestamp."""

        return self.source_message.timestamp

    @property
    def event_date(self) -> date:
        """Return the activity date."""

        return self.timestamp.date()

    @property
    def event_time(self) -> time:
        """Return the activity time."""

        return self.timestamp.time()

    @property
    def sender(self) -> str:
        """Return the message sender."""

        return self.source_message.sender

    @property
    def line_number(self) -> int:
        """Return the original source line number."""

        return self.source_message.line_number

    @property
    def activity_name(self) -> str:
        """Return the human-readable activity name."""

        return self.activity_type.value

    # =========================================================================
    # Activity Classification
    # =========================================================================

    @property
    def is_scripture_reading(self) -> bool:
        """Return True if this is a Scripture Reading activity."""

        return self.activity_type is ActivityType.SCRIPTURE_READING

    @property
    def is_insight(self) -> bool:
        """Return True if this is an Insight activity."""

        return self.activity_type is ActivityType.INSIGHT

    @property
    def is_discussion(self) -> bool:
        """Return True if this is a Discussion activity."""

        return self.activity_type is ActivityType.DISCUSSION

    @property
    def is_announcement(self) -> bool:
        """Return True if this is an Announcement activity."""

        return self.activity_type is ActivityType.ANNOUNCEMENT

    @property
    def is_done(self) -> bool:
        """Return True if this is a Done activity."""

        return self.activity_type is ActivityType.DONE

    @property
    def is_prayer_session(self) -> bool:
        """Return True if this is a Prayer Session activity."""

        return self.activity_type is ActivityType.PRAYER_SESSION

    # =========================================================================
    # Comparison
    # =========================================================================

    def occurred_before(
        self,
        other: ActivityEvent,
    ) -> bool:
        """Return True if this event occurred before another."""

        return self.timestamp < other.timestamp

    def occurred_after(
        self,
        other: ActivityEvent,
    ) -> bool:
        """Return True if this event occurred after another."""

        return self.timestamp > other.timestamp

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict[str, object]:
        """Return a dictionary representation."""

        return {
            "activity_type": self.activity_type.value,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "line_number": self.line_number,
        }

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __str__(self) -> str:
        """Return a readable representation."""

        return (
            f"ActivityEvent(type='{self.activity_type.value}', time='{self.timestamp}')"
        )
