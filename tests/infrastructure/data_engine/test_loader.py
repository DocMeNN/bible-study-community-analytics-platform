# tests/infrastructure/data_engine/test_loader.py

from pathlib import Path

import pytest

from src.infrastructure.data_engine.exceptions import (
    FileLoadError,
    InvalidExportFormatError,
)
from src.infrastructure.data_engine.loader import load_chat


def test_load_chat_reads_utf8_text(tmp_path: Path) -> None:
    filepath = tmp_path / "chat.txt"
    filepath.write_text("content", encoding="utf-8")

    assert load_chat(filepath) == "content"


def test_load_chat_supports_bom(tmp_path: Path) -> None:
    filepath = tmp_path / "chat.txt"
    filepath.write_text("\ufeffcontent", encoding="utf-8")

    assert load_chat(filepath) == "content"


def test_load_chat_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileLoadError):
        load_chat(tmp_path / "missing.txt")


def test_load_chat_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(FileLoadError):
        load_chat(tmp_path)


def test_load_chat_rejects_non_txt_file(tmp_path: Path) -> None:
    filepath = tmp_path / "chat.csv"
    filepath.write_text("content", encoding="utf-8")

    with pytest.raises(InvalidExportFormatError):
        load_chat(filepath)


def test_load_chat_rejects_empty_file(tmp_path: Path) -> None:
    filepath = tmp_path / "chat.txt"
    filepath.write_text("", encoding="utf-8")

    with pytest.raises(FileLoadError):
        load_chat(filepath)
