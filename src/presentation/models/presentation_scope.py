# src/presentation/models/presentation_scope.py

"""
Presentation Scope Model

Purpose
-------
Defines the single active Presentation Scope maintained by
the Presentation layer.

ADR-003
-------
The Presentation layer maintains exactly one active
PresentationScope.

A PresentationScope represents:

    GroupingConfiguration
            +
    SessionGroup
            +
    Selected Daily Session

The Domain remains centered on Daily Session.

The Presentation layer decides only how Sessions are
presented and navigated.

Architectural Rules
-------------------
- No business logic.
- No analytics.
- No parsing.
- No infrastructure access.
- No domain calculations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from src.domain.models.session import Session
from src.presentation.grouping.grouping_configuration import (
    GroupingConfiguration,
)
from src.presentation.models.session_group import SessionGroup


@dataclass(frozen=True, slots=True)
class PresentationScope:
    """
    Represents the active Presentation Scope.

    A Presentation Scope contains:

    - Active grouping configuration.
    - Selected presentation group.
    - Selected Daily Session.

    The selected Daily Session remains the atomic
    analytical target.
    """

    configuration: GroupingConfiguration

    session_group: SessionGroup

    session: Session | None = None

    def __post_init__(self) -> None:
        """
        Validate Presentation Scope construction.
        """

        if not isinstance(
            self.configuration,
            GroupingConfiguration,
        ):
            raise TypeError(
                "configuration must be a GroupingConfiguration.",
            )

        if not isinstance(
            self.session_group,
            SessionGroup,
        ):
            raise TypeError(
                "session_group must be a SessionGroup.",
            )

        if self.session is not None and not isinstance(
            self.session,
            Session,
        ):
            raise TypeError(
                "session must be a Session or None.",
            )

    @property
    def period(self):
        """
        Return the active presentation period.
        """

        return self.configuration.period

    @property
    def start_date(self) -> date:
        """
        Return scope start date.
        """

        return self.session_group.start_date

    @property
    def end_date(self) -> date:
        """
        Return scope end date.
        """

        return self.session_group.end_date

    @property
    def sessions(self) -> tuple[Session, ...]:
        """
        Return Daily Sessions contained in this scope.
        """

        return self.session_group.sessions

    @property
    def session_count(self) -> int:
        """
        Return number of Daily Sessions.
        """

        return self.session_group.count

    @property
    def selected_session_date(self) -> date | None:
        """
        Return selected Daily Session date.
        """

        if self.session is None:
            return None

        return self.session.session_date

    @property
    def is_daily(self) -> bool:
        """
        Return True when scope represents Daily view.
        """

        return self.configuration.period.value == "daily"

    @property
    def is_grouped(self) -> bool:
        """
        Return True when scope represents grouped view.
        """

        return not self.is_daily


__all__ = [
    "PresentationScope",
]
