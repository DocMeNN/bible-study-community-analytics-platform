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

Author:
    Me
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from typing import Any, cast

# ============================================================================
# Third-Party Imports
# ============================================================================
import requests

# ============================================================================
# Local Imports
# ============================================================================
from src.config.ai_config import AIConfig
from src.domain.ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIProviderError,
)

# ============================================================================
# Ollama Client
# ============================================================================


class OllamaClient:
    """
    Thin wrapper around the Ollama REST API.
    """

    def __init__(
        self,
        config: AIConfig,
    ) -> None:
        """
        Initialize the client.
        """

        self._base_url = (config.base_url or "http://127.0.0.1:11434").rstrip("/")

        self._timeout = config.timeout if config.timeout and config.timeout > 0 else 120

    # ------------------------------------------------------------------
    # Generate
    # ------------------------------------------------------------------

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

        # =====================================================================
        # TEMPORARY DIAGNOSTICS
        # =====================================================================

        print("\n" + "=" * 80)
        print("OLLAMA REQUEST")
        print("=" * 80)
        print(f"URL           : {self._base_url}/api/generate")
        print(f"Model         : {model}")
        print(f"Timeout       : {self._timeout}s")
        print(f"Temperature   : {temperature}")
        print(f"System Prompt : {system_prompt is not None}")
        print(f"Prompt Length : {len(prompt):,} characters")
        print("-" * 80)
        print(prompt[:3000])
        if len(prompt) > 3000:
            print("\n... PROMPT TRUNCATED ...")
        print("=" * 80)

        try:
            response = requests.post(
                f"{self._base_url}/api/generate",
                json=payload,
                timeout=self._timeout,
            )

            print("\n" + "=" * 80)
            print("OLLAMA RESPONSE")
            print("=" * 80)
            print(f"HTTP Status : {response.status_code}")
            print(response.text[:1000])

            if len(response.text) > 1000:
                print("\n... RESPONSE TRUNCATED ...")

            print("=" * 80)

        except requests.ConnectionError as exc:
            raise AIConnectionError("Unable to connect to the Ollama server.") from exc

        except requests.Timeout as exc:
            print("\n" + "=" * 80)
            print("OLLAMA REQUEST TIMED OUT")
            print("=" * 80)
            print(f"URL           : {self._base_url}/api/generate")
            print(f"Model         : {model}")
            print(f"Timeout       : {self._timeout}s")
            print(f"Prompt Length : {len(prompt):,} characters")
            print("=" * 80)

            raise AIConnectionError(
                (
                    "Connection to the Ollama server timed out. "
                    f"Timeout: {self._timeout}s."
                )
            ) from exc

        except requests.RequestException as exc:
            raise AIConnectionError("Unexpected Ollama connection failure.") from exc

        if response.status_code == 401:
            raise AIAuthenticationError("Ollama authentication failed.")

        if not response.ok:
            raise AIProviderError(f"Ollama returned HTTP {response.status_code}.")

        return cast(
            dict[str, Any],
            response.json(),
        )
