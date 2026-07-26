# src/domain/models/session_collection.py

"""
Session Collection Domain Model

Purpose
-------
Represents an immutable collection of detected study sessions.

Responsibilities
----------------
- Store multiple Session aggregates.
- Provide collection-level session information.
- Preserve chronological session ordering.
- Remain technology independent.

Domain Rules
------------
- A SessionCollection contains zero or more Session aggregates.
- Sessions are stored as an immutable tuple.
- Sessions are ordered chronologically by session date.
- The collection does not build or detect sessions.
- Session detection and construction remain separate responsibilities.

Notes
-----
- Immutable.
- Contains no UI, pandas, Streamlit, or infrastructure dependencies.

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
from dataclasses import dataclass
from datetime import date

# ============================================================================
# Local Imports
# ============================================================================
from .session import Session

# ============================================================================
# Session Collection
# ============================================================================


@dataclass(frozen=True, slots=True)
class SessionCollection:
    """
    Immutable collection of Session aggregates.
    """

    sessions: tuple[Session, ...]

    def __post_init__(self) -> None:
        """Validate and normalize the session collection."""

        if not isinstance(
            self.sessions,
            tuple,
        ):
            raise TypeError(
                "sessions must be a tuple of Session instances.",
            )

        for session in self.sessions:

            if not isinstance(
                session,
                Session,
            ):
                raise TypeError(
                    "sessions must contain only Session instances.",
                )

        ordered_sessions = tuple(
            sorted(
                self.sessions,
                key=lambda session: session.session_date,
            )
        )

        object.__setattr__(
            self,
            "sessions",
            ordered_sessions,
        )

    # =========================================================================
    # Collection Information
    # =========================================================================

    @property
    def count(self) -> int:
        """Return the number of sessions."""

        return len(
            self.sessions,
        )

    @property
    def is_empty(self) -> bool:
        """Return True if the collection contains no sessions."""

        return not self.sessions

    @property
    def has_sessions(self) -> bool:
        """Return True if at least one session exists."""

        return bool(
            self.sessions,
        )

    # =========================================================================
    # Timeline
    # =========================================================================

    @property
    def first_session(self) -> Session | None:
        """Return the earliest session."""

        if not self.sessions:
            return None

        return self.sessions[0]

    @property
    def last_session(self) -> Session | None:
        """Return the latest session."""

        if not self.sessions:
            return None

        return self.sessions[-1]

    @property
    def session_dates(self) -> tuple[date, ...]:
        """Return session dates in chronological order."""

        return tuple(
            session.session_date
            for session in self.sessions
        )

    @property
    def first_date(self) -> date | None:
        """Return the date of the first session."""

        if self.first_session is None:
            return None

        return self.first_session.session_date

    @property
    def last_date(self) -> date | None:
        """Return the date of the last session."""

        if self.last_session is None:
            return None

        return self.last_session.session_date

    # =========================================================================
    # Session Access
    # =========================================================================

    def get_session(
        self,
        session_date: date,
    ) -> Session | None:
        """
        Return the session occurring on the supplied date.
        """

        for session in self.sessions:

            if session.session_date == session_date:
                return session

        return None

    def contains_date(
        self,
        session_date: date,
    ) -> bool:
        """
        Return True if a session exists on the supplied date.
        """

        return self.get_session(
            session_date,
        ) is not None

    # =========================================================================
    # Iteration
    # =========================================================================

    def __iter__(self):
        """Iterate through sessions chronologically."""

        return iter(
            self.sessions,
        )

    def __len__(self) -> int:
        """Return the number of sessions."""

        return self.count

    def __getitem__(
        self,
        index: int,
    ) -> Session:
        """Return a session by index."""

        return self.sessions[index]

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "count": self.count,
            "is_empty": self.is_empty,
            "session_dates": self.session_dates,
            "first_date": self.first_date,
            "last_date": self.last_date,
            "sessions": tuple(
                session.to_dict()
                for session in self.sessions
            ),
        }

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __str__(self) -> str:
        """Return a readable representation."""

        return (
            "SessionCollection("
            f"count={self.count}, "
            f"first_date='{self.first_date}', "
            f"last_date='{self.last_date}')"
        )
