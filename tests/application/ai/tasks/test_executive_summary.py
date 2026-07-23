# tests/application/ai/tasks/test_executive_summary.py

"""
Executive Summary AI Task Tests

Purpose:
    Verify application-level orchestration of executive summary
    generation.

Coverage:
    - Task construction.
    - AI service delegation.
    - Correct prompt template selection.
    - Report data forwarding.
    - Result propagation.

Rules:
    - Test application orchestration only.
    - Do not duplicate AIService tests.
    - Do not test prompt rendering.
    - Do not test response parsing.
    - Do not test AI provider implementations.

Author:
    Me

Created:
    July 2026
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.application.ai.tasks.executive_summary import (
    ExecutiveSummaryTask,
)
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
) -> ExecutiveSummaryTask:
    """Return an executive summary task."""

    return ExecutiveSummaryTask(
        ai_service=ai_service,
    )


@pytest.fixture
def report() -> str:
    """Return representative report data."""

    return (
        "Period: January 2026\n"
        "Sessions: 31\n"
        "Participants: 145\n"
        "Average attendance: 82"
    )


# ============================================================================
# Construction
# ============================================================================


class TestExecutiveSummaryTaskConstruction:
    """Test ExecutiveSummaryTask construction."""

    def test_task_can_be_constructed(
        self,
        ai_service: Mock,
    ) -> None:
        """ExecutiveSummaryTask can be constructed."""

        task = ExecutiveSummaryTask(
            ai_service=ai_service,
        )

        assert isinstance(
            task,
            ExecutiveSummaryTask,
        )


# ============================================================================
# Execution
# ============================================================================


class TestExecute:
    """Test executive summary execution."""

    def test_execute_returns_ai_service_result(
        self,
        task: ExecutiveSummaryTask,
        ai_service: Mock,
        report: str,
    ) -> None:
        """execute returns the result from the AI service."""

        ai_service.process.return_value = "Executive summary"

        result = task.execute(
            report=report,
        )

        assert result == "Executive summary"

    def test_execute_calls_ai_service_once(
        self,
        task: ExecutiveSummaryTask,
        ai_service: Mock,
        report: str,
    ) -> None:
        """execute delegates to the AI service exactly once."""

        ai_service.process.return_value = "Executive summary"

        task.execute(
            report=report,
        )

        ai_service.process.assert_called_once()

    def test_execute_uses_executive_summary_template(
        self,
        task: ExecutiveSummaryTask,
        ai_service: Mock,
        report: str,
    ) -> None:
        """execute uses the executive summary prompt template."""

        ai_service.process.return_value = "Executive summary"

        task.execute(
            report=report,
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["template"] is PromptTemplate.EXECUTIVE_SUMMARY

    def test_execute_forwards_report(
        self,
        task: ExecutiveSummaryTask,
        ai_service: Mock,
        report: str,
    ) -> None:
        """execute forwards the report to the AI service."""

        ai_service.process.return_value = "Executive summary"

        task.execute(
            report=report,
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["report"] == report


# ============================================================================
# Dunder Methods
# ============================================================================


class TestDunderMethods:
    """Test ExecutiveSummaryTask dunder behaviour."""

    def test_default_object_representation_exists(
        self,
        task: ExecutiveSummaryTask,
    ) -> None:
        """ExecutiveSummaryTask has a standard object representation."""

        assert "ExecutiveSummaryTask" in repr(task)
