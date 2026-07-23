# tests/application/services/test_ai_service.py

"""
AIService Application Service Tests

Purpose:
    Verify application-level orchestration of AI operations.

Coverage:
    - Service construction.
    - Provider injection.
    - Prompt rendering.
    - Request construction.
    - Provider generation.
    - Response processing.
    - Prompt data forwarding.

Rules:
    - Test application orchestration only.
    - Do not duplicate PromptEngine tests.
    - Do not duplicate AIRequestBuilder tests.
    - Do not duplicate ResponseEngine tests.
    - Do not test individual provider implementations.

Author:
    Me

Created:
    July 2026
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.application.services.ai_service import AIService
from src.config.ai_config import AIConfig, AIProvider
from src.domain.ai.interfaces import AIProvider as AIProviderInterface
from src.domain.ai.models import AIRequest, AIResponse
from src.domain.ai.prompts import PromptTemplate

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def config() -> AIConfig:
    """Return a representative AI configuration."""

    return AIConfig(
        provider=AIProvider.OLLAMA,
        model="llama3.2:3b",
        api_key=None,
        base_url="http://localhost:11434",
        temperature=0.3,
        max_tokens=1024,
        timeout=60,
    )


@pytest.fixture
def provider() -> Mock:
    """Return a mocked AI provider."""

    return Mock(
        spec=AIProviderInterface,
    )


@pytest.fixture
def service(
    config: AIConfig,
    provider: Mock,
) -> AIService:
    """Return an AIService with an injected provider."""

    return AIService(
        config=config,
        provider=provider,
    )


@pytest.fixture
def template() -> PromptTemplate:
    """Return a supported prompt template."""

    return PromptTemplate.SCRIPTURE_SUMMARY


@pytest.fixture
def response() -> AIResponse:
    """Return a representative AI response."""

    return AIResponse(
        content="Generated response",
        provider=AIProvider.OLLAMA.value,
        model="llama3.2:3b",
    )


# ============================================================================
# Construction
# ============================================================================


class TestAIServiceConstruction:
    """Test AIService construction."""

    def test_service_can_be_constructed(
        self,
        config: AIConfig,
        provider: Mock,
    ) -> None:
        """AIService can be constructed with an injected provider."""

        service = AIService(
            config=config,
            provider=provider,
        )

        assert isinstance(
            service,
            AIService,
        )

    def test_injected_provider_is_used(
        self,
        config: AIConfig,
        provider: Mock,
        template: PromptTemplate,
        response: AIResponse,
    ) -> None:
        """Injected provider is used during generation."""

        provider.generate.return_value = response

        service = AIService(
            config=config,
            provider=provider,
        )

        service.generate(
            template=template,
            scripture="John 3:16",
        )

        provider.generate.assert_called_once()


# ============================================================================
# Generate
# ============================================================================


class TestGenerate:
    """Test AI response generation."""

    def test_generate_returns_provider_response(
        self,
        service: AIService,
        provider: Mock,
        template: PromptTemplate,
        response: AIResponse,
    ) -> None:
        """generate returns the provider response."""

        provider.generate.return_value = response

        result = service.generate(
            template=template,
            scripture="John 3:16",
        )

        assert result is response

    def test_generate_calls_provider_once(
        self,
        service: AIService,
        provider: Mock,
        template: PromptTemplate,
        response: AIResponse,
    ) -> None:
        """generate delegates to the provider exactly once."""

        provider.generate.return_value = response

        service.generate(
            template=template,
            scripture="John 3:16",
        )

        provider.generate.assert_called_once()

    def test_generate_passes_request_to_provider(
        self,
        service: AIService,
        provider: Mock,
        template: PromptTemplate,
        response: AIResponse,
    ) -> None:
        """generate passes a built AIRequest to the provider."""

        provider.generate.return_value = response

        service.generate(
            template=template,
            scripture="John 3:16",
        )

        request = provider.generate.call_args.args[0]

        assert isinstance(
            request,
            AIRequest,
        )


# ============================================================================
# Process
# ============================================================================


class TestProcess:
    """Test complete AI response processing."""

    def test_process_returns_processed_text(
        self,
        service: AIService,
        provider: Mock,
        template: PromptTemplate,
        response: AIResponse,
    ) -> None:
        """process returns the processed response text."""

        provider.generate.return_value = response

        result = service.process(
            template=template,
            scripture="John 3:16",
        )

        assert isinstance(
            result,
            str,
        )

    def test_process_generates_before_processing(
        self,
        service: AIService,
        provider: Mock,
        template: PromptTemplate,
        response: AIResponse,
    ) -> None:
        """process obtains a provider response before processing it."""

        provider.generate.return_value = response

        result = service.process(
            template=template,
            scripture="John 3:16",
        )

        assert result == "Generated response"


# ============================================================================
# Prompt Data
# ============================================================================


class TestPromptData:
    """Test prompt data forwarding."""

    def test_prompt_variables_are_forwarded(
        self,
        service: AIService,
        provider: Mock,
        template: PromptTemplate,
        response: AIResponse,
    ) -> None:
        """Prompt data is forwarded through the generation workflow."""

        provider.generate.return_value = response

        service.generate(
            template=template,
            scripture="John 3:16",
        )

        request = provider.generate.call_args.args[0]

        assert "John 3:16" in request.prompt


# ============================================================================
# Dunder Methods
# ============================================================================


class TestDunderMethods:
    """Test AIService dunder behaviour."""

    def test_default_object_representation_exists(
        self,
        service: AIService,
    ) -> None:
        """AIService has a standard object representation."""

        assert "AIService" in repr(service)
