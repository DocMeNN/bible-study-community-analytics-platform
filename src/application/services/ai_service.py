# src/application/services/ai_service.py

"""
AI Service

Purpose:
    Coordinates AI interactions for the application.

Architecture:
    Application Layer

Dependencies:
    Domain layer
    Configuration layer
    Prompt Engine
    Response Engine
    AI Request Builder
    Infrastructure factory

Notes:
    This service is provider-agnostic. It delegates prompt
    rendering, request construction, response processing,
    and provider interaction to dedicated components.

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.application.ai.prompt_engine import PromptEngine
from src.application.ai.prompt_registry import PromptRegistry
from src.application.ai.prompt_renderer import PromptRenderer
from src.application.ai.request_builder import AIRequestBuilder
from src.application.ai.response_engine import ResponseEngine
from src.application.ai.response_parser import ResponseParser
from src.application.ai.response_validator import ResponseValidator
from src.config.ai_config import AIConfig
from src.domain.ai.interfaces import AIProvider
from src.domain.ai.models import AIResponse
from src.domain.ai.prompts import PromptTemplate
from src.infrastructure.ai.provider_factory import AIProviderFactory


class AIService:
    """
    Coordinates AI operations.
    """

    def __init__(
        self,
        config: AIConfig,
        provider: AIProvider | None = None,
    ) -> None:
        """
        Initialize the AI service.
        """

        self._provider = provider or AIProviderFactory.create(config)

        self._prompt_engine = PromptEngine(
            registry=PromptRegistry(),
            renderer=PromptRenderer(),
        )

        self._request_builder = AIRequestBuilder(
            config=config,
        )

        self._response_engine = ResponseEngine(
            parser=ResponseParser(),
            validator=ResponseValidator(),
        )

    def generate(
        self,
        template: PromptTemplate,
        **prompt_data: object,
    ) -> AIResponse:
        """
        Generate an AI response.

        Returns
        -------
        AIResponse
            Provider response including metadata.
        """

        prompt = self._prompt_engine.render(
            prompt=template,
            variables=prompt_data,
        )

        request = self._request_builder.build(
            prompt=prompt,
        )

        return self._provider.generate(
            request,
        )

    def process(
        self,
        template: PromptTemplate,
        **prompt_data: object,
    ) -> str:
        """
        Generate, parse, and validate AI output.

        Returns
        -------
        str
            Parsed and validated response text.
        """

        response = self.generate(
            template=template,
            **prompt_data,
        )

        return self._response_engine.process(
            response=response,
        )
