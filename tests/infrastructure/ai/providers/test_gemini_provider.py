# tests/infrastructure/ai/providers/test_gemini_provider.py

from unittest.mock import Mock, patch

from src.config.ai_config import AIConfig, AIProvider
from src.domain.ai.models import AIRequest
from src.infrastructure.ai.providers.gemini_provider import (
    GeminiProvider,
)


def _config() -> AIConfig:
    return AIConfig(
        provider=AIProvider.GEMINI,
        model="test-model",
        api_key="test-api-key",
        base_url=None,
        temperature=0.3,
        max_tokens=1024,
        timeout=60,
    )


def test_gemini_provider_generates_response() -> None:
    provider = GeminiProvider(_config())

    response = Mock()
    response.text = "Generated response"
    response.usage_metadata = None
    response.finish_reason = None

    with patch.object(
        provider._client,
        "generate",
        return_value=response,
    ):
        result = provider.generate(
            AIRequest(prompt="Hello")
        )

    assert result.content == "Generated response"
    assert result.provider == "gemini"
