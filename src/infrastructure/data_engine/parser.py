# src/infrastructure/data_engine/parser.py

"""
Parse canonical WhatsApp chat exports into infrastructure models.

This module converts raw text loaded from a canonical WhatsApp export
into immutable infrastructure models. It performs only structural
parsing and basic data validation.

Responsibilities
----------------
- Split the raw chat export into records.
- Validate the expected record structure.
- Parse timestamps.
- Create RawMessageRecord objects.

This module deliberately does NOT:

- normalize sender names
- normalize messages
- remove duplicates
- detect attendance
- detect activities
- create Domain models

Those responsibilities belong to cleaner.py and validator.py.
"""

from __future__ import annotations

import logging
from datetime import datetime

from .exceptions import (
    MalformedRecordError,
    ParsingError,
)
from .models import RawMessageRecord

__all__ = [
    "parse_chat",
]

logger = logging.getLogger(__name__)

_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_chat(raw_text: str) -> list[RawMessageRecord]:
    """
    Parse a canonical WhatsApp export.

    Parameters
    ----------
    raw_text
        Raw text returned by ``loader.load_chat()``.

    Returns
    -------
    list[RawMessageRecord]
        Parsed infrastructure records.

    Raises
    ------
    MalformedRecordError
        If a record does not contain the expected number of fields.

    ParsingError
        If a timestamp cannot be parsed.
    """
    logger.info("Beginning chat parsing.")

    records: list[RawMessageRecord] = []

    for line_number, line in enumerate(
        raw_text.splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        record = _parse_line(
            line=line,
            line_number=line_number,
        )

        records.append(record)

    logger.info(
        "Successfully parsed %d records.",
        len(records),
    )

    return records


def _parse_line(
    *,
    line: str,
    line_number: int,
) -> RawMessageRecord:
    """
    Parse a single chat record.

    Parameters
    ----------
    line
        One line from the canonical export.

    line_number
        Original line number in the source file.

    Returns
    -------
    RawMessageRecord
        Parsed infrastructure record.

    Raises
    ------
    MalformedRecordError
        If the record structure is invalid.

    ParsingError
        If the timestamp cannot be parsed.
    """
    parts = line.rstrip("\n").split(
        "\t",
        maxsplit=2,
    )

    _validate_field_count(
        parts=parts,
        line_number=line_number,
    )

    timestamp = _parse_timestamp(
        parts[0],
        line_number,
    )

    sender = parts[1].strip()
    message = parts[2]

    if not sender:
        raise MalformedRecordError(f"Missing sender on line {line_number}.")

    return RawMessageRecord(
        timestamp=timestamp,
        sender=sender,
        message=message,
        source_line=line_number,
    )


def _parse_timestamp(
    value: str,
    line_number: int,
) -> datetime:
    """
    Convert a timestamp string into a datetime object.

    Parameters
    ----------
    value
        Timestamp extracted from the chat export.

    line_number
        Source line number.

    Returns
    -------
    datetime
        Parsed timestamp.

    Raises
    ------
    ParsingError
        If the timestamp format is invalid.
    """
    try:
        return datetime.strptime(
            value.strip(),
            _TIMESTAMP_FORMAT,
        )

    except ValueError as exc:
        raise ParsingError(
            (f"Invalid timestamp '{value}' on line {line_number}.")
        ) from exc


def _validate_field_count(
    *,
    parts: list[str],
    line_number: int,
) -> None:
    """
    Validate the number of fields in a parsed record.

    A canonical WhatsApp export must contain exactly three fields:

        timestamp<TAB>sender<TAB>message

    Parameters
    ----------
    parts
        Fields extracted from a single line.

    line_number
        Original line number in the source file.

    Raises
    ------
    MalformedRecordError
        If the record does not contain exactly three fields.
    """
    expected_fields = 3
    actual_fields = len(parts)

    if actual_fields != expected_fields:
        raise MalformedRecordError(
            (
                f"Malformed record on line {line_number}. "
                f"Expected {expected_fields} fields but "
                f"found {actual_fields}."
            )
        )

    if not parts[0].strip():
        raise MalformedRecordError(f"Missing timestamp on line {line_number}.")

    if not parts[1].strip():
        raise MalformedRecordError(f"Missing sender on line {line_number}.")

    # The message field may legitimately be empty in some exports,
    # so we intentionally do not reject an empty message.


logger.info("Chat parser initialized successfully.")
