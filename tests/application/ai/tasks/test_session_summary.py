# tests/application/ai/tasks/test_session_summary.py

"""
Session Summary AI Task Tests

Purpose:
    Verify application-level orchestration of the SessionSummaryTask.

Coverage:
    - Task construction.
    - AI service dependency injection.
    - Prompt template selection.
    - AI service delegation.
    - Session summary data forwarding.
    - Return value propagation.

Rules:
    - Test task orchestration only.
    - Do not duplicate AIService tests.
    - Do not duplicate prompt rendering tests.
    - Do not test AI provider implementations.

Author:
    Me

Created:
    July 2026
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.application.ai.tasks.session_summary import SessionSummaryTask
from src.application.services.ai_service import AIService
from src.domain.ai.prompts import PromptTemplate

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def ai_service() -> Mock:
    """Return a mocked AI service."""

    return Mock(
        spec=AIService,
    )


@pytest.fixture
def task(
    ai_service: Mock,
) -> SessionSummaryTask:
    """Return a SessionSummaryTask with an injected AI service."""

    return SessionSummaryTask(
        ai_service=ai_service,
    )


# ============================================================================
# Construction
# ============================================================================


class TestSessionSummaryTaskConstruction:
    """Test SessionSummaryTask construction."""

    def test_task_can_be_constructed(
        self,
        ai_service: Mock,
    ) -> None:
        """SessionSummaryTask can be constructed."""

        task = SessionSummaryTask(
            ai_service=ai_service,
        )

        assert isinstance(
            task,
            SessionSummaryTask,
        )


# ============================================================================
# Execution
# ============================================================================


class TestSessionSummaryTaskExecution:
    """Test session summary execution."""

    def test_execute_returns_ai_service_result(
        self,
        task: SessionSummaryTask,
        ai_service: Mock,
    ) -> None:
        """execute returns the result from AIService.process."""

        expected_result = "Generated session summary"

        ai_service.process.return_value = expected_result

        result = task.execute(
            session_information="Session information",
            attendance_summary="Attendance summary",
            activity_summary="Activity summary",
        )

        assert result == expected_result

    def test_execute_calls_ai_service_once(
        self,
        task: SessionSummaryTask,
        ai_service: Mock,
    ) -> None:
        """execute delegates to AIService exactly once."""

        ai_service.process.return_value = "Generated summary"

        task.execute(
            session_information="Session information",
            attendance_summary="Attendance summary",
            activity_summary="Activity summary",
        )

        ai_service.process.assert_called_once()

    def test_execute_uses_session_summary_template(
        self,
        task: SessionSummaryTask,
        ai_service: Mock,
    ) -> None:
        """execute selects the SESSION_SUMMARY prompt template."""

        ai_service.process.return_value = "Generated summary"

        task.execute(
            session_information="Session information",
            attendance_summary="Attendance summary",
            activity_summary="Activity summary",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["template"] is PromptTemplate.SESSION_SUMMARY


# ============================================================================
# Data Forwarding
# ============================================================================


class TestSessionSummaryDataForwarding:
    """Test session summary data forwarding."""

    def test_session_information_is_forwarded(
        self,
        task: SessionSummaryTask,
        ai_service: Mock,
    ) -> None:
        """Session information is forwarded to AIService."""

        ai_service.process.return_value = "Generated summary"

        task.execute(
            session_information="Session information",
            attendance_summary="Attendance summary",
            activity_summary="Activity summary",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["session_information"] == "Session information"

    def test_attendance_summary_is_forwarded(
        self,
        task: SessionSummaryTask,
        ai_service: Mock,
    ) -> None:
        """Attendance summary is forwarded to AIService."""

        ai_service.process.return_value = "Generated summary"

        task.execute(
            session_information="Session information",
            attendance_summary="Attendance summary",
            activity_summary="Activity summary",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["attendance_summary"] == "Attendance summary"

    def test_activity_summary_is_forwarded(
        self,
        task: SessionSummaryTask,
        ai_service: Mock,
    ) -> None:
        """Activity summary is forwarded to AIService."""

        ai_service.process.return_value = "Generated summary"

        task.execute(
            session_information="Session information",
            attendance_summary="Attendance summary",
            activity_summary="Activity summary",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["activity_summary"] == "Activity summary"


# ============================================================================
# Dunder Methods
# ============================================================================


class TestDunderMethods:
    """Test SessionSummaryTask dunder behaviour."""

    def test_default_object_representation_exists(
        self,
        task: SessionSummaryTask,
    ) -> None:
        """SessionSummaryTask has a standard object representation."""

        assert "SessionSummaryTask" in repr(task)
