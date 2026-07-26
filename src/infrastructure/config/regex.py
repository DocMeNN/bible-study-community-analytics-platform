# src/infrastructure/config/regex.py

"""
Regex Configuration

Purpose
-------
Central repository for all compiled regular expressions used
throughout the Attendance Dashboard application.

Responsibilities
----------------
- WhatsApp message parsing
- Date extraction
- Time extraction
- Attendance detection
- Scripture Reading announcement detection
- Prayer boundary detection
- System message detection
- Media message detection
- Phone number extraction

Important
---------
The Scripture Reading patterns intentionally distinguish between:

1. A Scripture Reading announcement header.
2. A Bible portion reference.

The combination of these structures is used by the domain policy
to identify a valid OYBS Scripture Reading announcement.

This module exposes ONLY compiled regular expressions.
Raw regex strings should never be imported elsewhere.

Author
------
OYBS Attendance Dashboard

Created
-------
July 2026
"""

from __future__ import annotations

import re
from re import Pattern

###############################################################################
# DATE / TIME
###############################################################################

DATE_PATTERN: Pattern[str] = re.compile(
    r"\d{1,2}/\d{1,2}/\d{2,4}",
)

TIME_PATTERN: Pattern[str] = re.compile(
    r"\d{1,2}:\d{2}",
)

DATETIME_PATTERN: Pattern[str] = re.compile(
    r"""
    ^
    (?P<date>\d{1,2}/\d{1,2}/\d{2,4})
    ,
    \s*
    (?P<time>\d{1,2}:\d{2})
    """,
    re.VERBOSE,
)

###############################################################################
# WHATSAPP MESSAGE PARSER
###############################################################################

WHATSAPP_MESSAGE_PATTERN: Pattern[str] = re.compile(
    r"""
    ^
    (?P<date>\d{1,2}/\d{1,2}/\d{2,4})
    ,
    \s*
    (?P<time>\d{1,2}:\d{2})
    \s*-\s*
    (?P<sender>.*?)
    :
    \s*
    (?P<message>.*)
    $
    """,
    re.VERBOSE,
)

###############################################################################
# ATTENDANCE
###############################################################################

DONE_PATTERN: Pattern[str] = re.compile(
    r"^\s*done[.!?]*\s*$",
    re.IGNORECASE,
)

PRESENT_PATTERN: Pattern[str] = re.compile(
    r"^\s*present[.!?]*\s*$",
    re.IGNORECASE,
)

ABSENT_PATTERN: Pattern[str] = re.compile(
    r"^\s*absent[.!?]*\s*$",
    re.IGNORECASE,
)

LATE_PATTERN: Pattern[str] = re.compile(
    r"^\s*late[.!?]*\s*$",
    re.IGNORECASE,
)

###############################################################################
# SCRIPTURE READING
###############################################################################

#
# Scripture Reading announcement header.
#
# Supported examples:
#
#   SCRIPTURE READING
#   SCRIPTURES READING
#   SCRIPTURE READING FOR TODAY
#   SCRIPTURES READING FOR TODAY
#   SCRIPTURES READING FOR FRIDAY, JULY 24TH, 2026
#
# The pattern intentionally matches the announcement header only.
# Validation of the Bible portion is handled separately.
#

SCRIPTURE_READING_HEADER_PATTERN: Pattern[str] = re.compile(
    r"""
    ^
    \s*
    scriptures?
    \s+
    reading
    (?:
        \s+
        for
        \s+
        .*
    )?
    \s*
    $
    """,
    re.IGNORECASE | re.VERBOSE,
)

#
# Bible book names.
#
# Supports:
#
#   ACTS
#   PSALMS
#   GENESIS
#   1 CORINTHIANS
#   2 KINGS
#   1 JOHN
#
# The pattern is intentionally broad enough to support canonical
# Bible book names while requiring a chapter reference.
#

BIBLE_BOOK_PATTERN: Pattern[str] = re.compile(
    r"""
    (?:
        (?:
            1|2|3
        )
        \s+
    )?
    (?:
        genesis
        |exodus
        |leviticus
        |numbers
        |deuteronomy
        |joshua
        |judges
        |ruth
        |samuel
        |kings
        |chronicles
        |ezra
        |nehemiah
        |esther
        |job
        |psalms?
        |proverbs
        |ecclesiastes
        |song\s+of\s+solomon
        |isaiah
        |jeremiah
        |lamentations
        |ezekiel
        |daniel
        |hosea
        |joel
        |amos
        |obadiah
        |jonah
        |micah
        |nahum
        |habakkuk
        |zephaniah
        |haggai
        |zechariah
        |malachi
        |matthew
        |mark
        |luke
        |john
        |acts
        |romans
        |corinthians
        |galatians
        |ephesians
        |philippians
        |colossians
        |thessalonians
        |timothy
        |titus
        |philemon
        |hebrews
        |james
        |peter
        |jude
        |revelation
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

#
# Bible portion reference.
#
# Supported examples:
#
#   ACTS 28:17-31
#   PSALMS 30-31
#   GENESIS 1-3
#   MATTHEW 5:1-12
#   1 CORINTHIANS 13
#
# The pattern requires:
#
#   Bible book
#       +
#   chapter number
#       +
#   optional verse/range reference
#
#

BIBLE_PORTION_PATTERN: Pattern[str] = re.compile(
    rf"""
    \b
    {BIBLE_BOOK_PATTERN.pattern}
    \s+
    \d+
    (?:
        :
        \d+
        (?:
            -
            \d+
        )?
    )?
    (?:
        \s*
        ;
        \s*
        {BIBLE_BOOK_PATTERN.pattern}
        \s+
        \d+
        (?:
            :
            \d+
            (?:
                -
                \d+
            )?
        )?
    )*
    \b
    """,
    re.IGNORECASE | re.VERBOSE,
)

#
# Backward-compatible alias.
#
# Existing consumers may still import SCRIPTURE_READING_PATTERN.
# The pattern now represents the structured Scripture Reading header
# rather than a generic substring search.
#

SCRIPTURE_READING_PATTERN: Pattern[str] = SCRIPTURE_READING_HEADER_PATTERN

###############################################################################
# PRAYER
###############################################################################

OPENING_PRAYER_PATTERN: Pattern[str] = re.compile(
    r"^\s*opening\s+prayer\b",
    re.IGNORECASE,
)

CLOSING_PRAYER_PATTERN: Pattern[str] = re.compile(
    r"^\s*closing\s+prayers?\b",
    re.IGNORECASE,
)

###############################################################################
# MEDIA
###############################################################################

MEDIA_PATTERN: Pattern[str] = re.compile(
    r"<media omitted>",
    re.IGNORECASE,
)

IMAGE_PATTERN: Pattern[str] = re.compile(
    r"image omitted",
    re.IGNORECASE,
)

VIDEO_PATTERN: Pattern[str] = re.compile(
    r"video omitted",
    re.IGNORECASE,
)

STICKER_PATTERN: Pattern[str] = re.compile(
    r"sticker omitted",
    re.IGNORECASE,
)

###############################################################################
# SYSTEM MESSAGES
###############################################################################

SYSTEM_MESSAGE_PATTERN: Pattern[str] = re.compile(
    r"""
    (
        joined\ using\ this\ group's\ invite\ link
        |
        left
        |
        removed
        |
        added
        |
        changed\ the\ subject
        |
        changed\ this\ group's\ description
        |
        created\ group
        |
        changed\ the\ group\ icon
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

###############################################################################
# DELETED MESSAGE
###############################################################################

DELETED_MESSAGE_PATTERN: Pattern[str] = re.compile(
    r"this message was deleted",
    re.IGNORECASE,
)

###############################################################################
# END-TO-END ENCRYPTION NOTICE
###############################################################################

ENCRYPTION_NOTICE_PATTERN: Pattern[str] = re.compile(
    r"end-to-end encrypted",
    re.IGNORECASE,
)

###############################################################################
# PHONE NUMBERS
###############################################################################

PHONE_NUMBER_PATTERN: Pattern[str] = re.compile(
    r"\+?\d[\d\s()-]{7,20}",
)

###############################################################################
# URLS
###############################################################################

URL_PATTERN: Pattern[str] = re.compile(
    r"https?://\S+",
    re.IGNORECASE,
)

###############################################################################
# EMAIL
###############################################################################

EMAIL_PATTERN: Pattern[str] = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
)

###############################################################################
# WHITESPACE
###############################################################################

MULTIPLE_WHITESPACE_PATTERN: Pattern[str] = re.compile(
    r"\s+",
)

LEADING_TRAILING_WHITESPACE_PATTERN: Pattern[str] = re.compile(
    r"^\s+|\s+$",
)

###############################################################################
# EMPTY MESSAGE
###############################################################################

EMPTY_MESSAGE_PATTERN: Pattern[str] = re.compile(
    r"^\s*$",
)

###############################################################################
# NUMERIC
###############################################################################

INTEGER_PATTERN: Pattern[str] = re.compile(
    r"^\d+$",
)

###############################################################################
# PUNCTUATION
###############################################################################

ENDING_PUNCTUATION_PATTERN: Pattern[str] = re.compile(
    r"[.!?]+$",
)
