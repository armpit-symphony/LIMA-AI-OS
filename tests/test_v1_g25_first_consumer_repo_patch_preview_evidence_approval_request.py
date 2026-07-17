"""Static checks for the V1-G25 consumer patch-preview evidence request."""

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
    / "v1_g25_first_consumer_repo_patch_preview_evidence_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g25_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g25_first_consumer_repo_patch_preview_evidence_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g25-first-consumer-repo-patch-preview-evidence-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g25_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["first_consumer_repo_patch_preview_evidence_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_repo_mutation_added"] is False
    assert fixture["arc_bot_shell_repo_mutation_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_repo_file_writes_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g25_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G25",
        "Revise-V1-G25",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G25 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g25-first-consumer-repo-patch-preview-evidence"
    )


def test_v1_g25_target_consumers_and_prerequisites_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["target_consumers"] == ["sparkbot", "arc_bot"]
    assert fixture["required_prior_evidence_refs"] == [
        "docs/V1_G18_CONSUMER_PROOF_PACKET_AUDIT_INTAKE.md",
        "docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE.md",
        "docs/V1_G22_FINAL_PUBLIC_API_FREEZE.md",
        "docs/V1_G23_CONSUMER_INTEGRATION_PROOF_TO_IMPORT_DRY_RUN.md",
        "docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS.md",
    ]

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g25_approved_file_scope_is_docs_tests_fixtures_only() -> None:
    approved_files = set(_load_fixture()["approved_files_if_operator_says_yes"])

    assert approved_files == {
        "docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE.md",
        "docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g25_first_consumer_repo_patch_preview_evidence.json",
        "tests/test_v1_g25_first_consumer_repo_patch_preview_evidence.py",
    }
    assert all(not path.startswith("lima/") for path in approved_files)
    assert all("Sparkbot/" not in path for path in approved_files)
    assert all("Arc-Bot-shell/" not in path for path in approved_files)


def test_v1_g25_patch_preview_boundaries_are_non_authorizing() -> None:
    fixture = _load_fixture()

    assert fixture["patch_preview_metadata_only"] is True
    assert fixture["patch_preview_grants_edit_authority"] is False
    assert fixture["raw_diff_or_patch_persisted"] is False
    assert fixture["raw_file_content_persisted"] is False
    assert fixture["consumer_repo_file_writes_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False


def test_v1_g25_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["product_ready"] is False


def test_v1_g25_docs_contain_patch_preview_boundary_language() -> None:
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

    assert "Sparkbot" in approval_text
    assert "Arc-Bot-shell" in approval_text
    assert "sanitized patch-preview evidence" in approval_text
    assert "persist raw diffs" in approval_text
    assert "No Sparkbot, Arc-Bot-shell, or other consumer repository files" in approval_text
    assert "Do not edit consumer repos" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G25" in decision_text
    assert "Consumer repo file writes remain forbidden" in preflight_text
