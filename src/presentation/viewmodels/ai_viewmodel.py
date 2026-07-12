# src/presentation/viewmodels/ai_viewmodel.py

"""
AI ViewModel

Purpose
-------
Transforms presentation data into AI-ready inputs and AI responses
into presentation-ready models.

Responsibilities
----------------
- Prepare prompt inputs.
- Delegate AI generation to the AIController.
- Return presentation-friendly models.

Architectural Rules
-------------------
- Presentation layer only.
- No business logic.
- No analytics.
- No provider communication.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from dataclasses import dataclass
from typing import Any

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation.controllers.ai_controller import AIController

# ============================================================================
# View Models
# ============================================================================


@dataclass(slots=True, frozen=True)
class AIResultViewModel:
    """
    Presentation model representing an AI response.
    """

    title: str
    content: str
    success: bool = True


# ============================================================================
# AI ViewModel
# ============================================================================


class AIViewModel:
    """
    Coordinates AI presentation workflows.
    """

    def __init__(
        self,
        controller: AIController,
    ) -> None:
        self._controller = controller

    # =====================================================================
    # Prompt Builders
    # =====================================================================

    def build_session_information(
        self,
        *,
        session: Any,
    ) -> str:
        """
        Build session information for AI prompts.
        """

        return (
            f"Session Date: {session.session_date}\n"
            f"Attendees: {session.attendee_count}\n"
            f"Attendance Events: {session.attendance_count}\n"
            f"Done Events: {session.done_count}\n"
            f"Activity Events: {session.activity_count}"
        )

    def build_attendance_summary(
        self,
        *,
        attendance: dict[str, Any],
    ) -> str:
        """
        Build attendance summary text.
        """

        lines: list[str] = []

        for key, value in attendance.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)

    def build_activity_summary(
        self,
        *,
        activity: dict[str, Any],
    ) -> str:
        """
        Build activity summary text.
        """

        lines: list[str] = []

        for key, value in activity.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)

    def build_executive_report(
        self,
        *,
        session: Any,
        dashboard_summary: dict[str, Any],
        attendance: dict[str, Any],
        activity: dict[str, Any],
    ) -> str:
        """
        Build a consolidated executive report.
        """

        sections = [
            "SESSION INFORMATION",
            self.build_session_information(
                session=session,
            ),
            "",
            "DASHBOARD SUMMARY",
            str(dashboard_summary),
            "",
            "ATTENDANCE SUMMARY",
            self.build_attendance_summary(
                attendance=attendance,
            ),
            "",
            "ACTIVITY SUMMARY",
            self.build_activity_summary(
                activity=activity,
            ),
        ]

        return "\n".join(sections)

    # =====================================================================
    # AI Generation
    # =====================================================================

    def session_summary(
        self,
        *,
        session_information: str,
        attendance_summary: str,
        activity_summary: str,
    ) -> AIResultViewModel:
        """
        Generate a session summary.
        """

        content = self._controller.generate_session_summary(
            session_information=session_information,
            attendance_summary=attendance_summary,
            activity_summary=activity_summary,
        )

        return AIResultViewModel(
            title="Session Summary",
            content=content,
        )

    def executive_summary(
        self,
        *,
        report: str,
    ) -> AIResultViewModel:
        """
        Generate an executive summary.
        """

        content = self._controller.generate_executive_summary(
            report=report,
        )

        return AIResultViewModel(
            title="Executive Summary",
            content=content,
        )

    def scripture_summary(
        self,
        *,
        scripture: str,
    ) -> AIResultViewModel:
        """
        Generate a scripture summary.
        """

        content = self._controller.generate_scripture_summary(
            scripture=scripture,
        )

        return AIResultViewModel(
            title="Scripture Summary",
            content=content,
        )

    def message_insights(
        self,
        *,
        messages: str,
    ) -> AIResultViewModel:
        """
        Generate message insights.
        """

        content = self._controller.generate_message_insights(
            messages=messages,
        )

        return AIResultViewModel(
            title="Message Insights",
            content=content,
        )

    def trend_analysis(
        self,
        *,
        metrics: str,
    ) -> AIResultViewModel:
        """
        Generate a trend analysis.
        """

        content = self._controller.generate_trend_analysis(
            metrics=metrics,
        )

        return AIResultViewModel(
            title="Trend Analysis",
            content=content,
        )

    def person_of_the_week(
        self,
        *,
        metrics: str,
    ) -> AIResultViewModel:
        """
        Generate a Person of the Week summary.
        """

        content = self._controller.generate_person_of_week(
            metrics=metrics,
        )

        return AIResultViewModel(
            title="Person of the Week",
            content=content,
        )


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "AIResultViewModel",
    "AIViewModel",
]
