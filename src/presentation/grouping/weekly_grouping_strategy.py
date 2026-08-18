# src/presentation/grouping/weekly_grouping_strategy.py

from __future__ import annotations

from datetime import date, timedelta

from .grouping_strategy import GroupBoundary


class WeeklyGroupingStrategy:
    """
    Groups dates into calendar weeks.

    Default calendar:
        Sunday ? Saturday
    """

    def __init__(
        self,
        week_start_day: int = 6,
    ) -> None:
        """
        Initialize the weekly grouping strategy.

        Python weekday convention:
            Monday = 0
            Sunday = 6
        """

        if not 0 <= week_start_day <= 6:
            raise ValueError(
                "week_start_day must be between 0 and 6.",
            )

        self._week_start_day = week_start_day

    def boundary_for(
        self,
        session_date: date,
    ) -> GroupBoundary:
        """
        Return the calendar-week boundary containing the date.
        """

        days_since_start = (session_date.weekday() - self._week_start_day) % 7

        start_date = session_date - timedelta(
            days=days_since_start,
        )

        end_date = start_date + timedelta(
            days=6,
        )

        return GroupBoundary(
            start_date=start_date,
            end_date=end_date,
        )


__all__ = [
    "WeeklyGroupingStrategy",
]
