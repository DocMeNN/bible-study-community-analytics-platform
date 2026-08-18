# tests/presentation/grouping/test_session_grouping_service.py

from datetime import date

from src.domain.models.session import Session
from src.domain.models.session_collection import SessionCollection
from src.presentation.grouping.first_half_grouping_strategy import (
    FirstHalfGroupingStrategy,
)
from src.presentation.grouping.grouping_types import GroupingPeriod
from src.presentation.grouping.period_grouping_strategy import (
    PeriodGroupingStrategy,
)
from src.presentation.grouping.second_half_grouping_strategy import (
    SecondHalfGroupingStrategy,
)
from src.presentation.grouping.session_grouping_service import (
    SessionGroupingService,
)
from src.presentation.grouping.weekly_grouping_strategy import (
    WeeklyGroupingStrategy,
)


def test_session_collection_is_grouped_by_week() -> None:
    session_collection = SessionCollection(
        sessions=(
            Session(
                session_date=date(2023, 1, 10),
            ),
            Session(
                session_date=date(2023, 1, 1),
            ),
            Session(
                session_date=date(2023, 1, 3),
            ),
            Session(
                session_date=date(2023, 1, 8),
            ),
        ),
    )

    service = SessionGroupingService(
        strategy=WeeklyGroupingStrategy(),
        period=GroupingPeriod.WEEK,
    )

    groups = service.group(
        session_collection,
    )

    assert len(groups) == 2

    assert groups[0].start_date == date(2023, 1, 1)
    assert groups[0].end_date == date(2023, 1, 7)
    assert groups[0].session_dates == (
        date(2023, 1, 1),
        date(2023, 1, 3),
    )

    assert groups[1].start_date == date(2023, 1, 8)
    assert groups[1].end_date == date(2023, 1, 14)
    assert groups[1].session_dates == (
        date(2023, 1, 8),
        date(2023, 1, 10),
    )


def test_grouping_does_not_mutate_session_collection() -> None:
    session_collection = SessionCollection(
        sessions=(
            Session(
                session_date=date(2023, 1, 3),
            ),
            Session(
                session_date=date(2023, 1, 1),
            ),
        ),
    )

    original_dates = session_collection.session_dates

    service = SessionGroupingService(
        strategy=WeeklyGroupingStrategy(),
        period=GroupingPeriod.WEEK,
    )

    service.group(
        session_collection,
    )

    assert session_collection.session_dates == original_dates


def test_session_collection_is_grouped_by_month() -> None:
    session_collection = SessionCollection(
        sessions=(
            Session(
                session_date=date(2023, 1, 31),
            ),
            Session(
                session_date=date(2023, 2, 1),
            ),
        ),
    )

    service = SessionGroupingService(
        strategy=PeriodGroupingStrategy(
            period=GroupingPeriod.MONTH,
        ),
        period=GroupingPeriod.MONTH,
    )

    groups = service.group(
        session_collection,
    )

    assert len(groups) == 2

    assert groups[0].start_date == date(2023, 1, 1)
    assert groups[0].end_date == date(2023, 1, 31)

    assert groups[1].start_date == date(2023, 2, 1)
    assert groups[1].end_date == date(2023, 2, 28)


def test_session_collection_is_grouped_by_first_half() -> None:
    session_collection = SessionCollection(
        sessions=(
            Session(
                session_date=date(2023, 1, 1),
            ),
            Session(
                session_date=date(2023, 6, 30),
            ),
            Session(
                session_date=date(2024, 1, 1),
            ),
        ),
    )

    service = SessionGroupingService(
        strategy=PeriodGroupingStrategy(
            period=GroupingPeriod.FIRST_HALF,
        ),
        period=GroupingPeriod.FIRST_HALF,
    )

    groups = service.group(
        session_collection,
    )

    assert len(groups) == 2

    assert groups[0].start_date == date(2023, 1, 1)
    assert groups[0].end_date == date(2023, 6, 30)
    assert groups[0].session_dates == (
        date(2023, 1, 1),
        date(2023, 6, 30),
    )

    assert groups[1].start_date == date(2024, 1, 1)
    assert groups[1].end_date == date(2024, 6, 30)
    assert groups[1].session_dates == (date(2024, 1, 1),)


def test_session_collection_is_grouped_by_second_half() -> None:
    session_collection = SessionCollection(
        sessions=(
            Session(
                session_date=date(2023, 7, 1),
            ),
            Session(
                session_date=date(2023, 12, 31),
            ),
            Session(
                session_date=date(2024, 7, 1),
            ),
        ),
    )

    service = SessionGroupingService(
        strategy=PeriodGroupingStrategy(
            period=GroupingPeriod.SECOND_HALF,
        ),
        period=GroupingPeriod.SECOND_HALF,
    )

    groups = service.group(
        session_collection,
    )

    assert len(groups) == 2

    assert groups[0].start_date == date(2023, 7, 1)
    assert groups[0].end_date == date(2023, 12, 31)
    assert groups[0].session_dates == (
        date(2023, 7, 1),
        date(2023, 12, 31),
    )

    assert groups[1].start_date == date(2024, 7, 1)
    assert groups[1].end_date == date(2024, 12, 31)
    assert groups[1].session_dates == (date(2024, 7, 1),)


def test_session_collection_is_grouped_by_year() -> None:
    session_collection = SessionCollection(
        sessions=(
            Session(
                session_date=date(2022, 12, 31),
            ),
            Session(
                session_date=date(2023, 1, 1),
            ),
        ),
    )

    service = SessionGroupingService(
        strategy=PeriodGroupingStrategy(
            period=GroupingPeriod.YEAR,
        ),
        period=GroupingPeriod.YEAR,
    )

    groups = service.group(
        session_collection,
    )

    assert len(groups) == 2

    assert groups[0].start_date == date(2022, 1, 1)
    assert groups[0].end_date == date(2022, 12, 31)

    assert groups[1].start_date == date(2023, 1, 1)
    assert groups[1].end_date == date(2023, 12, 31)


def test_direct_first_half_strategy_groups_first_half_dates() -> None:
    session_collection = SessionCollection(
        sessions=(
            Session(
                session_date=date(2023, 1, 1),
            ),
            Session(
                session_date=date(2023, 6, 30),
            ),
        ),
    )

    service = SessionGroupingService(
        strategy=FirstHalfGroupingStrategy(),
        period=GroupingPeriod.FIRST_HALF,
    )

    groups = service.group(
        session_collection,
    )

    assert len(groups) == 1

    assert groups[0].session_dates == (
        date(2023, 1, 1),
        date(2023, 6, 30),
    )


def test_direct_second_half_strategy_groups_second_half_dates() -> None:
    session_collection = SessionCollection(
        sessions=(
            Session(
                session_date=date(2023, 7, 1),
            ),
            Session(
                session_date=date(2023, 12, 31),
            ),
        ),
    )

    service = SessionGroupingService(
        strategy=SecondHalfGroupingStrategy(),
        period=GroupingPeriod.SECOND_HALF,
    )

    groups = service.group(
        session_collection,
    )

    assert len(groups) == 1

    assert groups[0].session_dates == (
        date(2023, 7, 1),
        date(2023, 12, 31),
    )
