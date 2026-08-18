# src/presentation/grouping/grouping_types.py

from __future__ import annotations

from enum import Enum


class GroupingPeriod(str, Enum):
    """Supported Presentation-layer grouping periods."""

    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    FIRST_HALF = "first_half"
    SECOND_HALF = "second_half"
    YEAR = "year"


__all__ = [
    "GroupingPeriod",
]
