# src/infrastructure/ai/clients/ollama_client.py

"""
Ollama SDK Client

Purpose:
    Encapsulates all communication with the Ollama REST API.

Architecture:
    Infrastructure Layer

Dependencies:
    requests

Notes:
    This client is a thin wrapper around the Ollama REST API.
    It does not know about AIRequest, AIResponse, PromptTemplate,
    or any domain concepts.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from typing import Any, cast

# Third-party imports
import requests

# Local application imports
from src.config.ai_config import AIConfig
from src.domain.ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIProviderError,
)


class OllamaClient:
    """
    Thin wrapper around the Ollama REST API.
    """

    def __init__(self, config: AIConfig) -> None:
        """
        Initialize the client.
        """
        self._base_url = (config.base_url or "http://localhost:11434").rstrip("/")

        self._timeout = config.timeout

    def generate(
        self,
        *,
        model: str,
        prompt: str,
        system_prompt: str | None,
        temperature: float,
    ) -> dict[str, Any]:
        """
        Generate text using the Ollama REST API.

        Parameters
        ----------
        model:
            Model name.

        prompt:
            User prompt.

        system_prompt:
            Optional system prompt.

        temperature:
            Sampling temperature.

        Returns
        -------
        dict[str, Any]
            Raw JSON response from Ollama.
        """

        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                f"{self._base_url}/api/generate",
                json=payload,
                timeout=self._timeout,
            )

        except requests.ConnectionError as exc:
            raise AIConnectionError("Unable to connect to the Ollama server.") from exc

        except requests.Timeout as exc:
            raise AIConnectionError(
                "Connection to the Ollama server timed out."
            ) from exc

        if response.status_code == 401:
            raise AIAuthenticationError("Ollama authentication failed.")

        if not response.ok:
            raise AIProviderError(f"Ollama returned HTTP {response.status_code}.")

        return cast(
            dict[str, Any],
            response.json(),
        )
