# tests/application/services/test_import_service.py

"""
ImportService Application Service Tests

Purpose:
    Verify the complete chat import orchestration workflow.

Coverage:
    - Service construction.
    - DashboardService dependency injection.
    - Native WhatsApp parser selection.
    - Canonical parser fallback.
    - Complete import workflow.
    - Empty import validation.
    - Session construction.
    - Service accessor.
    - Dunder methods.

Rules:
    - Test application orchestration only.
    - Do not duplicate parser tests.
    - Do not duplicate cleaner tests.
    - Do not duplicate validator tests.
    - Do not test Domain business rules.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest

from src.application.services.dashboard_service import DashboardService
from src.application.services.import_service import ImportService
from src.domain.models.message import Message
from src.domain.models.session import Session
from src.infrastructure.data_engine.exceptions import InvalidExportFormatError
from src.infrastructure.data_engine.models import RawMessageRecord

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def import_service() -> ImportService:
    """Return a default ImportService."""

    return ImportService()


@pytest.fixture
def dashboard_service() -> DashboardService:
    """Return a DashboardService."""

    return DashboardService()


@pytest.fixture
def raw_record() -> RawMessageRecord:
    """Return a representative raw message record."""

    return RawMessageRecord(
        timestamp=datetime(
            2026,
            7,
            23,
            8,
            0,
        ),
        sender="Alice",
        message="Scripture Reading",
        source_line=1,
    )


@pytest.fixture
def message() -> Message:
    """Return a representative validated Message."""

    return Message(
        timestamp=datetime(
            2026,
            7,
            23,
            8,
            0,
        ),
        sender="Alice",
        content="Scripture Reading",
        line_number=1,
    )


# ============================================================================
# Construction
# ============================================================================


class TestImportServiceConstruction:
    """Test ImportService construction."""

    def test_default_construction(
        self,
        import_service: ImportService,
    ) -> None:
        """Default construction creates a DashboardService."""

        assert isinstance(
            import_service.dashboard_service,
            DashboardService,
        )

    def test_dependency_injection_preserves_dashboard_service(
        self,
        dashboard_service: DashboardService,
    ) -> None:
        """Injected DashboardService is preserved."""

        service = ImportService(
            dashboard_service=dashboard_service,
        )

        assert service.dashboard_service is dashboard_service


# ============================================================================
# Parser Selection
# ============================================================================


class TestParserSelection:
    """Test parser selection orchestration."""

    def test_native_parser_is_used_when_supported(
        self,
        import_service: ImportService,
        raw_record: RawMessageRecord,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Native WhatsApp parser is attempted first."""

        native_parser = Mock(
            return_value=[raw_record],
        )

        fallback_parser = Mock()

        monkeypatch.setattr(
            "src.application.services.import_service.parse_whatsapp_chat",
            native_parser,
        )

        monkeypatch.setattr(
            "src.application.services.import_service.parse_chat",
            fallback_parser,
        )

        result = import_service._parse_records(
            "native export",
        )

        assert result == [raw_record]

        native_parser.assert_called_once_with(
            "native export",
        )

        fallback_parser.assert_not_called()

    def test_canonical_parser_is_used_when_native_parser_fails(
        self,
        import_service: ImportService,
        raw_record: RawMessageRecord,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Canonical parser is used after native format failure."""

        native_parser = Mock(
            side_effect=InvalidExportFormatError(
                "Unsupported export format",
            ),
        )

        fallback_parser = Mock(
            return_value=[raw_record],
        )

        monkeypatch.setattr(
            "src.application.services.import_service.parse_whatsapp_chat",
            native_parser,
        )

        monkeypatch.setattr(
            "src.application.services.import_service.parse_chat",
            fallback_parser,
        )

        result = import_service._parse_records(
            "canonical export",
        )

        assert result == [raw_record]

        native_parser.assert_called_once_with(
            "canonical export",
        )

        fallback_parser.assert_called_once_with(
            "canonical export",
        )


# ============================================================================
# Import Workflow
# ============================================================================


class TestImportWorkflow:
    """Test complete import workflow."""

    def test_import_chat_returns_session(
        self,
        import_service: ImportService,
        message: Message,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """import_chat returns a Session."""

        monkeypatch.setattr(
            "src.application.services.import_service.load_chat",
            Mock(
                return_value="chat text",
            ),
        )

        monkeypatch.setattr(
            import_service,
            "_parse_records",
            Mock(
                return_value=["parsed"],
            ),
        )

        monkeypatch.setattr(
            "src.application.services.import_service.clean_records",
            Mock(
                return_value=["cleaned"],
            ),
        )

        monkeypatch.setattr(
            "src.application.services.import_service.validate_records",
            Mock(
                return_value=[message],
            ),
        )

        result = import_service.import_chat(
            "chat.txt",
        )

        assert isinstance(
            result,
            Session,
        )

    def test_import_chat_uses_first_message_date(
        self,
        import_service: ImportService,
        message: Message,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Session date is derived from the first validated message."""

        dashboard_service = Mock(
            spec=DashboardService,
        )

        service = ImportService(
            dashboard_service=dashboard_service,
        )

        monkeypatch.setattr(
            "src.application.services.import_service.load_chat",
            Mock(
                return_value="chat text",
            ),
        )

        monkeypatch.setattr(
            service,
            "_parse_records",
            Mock(
                return_value=["parsed"],
            ),
        )

        monkeypatch.setattr(
            "src.application.services.import_service.clean_records",
            Mock(
                return_value=["cleaned"],
            ),
        )

        monkeypatch.setattr(
            "src.application.services.import_service.validate_records",
            Mock(
                return_value=[message],
            ),
        )

        expected_session = Session(
            session_date=message.timestamp.date(),
        )

        dashboard_service.build_session.return_value = expected_session

        result = service.import_chat(
            "chat.txt",
        )

        assert result is expected_session

        dashboard_service.build_session.assert_called_once_with(
            session_date=message.timestamp.date(),
            messages=[message],
        )

    def test_import_chat_executes_pipeline_in_order(
        self,
        import_service: ImportService,
        message: Message,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Import workflow passes each stage's result to the next stage."""

        load_chat = Mock(
            return_value="raw text",
        )

        parse_records = Mock(
            return_value=["parsed"],
        )

        clean_records = Mock(
            return_value=["cleaned"],
        )

        validate_records = Mock(
            return_value=[message],
        )

        monkeypatch.setattr(
            "src.application.services.import_service.load_chat",
            load_chat,
        )

        monkeypatch.setattr(
            import_service,
            "_parse_records",
            parse_records,
        )

        monkeypatch.setattr(
            "src.application.services.import_service.clean_records",
            clean_records,
        )

        monkeypatch.setattr(
            "src.application.services.import_service.validate_records",
            validate_records,
        )

        import_service.import_chat(
            "chat.txt",
        )

        load_chat.assert_called_once_with(
            "chat.txt",
        )

        parse_records.assert_called_once_with(
            "raw text",
        )

        clean_records.assert_called_once_with(
            ["parsed"],
        )

        validate_records.assert_called_once_with(
            ["cleaned"],
        )

    def test_import_chat_accepts_path(
        self,
        import_service: ImportService,
        message: Message,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """import_chat accepts a pathlib.Path."""

        filepath = tmp_path / "chat.txt"

        monkeypatch.setattr(
            "src.application.services.import_service.load_chat",
            Mock(
                return_value="chat text",
            ),
        )

        monkeypatch.setattr(
            import_service,
            "_parse_records",
            Mock(
                return_value=["parsed"],
            ),
        )

        monkeypatch.setattr(
            "src.application.services.import_service.clean_records",
            Mock(
                return_value=["cleaned"],
            ),
        )

        monkeypatch.setattr(
            "src.application.services.import_service.validate_records",
            Mock(
                return_value=[message],
            ),
        )

        result = import_service.import_chat(
            filepath,
        )

        assert isinstance(
            result,
            Session,
        )


# ============================================================================
# Empty Import
# ============================================================================


class TestEmptyImport:
    """Test empty import handling."""

    def test_empty_validated_messages_raise_value_error(
        self,
        import_service: ImportService,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Empty validated message collections are rejected."""

        monkeypatch.setattr(
            "src.application.services.import_service.load_chat",
            Mock(
                return_value="chat text",
            ),
        )

        monkeypatch.setattr(
            import_service,
            "_parse_records",
            Mock(
                return_value=["parsed"],
            ),
        )

        monkeypatch.setattr(
            "src.application.services.import_service.clean_records",
            Mock(
                return_value=["cleaned"],
            ),
        )

        monkeypatch.setattr(
            "src.application.services.import_service.validate_records",
            Mock(
                return_value=[],
            ),
        )

        with pytest.raises(
            ValueError,
            match="No valid messages were found",
        ):
            import_service.import_chat(
                "chat.txt",
            )


# ============================================================================
# Service Accessor
# ============================================================================


class TestServiceAccessor:
    """Test service accessors."""

    def test_dashboard_service_accessor(
        self,
        import_service: ImportService,
    ) -> None:
        """dashboard_service returns the configured service."""

        assert isinstance(
            import_service.dashboard_service,
            DashboardService,
        )


# ============================================================================
# Dunder Methods
# ============================================================================


class TestDunderMethods:
    """Test ImportService dunder methods."""

    def test_repr_contains_service_name(
        self,
        import_service: ImportService,
    ) -> None:
        """repr contains ImportService."""

        assert "ImportService" in repr(
            import_service,
        )

    def test_repr_contains_dashboard_service_name(
        self,
        import_service: ImportService,
    ) -> None:
        """repr identifies DashboardService."""

        assert "DashboardService" in repr(
            import_service,
        )

    def test_str_matches_repr(
        self,
        import_service: ImportService,
    ) -> None:
        """str and repr return the same representation."""

        assert str(
            import_service,
        ) == repr(
            import_service,
        )
