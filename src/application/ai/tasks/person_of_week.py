# src/application/ai/tasks/person_of_the_week.py

"""
Person of the Week AI Task

Purpose:
    Generates AI-powered recognition of outstanding contributors.

Architecture:
    Application Layer - AI Tasks

Dependencies:
    AI Service
    Domain AI Prompt Templates

Notes:
    This task coordinates the person-of-the-week workflow.

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


class PersonOfTheWeekTask:
    """
    AI task for identifying outstanding contributors.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize the person-of-the-week task.

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
        Identify outstanding contributors from participation metrics.

        Parameters
        ----------
        metrics:
            Participation metrics to analyze.

        Returns
        -------
        str
            AI-generated contributor recognition.
        """

        return self._ai_service.process(
            template=PromptTemplate.PERSON_OF_THE_WEEK,
            metrics=metrics,
        )
