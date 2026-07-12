# src/presentation/components/ai/__init__.py

"""
AI Presentation Components

Purpose
-------
Exports reusable AI presentation components.

Architecture
------------
Presentation Layer

Responsibilities
----------------
- Expose reusable AI UI components.
- Keep import paths concise.
- Define the public presentation API.
"""

from __future__ import annotations

# ============================================================================
# Local Imports
# ============================================================================
from . import (
    ai_button,
    ai_error,
    ai_loading,
    ai_panel,
    ai_result,
    provider_selector,
    provider_status,
    summary_card,
)

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "ai_button",
    "ai_error",
    "ai_loading",
    "ai_panel",
    "ai_result",
    "provider_selector",
    "provider_status",
    "summary_card",
]
