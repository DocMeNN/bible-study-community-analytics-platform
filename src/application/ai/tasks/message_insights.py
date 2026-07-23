# src/application/ai/tasks/message_insights.py

"""
Message Insights AI Task

Purpose:
    Generates AI-powered insights from discussion messages.

Architecture:
    Application Layer - AI Tasks

Dependencies:
    AI Service
    Domain AI Prompt Templates

Notes:
    This task coordinates the message insights workflow.

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


class MessageInsightsTask:
    """
    AI task for generating insights from discussion messages.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize the message insights task.

        Parameters
        ----------
        ai_service:
            AI service responsible for execution.
        """

        self._ai_service = ai_service

    def execute(
        self,
        *,
        messages: str,
    ) -> str:
        """
        Generate insights from discussion messages.

        Parameters
        ----------
        messages:
            Discussion messages to analyze.

        Returns
        -------
        str
            AI-generated message insights.
        """

        return self._ai_service.process(
            template=PromptTemplate.MESSAGE_INSIGHTS,
            messages=messages,
        )
