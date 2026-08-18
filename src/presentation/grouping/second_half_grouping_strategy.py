# src/presentation/grouping/second_half_grouping_strategy.py

from __future__ import annotations

from datetime import date

from .grouping_strategy import GroupBoundary


class SecondHalfGroupingStrategy:
    """
    Groups Daily Sessions from July through December.
    """

    def boundary_for(
        self,
        session_date: date,
    ) -> GroupBoundary:
        """
        Return the second-half-of-year boundary containing the date.
        """

        return GroupBoundary(
            start_date=date(
                session_date.year,
                7,
                1,
            ),
            end_date=date(
                session_date.year,
                12,
                31,
            ),
        )


__all__ = [
    "SecondHalfGroupingStrategy",
]
