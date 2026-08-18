# src/application/dto/multi_session_analytics_result.py

"""
Multi-Session Analytics Result DTO

Purpose
-------
Represent the application-layer analytics result produced when analytics are
coordinated across multiple Daily Session aggregates.

Architectural Responsibility
----------------------------
This DTO carries aggregated analytics from the Application layer to the
Presentation layer.

The DTO does not:

- perform analytics;
- contain business rules;
- own Streamlit state;
- perform Presentation-layer grouping.

Daily Session remains the atomic Domain aggregate.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MultiSessionAnalyticsResult:
    """
    Immutable analytics result for multiple Daily Sessions.
    """

    session_count: int
    start_date: date | None
    end_date: date | None
    total_participants: int
    total_done_events: int
    total_activity_events: int
