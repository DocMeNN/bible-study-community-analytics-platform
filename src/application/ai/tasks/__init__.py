# src/application/ai/tasks/__init__.py

"""
AI Tasks Package

Purpose:
    Contains application-level AI workflows that represent
    specific business capabilities.

Architecture:
    Application Layer - AI Tasks

Notes:
    AI Tasks coordinate domain/application data with the
    AI Service layer.

    They do not:
        - communicate directly with AI providers,
        - manage prompts,
        - parse AI responses.

Available Tasks:
    - SessionSummaryTask
    - ScriptureSummaryTask
    - MessageInsightsTask
    - ExecutiveSummaryTask
    - TrendAnalysisTask
    - PersonOfWeekTask

Author: Me
"""

from src.application.ai.tasks.executive_summary import (
    ExecutiveSummaryTask,
)
from src.application.ai.tasks.message_insights import (
    MessageInsightsTask,
)
from src.application.ai.tasks.person_of_week import (
    PersonOfWeekTask,
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
    "PersonOfWeekTask",
    "ScriptureSummaryTask",
    "SessionSummaryTask",
    "TrendAnalysisTask",
]
