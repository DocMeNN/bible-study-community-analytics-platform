# tests/presentation/grouping/test_grouping_configuration.py

import pytest

from src.presentation.grouping.grouping_configuration import (
    GroupingConfiguration,
)
from src.presentation.grouping.grouping_types import GroupingPeriod


def test_default_configuration_is_weekly_sunday_to_saturday() -> None:
    configuration = GroupingConfiguration()

    assert configuration.period is GroupingPeriod.WEEK
    assert configuration.week_start_day == 6


def test_daily_factory_creates_daily_configuration() -> None:
    configuration = GroupingConfiguration.daily()

    assert configuration.period is GroupingPeriod.DAY


def test_weekly_factory_creates_weekly_configuration() -> None:
    configuration = GroupingConfiguration.weekly()

    assert configuration.period is GroupingPeriod.WEEK
    assert configuration.week_start_day == 6


def test_monthly_factory_creates_monthly_configuration() -> None:
    configuration = GroupingConfiguration.monthly()

    assert configuration.period is GroupingPeriod.MONTH


def test_first_half_factory_creates_first_half_configuration() -> None:
    configuration = GroupingConfiguration.first_half()

    assert configuration.period is GroupingPeriod.FIRST_HALF


def test_second_half_factory_creates_second_half_configuration() -> None:
    configuration = GroupingConfiguration.second_half()

    assert configuration.period is GroupingPeriod.SECOND_HALF


def test_yearly_factory_creates_yearly_configuration() -> None:
    configuration = GroupingConfiguration.yearly()

    assert configuration.period is GroupingPeriod.YEAR


def test_invalid_week_start_day_raises_error() -> None:
    with pytest.raises(ValueError):
        GroupingConfiguration(
            week_start_day=7,
        )
