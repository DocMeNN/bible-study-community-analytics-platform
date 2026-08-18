# src/presentation/viewmodels/activity_viewmodel.py

"""
Activity ViewModel

Purpose
-------
Coordinates activity presentation workflows by consuming the
Application Layer ActivityService and adapting activity data
for Presentation Layer consumption.

Responsibilities
----------------
- Delegate activity workflows to ActivityService.
- Build Session aggregates through the Application Layer.
- Expose presentation-ready activity data.
- Adapt application results for existing presentation components.

Architectural Rules
-------------------
- Presentation layer only.
- No business logic.
- No analytics calculations.
- No Streamlit.
- No direct Domain analytics.
- No infrastructure dependencies.
- No direct data parsing.

Architecture
------------
Activity Page
        |
        v
ActivityViewModel
        |
        v
ActivityService
        |
        v
Domain Activity Analytics
        |
        v
Presentation Components

The ViewModel is an adapter between the Application Layer
and the Presentation Layer.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable
from datetime import date
from typing import Any

# ============================================================================
# Local Imports
# ============================================================================
from src.application.services.activity_service import ActivityService
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Activity ViewModel
# ============================================================================


class ActivityViewModel:
    """
    Presentation ViewModel for activity workflows.

    Coordinates the ActivityService and adapts activity
    application data for Presentation Layer consumption.

    The ViewModel does not calculate activity analytics.
    Activity calculations remain delegated to the
    Application and Domain layers.
    """

    def __init__(
        self,
        activity_service: ActivityService | None = None,
    ) -> None:
        """
        Initialize the ActivityViewModel.

        Parameters
        ----------
        activity_service:
            Optional ActivityService dependency.

            When omitted, a default ActivityService is created.
        """

        self._activity_service = (
            activity_service if activity_service is not None else ActivityService()
        )

    # =========================================================================
    # Session Construction
    # =========================================================================

    def build_session(
        self,
        *,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build a Session through the Application Layer.

        Session construction remains delegated to
        ActivityService.
        """

        return self._activity_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # =========================================================================
    # Activity Data
    # =========================================================================

    def get_activity(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        """
        Return activity data for the supplied Session.

        Activity calculations are delegated to ActivityService.
        The returned mapping is adapted for Presentation
        Layer components.
        """

        return self.to_presentation_data(
            session=session,
        )

    def to_presentation_data(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        """
        Adapt activity application results for Presentation components.

        This method performs structural presentation adaptation only.

        It does not:
            - calculate activity analytics;
            - apply business rules;
            - parse messages;
            - modify the Session aggregate.
        """

        return {
            "activity_count": self._activity_service.activity_count(
                session,
            ),
            "activity_types": self._activity_service.activity_counts(
                session,
            ),
            "first_activity": self._activity_service.first_activity(
                session,
            ),
            "last_activity": self._activity_service.last_activity(
                session,
            ),
        }

    # =========================================================================
    # Activity Lookup
    # =========================================================================

    def activity_events(
        self,
        *,
        session: Session,
    ) -> tuple[Any, ...]:
        """
        Return activity events from the supplied Session.
        """

        return self._activity_service.activity_events(
            session,
        )

    def activity_events_by_type(
        self,
        *,
        session: Session,
        activity_type: Any,
    ) -> tuple[Any, ...]:
        """
        Return activity events matching the supplied activity type.

        Activity type interpretation remains delegated to
        ActivityService.
        """

        return self._activity_service.activity_events_by_type(
            session,
            activity_type,
        )

    # =========================================================================
    # Presentation Workflow
    # =========================================================================

    def activity_data(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        """
        Return presentation-ready activity data.

        This is the primary convenience method for pages
        and components consuming mapping-based activity data.

        The workflow is:

            Session
                |
                v
            ActivityService
                |
                v
            Presentation Mapping
        """

        return self.get_activity(
            session=session,
        )

    # =========================================================================
    # State
    # =========================================================================

    def has_activities(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when the Session contains activity events.
        """

        return self._activity_service.has_activities(
            session,
        )

    def is_empty(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when the Session contains no events.
        """

        return self._activity_service.is_empty(
            session,
        )

    # =========================================================================
    # Service Access
    # =========================================================================

    @property
    def activity_service(self) -> ActivityService:
        """
        Return the underlying ActivityService.
        """

        return self._activity_service

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"activity_service="
            f"{self.activity_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "ActivityViewModel",
]
