# tests/infrastructure/ai/providers/test_ollama_provider.py

from unittest.mock import Mock

from src.config.ai_config import AIConfig, AIProvider
from src.domain.ai.models import AIRequest
from src.infrastructure.ai.providers.ollama_provider import (
    OllamaProvider,
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


def test_ollama_provider_generates_response() -> None:
    provider = OllamaProvider(_config())

    provider._client.generate = Mock(
        return_value={
            "response": "Generated response",
            "prompt_eval_count": 10,
            "eval_count": 20,
        }
    )

    response = provider.generate(
        AIRequest(prompt="Hello")
    )

    assert response.content == "Generated response"
    assert response.provider == "ollama"
    assert response.prompt_tokens == 10
    assert response.completion_tokens == 20
    assert response.total_tokens == 30
