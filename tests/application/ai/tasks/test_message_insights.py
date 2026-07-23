# tests/application/ai/tasks/test_message_insights.py

"""
MessageInsightsTask Application AI Task Tests

Purpose:
    Verify orchestration of message insight generation.

Coverage:
    - Task construction.
    - AI service delegation.
    - Correct prompt template selection.
    - Message forwarding.
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

from src.application.ai.tasks.message_insights import (
    MessageInsightsTask,
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
) -> MessageInsightsTask:
    """Return a configured MessageInsightsTask."""

    return MessageInsightsTask(
        ai_service=ai_service,
    )


# ============================================================================
# Construction
# ============================================================================


class TestMessageInsightsTaskConstruction:
    """Test MessageInsightsTask construction."""

    def test_task_can_be_constructed(
        self,
        ai_service: Mock,
    ) -> None:
        """Task can be constructed with an AI service."""

        task = MessageInsightsTask(
            ai_service=ai_service,
        )

        assert isinstance(
            task,
            MessageInsightsTask,
        )


# ============================================================================
# Execution
# ============================================================================


class TestExecution:
    """Test message insights execution."""

    def test_execute_returns_ai_service_result(
        self,
        task: MessageInsightsTask,
        ai_service: Mock,
    ) -> None:
        """execute returns the AI service result."""

        ai_service.process.return_value = "Generated message insights"

        result = task.execute(
            messages="Alice: I learned something today.",
        )

        assert result == "Generated message insights"

    def test_execute_calls_ai_service_once(
        self,
        task: MessageInsightsTask,
        ai_service: Mock,
    ) -> None:
        """execute delegates to the AI service exactly once."""

        ai_service.process.return_value = "Generated message insights"

        task.execute(
            messages="Alice: I learned something today.",
        )

        ai_service.process.assert_called_once()

    def test_execute_uses_message_insights_template(
        self,
        task: MessageInsightsTask,
        ai_service: Mock,
    ) -> None:
        """execute uses the message insights prompt template."""

        ai_service.process.return_value = "Generated message insights"

        task.execute(
            messages="Alice: I learned something today.",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["template"] is PromptTemplate.MESSAGE_INSIGHTS

    def test_execute_forwards_messages(
        self,
        task: MessageInsightsTask,
        ai_service: Mock,
    ) -> None:
        """execute forwards messages to the AI service."""

        messages = (
            "Alice: I learned something today.\n"
            "Bob: The discussion was helpful."
        )

        ai_service.process.return_value = "Generated message insights"

        task.execute(
            messages=messages,
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["messages"] == messages

    def test_execute_preserves_empty_message_text(
        self,
        task: MessageInsightsTask,
        ai_service: Mock,
    ) -> None:
        """execute forwards empty message text unchanged."""

        ai_service.process.return_value = "Generated message insights"

        task.execute(
            messages="",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["messages"] == ""


# ============================================================================
# Validation
# ============================================================================


class TestExecutionValidation:
    """Test execution argument requirements."""

    def test_messages_are_required(
        self,
        task: MessageInsightsTask,
    ) -> None:
        """execute requires messages."""

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
        task: MessageInsightsTask,
    ) -> None:
        """Task has a standard object representation."""

        assert "MessageInsightsTask" in repr(task)
