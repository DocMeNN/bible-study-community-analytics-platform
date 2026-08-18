# src/application/services/import_service.py

"""
Import Application Service

Purpose
-------
Coordinates the complete WhatsApp chat import workflow.

Responsibilities
----------------
- Load a WhatsApp chat export.
- Delegate parsing.
- Clean parsed records.
- Validate cleaned records.
- Build multiple Session aggregates.
- Return a SessionCollection.

Architectural Rules
-------------------
- Orchestrates application workflow only.
- Contains no business logic.
- Contains no UI code.
- Contains no analytics.

Dependency Flow
---------------
Presentation
    ↓
ImportService
    ↓
MultiSessionBuilder
    ↓
SessionBuilder
    ↓
SessionCollection
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from pathlib import Path

# ============================================================================
# Local Imports
# ============================================================================
from src.application.builders.multi_session_builder import (
    MultiSessionBuilder,
)
from src.domain.models.session_collection import SessionCollection
from src.infrastructure.data_engine.cleaner import clean_records
from src.infrastructure.data_engine.exceptions import (
    InvalidExportFormatError,
)
from src.infrastructure.data_engine.loader import load_chat
from src.infrastructure.data_engine.models import RawMessageRecord
from src.infrastructure.data_engine.parser import parse_chat
from src.infrastructure.data_engine.validator import validate_records
from src.infrastructure.data_engine.whatsapp_parser import (
    parse_whatsapp_chat,
)

# ============================================================================
# Import Service
# ============================================================================


class ImportService:
    """
    Application service responsible for importing chat exports.
    """

    def __init__(
        self,
        multi_session_builder: MultiSessionBuilder | None = None,
    ) -> None:
        """
        Initialize the ImportService.
        """

        self._multi_session_builder = (
            multi_session_builder
            if multi_session_builder is not None
            else MultiSessionBuilder()
        )

    # =========================================================================
    # Import Workflow
    # =========================================================================

    def import_chat(
        self,
        filepath: str | Path,
    ) -> SessionCollection:
        """
        Import a chat export and build multiple Sessions.
        """

        raw_text = load_chat(
            filepath,
        )

        parsed_records = self._parse_records(
            raw_text,
        )

        cleaned_records = clean_records(
            parsed_records,
        )

        messages = validate_records(
            cleaned_records,
        )

        if not messages:
            raise ValueError(
                "No valid messages were found in the chat export.",
            )

        return self._multi_session_builder.build(
            messages,
        )

    # =========================================================================
    # Parser Selection
    # =========================================================================

    def _parse_records(
        self,
        raw_text: str,
    ) -> list[RawMessageRecord]:
        """
        Parse records.

        Native WhatsApp exports are attempted first.

        If the input is not a supported WhatsApp export,
        fall back to the canonical parser.
        """

        try:
            return parse_whatsapp_chat(
                raw_text,
            )

        except InvalidExportFormatError:
            return parse_chat(
                raw_text,
            )

    # =========================================================================
    # Service Accessor
    # =========================================================================

    @property
    def multi_session_builder(
        self,
    ) -> MultiSessionBuilder:
        """
        Return the MultiSessionBuilder.
        """

        return self._multi_session_builder

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(
        self,
    ) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"multi_session_builder="
            f"{self.multi_session_builder.__class__.__name__})"
        )

    def __str__(
        self,
    ) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
