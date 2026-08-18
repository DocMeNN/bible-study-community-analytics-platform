# src/presentation/grouping/grouping_configuration.py

from __future__ import annotations

from dataclasses import dataclass

from .grouping_types import GroupingPeriod


@dataclass(frozen=True, slots=True)
class GroupingConfiguration:
    """
    Presentation-layer configuration for session grouping.
    """

    period: GroupingPeriod = GroupingPeriod.WEEK
    week_start_day: int = 6

    def __post_init__(self) -> None:
        """Validate grouping configuration."""

        if not isinstance(
            self.period,
            GroupingPeriod,
        ):
            raise TypeError(
                "period must be a GroupingPeriod.",
            )

        if not 0 <= self.week_start_day <= 6:
            raise ValueError(
                "week_start_day must be between 0 and 6.",
            )

    @classmethod
    def daily(
        cls,
    ) -> GroupingConfiguration:
        """Return daily grouping configuration."""

        return cls(
            period=GroupingPeriod.DAY,
        )

    @classmethod
    def weekly(
        cls,
        week_start_day: int = 6,
    ) -> GroupingConfiguration:
        """Return weekly grouping configuration."""

        return cls(
            period=GroupingPeriod.WEEK,
            week_start_day=week_start_day,
        )

    @classmethod
    def monthly(
        cls,
    ) -> GroupingConfiguration:
        """Return monthly grouping configuration."""

        return cls(
            period=GroupingPeriod.MONTH,
        )

    @classmethod
    def first_half(
        cls,
    ) -> GroupingConfiguration:
        """Return first-half-of-year grouping configuration."""

        return cls(
            period=GroupingPeriod.FIRST_HALF,
        )

    @classmethod
    def second_half(
        cls,
    ) -> GroupingConfiguration:
        """Return second-half-of-year grouping configuration."""

        return cls(
            period=GroupingPeriod.SECOND_HALF,
        )

    @classmethod
    def yearly(
        cls,
    ) -> GroupingConfiguration:
        """Return yearly grouping configuration."""

        return cls(
            period=GroupingPeriod.YEAR,
        )


__all__ = [
    "GroupingConfiguration",
]
