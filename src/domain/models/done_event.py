# src/domain/models/done_event.py

"""
Done Event Domain Model

Purpose:
    Represents a validated "Done" acknowledgement derived from a
    WhatsApp message.

Responsibilities:
    - Represent a member's acknowledgement of the Scripture Reading.
    - Preserve the originating message.
    - Provide Done-related business behaviour.
    - Remain technology independent.

Notes:
    - Immutable.
    - Derived from a Message.
    - Timestamp is obtained from the source message.
    - Contains no UI, pandas or infrastructure dependencies.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time

from .message import Message


@dataclass(frozen=True, slots=True)
class DoneEvent:
    """
    Immutable Done acknowledgement.

    Attributes:
        attendee:
            Member who acknowledged the Scripture Reading.

        source_message:
            Message that generated this event.
    """

    attendee: str
    source_message: Message

    def __post_init__(self) -> None:
        """Validate the Done event."""

        attendee = self.attendee.strip()

        if not attendee:
            raise ValueError("attendee cannot be empty.")

        if not isinstance(self.source_message, Message):
            raise TypeError("source_message must be a Message.")

        object.__setattr__(self, "attendee", attendee)

    # ------------------------------------------------------------------
    # Derived Properties
    # ------------------------------------------------------------------

    @property
    def timestamp(self) -> datetime:
        """Return the acknowledgement timestamp."""
        return self.source_message.timestamp

    @property
    def event_date(self) -> date:
        """Return the acknowledgement date."""
        return self.timestamp.date()

    @property
    def event_time(self) -> time:
        """Return the acknowledgement time."""
        return self.timestamp.time()

    @property
    def sender(self) -> str:
        """Return the original sender."""
        return self.source_message.sender

    @property
    def line_number(self) -> int:
        """Return the original line number."""
        return self.source_message.line_number

    @property
    def attendee_name(self) -> str:
        """Return the attendee name."""
        return self.attendee

    @property
    def message_text(self) -> str:
        """Return the original message text."""
        return self.source_message.content

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def occurred_before(self, other: "DoneEvent") -> bool:
        """Return True if this event occurred before another."""
        return self.timestamp < other.timestamp

    def occurred_after(self, other: "DoneEvent") -> bool:
        """Return True if this event occurred after another."""
        return self.timestamp > other.timestamp

    def same_attendee(self, other: "DoneEvent") -> bool:
        """Return True if both events belong to the same attendee."""
        return self.attendee.casefold() == other.attendee.casefold()

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "attendee": self.attendee,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "line_number": self.line_number,
            "message": self.message_text,
        }

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a readable representation."""

        return f"DoneEvent(attendee='{self.attendee}', time='{self.timestamp}')"
