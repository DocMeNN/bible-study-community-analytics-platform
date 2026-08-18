# src/presentation/grouping/daily_grouping_strategy.py

from __future__ import annotations

from datetime import date

from .grouping_strategy import GroupBoundary


class DailyGroupingStrategy:
    """
    Groups each Daily Session into its own calendar day.
    """

    def boundary_for(
        self,
        session_date: date,
    ) -> GroupBoundary:
        """
        Return a one-day boundary for the session date.
        """

        return GroupBoundary(
            start_date=session_date,
            end_date=session_date,
        )


__all__ = [
    "DailyGroupingStrategy",
]
