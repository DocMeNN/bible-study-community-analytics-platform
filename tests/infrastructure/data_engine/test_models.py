# tests/infrastructure/data_engine/test_models.py

from datetime import datetime

from src.infrastructure.data_engine.models import (
    CleanMessageRecord,
    RawMessageRecord,
)


def test_raw_message_record_is_immutable() -> None:
    record = RawMessageRecord(
        timestamp=datetime(2026, 1, 1, 10, 0),
        sender="John",
        message="Hello",
        source_line=1,
    )

    assert record.sender == "John"
    assert record.message == "Hello"
    assert record.source_line == 1


def test_clean_message_record_stores_metadata() -> None:
    record = CleanMessageRecord(
        timestamp=datetime(2026, 1, 1, 10, 0),
        sender="John",
        message="Hello",
        source_line=1,
        sender_is_phone_number=False,
        is_deleted_message=False,
        has_media_omitted=False,
    )

    assert record.sender == "John"
    assert record.sender_is_phone_number is False
    assert record.is_deleted_message is False
    assert record.has_media_omitted is False
