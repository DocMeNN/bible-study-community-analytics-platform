# src/application/ai/tasks/executive_summary.py

"""
Executive Summary AI Task

Purpose:
    Generates AI-powered executive summaries from
    aggregated ministry reports.

Architecture:
    Application Layer - AI Tasks

Dependencies:
    AI Service
    Domain AI Prompt Templates

Notes:
    This task coordinates the executive summary workflow.

    It does not:
        - communicate with AI providers,
        - render prompts directly,
        - parse responses.

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.application.services.ai_service import AIService
from src.domain.ai.prompts import PromptTemplate


class ExecutiveSummaryTask:
    """
    AI task for generating executive summaries.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize the executive summary task.

        Parameters
        ----------
        ai_service:
            AI service responsible for execution.
        """

        self._ai_service = ai_service

    def execute(
        self,
        *,
        report: str,
    ) -> str:
        """
        Generate an executive summary.

        Parameters
        ----------
        report:
            Aggregated report data.

        Returns
        -------
        str
            AI-generated executive summary.
        """

        return self._ai_service.process(
            template=PromptTemplate.EXECUTIVE_SUMMARY,
            report=report,
        )
