# src/presentation/components/analytics/scope_summary.py

"""
Analytics Scope Summary Component
"""

from __future__ import annotations

import streamlit as st

from src.presentation.dto.multi_session_overview import (
    MultiSessionOverview,
)


def render_scope_summary(
    overview: MultiSessionOverview,
) -> None:
    """
    Render the selected scope summary.
    """

    if overview.start_date and overview.end_date:
        st.info(f"Scope: {overview.start_date:%d %b %Y} ? {overview.end_date:%d %b %Y}")
