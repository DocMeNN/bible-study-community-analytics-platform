# tests/infrastructure/data_engine/test_whatsapp_parser.py

from datetime import datetime

from src.infrastructure.data_engine.whatsapp_parser import (
    parse_whatsapp_chat,
)


def test_parse_android_whatsapp_message() -> None:
    raw_text = "2/8/26, 11:02 - John: Hello"

    records = parse_whatsapp_chat(raw_text)

    assert len(records) == 1
    assert records[0].sender == "John"
    assert records[0].message == "Hello"


def test_parse_android_12_hour_message() -> None:
    raw_text = "2/8/26, 11:02 AM - John: Hello"

    records = parse_whatsapp_chat(raw_text)

    assert len(records) == 1
    assert records[0].sender == "John"


def test_parse_iphone_message() -> None:
    raw_text = "[08/02/2026, 11:02:15] John: Hello"

    records = parse_whatsapp_chat(raw_text)

    assert len(records) == 1
    assert records[0].sender == "John"
    assert records[0].message == "Hello"


def test_parse_multiline_message() -> None:
    raw_text = (
        "2/8/26, 11:02 - John: First line\n"
        "Second line\n"
        "Third line"
    )

    records = parse_whatsapp_chat(raw_text)

    assert len(records) == 1
    assert records[0].message == "First line\nSecond line\nThird line"


def test_parse_multiple_messages() -> None:
    raw_text = (
        "2/8/26, 11:02 - John: Hello\n"
        "2/8/26, 11:03 - Jane: Hi"
    )

    records = parse_whatsapp_chat(raw_text)

    assert len(records) == 2


def test_parse_ignores_system_messages() -> None:
    raw_text = (
        "2/8/26, 11:02 - Messages and calls are end-to-end encrypted. "
        "No one outside of this chat, not even WhatsApp, can read or listen "
        "to them.\n"
        "2/8/26, 11:03 - John: Hello"
    )

    records = parse_whatsapp_chat(raw_text)

    assert len(records) == 1
    assert records[0].sender == "John"
