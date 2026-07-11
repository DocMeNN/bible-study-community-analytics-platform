# src/application/ai/tasks/person_of_week.py

"""
Person of the Week AI Task

Purpose:
    Generates AI-powered recognition summaries for outstanding
    contributors.

Architecture:
    Application Layer - AI Tasks

Dependencies:
    AI Service
    Domain AI Prompt Templates

Notes:
    This task explains contributor metrics.

    It does not:
        - calculate rankings,
        - determine winners,
        - communicate with AI providers,
        - render prompts directly,
        - parse responses.

    Ranking logic remains within the analytics/domain layer.

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.application.services.ai_service import AIService
from src.domain.ai.prompts import PromptTemplate


class PersonOfWeekTask:
    """
    AI task for generating contributor recognition summaries.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize the person of the week task.

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
        Generate a person of the week explanation.

        Parameters
        ----------
        metrics:
            Contributor performance metrics.

        Returns
        -------
        str
            AI-generated recognition summary.
        """

        return self._ai_service.process(
            template=PromptTemplate.PERSON_OF_THE_WEEK,
            metrics=metrics,
        )
