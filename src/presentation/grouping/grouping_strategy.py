# src/presentation/grouping/grouping_strategy.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True, slots=True)
class GroupBoundary:
    """
    Immutable presentation grouping boundary.
    """

    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        """Validate the grouping boundary."""

        if self.end_date < self.start_date:
            raise ValueError(
                "end_date cannot be earlier than start_date.",
            )


class GroupingStrategy(Protocol):
    """
    Contract for Presentation-layer grouping strategies.
    """

    def boundary_for(
        self,
        session_date: date,
    ) -> GroupBoundary:
        """
        Return the grouping boundary for a session date.
        """
        ...


__all__ = [
    "GroupBoundary",
    "GroupingStrategy",
]
