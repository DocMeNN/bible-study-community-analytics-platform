# tests/presentation/grouping/test_period_grouping_strategy.py

from datetime import date

import pytest

from src.presentation.grouping.grouping_types import GroupingPeriod
from src.presentation.grouping.period_grouping_strategy import (
    PeriodGroupingStrategy,
)


def test_week_period_returns_week_boundary() -> None:
    strategy = PeriodGroupingStrategy(
        GroupingPeriod.WEEK,
    )

    boundary = strategy.boundary_for(
        date(2023, 1, 4),
    )

    assert boundary.start_date == date(2023, 1, 1)
    assert boundary.end_date == date(2023, 1, 7)


def test_month_period_returns_month_boundary() -> None:
    strategy = PeriodGroupingStrategy(
        GroupingPeriod.MONTH,
    )

    boundary = strategy.boundary_for(
        date(2023, 2, 15),
    )

    assert boundary.start_date == date(2023, 2, 1)
    assert boundary.end_date == date(2023, 2, 28)


def test_first_half_period_returns_first_half_boundary() -> None:
    strategy = PeriodGroupingStrategy(
        GroupingPeriod.FIRST_HALF,
    )

    boundary = strategy.boundary_for(
        date(2023, 3, 15),
    )

    assert boundary.start_date == date(2023, 1, 1)
    assert boundary.end_date == date(2023, 6, 30)


def test_second_half_period_returns_second_half_boundary() -> None:
    strategy = PeriodGroupingStrategy(
        GroupingPeriod.SECOND_HALF,
    )

    boundary = strategy.boundary_for(
        date(2023, 9, 15),
    )

    assert boundary.start_date == date(2023, 7, 1)
    assert boundary.end_date == date(2023, 12, 31)


def test_year_period_returns_year_boundary() -> None:
    strategy = PeriodGroupingStrategy(
        GroupingPeriod.YEAR,
    )

    boundary = strategy.boundary_for(
        date(2023, 7, 15),
    )

    assert boundary.start_date == date(2023, 1, 1)
    assert boundary.end_date == date(2023, 12, 31)


def test_period_is_exposed() -> None:
    strategy = PeriodGroupingStrategy(
        GroupingPeriod.MONTH,
    )

    assert strategy.period is GroupingPeriod.MONTH


def test_day_period_is_not_yet_supported() -> None:
    with pytest.raises(ValueError):
        PeriodGroupingStrategy(
            GroupingPeriod.DAY,
        )
