# src/presentation/controllers/__init__.py

"""
Presentation Controllers

Purpose
-------
Coordinates user interactions between the Presentation layer
and the Application layer.

Architectural Rules
-------------------
- No business logic.
- No infrastructure access.
- Delegates application use cases.
"""

from .ai_controller import AIController

__all__ = [
    "AIController",
]
