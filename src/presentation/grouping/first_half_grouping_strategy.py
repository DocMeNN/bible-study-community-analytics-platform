# src/presentation/grouping/first_half_grouping_strategy.py

from __future__ import annotations

from datetime import date

from .grouping_strategy import GroupBoundary


class FirstHalfGroupingStrategy:
    """
    Groups Daily Sessions from January through June.
    """

    def boundary_for(
        self,
        session_date: date,
    ) -> GroupBoundary:
        """
        Return the first-half-of-year boundary containing the date.
        """

        return GroupBoundary(
            start_date=date(
                session_date.year,
                1,
                1,
            ),
            end_date=date(
                session_date.year,
                6,
                30,
            ),
        )


__all__ = [
    "FirstHalfGroupingStrategy",
]
