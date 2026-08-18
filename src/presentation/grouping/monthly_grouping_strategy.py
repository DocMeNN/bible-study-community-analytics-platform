# src/presentation/grouping/monthly_grouping_strategy.py

from __future__ import annotations

import calendar
from datetime import date

from .grouping_strategy import GroupBoundary


class MonthlyGroupingStrategy:
    """
    Groups Daily Sessions by calendar month.
    """

    def boundary_for(
        self,
        session_date: date,
    ) -> GroupBoundary:
        """
        Return the calendar-month boundary containing the date.
        """

        start_date = date(
            session_date.year,
            session_date.month,
            1,
        )

        last_day = calendar.monthrange(
            session_date.year,
            session_date.month,
        )[1]

        end_date = date(
            session_date.year,
            session_date.month,
            last_day,
        )

        return GroupBoundary(
            start_date=start_date,
            end_date=end_date,
        )


__all__ = [
    "MonthlyGroupingStrategy",
]
