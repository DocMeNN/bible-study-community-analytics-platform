# src/presentation/controllers/ai_controller.py

"""
AI Controller

Purpose
-------
Coordinates AI requests initiated by the Presentation layer.

Responsibilities
----------------
- Bridge the Presentation and Application layers.
- Delegate AI requests to the appropriate application task.
- Return presentation-ready AI results.

Architectural Rules
-------------------
- No business logic.
- No analytics.
- No prompt rendering.
- No provider communication.
- No response parsing.
"""

from __future__ import annotations

# ============================================================================
# Local Imports
# ============================================================================
from src.application.ai.tasks.executive_summary import ExecutiveSummaryTask
from src.application.ai.tasks.message_insights import MessageInsightsTask
from src.application.ai.tasks.person_of_week import PersonOfTheWeekTask
from src.application.ai.tasks.scripture_summary import ScriptureSummaryTask
from src.application.ai.tasks.session_summary import SessionSummaryTask
from src.application.ai.tasks.trend_analysis import TrendAnalysisTask
from src.application.services.ai_service import AIService


class AIController:
    """
    Coordinates AI operations for the Presentation layer.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize the AI controller.
        """

        self._session_summary_task = SessionSummaryTask(
            ai_service=ai_service,
        )

        self._scripture_summary_task = ScriptureSummaryTask(
            ai_service=ai_service,
        )

        self._message_insights_task = MessageInsightsTask(
            ai_service=ai_service,
        )

        self._executive_summary_task = ExecutiveSummaryTask(
            ai_service=ai_service,
        )

        self._trend_analysis_task = TrendAnalysisTask(
            ai_service=ai_service,
        )

        self._person_of_week_task = PersonOfTheWeekTask(
            ai_service=ai_service,
        )

    # =========================================================================
    # Session Summary
    # =========================================================================

    def generate_session_summary(
        self,
        *,
        session_information: str,
        attendance_summary: str,
        activity_summary: str,
    ) -> str:
        """
        Generate an AI session summary.
        """

        result = self._session_summary_task.execute(
            session_information=session_information,
            attendance_summary=attendance_summary,
            activity_summary=activity_summary,
        )

        return str(result)

    # =========================================================================
    # Scripture Summary
    # =========================================================================

    def generate_scripture_summary(
        self,
        *,
        scripture: str,
    ) -> str:
        """
        Generate an AI scripture summary.
        """

        result = self._scripture_summary_task.execute(
            scripture=scripture,
        )

        return str(result)

    # =========================================================================
    # Message Insights
    # =========================================================================

    def generate_message_insights(
        self,
        *,
        messages: str,
    ) -> str:
        """
        Generate AI insights from discussion messages.
        """

        result = self._message_insights_task.execute(
            messages=messages,
        )

        return str(result)

    # =========================================================================
    # Executive Summary
    # =========================================================================

    def generate_executive_summary(
        self,
        *,
        report: str,
    ) -> str:
        """
        Generate an executive summary.
        """

        result = self._executive_summary_task.execute(
            report=report,
        )

        return str(result)

    # =========================================================================
    # Trend Analysis
    # =========================================================================

    def generate_trend_analysis(
        self,
        *,
        metrics: str,
    ) -> str:
        """
        Generate an AI trend analysis.
        """

        result = self._trend_analysis_task.execute(
            metrics=metrics,
        )

        return str(result)

    # =========================================================================
    # Person of the Week
    # =========================================================================

    def generate_person_of_week(
        self,
        *,
        metrics: str,
    ) -> str:
        """
        Generate an AI explanation for Person of the Week.
        """

        result = self._person_of_week_task.execute(
            metrics=metrics,
        )

        return str(result)
