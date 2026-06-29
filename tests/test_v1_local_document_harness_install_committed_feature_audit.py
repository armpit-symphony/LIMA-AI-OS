"""Static checks for the committed V1 local document harness/install audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_local_document_harness_install_committed_feature_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_local_document_harness_install_audit_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_local_document_harness_install_committed_feature_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["observed_lima_commit"] == (
        "bc63ed3b00055976b1728d80124137d7ce15d871"
    )
    assert fixture["audit_verdict"] == (
        "PASS_COMMITTED_LOCAL_DOCUMENT_HARNESS_INSTALL_CANDIDATE_ONLY_CUTOVER_STILL_BLOCKED"
    )
    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_local_document_harness_install_artifacts_are_committed_candidate_only() -> None:
    artifacts = _load_fixture()["committed_artifacts"]

    assert [artifact["path"] for artifact in artifacts] == [
        "docs/readiness/V1_LOCAL_INSTALL_AND_DOCUMENT_HARNESS_QUICKSTART.md",
        "lima/harness/v1_local_document_harness.py",
        "scripts/download_lima_ai_os_candidate.ps1",
        "scripts/install_lima_ai_os_candidate.ps1",
        "tests/test_v1_local_document_harness.py",
    ]
    for artifact in artifacts:
        assert artifact["git_state"] == "tracked"
        assert "candidate" in artifact["release_proof_treatment"] or (
            artifact["release_proof_treatment"] == "operator_run_dry_run_first"
        )
        assert (REPO_ROOT / artifact["path"]).exists(), artifact["path"]


def test_v1_local_document_harness_guardian_and_runtime_boundaries() -> None:
    fixture = _load_fixture()
    guardian = fixture["guardian_boundary"]
    runtime = fixture["runtime_boundary"]

    assert guardian == {
        "request_action_type": "FILE_OPERATION",
        "risk_class": "read_only",
        "requested_tool_pack": "files",
        "requires_review_v1_runtime_request": True,
        "requires_guardian_decision_status": "APPROVED",
        "requires_v1_preflight_only": True,
        "requires_execution_allowed_false": True,
        "requires_side_effects_allowed_false": True,
        "requires_approval_token_issued_false": True,
        "requires_allowed_tool_packs_empty": True,
    }
    assert runtime["file_read"] is True
    for key in (
        "file_written",
        "file_deleted",
        "file_mutated",
        "provider_model_routed",
        "provider_called",
        "network_action_executed",
        "connector_invoked",
        "audit_persisted",
        "product_ready",
    ):
        assert runtime[key] is False, key
    assert runtime["preview_bounded"] is True
    assert runtime["default_max_bytes"] == 2_000_000
    assert runtime["default_max_preview_chars"] == 1200
    assert runtime["supported_extensions"] == [
        ".csv",
        ".docx",
        ".html",
        ".htm",
        ".json",
        ".log",
        ".md",
        ".pdf",
        ".txt",
        ".xml",
    ]


def test_v1_local_document_harness_installer_downloader_boundaries() -> None:
    boundary = _load_fixture()["installer_downloader_boundary"]

    assert boundary["downloader_network_capable_unless_dry_run"] is True
    assert boundary["downloader_uses_invoke_webrequest"] is True
    assert boundary["installer_writes_install_root_unless_dry_run"] is True
    assert boundary["installer_uses_pip_install_editable"] is True
    assert boundary["installer_uses_no_deps_by_default"] is True
    assert boundary["audit_executes_downloader"] is False
    assert boundary["audit_executes_installer"] is False


def test_v1_local_document_harness_install_records_validation_evidence() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_result"] == "passed_20_tests"
    assert validation["broader_v1_readiness_status_result"] == "passed_78_tests"
    assert validation["compileall_lima_passed"] is True
    assert validation["full_lima_suite_result"] == "passed_5457_tests"
    assert validation["diff_hygiene_passed"] is True

def test_v1_local_document_harness_install_release_impact_remains_blocked() -> None:
    fixture = _load_fixture()
    release = fixture["release_impact"]

    assert release["cutover_blocker_changed_by_audit"] is False
    assert release["required_cutover_action"] == (
        "record_exactly_one_valid_cutover_operator_choice"
    )
    for key in (
        "release_candidate_branch_created",
        "release_candidate_tag_created",
        "v1_completion_claimed",
        "product_readiness_claimed",
        "production_readiness_claimed",
        "consumer_production_integration_authorized",
    ):
        assert release[key] is False, key
    assert fixture["next_required_action"] == (
        "record_exactly_one_valid_cutover_operator_choice_before_cutover_runbook"
    )


def test_v1_local_document_harness_install_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert fixture["observed_lima_commit"] in text
    assert fixture["audit_verdict"] in text
    assert "review_v1_runtime_request" in text
    assert "execution_allowed=False" in text
    assert "Invoke-WebRequest" in text
    assert "pip install -e" in text
    assert "Use synthetic or non-sensitive local test documents only" in text
    assert "passed, 20 tests" in text
    assert "passed, 78 tests" in text
    assert "passed, 5457 tests" in text
    assert "Cutover operator choice recorded by this audit: no." in text
    assert "Product readiness claimed by this audit: no." in text


def test_v1_local_document_harness_install_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["audit"]).read_text(
        encoding="utf-8"
    )

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
