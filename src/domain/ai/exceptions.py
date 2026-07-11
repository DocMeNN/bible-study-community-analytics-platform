# src/domain/ai/exceptions.py

"""
AI Domain Exceptions

Purpose:
    Defines the exception hierarchy for the AI subsystem.

Architecture:
    Domain Layer

Dependencies:
    Standard Library Only

Notes:
    These exceptions are provider-agnostic. Infrastructure providers
    should translate provider-specific errors into these domain
    exceptions before propagating them to the Application layer.

Author: Me
"""

from __future__ import annotations


class AIError(Exception):
    """
    Base exception for all AI-related errors.
    """


# ============================================================================
# AI Exceptions
# ============================================================================


class AIConfigurationError(AIError):
    """
    Raised when AI configuration is invalid or incomplete.
    """


class AIAuthenticationError(AIError):
    """
    Raised when authentication with an AI provider fails.
    """


class AIConnectionError(AIError):
    """
    Raised when communication with an AI provider fails.
    """


class AIRateLimitError(AIError):
    """
    Raised when an AI provider's rate limit is exceeded.
    """


class AIRequestError(AIError):
    """
    Raised when an AI request is invalid.
    """


class AIResponseError(AIError):
    """
    Raised when an AI provider returns an invalid or
    unusable response.
    """


class AIProviderError(AIError):
    """
    Raised when an AI provider encounters an internal error.
    """


# ============================================================================
# Prompt Exceptions
# ============================================================================


class PromptError(AIError):
    """
    Base exception for all prompt-related errors.
    """


class PromptNotFoundError(PromptError):
    """
    Raised when a requested prompt template
    is not registered.
    """


class PromptValidationError(PromptError):
    """
    Raised when prompt variables fail validation.
    """


class PromptRenderError(PromptError):
    """
    Raised when prompt rendering fails.
    """
