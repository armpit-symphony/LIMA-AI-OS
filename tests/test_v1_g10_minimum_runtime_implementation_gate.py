"""Static checks for the V1-G10 minimum runtime implementation gate."""

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
    / "v1_g10_minimum_runtime_implementation_gate.json"
)
DOCS = {
    "gate": REPO_ROOT / "docs" / "V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_GATE.md",
    "closeout": REPO_ROOT / "docs" / "V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_CLOSEOUT.md",
}


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g10_documents_exist_and_stay_candidate_only() -> None:
    fixture = _load_fixture()
    assert FIXTURE_PATH.exists()
    for path in DOCS.values():
        assert path.exists()

    assert fixture["gap_id"] == "V1-G10"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g10-minimum-runtime-implementation-gate"
    assert fixture["implementation_gate_defined"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_g10_adds_no_runtime_behavior() -> None:
    fixture = _load_fixture()
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_code_copied",
        "sparkbot_import_added",
        "runtime_exports_changed",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False


def test_v1_g10_reviews_existing_runtime_surfaces() -> None:
    fixture = _load_fixture()
    reviewed = set(fixture["current_runtime_surface_reviewed"])
    assert "lima/kernel/intake_candidate.py" in reviewed
    assert "lima/kernel/candidate_status.py" in reviewed
    assert "lima/kernel/candidate_preview.py" in reviewed
    assert "lima/kernel/runtime_state.py" in reviewed
    assert "lima/contracts/guardian.py" in reviewed
    assert "lima/contracts/intent.py" in reviewed
    assert "lima/contracts/approval.py" in reviewed
    assert "lima/contracts/events.py" in reviewed
    assert "lima/guardian/decision_fakes.py" in reviewed
    assert "lima/guardian/pipeline_fakes.py" in reviewed

    truth = fixture["current_runtime_truth"]
    assert truth["non_executing_candidate_runtime_exists"] is True
    assert truth["guardian_approval_spine_behavior_fake_only"] is True
    assert truth["live_typed_bridge_exists"] is False
    assert truth["real_runtime_guardian_decision_exists"] is False
    assert truth["approval_enforcement_exists"] is False
    assert truth["durable_audit_persistence_exists"] is False
    assert truth["provider_model_routing_exists"] is False
    assert truth["shell_wiring_exists"] is False


def test_v1_g10_defines_exact_future_v1_g11_file_scope() -> None:
    fixture = _load_fixture()
    assert fixture["recommended_next_gap_id"] == "V1-G11"
    assert (
        fixture["recommended_next_lane"]
        == "typed_request_guardian_decision_preflight_runtime_slice"
    )
    assert fixture["recommended_next_lane_requires_explicit_runtime_approval"] is True

    runtime_files = set(fixture["future_v1_g11_eligible_runtime_files"])
    assert runtime_files == {
        "lima/kernel/v1_runtime_request.py",
        "lima/kernel/__init__.py",
        "lima/guardian/v1_decision_gate.py",
        "lima/guardian/__init__.py",
    }

    non_runtime_files = set(fixture["future_v1_g11_eligible_non_runtime_files"])
    assert "tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json" in (
        non_runtime_files
    )
    assert "tests/test_v1_g11_runtime_request_decision_gate.py" in non_runtime_files
    assert "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md" in non_runtime_files


def test_v1_g10_forbidden_surfaces_block_scope_creep() -> None:
    forbidden = set(_load_fixture()["future_v1_g11_forbidden_surfaces"])
    assert "tests/support" in forbidden
    assert "lima/harness" in forbidden
    assert "lima/io" in forbidden
    assert "lima/persistence" in forbidden
    assert "lima/services" in forbidden
    assert "lima/shells" in forbidden
    assert "shell_repositories" in forbidden
    assert "sparkbot_imports" in forbidden
    assert "provider_model_calls" in forbidden
    assert "tool_execution" in forbidden
    assert "file_mutation" in forbidden
    assert "browser_network_behavior" in forbidden
    assert "device_robotics_physical_world_behavior" in forbidden
    assert "durable_persistence" in forbidden
    assert "runtime_export_cleanup" in forbidden
    assert "final_api_freeze" in forbidden


def test_v1_g10_future_behaviors_protect_destructive_edit_delete_and_guardian() -> None:
    fixture = _load_fixture()
    behaviors = set(fixture["future_v1_g11_required_runtime_behaviors"])
    assert "raw_natural_language_not_accepted" in behaviors
    assert "only_validated_candidate_metadata_enters_slice" in behaviors
    assert "caller_supplied_approved_true_fails_closed" in behaviors
    assert "caller_supplied_guardian_decision_authority_fails_closed" in behaviors
    assert "destructive_edit_delete_maps_to_approval_required_not_execution" in behaviors
    assert "runtime_guardian_decision_metadata_is_produced_for_reviewed_requests" in behaviors
    assert "approval_required_decisions_do_not_execute_or_issue_tokens" in behaviors
    assert "audit_evidence_linkage_metadata_is_present_and_non_persistent" in behaviors

    tests = set(fixture["future_v1_g11_required_acceptance_tests"])
    assert "destructive_edit_candidate_requires_operator_approval" in tests
    assert "destructive_delete_candidate_requires_operator_approval" in tests
    assert "caller_supplied_approval_claim_is_blocked" in tests
    assert "caller_supplied_decision_authority_is_blocked" in tests
    assert "audit_evidence_linkage_is_present_and_non_persistent" in tests


def test_v1_g10_rollback_and_stop_conditions_are_explicit() -> None:
    fixture = _load_fixture()
    rollback = set(fixture["future_v1_g11_rollback_files"])
    assert "lima/kernel/v1_runtime_request.py" in rollback
    assert "lima/guardian/v1_decision_gate.py" in rollback
    assert "candidate_exports_added_to_lima/kernel/__init__.py" in rollback
    assert "candidate_exports_added_to_lima/guardian/__init__.py" in rollback

    stops = set(fixture["stop_conditions"])
    assert "file_scope_exceeds_v1_g11_eligible_files" in stops
    assert "raw_natural_language_reaches_runtime_slice" in stops
    assert "request_metadata_executes_directly" in stops
    assert "destructive_edit_delete_approved_without_operator_approval_evidence" in stops
    assert "guardian_decision_forged_by_caller_metadata" in stops
    assert "provider_model_calls_made" in stops
    assert "persistent_storage_or_database_writes_added" in stops
    assert "sparkbot_code_imported_or_copied" in stops
    assert "runtime_exports_cleaned_up_or_frozen" in stops


def test_v1_g10_remaining_blockers_and_docs_match_gate_verdict() -> None:
    fixture = _load_fixture()
    blockers = set(fixture["remaining_v1_blockers"])
    assert "v1_g11_implementation_approval_required" in blockers
    assert "typed_bridge_runtime_behavior_not_implemented" in blockers
    assert "real_lima_guardian_decision_runtime_authority_missing" in blockers
    assert "live_approval_enforcement_missing" in blockers
    assert "destructive_edit_delete_enforcement_not_implemented" in blockers
    assert "provider_model_runtime_routing_missing" in blockers
    assert "durable_lima_audit_evidence_persistence_not_implemented" in blockers
    assert "shell_runtime_wiring_missing" in blockers
    assert "final_api_freeze_unapproved" in blockers

    gate_text = DOCS["gate"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    assert "Gate verdict: `defined_not_approved_for_runtime`" in gate_text
    assert "Recommended next lane: `V1-G11`." in gate_text
    assert "Verdict: `implementation_gate_defined_runtime_not_approved`" in closeout_text
    assert "Recommended: `V1-G11`, after explicit approval." in closeout_text
