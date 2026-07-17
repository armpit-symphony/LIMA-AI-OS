"""Static checks for the V1-G11 runtime-slice approval request."""

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
    / "v1_g11_runtime_request_decision_gate_approval_request.json"
)
DOCS = {
    "approval_request": (
        REPO_ROOT / "docs" / "V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md"
    ),
    "preflight_audit": (
        REPO_ROOT / "docs" / "V1_G11_RUNTIME_REQUEST_DECISION_GATE_PREFLIGHT_AUDIT.md"
    ),
}


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_approval_request_docs_exist_and_remain_candidate_only() -> None:
    fixture = _load_fixture()
    assert FIXTURE_PATH.exists()
    for path in DOCS.values():
        assert path.exists()

    assert fixture["gap_id"] == "V1-G11"
    assert fixture["packet_type"] == "runtime_slice_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert fixture["source_branch"] == "v1-g10-minimum-runtime-implementation-gate"
    assert fixture["base_commit"] == "39b866a3be3756d10287e3cefbd674ace7d2d469"
    assert fixture["approval_request_ready"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_g11_approval_request_adds_no_runtime_behavior() -> None:
    fixture = _load_fixture()
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_code_copied",
        "sparkbot_import_added",
        "provider_model_routing_added",
        "runtime_exports_changed",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False


def test_v1_g11_exact_approval_scope_is_machine_readable() -> None:
    fixture = _load_fixture()
    assert "Do you explicitly approve V1-G11 implementation" in fixture["exact_approval_question"]
    assert fixture["if_approved_next_branch"] == "v1-g11-runtime-request-decision-gate"
    assert (
        fixture["if_approved_objective"]
        == "typed_request_guardian_decision_preflight_runtime_slice"
    )

    runtime_files = set(fixture["eligible_runtime_files_if_approved"])
    assert runtime_files == {
        "lima/kernel/v1_runtime_request.py",
        "lima/kernel/__init__.py",
        "lima/guardian/v1_decision_gate.py",
        "lima/guardian/__init__.py",
    }

    non_runtime_files = set(fixture["eligible_non_runtime_files_if_approved"])
    assert "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md" in non_runtime_files
    assert "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md" in non_runtime_files
    assert (
        "tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json"
        in non_runtime_files
    )
    assert "tests/test_v1_g11_runtime_request_decision_gate.py" in non_runtime_files


def test_v1_g11_allowed_behaviors_preserve_no_execution_boundary() -> None:
    behaviors = set(_load_fixture()["allowed_runtime_behaviors_if_approved"])
    assert "raw_natural_language_not_accepted" in behaviors
    assert "only_validated_candidate_metadata_enters_slice" in behaviors
    assert "caller_supplied_approved_true_fails_closed" in behaviors
    assert "caller_supplied_guardian_decision_authority_fails_closed" in behaviors
    assert "destructive_edit_delete_maps_to_approval_required_not_execution" in behaviors
    assert "runtime_guardian_decision_metadata_is_produced_for_reviewed_requests" in behaviors
    assert "approval_required_decisions_do_not_execute_or_issue_tokens" in behaviors
    assert "audit_evidence_linkage_metadata_is_present_and_non_persistent" in behaviors
    assert "output_remains_deterministic_local_in_process_side_effect_free" in behaviors


def test_v1_g11_forbidden_surfaces_cover_scope_creep() -> None:
    forbidden = set(_load_fixture()["forbidden_surfaces"])
    assert "raw_natural_language_parsing" in forbidden
    assert "provider_model_calls_or_routing" in forbidden
    assert "tool_execution" in forbidden
    assert "file_mutation" in forbidden
    assert "browser_network_behavior" in forbidden
    assert "connector_behavior" in forbidden
    assert "shell_runtime_wiring" in forbidden
    assert "sparkbot_sparkbot_shell_arc_bot_shell_imports_or_code_copy" in forbidden
    assert "durable_persistence_database_writes_queues_workers_daemons_subprocesses_threads" in (
        forbidden
    )
    assert "haptic_device_behavior" in forbidden
    assert "device_robotics_iot_drone_robot_humanoid_physical_world_behavior" in forbidden
    assert "runtime_export_cleanup" in forbidden
    assert "final_api_freeze" in forbidden


def test_v1_g11_acceptance_tests_require_destructive_approval_and_fail_closed_cases() -> None:
    tests = set(_load_fixture()["required_acceptance_tests_if_approved"])
    assert "safe_informational_candidate_produces_reviewed_decision_without_execution" in tests
    assert "destructive_edit_candidate_requires_operator_approval" in tests
    assert "destructive_delete_candidate_requires_operator_approval" in tests
    assert "caller_supplied_approval_claim_is_blocked" in tests
    assert "caller_supplied_decision_authority_is_blocked" in tests
    assert "stale_or_replayed_candidate_is_blocked" in tests
    assert "missing_provenance_is_blocked" in tests
    assert "provider_model_request_is_not_routed" in tests
    assert "file_browser_network_device_robotics_claims_do_not_execute" in tests
    assert "raw_secret_prompt_file_content_pin_token_is_not_emitted" in tests


def test_v1_g11_rollback_and_stop_conditions_are_explicit() -> None:
    fixture = _load_fixture()
    rollback = set(fixture["rollback_files_if_approved"])
    assert "lima/kernel/v1_runtime_request.py" in rollback
    assert "lima/guardian/v1_decision_gate.py" in rollback
    assert "candidate_exports_added_to_lima/kernel/__init__.py" in rollback
    assert "candidate_exports_added_to_lima/guardian/__init__.py" in rollback

    stops = set(fixture["stop_conditions"])
    assert "file_scope_exceeds_approved_v1_g11_files" in stops
    assert "raw_natural_language_reaches_runtime_slice" in stops
    assert "request_metadata_executes_directly" in stops
    assert "destructive_edit_delete_approved_without_operator_approval_evidence" in stops
    assert "caller_metadata_can_forge_guardian_decision_authority" in stops
    assert "provider_model_calls_made" in stops
    assert "persistent_storage_or_database_writes_added" in stops
    assert "shell_runtime_wiring_added" in stops
    assert "sparkbot_code_imported_or_copied" in stops
    assert "runtime_exports_cleaned_up_or_frozen" in stops


def test_v1_g11_docs_match_preflight_verdict() -> None:
    fixture = _load_fixture()
    assert fixture["preflight_audit_result"] == "approval_request_ready_runtime_not_approved"
    assert fixture["recommended_next_step"] == "operator_decision_on_exact_v1_g11_approval_question"

    approval_text = DOCS["approval_request"].read_text(encoding="utf-8")
    audit_text = DOCS["preflight_audit"].read_text(encoding="utf-8")
    assert "Request verdict: `ready_for_operator_decision_not_approved`" in approval_text
    assert "Approval must be explicit before implementation begins." in approval_text
    assert "Preflight verdict: `approval_request_ready_runtime_not_approved`" in audit_text
    assert "Does this packet approve runtime implementation?" in audit_text
