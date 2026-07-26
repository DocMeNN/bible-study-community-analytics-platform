# tests/presentation/grouping/test_session_group.py

from datetime import date

from src.domain.models.session import Session
from src.presentation.models.session_group import SessionGroup


def test_session_group_sorts_sessions_chronologically() -> None:
    sessions = (
        Session(
            session_date=date(2023, 1, 5),
        ),
        Session(
            session_date=date(2023, 1, 1),
        ),
    )

    group = SessionGroup(
        start_date=date(2023, 1, 1),
        end_date=date(2023, 1, 7),
        sessions=sessions,
    )

    assert group.session_dates == (
        date(2023, 1, 1),
        date(2023, 1, 5),
    )


def test_session_group_returns_session_by_date() -> None:
    session = Session(
        session_date=date(2023, 1, 3),
    )

    group = SessionGroup(
        start_date=date(2023, 1, 1),
        end_date=date(2023, 1, 7),
        sessions=(session,),
    )

    assert group.get_session(
        date(2023, 1, 3),
    ) is session
