"""
Analytics Presentation Components

Purpose
-------
Presentation components for Multi-Session Analytics.

These components render Application analytics that have already been
adapted into Presentation DTOs.

Architectural Rules
-------------------
- Presentation layer only.
- No business logic.
- No analytics calculations.
- No Streamlit session state.
- No Domain dependencies.
"""

from .distributions import render_distributions
from .overview import render_overview
from .rankings import render_rankings
from .scope_summary import render_scope_summary
from .trends import render_trends

__all__ = [
    "render_overview",
    "render_scope_summary",
    "render_trends",
    "render_rankings",
    "render_distributions",
]
