# src/application/services/activity_service.py

"""
Activity Application Service

Purpose:
    Provides application-level activity use cases by orchestrating
    Session construction and Domain activity analytics.

Responsibilities:
    - Build Session aggregates.
    - Coordinate activity analytics.
    - Expose activity-related application services.
    - Remain free of business logic.

Rules:
    - No pandas.
    - No Streamlit.
    - No plotting.
    - No reporting.
    - No infrastructure parsing.
    - No business rules.

Notes:
    - Business rules remain inside the Domain layer.
    - This service coordinates Domain components only.
    - Activity calculations are delegated to Domain analytics.
    - Technology independent.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections import Counter
from collections.abc import Iterable
from datetime import date

# ============================================================================
# Local Imports
# ============================================================================
from src.application.builders.session_builder import SessionBuilder
from src.domain.analytics.activity import (
    count_activity_types,
    first_activity_event,
    get_activity_events,
    last_activity_event,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.message import Message
from src.domain.models.session import Session


class ActivityService:
    """
    Application service for activity workflows.

    Coordinates Session construction and delegates
    activity-related business calculations to the
    Domain layer.
    """

    def __init__(
        self,
        session_builder: SessionBuilder | None = None,
    ) -> None:
        """
        Initialize the ActivityService.

        Parameters
        ----------
        session_builder:
            Optional SessionBuilder used to construct Session aggregates.
            A default builder is created when none is supplied.
        """

        self._session_builder = (
            session_builder
            if session_builder is not None
            else SessionBuilder()
        )

    # =========================================================================
    # Session Construction
    # =========================================================================

    def build_session(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build an immutable Session aggregate.

        Session construction is delegated to SessionBuilder.
        """

        return self._session_builder.build(
            session_date=session_date,
            messages=messages,
        )

    # =========================================================================
    # Activity Events
    # =========================================================================

    def activity_events(
        self,
        session: Session,
    ) -> tuple[ActivityEvent, ...]:
        """
        Return all activity events from the supplied Session.
        """

        return get_activity_events(
            session.activity_events,
        )

    def activity_count(
        self,
        session: Session,
    ) -> int:
        """
        Return the total number of activity events.
        """

        return len(
            self.activity_events(
                session,
            )
        )

    def activity_counts(
        self,
        session: Session,
    ) -> Counter[ActivityType]:
        """
        Return activity counts grouped by ActivityType.
        """

        return count_activity_types(
            session.activity_events,
        )

    def first_activity(
        self,
        session: Session,
    ) -> ActivityEvent | None:
        """
        Return the earliest activity event.

        Returns None when the Session contains no activities.
        """

        return first_activity_event(
            session.activity_events,
        )

    def last_activity(
        self,
        session: Session,
    ) -> ActivityEvent | None:
        """
        Return the latest activity event.

        Returns None when the Session contains no activities.
        """

        return last_activity_event(
            session.activity_events,
        )

    # =========================================================================
    # Activity Lookup
    # =========================================================================

    def activity_events_by_type(
        self,
        session: Session,
        activity_type: ActivityType,
    ) -> tuple[ActivityEvent, ...]:
        """
        Return activity events matching the supplied ActivityType.
        """

        return tuple(
            event
            for event in session.activity_events
            if event.activity_type is activity_type
        )

    def has_activity(
        self,
        session: Session,
        activity_type: ActivityType,
    ) -> bool:
        """
        Return True when the Session contains the specified activity type.
        """

        return bool(
            self.activity_events_by_type(
                session,
                activity_type,
            )
        )

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def has_activities(
        self,
        session: Session,
    ) -> bool:
        """
        Return True when the Session contains activity events.
        """

        return session.has_activities

    def is_empty(
        self,
        session: Session,
    ) -> bool:
        """
        Return True when the Session contains no events.
        """

        return session.is_empty

    # =========================================================================
    # Builder Access
    # =========================================================================

    @property
    def builder(self) -> SessionBuilder:
        """
        Return the SessionBuilder used by this service.
        """

        return self._session_builder

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}"
            f"(builder={self.builder.name})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()
