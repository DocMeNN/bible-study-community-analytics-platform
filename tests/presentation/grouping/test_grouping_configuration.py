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


def test_weekly_factory_creates_weekly_configuration() -> None:
    configuration = GroupingConfiguration.weekly()

    assert configuration.period is GroupingPeriod.WEEK
    assert configuration.week_start_day == 6


def test_invalid_week_start_day_raises_error() -> None:
    with pytest.raises(ValueError):
        GroupingConfiguration(
            week_start_day=7,
        )
