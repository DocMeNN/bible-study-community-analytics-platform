# tests/infrastructure/data_engine/test_validator.py

from datetime import datetime

import pytest

from src.domain.models.message import Message
from src.infrastructure.data_engine.exceptions import MalformedRecordError
from src.infrastructure.data_engine.models import CleanMessageRecord
from src.infrastructure.data_engine.validator import validate_records


def _record(
    sender: str = "John",
    timestamp: datetime | None = datetime(2026, 1, 1, 10, 0),
) -> CleanMessageRecord:
    return CleanMessageRecord(
        timestamp=timestamp,
        sender=sender,
        message="Hello",
        source_line=1,
        sender_is_phone_number=False,
        is_deleted_message=False,
        has_media_omitted=False,
    )


def test_validate_records_creates_domain_messages() -> None:
    result = validate_records([_record()])

    assert len(result) == 1
    assert isinstance(result[0], Message)
    assert result[0].sender == "John"


def test_validate_records_returns_empty_list_for_empty_input() -> None:
    assert validate_records([]) == []


def test_validate_records_rejects_missing_sender() -> None:
    with pytest.raises(MalformedRecordError):
        validate_records([_record(sender="")])


def test_validate_records_rejects_missing_timestamp() -> None:
    with pytest.raises(MalformedRecordError):
        validate_records([_record(timestamp=None)])
