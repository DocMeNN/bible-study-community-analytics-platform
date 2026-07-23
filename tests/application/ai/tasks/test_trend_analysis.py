# tests/application/ai/tasks/test_trend_analysis.py

"""
TrendAnalysisTask Application AI Task Tests

Purpose:
    Verify orchestration of trend analysis generation.

Coverage:
    - Task construction.
    - AI service delegation.
    - Correct prompt template selection.
    - Metrics forwarding.
    - Result propagation.
    - Required argument behaviour.

Rules:
    - Test task orchestration only.
    - Do not duplicate AIService tests.
    - Do not duplicate PromptEngine tests.
    - Do not test AI provider implementations.

Author:
    Me

Created:
    July 2026
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.application.ai.tasks.trend_analysis import (
    TrendAnalysisTask,
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
) -> TrendAnalysisTask:
    """Return a configured TrendAnalysisTask."""

    return TrendAnalysisTask(
        ai_service=ai_service,
    )


# ============================================================================
# Construction
# ============================================================================


class TestTrendAnalysisTaskConstruction:
    """Test TrendAnalysisTask construction."""

    def test_task_can_be_constructed(
        self,
        ai_service: Mock,
    ) -> None:
        """Task can be constructed with an AI service."""

        task = TrendAnalysisTask(
            ai_service=ai_service,
        )

        assert isinstance(
            task,
            TrendAnalysisTask,
        )


# ============================================================================
# Execution
# ============================================================================


class TestExecution:
    """Test trend analysis execution."""

    def test_execute_returns_ai_service_result(
        self,
        task: TrendAnalysisTask,
        ai_service: Mock,
    ) -> None:
        """execute returns the AI service result."""

        ai_service.process.return_value = "Generated trend analysis"

        result = task.execute(
            metrics="Week 1: 20 participants\nWeek 2: 25 participants",
        )

        assert result == "Generated trend analysis"

    def test_execute_calls_ai_service_once(
        self,
        task: TrendAnalysisTask,
        ai_service: Mock,
    ) -> None:
        """execute delegates to the AI service exactly once."""

        ai_service.process.return_value = "Generated trend analysis"

        task.execute(
            metrics="Week 1: 20 participants",
        )

        ai_service.process.assert_called_once()

    def test_execute_uses_trend_analysis_template(
        self,
        task: TrendAnalysisTask,
        ai_service: Mock,
    ) -> None:
        """execute uses the trend analysis prompt template."""

        ai_service.process.return_value = "Generated trend analysis"

        task.execute(
            metrics="Week 1: 20 participants",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["template"] is PromptTemplate.TREND_ANALYSIS

    def test_execute_forwards_metrics(
        self,
        task: TrendAnalysisTask,
        ai_service: Mock,
    ) -> None:
        """execute forwards metrics to the AI service."""

        metrics = (
            "Week 1: 20 participants\n"
            "Week 2: 25 participants"
        )

        ai_service.process.return_value = "Generated trend analysis"

        task.execute(
            metrics=metrics,
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["metrics"] == metrics

    def test_execute_preserves_multiline_metrics(
        self,
        task: TrendAnalysisTask,
        ai_service: Mock,
    ) -> None:
        """execute preserves multiline metrics."""

        metrics = (
            "Period | Attendance | Activities\n"
            "Week 1 | 20 | 45\n"
            "Week 2 | 25 | 62"
        )

        ai_service.process.return_value = "Generated trend analysis"

        task.execute(
            metrics=metrics,
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["metrics"] == metrics


# ============================================================================
# Validation
# ============================================================================


class TestExecutionValidation:
    """Test execution argument requirements."""

    def test_metrics_are_required(
        self,
        task: TrendAnalysisTask,
    ) -> None:
        """execute requires metrics."""

        with pytest.raises(
            TypeError,
        ):
            task.execute()


# ============================================================================
# Dunder Methods
# ============================================================================


class TestDunderMethods:
    """Test task dunder behaviour."""

    def test_default_object_representation_exists(
        self,
        task: TrendAnalysisTask,
    ) -> None:
        """Task has a standard object representation."""

        assert "TrendAnalysisTask" in repr(task)
