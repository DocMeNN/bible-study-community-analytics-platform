# src/domain/policies/activity_policy.py

"""
Activity Policy

Purpose
-------
Defines the business rules for identifying and classifying
activities within an OYBS study session.

Responsibilities
----------------
- Identify supported OYBS activities.
- Classify messages by activity.
- Recognize valid Scripture Reading announcements.
- Recognize prayer-session boundaries.
- Distinguish Scripture Reading acknowledgements.
- Apply Discussion as the fallback activity.

Domain Rules
------------
Scripture Reading:
    A message is classified as Scripture Reading only when:

    1. It contains a valid Scripture Reading announcement header.
    2. It contains a recognizable Bible portion reference.

    Examples:

        SCRIPTURE READING
        ACTS 28:17-31

    and:

        SCRIPTURES READING FOR FRIDAY, JULY 24TH, 2026

        ACTS 28:17-31; PSALMS 30-31

Insight:
    Any message beginning with:
        "insight"
        "insights"

Announcement:
    Any message beginning with a supported announcement keyword.

Done:
    Any message beginning with:
        "done"

Discussion:
    Any message that does not match another activity and is
    not inside an active Prayer Session.

Prayer Session:
    A prayer session opens when a message starts with either:

        "opening prayer"
        "prayer session opens"

    A prayer session closes when a message starts with either:

        "closing prayer"
        "closing prayers"
        "prayer session closes"

Important
---------
- Matching is case-insensitive.
- Scripture Reading detection is structural, not substring-based.
- A casual mention of "scripture reading" is not a Scripture Reading activity.
- A Scripture Reading header without a Bible portion is not a valid
  Scripture Reading announcement.
- Discussion is the fallback activity for ordinary study messages.
- Discussion does not include messages inside an active Prayer Session.
- No worship, offering, sermon, ministration, or generic Message
  activity exists in the OYBS domain.
- This module contains domain policy only.
- No pandas.
- No Streamlit.
- No infrastructure dependencies.

Author
------
OYBS Attendance Dashboard

Created
-------
July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from typing import Final

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.constants.keywords import (
    ANNOUNCEMENT_KEYWORDS,
    CLOSING_PRAYER_KEYWORDS,
    DONE_KEYWORDS,
    OPENING_PRAYER_KEYWORDS,
)
from src.infrastructure.config.regex import (
    BIBLE_PORTION_PATTERN,
    SCRIPTURE_READING_HEADER_PATTERN,
)

# ============================================================================
# Supported Activity Names
# ============================================================================

ACTIVITY_SCRIPTURE_READING: Final[str] = "Scripture Reading"

ACTIVITY_INSIGHT: Final[str] = "Insight"

ACTIVITY_DISCUSSION: Final[str] = "Discussion"

ACTIVITY_ANNOUNCEMENT: Final[str] = "Announcement"

ACTIVITY_DONE: Final[str] = "Done"

ACTIVITY_PRAYER_SESSION: Final[str] = "Prayer Session"


# ============================================================================
# Message Normalization
# ============================================================================


def normalize_message(
    content: str,
) -> str:
    """
    Normalize message content for policy evaluation.

    Rules
    -----
    - Strip leading and trailing whitespace.
    - Collapse repeated whitespace within each line.
    - Convert to casefolded text.
    """

    return "\n".join(
        " ".join(line.strip().casefold().split())
        for line in content.splitlines()
        if line.strip()
    )


# ============================================================================
# Prefix Matching
# ============================================================================


def starts_with_keyword(
    content: str,
    keywords: frozenset[str],
) -> bool:
    """
    Return True if content starts with one of the supplied keywords.
    """

    normalized = normalize_message(
        content,
    )

    return any(
        normalized.startswith(
            keyword.casefold(),
        )
        for keyword in keywords
    )


# ============================================================================
# Prayer Session Boundaries
# ============================================================================


def is_prayer_session_opening(
    content: str,
) -> bool:
    """
    Return True if the message opens a prayer session.
    """

    return starts_with_keyword(
        content,
        OPENING_PRAYER_KEYWORDS,
    )


def is_prayer_session_closing(
    content: str,
) -> bool:
    """
    Return True if the message closes a prayer session.
    """

    return starts_with_keyword(
        content,
        CLOSING_PRAYER_KEYWORDS,
    )


# ============================================================================
# Scripture Reading Detection
# ============================================================================


def _contains_scripture_reading_header(
    content: str,
) -> bool:
    """
    Return True if a complete line is a Scripture Reading header.

    Supported examples
    ------------------
    SCRIPTURE READING

    SCRIPTURES READING

    SCRIPTURES READING FOR TODAY

    SCRIPTURES READING FOR FRIDAY, JULY 24TH, 2026
    """

    for line in content.splitlines():
        normalized_line = " ".join(line.strip().casefold().split())

        if not normalized_line:
            continue

        if SCRIPTURE_READING_HEADER_PATTERN.fullmatch(
            normalized_line,
        ):
            return True

    return False


def _contains_bible_portion(
    content: str,
) -> bool:
    """
    Return True if the message contains a recognizable Bible portion.

    Examples
    --------
    ACTS 28:17-31

    PSALMS 30-31

    GENESIS 1-3

    MATTHEW 5:1-12

    1 CORINTHIANS 13
    """

    return (
        BIBLE_PORTION_PATTERN.search(
            content,
        )
        is not None
    )


def is_scripture_reading_activity(
    content: str,
) -> bool:
    """
    Return True if content is a valid Scripture Reading announcement.

    A valid Scripture Reading announcement requires both:

    1. A complete Scripture Reading header.
    2. A recognizable Bible portion.

    This prevents ordinary conversational references such as:

        I enjoyed the scripture reading today.

    from being incorrectly classified as Scripture Reading.
    """

    if not _contains_scripture_reading_header(
        content,
    ):
        return False

    return _contains_bible_portion(
        content,
    )


# ============================================================================
# Explicit Activity Detection
# ============================================================================


def is_done_activity(
    content: str,
) -> bool:
    """
    Return True if the message represents a Done acknowledgement.
    """

    return starts_with_keyword(
        content,
        DONE_KEYWORDS,
    )


def is_insight_activity(
    content: str,
) -> bool:
    """
    Return True if the message represents an Insight.
    """

    normalized = normalize_message(
        content,
    )

    return normalized.startswith("insight") or normalized.startswith("insights")


def is_announcement_activity(
    content: str,
) -> bool:
    """
    Return True if the message represents an Announcement.
    """

    return starts_with_keyword(
        content,
        ANNOUNCEMENT_KEYWORDS,
    )


# ============================================================================
# Activity Classification
# ============================================================================


def classify_activity(
    content: str,
    *,
    prayer_session_active: bool = False,
) -> str:
    """
    Classify a message according to OYBS activity rules.

    Classification Order
    --------------------
    1. Prayer Session opening
    2. Prayer Session closing
    3. Scripture Reading
    4. Done
    5. Insight
    6. Announcement
    7. Prayer Session
    8. Discussion
    """

    if is_prayer_session_opening(
        content,
    ):
        return ACTIVITY_PRAYER_SESSION

    if is_prayer_session_closing(
        content,
    ):
        return ACTIVITY_PRAYER_SESSION

    if is_scripture_reading_activity(
        content,
    ):
        return ACTIVITY_SCRIPTURE_READING

    if is_done_activity(
        content,
    ):
        return ACTIVITY_DONE

    if is_insight_activity(
        content,
    ):
        return ACTIVITY_INSIGHT

    if is_announcement_activity(
        content,
    ):
        return ACTIVITY_ANNOUNCEMENT

    if prayer_session_active:
        return ACTIVITY_PRAYER_SESSION

    return ACTIVITY_DISCUSSION


# ============================================================================
# Supported Activity Inspection
# ============================================================================


def is_supported_activity(
    content: str,
    *,
    prayer_session_active: bool = False,
) -> bool:
    """
    Return True if the message represents a supported activity.

    Since Discussion is the fallback activity, every non-empty
    message is classified as a supported activity.
    """

    return bool(
        normalize_message(
            content,
        )
    )


def is_session_boundary_activity(
    content: str,
) -> bool:
    """
    Return True if the message marks a Prayer Session boundary.
    """

    return is_prayer_session_opening(
        content,
    ) or is_prayer_session_closing(
        content,
    )


# ============================================================================
# Supported Activity Inspection
# ============================================================================


def supported_activity_names() -> tuple[str, ...]:
    """
    Return all canonical supported activity names.
    """

    return (
        ACTIVITY_SCRIPTURE_READING,
        ACTIVITY_INSIGHT,
        ACTIVITY_DISCUSSION,
        ACTIVITY_ANNOUNCEMENT,
        ACTIVITY_DONE,
        ACTIVITY_PRAYER_SESSION,
    )
