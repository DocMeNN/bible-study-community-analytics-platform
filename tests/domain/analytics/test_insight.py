# tests/domain/analytics/test_insight.py

"""
Tests for Domain Insight Analytics.
"""

from datetime import date

import pytest

from src.domain.analytics.insight import (
    count_insights,
    count_insights_by_severity,
    get_critical_insights,
    get_general_insights,
    get_informational_insights,
    get_insights,
    get_insights_by_severity,
    get_positive_insights,
    get_session_insights,
    get_warning_insights,
    highest_priority_insight,
    insight_summary,
    sort_by_importance,
    top_insights,
)
from src.domain.models.insight_event import (
    InsightEvent,
    InsightSeverity,
)


@pytest.fixture
def insights() -> tuple[InsightEvent, ...]:
    """Return sample insight events."""
    return (
        InsightEvent(
            title="Strong Participation",
            description="Strong participation observed.",
            severity=InsightSeverity.POSITIVE,
            session_date=date(2026, 7, 22),
        ),
        InsightEvent(
            title="Participation Decline",
            description="Participation declining.",
            severity=InsightSeverity.WARNING,
            session_date=date(2026, 7, 22),
        ),
        InsightEvent(
            title="Critical Participation Gap",
            description="Critical participation gap detected.",
            severity=InsightSeverity.CRITICAL,
            session_date=None,
        ),
        InsightEvent(
            title="Analysis Completed",
            description="Analysis period completed.",
            severity=InsightSeverity.INFO,
            session_date=None,
        ),
    )


def test_get_insights_preserves_supplied_order(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Insights should preserve their supplied order."""
    assert get_insights(insights) == insights


def test_get_insights_by_severity(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Insights should be filtered by severity."""
    result = get_insights_by_severity(
        insights,
        InsightSeverity.WARNING,
    )

    assert len(result) == 1
    assert result[0].severity is InsightSeverity.WARNING


def test_get_session_insights(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Session-specific insights should be retrieved by date."""
    result = get_session_insights(
        insights,
        date(2026, 7, 22),
    )

    assert len(result) == 2


def test_get_general_insights(
    insights: tuple[InsightEvent, ...],
) -> None:
    """General insights should have no session date."""
    result = get_general_insights(insights)

    assert len(result) == 2
    assert all(insight.session_date is None for insight in result)


def test_classification_helpers(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Classification helpers should return the correct insights."""
    assert len(get_positive_insights(insights)) == 1
    assert len(get_warning_insights(insights)) == 1
    assert len(get_critical_insights(insights)) == 1
    assert len(get_informational_insights(insights)) == 1


def test_count_insights(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Total insight count should be returned."""
    assert count_insights(insights) == 4


def test_count_insights_by_severity(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Insights should be counted by severity."""
    counts = count_insights_by_severity(insights)

    assert counts[InsightSeverity.POSITIVE] == 1
    assert counts[InsightSeverity.WARNING] == 1
    assert counts[InsightSeverity.CRITICAL] == 1
    assert counts[InsightSeverity.INFO] == 1


def test_sort_by_importance(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Insights should be ordered from highest to lowest importance."""
    result = sort_by_importance(insights)

    assert [insight.severity for insight in result] == [
        InsightSeverity.CRITICAL,
        InsightSeverity.WARNING,
        InsightSeverity.POSITIVE,
        InsightSeverity.INFO,
    ]


def test_same_severity_preserves_original_order() -> None:
    """Equal-severity insights should preserve their original order."""
    first = InsightEvent(
        title="First Warning",
        description="First warning.",
        severity=InsightSeverity.WARNING,
        session_date=None,
    )

    second = InsightEvent(
        title="Second Warning",
        description="Second warning.",
        severity=InsightSeverity.WARNING,
        session_date=None,
    )

    result = sort_by_importance((first, second))

    assert result == (first, second)


def test_highest_priority_insight(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Highest-priority insight should be returned."""
    result = highest_priority_insight(insights)

    assert result is not None
    assert result.severity is InsightSeverity.CRITICAL


def test_highest_priority_insight_empty() -> None:
    """Empty input should return no highest-priority insight."""
    assert highest_priority_insight([]) is None


def test_top_insights(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Top insights should respect the requested limit."""
    result = top_insights(
        insights,
        limit=2,
    )

    assert len(result) == 2
    assert result[0].severity is InsightSeverity.CRITICAL
    assert result[1].severity is InsightSeverity.WARNING


def test_top_insights_rejects_invalid_limit(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Invalid limits should be rejected."""
    with pytest.raises(ValueError):
        top_insights(
            insights,
            limit=0,
        )


def test_insight_summary(
    insights: tuple[InsightEvent, ...],
) -> None:
    """Insight summary should contain expected values."""
    summary = insight_summary(insights)

    assert summary["insight_count"] == 4
    assert summary["positive_count"] == 1
    assert summary["warning_count"] == 1
    assert summary["critical_count"] == 1
    assert summary["informational_count"] == 1
    assert summary["session_specific_count"] == 2
    assert summary["general_count"] == 2
    assert summary["highest_priority"].severity is InsightSeverity.CRITICAL


def test_empty_insights_return_empty_results() -> None:
    """Empty input should return empty results."""
    assert get_insights([]) == ()
    assert get_general_insights([]) == ()
    assert count_insights([]) == 0
    assert highest_priority_insight([]) is None
    assert top_insights([]) == ()


def test_generator_input_is_supported() -> None:
    """Analytics should support iterable inputs."""
    insights = (
        InsightEvent(
            title="Positive",
            description="Positive.",
            severity=InsightSeverity.POSITIVE,
            session_date=None,
        ),
        InsightEvent(
            title="Warning",
            description="Warning.",
            severity=InsightSeverity.WARNING,
            session_date=None,
        ),
    )

    generator = (insight for insight in insights)

    assert count_insights(generator) == 2
