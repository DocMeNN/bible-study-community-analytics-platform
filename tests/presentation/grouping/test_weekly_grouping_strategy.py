# tests/presentation/grouping/test_weekly_grouping_strategy.py

from datetime import date

from src.presentation.grouping.weekly_grouping_strategy import (
    WeeklyGroupingStrategy,
)


def test_sunday_starts_a_new_week() -> None:
    strategy = WeeklyGroupingStrategy()

    boundary = strategy.boundary_for(
        date(2023, 1, 1),
    )

    assert boundary.start_date == date(2023, 1, 1)
    assert boundary.end_date == date(2023, 1, 7)


def test_midweek_date_belongs_to_previous_sunday_week() -> None:
    strategy = WeeklyGroupingStrategy()

    boundary = strategy.boundary_for(
        date(2023, 1, 4),
    )

    assert boundary.start_date == date(2023, 1, 1)
    assert boundary.end_date == date(2023, 1, 7)


def test_saturday_ends_the_week() -> None:
    strategy = WeeklyGroupingStrategy()

    boundary = strategy.boundary_for(
        date(2023, 1, 7),
    )

    assert boundary.start_date == date(2023, 1, 1)
    assert boundary.end_date == date(2023, 1, 7)


def test_year_boundary_is_handled_correctly() -> None:
    strategy = WeeklyGroupingStrategy()

    boundary = strategy.boundary_for(
        date(2022, 12, 31),
    )

    assert boundary.start_date == date(2022, 12, 25)
    assert boundary.end_date == date(2022, 12, 31)
