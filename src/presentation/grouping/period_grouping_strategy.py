# src/presentation/grouping/period_grouping_strategy.py

from __future__ import annotations

from datetime import date

from .first_half_grouping_strategy import (
    FirstHalfGroupingStrategy,
)
from .grouping_strategy import (
    GroupBoundary,
    GroupingStrategy,
)
from .grouping_types import GroupingPeriod
from .monthly_grouping_strategy import (
    MonthlyGroupingStrategy,
)
from .second_half_grouping_strategy import (
    SecondHalfGroupingStrategy,
)
from .weekly_grouping_strategy import (
    WeeklyGroupingStrategy,
)
from .yearly_grouping_strategy import (
    YearlyGroupingStrategy,
)


class PeriodGroupingStrategy:
    """
    Presentation-layer grouping strategy dispatcher.
    """

    def __init__(
        self,
        period: GroupingPeriod,
        *,
        week_start_day: int = 6,
    ) -> None:
        self._period = period
        self._strategy = self._build_strategy(
            period=period,
            week_start_day=week_start_day,
        )

    @staticmethod
    def _build_strategy(
        *,
        period: GroupingPeriod,
        week_start_day: int,
    ) -> GroupingStrategy:
        if period is GroupingPeriod.WEEK:
            return WeeklyGroupingStrategy(
                week_start_day=week_start_day,
            )

        if period is GroupingPeriod.MONTH:
            return MonthlyGroupingStrategy()

        if period is GroupingPeriod.FIRST_HALF:
            return FirstHalfGroupingStrategy()

        if period is GroupingPeriod.SECOND_HALF:
            return SecondHalfGroupingStrategy()

        if period is GroupingPeriod.YEAR:
            return YearlyGroupingStrategy()

        raise ValueError(
            f"Unsupported grouping period: {period}.",
        )

    def boundary_for(
        self,
        session_date: date,
    ) -> GroupBoundary:
        """Return the boundary for the configured grouping period."""

        return self._strategy.boundary_for(
            session_date,
        )

    @property
    def period(self) -> GroupingPeriod:
        """Return the configured grouping period."""

        return self._period


__all__ = [
    "PeriodGroupingStrategy",
]
