# src/infrastructure/data_engine/whatsapp_parser.py

"""
WhatsApp Export Parser

Purpose
-------
Parses native WhatsApp exported chat files into
RawMessageRecord objects.

Unlike parser.py, which parses the project's canonical
tab-separated intermediate format, this module understands
the text format produced directly by WhatsApp.

Supported Formats
-----------------
Android

    2/8/26, 11:02 - John: Hello

    2/8/26, 11:02 AM - John: Hello

iPhone

    [08/02/2026, 11:02:15] John: Hello

New WhatsApp

    [1/12/2022, 9:08:52 PM] John: Hello

Responsibilities
----------------
- Detect WhatsApp record boundaries.
- Merge multiline messages.
- Parse timestamps.
- Extract sender names.
- Ignore WhatsApp system events.
- Create RawMessageRecord objects.

This module intentionally does NOT

- Detect attendance
- Detect activities
- Apply business rules
- Create Domain models
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
import logging
import re
from datetime import datetime

# ============================================================================
# Local Imports
# ============================================================================
from .exceptions import (
    InvalidExportFormatError,
    ParsingError,
)
from .models import RawMessageRecord

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "parse_whatsapp_chat",
]

# ============================================================================
# Logging
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# Unicode Normalization
# ============================================================================

#
# Modern WhatsApp exports contain several Unicode whitespace
# characters that visually resemble normal spaces but prevent
# regex matching.
#

UNICODE_TRANSLATION = str.maketrans(
    {
        "\u202f": " ",  # Narrow no-break space
        "\u00a0": " ",  # Non-breaking space
        "\u200e": "",  # Left-to-right mark
        "\u200f": "",  # Right-to-left mark
        "\u2060": "",  # Word joiner
        "\ufeff": "",  # BOM
    }
)

# ============================================================================
# Record Detection
# ============================================================================

ANDROID_RECORD_START_PATTERN = re.compile(
    r"""
^
\d{1,2}/\d{1,2}/\d{2,4},
\s*
\d{1,2}:\d{2}
(?::\d{2})?
(?:\s?(?:AM|PM|am|pm))?
\s*-\s*
""",
    re.VERBOSE,
)

IPHONE_RECORD_START_PATTERN = re.compile(
    r"""
^\[
\d{1,2}/\d{1,2}/\d{2,4},
\s*
\d{1,2}:\d{2}
(?::\d{2})?
(?:\s?(?:AM|PM|am|pm))?
\]
\s*
""",
    re.VERBOSE,
)

# ============================================================================
# User Message Patterns
# ============================================================================

ANDROID_MESSAGE_PATTERN = re.compile(
    r"""
^
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s*
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
(?:\s?(?P<ampm>AM|PM|am|pm))?
\s*-\s*
(?P<sender>.+?)
:
\s?
(?P<message>.*)
$
""",
    re.VERBOSE | re.DOTALL,
)

IPHONE_MESSAGE_PATTERN = re.compile(
    r"""
^\[
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s*
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
(?:\s?(?P<ampm>AM|PM|am|pm))?
\]
\s*
(?P<sender>.+?)
:
\s?
(?P<message>.*)
$
""",
    re.VERBOSE | re.DOTALL,
)

# ============================================================================
# System Message Patterns
# ============================================================================

ANDROID_SYSTEM_PATTERN = re.compile(
    r"""
^
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s*
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
(?:\s?(?P<ampm>AM|PM|am|pm))?
\s*-\s*
(?P<message>.+)
$
""",
    re.VERBOSE | re.DOTALL,
)

IPHONE_SYSTEM_PATTERN = re.compile(
    r"""
^\[
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s*
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
(?:\s?(?P<ampm>AM|PM|am|pm))?
\]
\s*
(?P<message>.+)
$
""",
    re.VERBOSE | re.DOTALL,
)

# ============================================================================
# Known WhatsApp System Keywords
# ============================================================================

SYSTEM_KEYWORDS = (
    "messages and calls are end-to-end encrypted",
    "created this group",
    "changed the group description",
    "changed the group icon",
    "changed this group's icon",
    "joined using a group link",
    "added",
    "removed",
    "left",
    "was added",
    "was removed",
    "security code changed",
    "you joined",
    "you were added",
)

# ============================================================================
# Public API
# ============================================================================


def parse_whatsapp_chat(
    raw_text: str,
) -> list[RawMessageRecord]:
    """
    Parse a native WhatsApp export.

    Parameters
    ----------
    raw_text:
        Raw WhatsApp export text.

    Returns
    -------
    list[RawMessageRecord]
    """

    logger.info("Parsing WhatsApp export.")

    raw_text = _normalize_text(raw_text)

    logical_messages = _build_logical_messages(raw_text)

    if not logical_messages:
        raise InvalidExportFormatError("No WhatsApp messages were detected.")

    records: list[RawMessageRecord] = []

    for line_number, message in logical_messages:
        record = _parse_message(
            message=message,
            line_number=line_number,
        )

        if record is not None:
            records.append(record)

    logger.info(
        "Successfully parsed %d WhatsApp messages.",
        len(records),
    )

    return records


# ============================================================================
# Message Builder
# ============================================================================


def _build_logical_messages(
    raw_text: str,
) -> list[tuple[int, str]]:
    """
    Build logical WhatsApp records.

    Every record begins with a timestamp.

    Any following lines belong to that record until another
    timestamp is encountered.

    This implementation also tolerates malformed lines before
    the first valid WhatsApp record.
    """

    logical_messages: list[tuple[int, str]] = []

    current_lines: list[str] = []
    current_line_number: int | None = None

    for line_number, raw_line in enumerate(
        raw_text.splitlines(),
        start=1,
    ):
        line = raw_line.rstrip()

        #
        # Ignore completely blank lines before a record.
        #
        if not current_lines and not line.strip():
            continue

        #
        # New WhatsApp record detected.
        #
        if _starts_new_message(line):
            if current_lines:
                logical_messages.append(
                    (
                        current_line_number or line_number,
                        "\n".join(current_lines),
                    )
                )

            current_lines = [line]
            current_line_number = line_number

            continue

        #
        # Ignore malformed preamble before the first record.
        #
        if not current_lines:
            logger.debug(
                "Ignoring non-record line %d.",
                line_number,
            )

            continue

        #
        # Continuation of previous message.
        #
        current_lines.append(line)

    if current_lines:
        logical_messages.append(
            (
                current_line_number or 1,
                "\n".join(current_lines),
            )
        )

    logger.debug(
        "Built %d logical WhatsApp records.",
        len(logical_messages),
    )

    return logical_messages


# ============================================================================
# Record Detection
# ============================================================================


def _starts_new_message(
    line: str,
) -> bool:
    """
    Determine whether a line begins a WhatsApp record.
    """

    line = line.translate(UNICODE_TRANSLATION)

    return bool(
        ANDROID_RECORD_START_PATTERN.match(line)
        or IPHONE_RECORD_START_PATTERN.match(line)
    )


# ============================================================================
# Text Normalization
# ============================================================================


def _normalize_text(
    raw_text: str,
) -> str:
    """
    Normalize exported WhatsApp text.

    Modern WhatsApp exports include invisible Unicode
    formatting characters that interfere with parsing.

    This function removes them before parsing begins.
    """

    return raw_text.translate(
        UNICODE_TRANSLATION,
    )


# ============================================================================
# Record Parser
# ============================================================================


def _parse_message(
    *,
    message: str,
    line_number: int,
) -> RawMessageRecord | None:
    """
    Parse a logical WhatsApp record.

    Returns
    -------
    RawMessageRecord
        Parsed user message.

    None
        WhatsApp system message.
    """

    message = message.translate(
        UNICODE_TRANSLATION,
    )

    #
    # Android user message
    #

    match = ANDROID_MESSAGE_PATTERN.match(message)

    if match is not None:
        return _build_record(
            match=match,
            line_number=line_number,
        )

    #
    # iPhone user message
    #

    match = IPHONE_MESSAGE_PATTERN.match(message)

    if match is not None:
        return _build_record(
            match=match,
            line_number=line_number,
        )

    #
    # Android system event
    #

    match = ANDROID_SYSTEM_PATTERN.match(message)

    if match is not None:
        if _is_system_message(
            match.group("message"),
        ):
            logger.debug(
                "Ignoring Android system event on line %d.",
                line_number,
            )

            return None

    #
    # iPhone system event
    #

    match = IPHONE_SYSTEM_PATTERN.match(message)

    if match is not None:
        if _is_system_message(
            match.group("message"),
        ):
            logger.debug(
                "Ignoring iPhone system event on line %d.",
                line_number,
            )

            return None

    #
    # Unknown record.
    #
    # Do NOT abort the entire import because one record
    # could not be parsed.
    #

    logger.warning(
        "Skipping malformed WhatsApp record on line %d.",
        line_number,
    )

    return None


# ============================================================================
# Record Builder
# ============================================================================


def _build_record(
    *,
    match: re.Match[str],
    line_number: int,
) -> RawMessageRecord:
    """
    Build RawMessageRecord from regex match.
    """

    timestamp = _parse_timestamp(
        date_text=match.group("date"),
        time_text=match.group("time"),
        ampm=match.groupdict().get("ampm"),
        line_number=line_number,
    )

    sender = match.group("sender").strip()

    message = match.group("message").strip()

    return RawMessageRecord(
        timestamp=timestamp,
        sender=sender,
        message=message,
        source_line=line_number,
    )


# ============================================================================
# System Message Detection
# ============================================================================


def _is_system_message(
    text: str,
) -> bool:
    """
    Determine whether a parsed record is a WhatsApp
    system-generated event.

    This allows us to ignore events without relying
    solely on regex structure.
    """

    normalized = text.casefold()

    return any(keyword in normalized for keyword in SYSTEM_KEYWORDS)


# ============================================================================
# Timestamp Parsing
# ============================================================================


def _parse_timestamp(
    *,
    date_text: str,
    time_text: str,
    ampm: str | None,
    line_number: int,
) -> datetime:
    """
    Parse a WhatsApp timestamp.

    Supports:

    - DD/MM/YY
    - DD/MM/YYYY
    - MM/DD/YY
    - MM/DD/YYYY
    - 24-hour time
    - 12-hour time
    - Optional seconds
    """

    timestamp = f"{date_text} {time_text}"

    if ampm:
        timestamp += f" {ampm.upper()}"

    formats = (
        # -----------------------------------------------------------------
        # Month / Day
        # -----------------------------------------------------------------
        "%m/%d/%y %H:%M",
        "%m/%d/%Y %H:%M",
        "%m/%d/%y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%y %I:%M %p",
        "%m/%d/%Y %I:%M %p",
        "%m/%d/%y %I:%M:%S %p",
        "%m/%d/%Y %I:%M:%S %p",
        # -----------------------------------------------------------------
        # Day / Month
        # -----------------------------------------------------------------
        "%d/%m/%y %H:%M",
        "%d/%m/%Y %H:%M",
        "%d/%m/%y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%y %I:%M %p",
        "%d/%m/%Y %I:%M %p",
        "%d/%m/%y %I:%M:%S %p",
        "%d/%m/%Y %I:%M:%S %p",
    )

    for fmt in formats:
        try:
            return datetime.strptime(
                timestamp,
                fmt,
            )

        except ValueError:
            continue

    raise ParsingError(
        (f"Unable to parse timestamp '{timestamp}' on line {line_number}.")
    )


# ============================================================================
# Module Initialization
# ============================================================================

logger.info("WhatsApp parser initialized successfully.")
