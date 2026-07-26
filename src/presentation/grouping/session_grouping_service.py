# src/presentation/grouping/session_grouping_service.py

from __future__ import annotations

from collections import defaultdict

from src.domain.models.session_collection import SessionCollection
from src.presentation.models.session_group import SessionGroup

from .grouping_strategy import GroupingStrategy
from .grouping_types import GroupingPeriod


class SessionGroupingService:
    """
    Presentation-layer service for grouping Daily Sessions.
    """

    def __init__(
        self,
        strategy: GroupingStrategy,
        period: GroupingPeriod,
    ) -> None:
        self._strategy = strategy
        self._period = period

    def group(
        self,
        session_collection: SessionCollection,
    ) -> tuple[SessionGroup, ...]:
        """
        Group sessions without modifying the source collection.
        """

        grouped_sessions = defaultdict(list)

        for session in session_collection:

            boundary = self._strategy.boundary_for(
                session.session_date,
            )

            key = (
                boundary.start_date,
                boundary.end_date,
            )

            grouped_sessions[key].append(
                session,
            )

        groups = tuple(
            SessionGroup(
                start_date=start_date,
                end_date=end_date,
                sessions=tuple(sessions),
            )
            for (
                start_date,
                end_date,
            ), sessions in sorted(
                grouped_sessions.items(),
            )
        )

        return groups


__all__ = [
    "SessionGroupingService",
]
