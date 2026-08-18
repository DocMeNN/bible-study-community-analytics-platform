# src/presentation/dto/multi_session_overview.py

"""
Multi-Session Overview Presentation DTO

Purpose
-------
Provides a Presentation-layer representation of aggregated
multi-session analytics.

Responsibilities
----------------
- Adapt Application-layer analytics for Presentation.
- Remain immutable.
- Contain no business logic.
- Contain no analytics calculations.

Architecture
------------
MultiSessionAnalyticsResult
            ?
DashboardViewModel
            ?
MultiSessionOverview
            ?
Presentation Components
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from dataclasses import dataclass
from datetime import date

# ============================================================================
# Presentation DTO
# ============================================================================


@dataclass(frozen=True, slots=True)
class MultiSessionOverview:
    """
    Presentation DTO representing an overview of multiple Daily Sessions.

    This DTO is Presentation-only.

    It is populated by DashboardViewModel from the
    Application-layer MultiSessionAnalyticsResult.
    """

    session_count: int

    start_date: date | None

    end_date: date | None

    participant_count: int

    done_events: int

    activity_events: int


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "MultiSessionOverview",
]
