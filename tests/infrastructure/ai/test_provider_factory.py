# tests/infrastructure/ai/test_provider_factory.py

from unittest.mock import patch

from src.config.ai_config import AIConfig, AIProvider
from src.infrastructure.ai.provider_factory import AIProviderFactory


def _config(provider: AIProvider) -> AIConfig:
    return AIConfig(
        provider=provider,
        model="test-model",
        api_key=None,
        base_url=None,
        temperature=0.3,
        max_tokens=1024,
        timeout=60,
    )


def test_factory_creates_ollama_provider() -> None:
    config = _config(AIProvider.OLLAMA)

    provider = AIProviderFactory.create(config)

    assert provider.__class__.__name__ == "OllamaProvider"


def test_factory_creates_openai_provider() -> None:
    config = _config(AIProvider.OPENAI)

    with patch(
        "src.infrastructure.ai.providers.openai_provider.OpenAIClient"
    ):
        provider = AIProviderFactory.create(config)

    assert provider.__class__.__name__ == "OpenAIProvider"


def test_factory_creates_gemini_provider() -> None:
    config = _config(AIProvider.GEMINI)

    with patch(
        "src.infrastructure.ai.providers.gemini_provider.GeminiClient"
    ):
        provider = AIProviderFactory.create(config)

    assert provider.__class__.__name__ == "GeminiProvider"
