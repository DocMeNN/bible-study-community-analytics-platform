# tests/presentation/grouping/test_grouping_types.py

from src.presentation.grouping.grouping_types import GroupingPeriod


def test_grouping_period_contains_supported_periods() -> None:
    assert GroupingPeriod.DAY.value == "day"
    assert GroupingPeriod.WEEK.value == "week"
    assert GroupingPeriod.MONTH.value == "month"
    assert GroupingPeriod.FIRST_HALF.value == "first_half"
    assert GroupingPeriod.SECOND_HALF.value == "second_half"
    assert GroupingPeriod.YEAR.value == "year"
