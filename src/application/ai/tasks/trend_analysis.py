# src/application/ai/tasks/trend_analysis.py

"""
Trend Analysis AI Task

Purpose:
    Generates AI-powered interpretations of attendance
    and engagement trends.

Architecture:
    Application Layer - AI Tasks

Dependencies:
    AI Service
    Domain AI Prompt Templates

Notes:
    This task coordinates the trend analysis workflow.

    It does not:
        - calculate analytics,
        - communicate with AI providers,
        - render prompts directly,
        - parse responses.

    Analytics calculations remain inside the domain
    analytics layer.

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.application.services.ai_service import AIService
from src.domain.ai.prompts import PromptTemplate


class TrendAnalysisTask:
    """
    AI task for interpreting analytics trends.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize the trend analysis task.

        Parameters
        ----------
        ai_service:
            AI service responsible for execution.
        """

        self._ai_service = ai_service

    def execute(
        self,
        *,
        metrics: str,
    ) -> str:
        """
        Generate a trend analysis.

        Parameters
        ----------
        metrics:
            Historical analytics metrics.

        Returns
        -------
        str
            AI-generated trend analysis.
        """

        return self._ai_service.process(
            template=PromptTemplate.TREND_ANALYSIS,
            metrics=metrics,
        )
