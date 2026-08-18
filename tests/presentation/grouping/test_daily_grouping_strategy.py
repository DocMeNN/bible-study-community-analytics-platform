# tests/presentation/grouping/test_daily_grouping_strategy.py

from datetime import date

from src.presentation.grouping.daily_grouping_strategy import (
    DailyGroupingStrategy,
)


def test_daily_grouping_boundary_contains_only_the_session_date() -> None:
    strategy = DailyGroupingStrategy()

    boundary = strategy.boundary_for(
        date(2023, 1, 15),
    )

    assert boundary.start_date == date(2023, 1, 15)
    assert boundary.end_date == date(2023, 1, 15)


def test_daily_grouping_works_at_start_of_year() -> None:
    strategy = DailyGroupingStrategy()

    boundary = strategy.boundary_for(
        date(2023, 1, 1),
    )

    assert boundary.start_date == date(2023, 1, 1)
    assert boundary.end_date == date(2023, 1, 1)


def test_daily_grouping_works_at_end_of_year() -> None:
    strategy = DailyGroupingStrategy()

    boundary = strategy.boundary_for(
        date(2023, 12, 31),
    )

    assert boundary.start_date == date(2023, 12, 31)
    assert boundary.end_date == date(2023, 12, 31)


def test_daily_grouping_handles_leap_day() -> None:
    strategy = DailyGroupingStrategy()

    boundary = strategy.boundary_for(
        date(2024, 2, 29),
    )

    assert boundary.start_date == date(2024, 2, 29)
    assert boundary.end_date == date(2024, 2, 29)
