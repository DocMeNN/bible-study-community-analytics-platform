# src/infrastructure/ai/provider_factory.py

"""
AI Provider Factory

Purpose:
    Creates AI provider implementations based on the
    application configuration.

Architecture:
    Infrastructure Layer

Dependencies:
    Configuration Layer
    Domain Layer
    Provider Implementations

Notes:
    This factory is the single entry point for creating
    AI providers.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from collections.abc import Callable

# Local application imports
from src.config.ai_config import AIConfig, AIProvider
from src.domain.ai.exceptions import AIConfigurationError
from src.domain.ai.interfaces import AIProvider as AIProviderInterface

from .providers.gemini_provider import GeminiProvider
from .providers.ollama_provider import OllamaProvider
from .providers.openai_provider import OpenAIProvider

_PROVIDER_REGISTRY: dict[
    AIProvider,
    Callable[[AIConfig], AIProviderInterface],
] = {
    AIProvider.OPENAI: OpenAIProvider,
    AIProvider.GEMINI: GeminiProvider,
    AIProvider.OLLAMA: OllamaProvider,
}


class AIProviderFactory:
    """
    Factory for AI provider implementations.
    """

    @staticmethod
    def create(
        config: AIConfig,
    ) -> AIProviderInterface:
        """
        Create an AI provider.

        Parameters
        ----------
        config:
            AI configuration.

        Returns
        -------
        AIProviderInterface
            Configured AI provider.

        Raises
        ------
        AIConfigurationError
            If the configured provider is unsupported.
        """

        provider_factory = _PROVIDER_REGISTRY.get(config.provider)

        if provider_factory is None:
            raise AIConfigurationError(f"Unsupported AI provider: {config.provider}")

        return provider_factory(config)
