# tests/infrastructure/data_engine/test_parser.py

import pytest

from src.infrastructure.data_engine.exceptions import (
    MalformedRecordError,
    ParsingError,
)
from src.infrastructure.data_engine.parser import parse_chat


def test_parse_chat_parses_valid_record() -> None:
    raw_text = "2026-01-01 10:00:00\tJohn\tHello"

    records = parse_chat(raw_text)

    assert len(records) == 1
    assert records[0].sender == "John"
    assert records[0].message == "Hello"
    assert records[0].source_line == 1


def test_parse_chat_skips_blank_lines() -> None:
    raw_text = (
        "\n"
        "2026-01-01 10:00:00\tJohn\tHello\n"
        "\n"
    )

    records = parse_chat(raw_text)

    assert len(records) == 1


def test_parse_chat_preserves_tabs_inside_message() -> None:
    raw_text = "2026-01-01 10:00:00\tJohn\tHello\tWorld"

    records = parse_chat(raw_text)

    assert records[0].message == "Hello\tWorld"


def test_parse_chat_rejects_invalid_timestamp() -> None:
    raw_text = "invalid\tJohn\tHello"

    with pytest.raises(ParsingError):
        parse_chat(raw_text)


def test_parse_chat_rejects_missing_sender() -> None:
    raw_text = "2026-01-01 10:00:00\t\tHello"

    with pytest.raises(MalformedRecordError):
        parse_chat(raw_text)


def test_parse_chat_rejects_missing_fields() -> None:
    raw_text = "2026-01-01 10:00:00\tJohn"

    with pytest.raises(MalformedRecordError):
        parse_chat(raw_text)
