# src/infrastructure/data_engine/validator.py

"""
Validate cleaned infrastructure records and convert them into Domain models.

This module represents the final stage of the Infrastructure Data Engine.
It validates structurally normalized records before transforming them
into immutable Domain models.

Responsibilities
----------------
- Validate cleaned infrastructure records.
- Convert infrastructure records into Domain models.
- Reject structurally invalid records.

This module intentionally performs NO business interpretation.

Business concepts such as attendance detection, activity
classification, session identification, and analytics belong
to the Domain layer.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable

from src.domain.models.message import Message

from .exceptions import MalformedRecordError
from .models import CleanMessageRecord

__all__ = [
    "validate_records",
]

logger = logging.getLogger(__name__)


def validate_records(
    records: Iterable[CleanMessageRecord],
) -> list[Message]:
    """
    Validate cleaned infrastructure records.

    Parameters
    ----------
    records
        Cleaned infrastructure records.

    Returns
    -------
    list[Message]
        Validated Domain Message objects.

    Raises
    ------
    MalformedRecordError
        If any record fails structural validation.
    """
    records = list(records)

    logger.info(
        "Validating %d cleaned records.",
        len(records),
    )

    messages = [_validate_record(record) for record in records]

    logger.info(
        "Successfully validated %d records.",
        len(messages),
    )

    return messages


def _validate_record(
    record: CleanMessageRecord,
) -> Message:
    """
    Validate a single cleaned record.

    Parameters
    ----------
    record
        Infrastructure record.

    Returns
    -------
    Message
        Domain model.

    Raises
    ------
    MalformedRecordError
        If required fields are missing.
    """
    if not record.sender:
        raise MalformedRecordError(f"Missing sender on line {record.source_line}.")

    if record.timestamp is None:
        raise MalformedRecordError(f"Missing timestamp on line {record.source_line}.")

    return _build_message(record)


def _build_message(
    record: CleanMessageRecord,
) -> Message:
    """
    Build a Domain Message from a validated infrastructure record.

    Parameters
    ----------
    record
        Validated infrastructure record.

    Returns
    -------
    Message
        Immutable Domain Message object.
    """
    try:
        return Message(
            timestamp=record.timestamp,
            sender=record.sender,
            content=record.message,
            line_number=record.source_line,
        )

    except ValueError as exc:
        raise MalformedRecordError(
            (f"Failed to create Message from line {record.source_line}: {exc}")
        ) from exc
