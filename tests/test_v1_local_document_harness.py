"""Tests for the V1 local document harness candidate path."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest

from lima.contracts.guardian import (
    ConsequentialActionType,
    GuardianDecision,
    GuardianDecisionStatus,
)
from lima.guardian.v1_decision_gate import review_v1_runtime_request
from lima.harness.v1_local_document_harness import (
    V1LocalDocumentHarnessError,
    build_v1_local_document_request,
    inspect_v1_local_document,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "lima" / "harness" / "v1_local_document_harness.py"
INSTALLER_PATH = REPO_ROOT / "scripts" / "install_lima_ai_os_candidate.ps1"
DOWNLOADER_PATH = REPO_ROOT / "scripts" / "download_lima_ai_os_candidate.ps1"
QUICKSTART_PATH = (
    REPO_ROOT
    / "docs"
    / "readiness"
    / "V1_LOCAL_INSTALL_AND_DOCUMENT_HARNESS_QUICKSTART.md"
)


def _decision(path: Path) -> GuardianDecision:
    request = build_v1_local_document_request(path)
    return review_v1_runtime_request(request)


def test_text_document_is_inspected_read_only(tmp_path: Path) -> None:
    document = tmp_path / "sample.txt"
    document.write_text("Account note\nDocument intake test\n", encoding="utf-8")

    record = inspect_v1_local_document(
        document,
        guardian_decision=_decision(document),
        allowed_root=tmp_path,
    )

    assert record["record_type"] == "v1_local_document_harness_result"
    assert record["candidate_only"] is True
    assert record["local_only"] is True
    assert record["guardian_gated"] is True
    assert record["read_only"] is True
    assert record["file_read"] is True
    assert record["file_written"] is False
    assert record["file_deleted"] is False
    assert record["file_mutated"] is False
    assert record["execution_allowed"] is False
    assert record["side_effects_allowed"] is False
    assert record["provider_called"] is False
    assert record["network_action_executed"] is False
    assert "Document intake test" in record["preview_text"]
    assert len(record["sha256"]) == 64
    assert record["record_hash"]


def test_docx_document_uses_stdlib_xml_preview(tmp_path: Path) -> None:
    document = tmp_path / "sample.docx"
    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body><w:p><w:r><w:t>Hello local docx harness</w:t></w:r></w:p></w:body>"
        "</w:document>"
    )
    with zipfile.ZipFile(document, "w") as archive:
        archive.writestr("word/document.xml", xml)

    record = inspect_v1_local_document(
        document,
        guardian_decision=_decision(document),
        allowed_root=tmp_path,
    )

    assert record["extension"] == ".docx"
    assert record["parser"] == "docx_xml_text"
    assert "Hello local docx harness" in record["preview_text"]


def test_pdf_document_returns_metadata_without_text_extraction(tmp_path: Path) -> None:
    document = tmp_path / "sample.pdf"
    document.write_bytes(b"%PDF-1.4\n1 0 obj\n<< /Type /Page >>\nendobj\n%%EOF\n")

    record = inspect_v1_local_document(
        document,
        guardian_decision=_decision(document),
        allowed_root=tmp_path,
    )

    assert record["extension"] == ".pdf"
    assert record["parser"] == "pdf_metadata"
    assert "page markers detected: 1" in record["preview_text"]


def test_guardian_preflight_is_required(tmp_path: Path) -> None:
    document = tmp_path / "sample.txt"
    document.write_text("blocked", encoding="utf-8")
    request = build_v1_local_document_request(document)
    denied = GuardianDecision(
        decision_id="v1-decision:denied",
        request_id=request.request_id,
        intent_id=request.intent_id,
        input_id=request.input_id,
        actor_id=request.actor_id,
        shell_id=request.shell_id,
        action_type=ConsequentialActionType.FILE_OPERATION,
        target_ref=request.target_ref,
        risk_class="read_only",
        status=GuardianDecisionStatus.DENIED,
        approval_level=None,
        constraints={
            "v1_preflight_only": True,
            "execution_allowed": False,
            "side_effects_allowed": False,
            "approval_token_issued": False,
        },
    )

    with pytest.raises(V1LocalDocumentHarnessError, match="must be approved"):
        inspect_v1_local_document(document, guardian_decision=denied)


def test_allowed_root_is_enforced(tmp_path: Path) -> None:
    inside = tmp_path / "inside"
    outside = tmp_path / "outside"
    inside.mkdir()
    outside.mkdir()
    document = outside / "sample.txt"
    document.write_text("outside", encoding="utf-8")

    with pytest.raises(V1LocalDocumentHarnessError, match="inside allowed_root"):
        inspect_v1_local_document(
            document,
            guardian_decision=_decision(document),
            allowed_root=inside,
        )


def test_cli_outputs_json_record(tmp_path: Path) -> None:
    document = tmp_path / "sample.md"
    document.write_text("# Local Harness\nCLI path\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "lima.harness.v1_local_document_harness",
            "--path",
            str(document),
            "--allowed-root",
            str(tmp_path),
        ],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["record_type"] == "v1_local_document_harness_result"
    assert payload["decision_id"].startswith("v1-decision:")
    assert "CLI path" in payload["preview_text"]


def test_module_preserves_candidate_boundaries() -> None:
    module_text = MODULE_PATH.read_text(encoding="utf-8").lower()
    forbidden_patterns = [
        "import requests",
        "import urllib",
        "import socket",
        "import webbrowser",
        "import openai",
        "from openai",
        "eval(",
        "exec(",
        "subprocess.",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in module_text
    assert "file_written" in module_text
    assert "provider_called" in module_text
    assert "product_ready" in module_text


def test_installer_downloader_and_quickstart_exist_with_blocked_boundaries() -> None:
    assert INSTALLER_PATH.exists()
    assert DOWNLOADER_PATH.exists()
    assert QUICKSTART_PATH.exists()
    combined = (
        INSTALLER_PATH.read_text(encoding="utf-8")
        + DOWNLOADER_PATH.read_text(encoding="utf-8")
        + QUICKSTART_PATH.read_text(encoding="utf-8")
    )
    assert "CANDIDATE_ONLY" in combined
    assert "production readiness" in combined.lower()
    assert "product readiness" in combined.lower()
    assert "v1_local_document_harness" in combined
