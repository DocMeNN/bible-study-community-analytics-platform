# src/presentation/grouping/yearly_grouping_strategy.py

from __future__ import annotations

from datetime import date

from .grouping_strategy import GroupBoundary


class YearlyGroupingStrategy:
    """
    Groups Daily Sessions by calendar year.
    """

    def boundary_for(
        self,
        session_date: date,
    ) -> GroupBoundary:
        """
        Return the calendar-year boundary containing the date.
        """

        return GroupBoundary(
            start_date=date(
                session_date.year,
                1,
                1,
            ),
            end_date=date(
                session_date.year,
                12,
                31,
            ),
        )


__all__ = [
    "YearlyGroupingStrategy",
]
