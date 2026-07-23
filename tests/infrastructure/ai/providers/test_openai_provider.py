# tests/infrastructure/ai/providers/test_openai_provider.py

from unittest.mock import Mock, patch

from src.config.ai_config import AIConfig, AIProvider
from src.domain.ai.models import AIRequest
from src.infrastructure.ai.providers.openai_provider import (
    OpenAIProvider,
)


def _config() -> AIConfig:
    return AIConfig(
        provider=AIProvider.OPENAI,
        model="test-model",
        api_key="test-api-key",
        base_url=None,
        temperature=0.3,
        max_tokens=1024,
        timeout=60,
    )


def test_openai_provider_generates_response() -> None:
    provider = OpenAIProvider(_config())

    response = Mock()
    response.model = "gpt-test"
    response.choices = [
        Mock(
            message=Mock(
                content="Generated response"
            ),
            finish_reason="stop",
        )
    ]
    response.usage = Mock(
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
    )

    with patch.object(
        provider._client,
        "generate",
        return_value=response,
    ):
        result = provider.generate(
            AIRequest(prompt="Hello")
        )

    assert result.content == "Generated response"
    assert result.provider == "openai"
    assert result.total_tokens == 30
