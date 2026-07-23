# tests/infrastructure/config/test_ai_config.py

from src.config.ai_config import (
    AIConfig,
    AIProvider,
    load_ai_config,
)


def test_ai_provider_contains_supported_providers() -> None:
    assert AIProvider.OPENAI.value == "openai"
    assert AIProvider.GEMINI.value == "gemini"
    assert AIProvider.OLLAMA.value == "ollama"


def test_ai_config_stores_configuration() -> None:
    config = AIConfig(
        provider=AIProvider.OLLAMA,
        model="test-model",
        api_key=None,
        base_url=None,
        temperature=0.3,
        max_tokens=1024,
        timeout=60,
    )

    assert config.provider == AIProvider.OLLAMA
    assert config.model == "test-model"
    assert config.temperature == 0.3
    assert config.max_tokens == 1024
    assert config.timeout == 60


def test_load_ai_config_uses_ollama_defaults(monkeypatch) -> None:
    monkeypatch.delenv("AI_PROVIDER", raising=False)
    monkeypatch.delenv("AI_MODEL", raising=False)
    monkeypatch.delenv("AI_API_KEY", raising=False)
    monkeypatch.delenv("AI_BASE_URL", raising=False)
    monkeypatch.delenv("AI_TEMPERATURE", raising=False)
    monkeypatch.delenv("AI_MAX_TOKENS", raising=False)
    monkeypatch.delenv("AI_TIMEOUT", raising=False)

    config = load_ai_config()

    assert config.provider == AIProvider.OLLAMA
    assert config.model == "llama3.2:3b"
    assert config.temperature == 0.3
    assert config.max_tokens == 1024
    assert config.timeout == 60
