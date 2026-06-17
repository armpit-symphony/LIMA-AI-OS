"""Static checks for the V1-G26 first consumer repository edit request."""

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
    / "v1_g26_first_consumer_repository_edit_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g26_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g26_first_consumer_repository_edit_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-g26-first-consumer-repository-edit-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g26_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["consumer_repository_edit_implementation_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_runtime_source_mutation_added"] is False
    assert fixture["arc_bot_shell_runtime_source_mutation_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g26_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G26",
        "Revise-V1-G26",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G26 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g26-first-consumer-repository-edit"
    )


def test_v1_g26_local_path_audit_is_read_only_and_scoped() -> None:
    audit = _load_fixture()["local_path_audit"]

    assert audit["read_only"] is True
    assert audit["sparkbot_repo"] == "C:/Users/limap/Sparkbot"
    assert audit["sparkbot_branch_seen"] == "proof-sparkbot-shell-lima-consumer-packet"
    assert audit["arc_bot_shell_repo"] == "C:/Users/limap/Arc-Bot-shell"
    assert audit["arc_bot_shell_branch_seen"] == (
        "v1-g7-arc-bot-shell-integration-proof-packet"
    )
    assert audit["arc_bot_shell_pytest_cache_warning_seen"] is True
    assert audit["pytest_cache_allowed"] is False


def test_v1_g26_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["target_consumers"] == ["sparkbot", "arc_bot"]
    assert fixture["required_prior_evidence_refs"] == [
        "docs/V1_G18_CONSUMER_PROOF_PACKET_AUDIT_INTAKE.md",
        "docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE.md",
        "docs/V1_G22_FINAL_PUBLIC_API_FREEZE.md",
        "docs/V1_G23_CONSUMER_INTEGRATION_PROOF_TO_IMPORT_DRY_RUN.md",
        "docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS.md",
        "docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE.md",
    ]

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g26_approved_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert set(fixture["approved_lima_files_if_operator_says_yes"]) == {
        "docs/V1_G26_FIRST_CONSUMER_REPOSITORY_EDIT.md",
        "docs/V1_G26_FIRST_CONSUMER_REPOSITORY_EDIT_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g26_first_consumer_repository_edit.json",
        "tests/test_v1_g26_first_consumer_repository_edit.py",
    }
    assert set(fixture["approved_sparkbot_files_if_operator_says_yes"]) == {
        "docs/proof_packets/SPARKBOT_LIMA_V1_G26_STATIC_CONSUMER_EDIT_PACKET.md",
        "tests/fixtures/sparkbot_lima_v1_g26_static_consumer_edit_packet.json",
        "tests/test_sparkbot_lima_v1_g26_static_consumer_edit_packet.py",
    }
    assert set(fixture["approved_arc_bot_shell_files_if_operator_says_yes"]) == {
        "docs/proof_packets/ARC_BOT_SHELL_LIMA_V1_G26_STATIC_CONSUMER_EDIT_PACKET.md",
        "tests/fixtures/arc_bot_shell_lima_v1_g26_static_consumer_edit_packet.json",
        "tests/test_arc_bot_shell_lima_v1_g26_static_consumer_edit_packet.py",
    }
    assert all(
        not path.startswith("lima/")
        for path in fixture["approved_lima_files_if_operator_says_yes"]
    )


def test_v1_g26_consumer_edit_scope_is_static_only() -> None:
    fixture = _load_fixture()
    scope = fixture["consumer_edit_scope_if_approved"]

    assert scope["sparkbot"] == "static_docs_tests_fixtures_only"
    assert scope["arc_bot"] == "static_docs_tests_fixtures_only"
    assert scope["runtime_source_files_allowed"] is False
    assert scope["live_imports_allowed"] is False
    assert scope["runtime_calls_allowed"] is False


def test_v1_g26_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["live_lima_imports_from_consumers_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["raw_diff_or_patch_persisted"] is False
    assert fixture["raw_file_content_persisted"] is False
    assert fixture["product_ready"] is False


def test_v1_g26_docs_contain_consumer_edit_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )
    preflight_text = (REPO_ROOT / fixture["documents"]["preflight_audit"]).read_text(
        encoding="utf-8"
    )

    assert "Sparkbot docs/tests/fixtures" in approval_text
    assert "Arc-Bot-shell docs/tests/fixtures" in approval_text
    assert "No `lima/` runtime files" in approval_text
    assert "No Sparkbot or Arc-Bot-shell runtime/source files" in approval_text
    assert "Do not add runtime imports" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G26" in decision_text
    assert "Implementation must not start until `Approve-V1-G26`" in preflight_text
