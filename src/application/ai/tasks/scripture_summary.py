# src/application/ai/tasks/scripture_summary.py

"""
Scripture Summary AI Task

Purpose:
    Generates AI-powered summaries of scripture passages.

Architecture:
    Application Layer - AI Tasks

Dependencies:
    AI Service
    Domain AI Prompt Templates

Notes:
    This task coordinates the scripture summary workflow.

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


class ScriptureSummaryTask:
    """
    AI task for generating scripture summaries.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize the scripture summary task.

        Parameters
        ----------
        ai_service:
            AI service responsible for execution.
        """

        self._ai_service = ai_service

    def execute(
        self,
        *,
        scripture: str,
    ) -> str:
        """
        Generate a scripture summary.

        Parameters
        ----------
        scripture:
            Scripture passage or reference to summarize.

        Returns
        -------
        str
            AI-generated scripture summary.
        """

        return self._ai_service.process(
            template=PromptTemplate.SCRIPTURE_SUMMARY,
            scripture=scripture,
        )
