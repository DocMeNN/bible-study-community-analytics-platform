# src/presentation/models/session_group.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from src.domain.models.session import Session


@dataclass(frozen=True, slots=True)
class SessionGroup:
    """
    Immutable Presentation-layer grouping of Daily Sessions.
    """

    start_date: date
    end_date: date
    sessions: tuple[Session, ...]

    def __post_init__(self) -> None:
        """Validate and normalize the SessionGroup."""

        if self.end_date < self.start_date:
            raise ValueError(
                "end_date cannot be earlier than start_date.",
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

    @property
    def count(self) -> int:
        """Return the number of Daily Sessions in the group."""

        return len(self.sessions)

    @property
    def is_empty(self) -> bool:
        """Return True when the group contains no sessions."""

        return not self.sessions

    @property
    def session_dates(self) -> tuple[date, ...]:
        """Return contained Daily Session dates."""

        return tuple(session.session_date for session in self.sessions)

    def get_session(
        self,
        session_date: date,
    ) -> Session | None:
        """Return the Daily Session for a date."""

        for session in self.sessions:
            if session.session_date == session_date:
                return session

        return None

    def __iter__(self):
        """Iterate through Daily Sessions chronologically."""

        return iter(
            self.sessions,
        )

    def __len__(self) -> int:
        """Return the number of Daily Sessions."""

        return self.count

    def __getitem__(
        self,
        index: int,
    ) -> Session:
        """Return a Daily Session by index."""

        return self.sessions[index]


__all__ = [
    "SessionGroup",
]
