"""Static checks for the V1-G3 destructive approval contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
SUMMARY_PATH = FIXTURE_DIR / "v1_g3_destructive_edit_delete_operator_approval_contract.json"
DOCS = {
    "contract": REPO_ROOT
    / "docs"
    / "V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CONTRACT.md",
    "audit": REPO_ROOT
    / "docs"
    / "V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_AUDIT.md",
    "closeout": REPO_ROOT
    / "docs"
    / "V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CLOSEOUT.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g3_summary_and_docs_exist_and_accept_static_contract_only() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert SUMMARY_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()
    assert summary["gap_id"] == "V1-G3"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["contract_completed"] is True
    assert summary["contract_accepted_as_static_evidence"] is True
    assert summary["contract_accepted_as_runtime_enforcement"] is False
    assert summary["v1_product_ready"] is False


def test_v1_g3_summary_tracks_expected_case_fixtures() -> None:
    summary = _load_json(SUMMARY_PATH)
    expected = {
        "tests/fixtures/runtime_extraction/v1_g3_delete_file_requires_operator_approval.json",
        "tests/fixtures/runtime_extraction/v1_g3_edit_file_requires_operator_approval.json",
        (
            "tests/fixtures/runtime_extraction/"
            "v1_g3_overwrite_existing_content_requires_operator_approval.json"
        ),
        "tests/fixtures/runtime_extraction/v1_g3_delete_memory_record_requires_operator_approval.json",
        (
            "tests/fixtures/runtime_extraction/"
            "v1_g3_connector_customer_record_mutation_requires_operator_approval.json"
        ),
        (
            "tests/fixtures/runtime_extraction/"
            "v1_g3_safe_draft_preview_no_operator_approval_required.json"
        ),
        "tests/fixtures/runtime_extraction/v1_g3_approval_bypass_claim_fail_closed.json",
    }
    assert set(summary["case_fixture_files"]) == expected
    for relative_path in expected:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g3_contract_covers_destructive_and_safe_action_classes() -> None:
    summary = _load_json(SUMMARY_PATH)
    destructive = set(summary["destructive_action_classes"])
    assert {
        "delete_file",
        "edit_file",
        "overwrite_existing_content",
        "delete_record_memory_message_task_event_customer_data_or_shell_state",
        "edit_record_memory_message_task_event_customer_data_or_shell_state",
        "connector_customer_record_write",
        "destructive_admin_action",
    }.issubset(destructive)
    safe = set(summary["non_destructive_safe_classes"])
    assert {
        "read_only_inspection",
        "draft_generation",
        "preview_only_planning",
        "explain_only_plan",
    }.issubset(safe)


def test_v1_g3_operator_approval_states_fail_closed_without_live_grant() -> None:
    contract = _load_json(SUMMARY_PATH)["operator_approval_contract"]
    assert contract["operator_approval_required_for_destructive_actions"] is True
    assert set(contract["allowed_future_operator_approval_states"]) == {
        "missing",
        "required_not_granted",
        "granted",
        "expired",
        "revoked",
        "denied",
    }
    assert "granted" not in set(contract["accepted_static_states_without_runtime_grant"])
    assert contract["static_granted_state_accepted_as_approval"] is False
    assert contract["static_approval_granted_claim_fails_closed"] is True
    assert contract["approval_metadata_replaces_guardian_decision"] is False
    assert contract["guardian_decision_required_before_future_execution"] is True


def test_v1_g3_status_mappings_keep_destructive_actions_out_of_preview_only() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert set(summary["packet_statuses"]) == {
        "preview_only",
        "explain_plan",
        "blocked",
        "deferred",
    }
    mappings = {
        entry["kernel_status"]: entry["packet_status"]
        for entry in summary["kernel_status_mappings"]
    }
    assert mappings == {
        "proposed": "preview_only",
        "needs_review": "explain_plan",
        "blocked": "blocked",
    }


def test_v1_g3_summary_boundary_results_add_no_runtime_behavior() -> None:
    summary = _load_json(SUMMARY_PATH)
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
        "shell_repos_changed",
        "sparkbot_shell_wiring_added",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "arc_bot_shell_wiring_added",
        "provider_model_routing_added",
        "guardian_decision_runtime_added",
        "operator_approval_enforcement_added",
        "approval_granted_by_contract",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "haptic_device_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert summary[key] is False


def test_v1_g3_docs_state_static_only_verdict_and_next_gap() -> None:
    contract_text = DOCS["contract"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    assert "`V1-G3` is complete as a static destructive-action approval contract." in contract_text
    assert "A docs/fixture claim that approval is `granted` must fail closed" in contract_text
    assert "Verdict: `accept_static_destructive_operator_approval_contract_only`." in audit_text
    assert "Recommended: `V1-G4`." in closeout_text
