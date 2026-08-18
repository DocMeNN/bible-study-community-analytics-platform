# src/infrastructure/data_engine/loader.py

"""
Load WhatsApp chat exports from disk.

This module is responsible only for reading chat export files from the
filesystem. It performs no parsing, normalization, validation, or
business logic.

Responsibilities
----------------
- Validate the input path.
- Validate the file type.
- Read the file using UTF-8 (with BOM support).
- Return the raw text exactly as stored in the file.

The returned text is consumed by ``parser.py``.
"""

from __future__ import annotations

import logging
from pathlib import Path

from .exceptions import FileLoadError, InvalidExportFormatError

__all__ = [
    "load_chat",
]

logger = logging.getLogger(__name__)


def load_chat(filepath: str | Path) -> str:
    """
    Load a WhatsApp chat export into memory.

    Parameters
    ----------
    filepath
        Path to the exported chat text file.

    Returns
    -------
    str
        Raw file contents.

    Raises
    ------
    FileLoadError
        If the file cannot be found or read.

    InvalidExportFormatError
        If the supplied file is not a supported text export.
    """
    path = Path(filepath)

    logger.info("Loading WhatsApp export: %s", path)

    if not path.exists():
        raise FileLoadError(f"Chat export not found: '{path}'.")

    if not path.is_file():
        raise FileLoadError(f"Expected a file but received: '{path}'.")

    if path.suffix.lower() != ".txt":
        raise InvalidExportFormatError(
            f"Unsupported file type '{path.suffix}'. Expected a '.txt' export."
        )

    try:
        raw_text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise FileLoadError(f"Unable to read chat export: '{path}'.") from exc

    if not raw_text.strip():
        raise FileLoadError("The chat export is empty.")

    logger.info(
        "Successfully loaded chat export (%d characters).",
        len(raw_text),
    )

    return raw_text
