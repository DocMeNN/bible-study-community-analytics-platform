# tests/infrastructure/ai/providers/test_base_provider.py

from src.config.ai_config import AIConfig, AIProvider
from src.domain.ai.models import AIRequest, AIResponse
from src.infrastructure.ai.providers.base_provider import (
    BaseAIProvider,
)


def _config() -> AIConfig:
    return AIConfig(
        provider=AIProvider.OLLAMA,
        model="test-model",
        api_key=None,
        base_url=None,
        temperature=0.3,
        max_tokens=1024,
        timeout=60,
    )


class ConcreteTestProvider(BaseAIProvider):
    """
    Minimal concrete provider used to test shared base functionality.
    """

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        return AIResponse(
            content="test response",
            provider="test",
            model=self.model,
        )


def test_base_provider_exposes_configuration() -> None:
    config = _config()

    provider = ConcreteTestProvider(config)

    assert provider.config == config
    assert provider.model == config.model
    assert provider.timeout == config.timeout
    assert provider.temperature == config.temperature
    assert provider.max_tokens == config.max_tokens


def test_require_text_returns_clean_text() -> None:
    assert BaseAIProvider.require_text("  hello  ") == "hello"


def test_safe_int_converts_valid_values() -> None:
    assert BaseAIProvider.safe_int("42") == 42


def test_safe_int_returns_zero_for_invalid_values() -> None:
    assert BaseAIProvider.safe_int("invalid") == 0
