# tests/application/ai/tasks/test_person_of_week.py

"""
PersonOfTheWeekTask Application AI Task Tests

Purpose:
    Verify orchestration of contributor recognition generation.

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

from src.application.ai.tasks.person_of_week import (
    PersonOfTheWeekTask,
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
) -> PersonOfTheWeekTask:
    """Return a configured PersonOfTheWeekTask."""

    return PersonOfTheWeekTask(
        ai_service=ai_service,
    )


# ============================================================================
# Construction
# ============================================================================


class TestPersonOfTheWeekTaskConstruction:
    """Test PersonOfTheWeekTask construction."""

    def test_task_can_be_constructed(
        self,
        ai_service: Mock,
    ) -> None:
        """Task can be constructed with an AI service."""

        task = PersonOfTheWeekTask(
            ai_service=ai_service,
        )

        assert isinstance(
            task,
            PersonOfTheWeekTask,
        )


# ============================================================================
# Execution
# ============================================================================


class TestExecution:
    """Test person-of-the-week execution."""

    def test_execute_returns_ai_service_result(
        self,
        task: PersonOfTheWeekTask,
        ai_service: Mock,
    ) -> None:
        """execute returns the AI service result."""

        ai_service.process.return_value = "Outstanding contributors identified"

        result = task.execute(
            metrics="Alice: 12 participations\nBob: 10 participations",
        )

        assert result == "Outstanding contributors identified"

    def test_execute_calls_ai_service_once(
        self,
        task: PersonOfTheWeekTask,
        ai_service: Mock,
    ) -> None:
        """execute delegates to the AI service exactly once."""

        ai_service.process.return_value = "Outstanding contributors identified"

        task.execute(
            metrics="Alice: 12 participations",
        )

        ai_service.process.assert_called_once()

    def test_execute_uses_person_of_the_week_template(
        self,
        task: PersonOfTheWeekTask,
        ai_service: Mock,
    ) -> None:
        """execute uses the person-of-the-week prompt template."""

        ai_service.process.return_value = "Outstanding contributors identified"

        task.execute(
            metrics="Alice: 12 participations",
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["template"] is PromptTemplate.PERSON_OF_THE_WEEK

    def test_execute_forwards_metrics(
        self,
        task: PersonOfTheWeekTask,
        ai_service: Mock,
    ) -> None:
        """execute forwards metrics to the AI service."""

        metrics = (
            "Alice: 12 participations\n"
            "Bob: 10 participations"
        )

        ai_service.process.return_value = "Outstanding contributors identified"

        task.execute(
            metrics=metrics,
        )

        call_kwargs = ai_service.process.call_args.kwargs

        assert call_kwargs["metrics"] == metrics

    def test_execute_preserves_multiline_metrics(
        self,
        task: PersonOfTheWeekTask,
        ai_service: Mock,
    ) -> None:
        """execute preserves multiline metrics."""

        metrics = (
            "Participant | Sessions | Activities\n"
            "Alice | 12 | 35\n"
            "Bob | 10 | 28"
        )

        ai_service.process.return_value = "Outstanding contributors identified"

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
        task: PersonOfTheWeekTask,
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
        task: PersonOfTheWeekTask,
    ) -> None:
        """Task has a standard object representation."""

        assert "PersonOfTheWeekTask" in repr(task)
