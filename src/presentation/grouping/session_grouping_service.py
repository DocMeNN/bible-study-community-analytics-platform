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
        if not isinstance(
            period,
            GroupingPeriod,
        ):
            raise TypeError(
                "period must be a GroupingPeriod.",
            )

        self._strategy = strategy
        self._period = period

    @property
    def period(self) -> GroupingPeriod:
        """Return the active grouping period."""

        return self._period

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

        # =====================================================================
        # TEMPORARY DEBUG
        # =====================================================================

        print("\n================ SESSION GROUPING DEBUG ================")
        print("SessionCollection type:", type(session_collection))
        print("SessionCollection count:", len(session_collection))

        for key, sessions in grouped_sessions.items():
            print(f"\nGROUP: {key}")

            for index, item in enumerate(sessions):
                print(
                    f"  [{index}]",
                    "type =", type(item),
                    "module =", type(item).__module__,
                    "class =", type(item).__name__,
                    "session_date =",
                    getattr(item, "session_date", None),
                )

        print("========================================================\n")

        return tuple(
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


__all__ = [
    "SessionGroupingService",
]
