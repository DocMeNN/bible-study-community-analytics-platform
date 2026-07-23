# src/application/ai/tasks/__init__.py

"""
AI Task Package

Purpose:
    Exposes application-level AI task coordinators.

Architecture:
    Application Layer - AI Tasks

Author: Me
"""

from __future__ import annotations

from src.application.ai.tasks.executive_summary import (
    ExecutiveSummaryTask,
)
from src.application.ai.tasks.message_insights import (
    MessageInsightsTask,
)
from src.application.ai.tasks.person_of_week import (
    PersonOfTheWeekTask,
)
from src.application.ai.tasks.scripture_summary import (
    ScriptureSummaryTask,
)
from src.application.ai.tasks.session_summary import (
    SessionSummaryTask,
)
from src.application.ai.tasks.trend_analysis import (
    TrendAnalysisTask,
)

__all__ = [
    "ExecutiveSummaryTask",
    "MessageInsightsTask",
    "PersonOfTheWeekTask",
    "ScriptureSummaryTask",
    "SessionSummaryTask",
    "TrendAnalysisTask",
]
