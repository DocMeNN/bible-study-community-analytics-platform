# tests/infrastructure/data_engine/test_cleaner.py

from datetime import datetime

from src.infrastructure.data_engine.cleaner import clean_records
from src.infrastructure.data_engine.models import RawMessageRecord


def _record(
    sender: str = "  John   Doe  ",
    message: str = "  Hello   world  ",
) -> RawMessageRecord:
    return RawMessageRecord(
        timestamp=datetime(2026, 1, 1, 10, 0),
        sender=sender,
        message=message,
        source_line=1,
    )


def test_clean_records_normalizes_sender() -> None:
    result = clean_records([_record()])

    assert result[0].sender == "John Doe"


def test_clean_records_normalizes_message() -> None:
    result = clean_records(
        [
            _record(
                message="  Hello   world\n\n  Second   line  ",
            )
        ]
    )

    assert result[0].message == "Hello world\nSecond line"


def test_clean_records_detects_phone_number() -> None:
    result = clean_records(
        [_record(sender="+2348061234567")]
    )

    assert result[0].sender_is_phone_number is True


def test_clean_records_detects_deleted_message() -> None:
    result = clean_records(
        [_record(message="This message was deleted")]
    )

    assert result[0].is_deleted_message is True


def test_clean_records_detects_media_placeholder() -> None:
    result = clean_records(
        [_record(message="<Media omitted>")]
    )

    assert result[0].has_media_omitted is True
