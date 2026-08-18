"""
Presentation Theme Configuration

Purpose
-------
Centralized location for Streamlit page configuration and
presentation constants.

Responsibilities
----------------
- Configure Streamlit page settings.
- Define application metadata.
- Provide reusable UI constants.
- Initialize the presentation theme.

Architectural Notes
-------------------
This module contains presentation-only configuration.

- No business logic.
- No domain calculations.
- No infrastructure access.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from typing import Final, Literal

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Application Metadata
# ============================================================================

APP_TITLE: Final[str] = "WhatsApp Attendance Dashboard"

APP_ICON: Final[str] = "📊"

APP_TAGLINE: Final[str] = (
    "Transform WhatsApp chat exports into attendance and engagement insights."
)

# ============================================================================
# Streamlit Configuration
# ============================================================================

PAGE_LAYOUT: Final[Literal["wide", "centered"]] = "wide"

SIDEBAR_STATE: Final[Literal["auto", "expanded", "collapsed"]] = "expanded"

# ============================================================================
# Page Names
# ============================================================================

HOME_PAGE: Final[str] = "Home"

DASHBOARD_PAGE: Final[str] = "Dashboard"

ATTENDANCE_PAGE: Final[str] = "Attendance"

ACTIVITY_PAGE: Final[str] = "Activity"

REPORTS_PAGE: Final[str] = "Reports"

SETTINGS_PAGE: Final[str] = "Settings"

# ============================================================================
# Navigation
# ============================================================================

NAVIGATION_PAGES: Final[tuple[str, ...]] = (
    HOME_PAGE,
    DASHBOARD_PAGE,
    ATTENDANCE_PAGE,
    ACTIVITY_PAGE,
    REPORTS_PAGE,
    SETTINGS_PAGE,
)

# ============================================================================
# Theme Initialization
# ============================================================================


def configure_page() -> None:
    """
    Configure the Streamlit application.
    """

    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state=SIDEBAR_STATE,
    )


# ============================================================================
# Shared UI
# ============================================================================


def render_application_header() -> None:
    """
    Render the application header.
    """

    st.title(APP_TITLE)
    st.caption(APP_TAGLINE)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "APP_TITLE",
    "APP_ICON",
    "APP_TAGLINE",
    "PAGE_LAYOUT",
    "SIDEBAR_STATE",
    "HOME_PAGE",
    "DASHBOARD_PAGE",
    "ATTENDANCE_PAGE",
    "ACTIVITY_PAGE",
    "REPORTS_PAGE",
    "SETTINGS_PAGE",
    "NAVIGATION_PAGES",
    "configure_page",
    "render_application_header",
]
