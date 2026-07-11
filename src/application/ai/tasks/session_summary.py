# src/application/ai/tasks/session_summary.py

"""
Session Summary AI Task

Purpose:
    Generates AI-powered summaries for ministry sessions.

Architecture:
    Application Layer - AI Tasks

Dependencies:
    AI Service
    Domain AI Prompt Templates

Notes:
    This task coordinates the session summary workflow.
    It prepares session data, selects the correct prompt,
    and delegates generation to the AI pipeline.

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


class SessionSummaryTask:
    """
    AI task for generating session summaries.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        """
        Initialize the session summary task.

        Parameters
        ----------
        ai_service:
            AI service responsible for execution.
        """

        self._ai_service = ai_service

    def execute(
        self,
        *,
        session_information: str,
        attendance_summary: str,
        activity_summary: str,
    ) -> str:
        """
        Generate a session summary.

        Parameters
        ----------
        session_information:
            Session details.

        attendance_summary:
            Attendance information.

        activity_summary:
            Activity information.

        Returns
        -------
        str
            AI-generated session summary.
        """

        return self._ai_service.process(
            template=PromptTemplate.SESSION_SUMMARY,
            session_information=session_information,
            attendance_summary=attendance_summary,
            activity_summary=activity_summary,
        )
