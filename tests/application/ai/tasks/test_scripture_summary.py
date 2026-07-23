# tests/application/ai/tasks/test_scripture_summary.py

"""
ScriptureSummaryTask Application AI Task Tests

Purpose:
    Verify orchestration of scripture summary generation.

Coverage:
    - Task construction.
    - AI service delegation.
    - Correct prompt template selection.
    - Scripture forwarding.
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

from src.application.ai.tasks.scripture_summary import (
    ScriptureSummaryTask,
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
) -> ScriptureSummaryTask:
    """Return a configured ScriptureSummaryTask."""

    return ScriptureSummaryTask(
        ai_service=ai_service,
    )


# ============================================================================
# Construction
# ============================================================================


class TestScriptureSummaryTaskConstruction:
    """Test ScriptureSummaryTask construction."""

    def test_task_can_be_constructed(
        self,
        ai_service: Mock,
    ) -> None:
        """Task can be constructed with an AI service."""

        task = ScriptureSummaryTask(
            ai_service=ai_service,
        )

        assert isinstance(
            task,
            ScriptureSummaryTask,
        )


# ============================================================================
# Execution
# ============================================================================


class TestExecution:
    """Test scripture summary execution."""

    def test_execute_returns_ai_service_result(
        self,
        task: ScriptureSummaryTask,
        ai_service: Mock,
    ) -> None:
        """execute returns the AI service result."""

        ai_service.process.return_value = "Generated scripture summary"

        result = task.execute(
            scripture="John 3:16",
        )

        assert result == "Generated scripture summary"

    def test_execute_calls_ai_service_once(
        self,
        task: ScriptureSummaryTask,
        ai_service: Mock,
    ) -> None:
        """execute delegates to the AI service exactly once."""

        ai_service.process.return_value = "Generated scripture summary"

        task.execute(
            scripture="John 3:16",
        )

        ai_service.process.assert_called_once()

    def test_execute_uses_scripture_summary_template(
        self,
        task: ScriptureSummaryTask,
        ai_service: Mock,
    ) -> None:
        """execute uses the scripture summary prompt template."""

        ai_service.process.return_value = "Generated scripture summary"

        task.execute(
            scripture="John 3:16",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["template"] is PromptTemplate.SCRIPTURE_SUMMARY

    def test_execute_forwards_scripture(
        self,
        task: ScriptureSummaryTask,
        ai_service: Mock,
    ) -> None:
        """execute forwards the scripture to the AI service."""

        ai_service.process.return_value = "Generated scripture summary"

        task.execute(
            scripture="John 3:16",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["scripture"] == "John 3:16"

    def test_execute_preserves_multiline_scripture(
        self,
        task: ScriptureSummaryTask,
        ai_service: Mock,
    ) -> None:
        """execute preserves multiline scripture input."""

        scripture = (
            "John 3:16\n"
            "For God so loved the world..."
        )

        ai_service.process.return_value = "Generated scripture summary"

        task.execute(
            scripture=scripture,
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["scripture"] == scripture


# ============================================================================
# Validation
# ============================================================================


class TestExecutionValidation:
    """Test execution argument requirements."""

    def test_scripture_is_required(
        self,
        task: ScriptureSummaryTask,
    ) -> None:
        """execute requires scripture."""

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
        task: ScriptureSummaryTask,
    ) -> None:
        """Task has a standard object representation."""

        assert "ScriptureSummaryTask" in repr(task)
