"""Static checks for the V1-G2 typed bridge acceptance proof gate."""

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
    / "v1_g2_typed_bridge_acceptance_proof_gate.json"
)
DOC_PATH = REPO_ROOT / "docs" / "V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF_GATE.md"


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g2_gate_doc_and_fixture_exist() -> None:
    fixture = _load_fixture()
    assert DOC_PATH.exists()
    assert FIXTURE_PATH.exists()
    assert fixture["gap_id"] == "V1-G2"
    assert fixture["gap_name"] == "typed_bridge_acceptance_proof"
    assert fixture["gate_document"] == "docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF_GATE.md"
    assert fixture["source_branch"] == "intake-sparkbot-shell-thinking-state-proof-packet"
    assert fixture["gate_branch"] == "v1-g2-typed-bridge-acceptance-proof-gate"
    assert fixture["base_commit"] == "5f6472becee8c409b0a330053cf9a619e2be4d74"


def test_v1_g2_gate_preserves_candidate_only_non_implementation_scope() -> None:
    fixture = _load_fixture()
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["v1_product_ready"] is False
    assert fixture["v1_g2_status"] == "approval_gate_created_implementation_not_started"
    assert fixture["proof_completed"] is False
    assert fixture["implementation_approved"] is False
    assert fixture["approval_answer"] == "not_approved_by_this_gate"
    assert fixture["docs_tests_fixtures_only"] is True


def test_v1_g2_gate_adds_no_runtime_shell_or_support_behavior() -> None:
    fixture = _load_fixture()
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
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "haptic_device_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False


def test_v1_g2_gate_records_v1_g1_precondition_without_accepting_live_parity() -> None:
    preconditions = _load_fixture()["preconditions"]
    assert preconditions["v1_g1_status"] == "accepted_source_backed_local_shell_evidence"
    assert (
        preconditions["v1_g1_intake_document"]
        == "docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md"
    )
    assert (
        preconditions["sparkbot_shell_thinking_commit"]
        == "36d697bf875a44dbafa41fc841ded86437917627"
    )
    assert preconditions["live_streaming_parity_proven"] is False
    assert preconditions["v1_product_ready"] is False


def test_v1_g2_gate_reviews_typed_bridge_source_evidence() -> None:
    reviewed = set(_load_fixture()["evidence_reviewed"])
    assert "docs/PHASE_44_0_TYPED_INTENTENVELOPE_GUARDIAN_REQUEST_BRIDGE_DESIGN_CHARTER.md" in reviewed
    assert "docs/PHASE_45_0_TYPED_BRIDGE_ACCEPTANCE_TEST_DESIGN.md" in reviewed
    assert "docs/PHASE_45_1_TYPED_BRIDGE_ACCEPTANCE_TEST_FIXTURE_MATRIX_SCAFFOLDING_DESIGN.md" in reviewed
    assert "docs/PHASE_47_1_STATIC_ACCEPTANCE_TEST_IMPLEMENTATION_CHECKLIST.md" in reviewed
    assert "docs/PHASE_48_0_IMPLEMENTATION_GATE_DECISION_CHARTER.md" in reviewed
    assert "docs/PHASE_48_2_CONCRETE_IMPLEMENTATION_DESIGN_REVIEW.md" in reviewed
    assert "docs/V1_PRODUCT_READINESS_TARGET.md" in reviewed
    assert "docs/V1_READINESS_GAP_MATRIX.md" in reviewed


def test_v1_g2_gate_defines_required_metadata_chain_and_cases() -> None:
    fixture = _load_fixture()
    assert fixture["metadata_chain_under_gate"] == [
        "source_request_metadata",
        "typed_intentenvelope_candidate_metadata",
        "guardian_request_metadata",
        "future_guardian_decision_metadata_absent_pending_or_blocked",
        "still_no_execution",
    ]
    future_cases = set(fixture["future_acceptance_cases"])
    assert "source_request_shape_positive" in future_cases
    assert "typed_intent_candidate_shape_positive" in future_cases
    assert "guardian_request_shape_positive" in future_cases
    assert "guardian_decision_metadata_boundary" in future_cases
    assert "kernel_status_mapping_to_shell_packet_statuses" in future_cases
    fail_closed = set(fixture["future_fail_closed_cases"])
    assert "malicious_approval_bypass" in fail_closed
    assert "forged_guardian_decision_authority" in fail_closed
    assert "runtime_execution_claim" in fail_closed
    assert "provider_model_tool_driver_call_claim" in fail_closed
    assert "browser_file_network_device_robotics_claim" in fail_closed


def test_v1_g2_gate_names_candidate_allowed_files_but_does_not_create_them() -> None:
    fixture = _load_fixture()
    allowed = set(fixture["candidate_future_allowed_files"])
    expected = {
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_preview_only_positive.json",
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_approval_bypass.json",
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_runtime_claim.json",
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_missing_guardian_request.json",
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_execution_claim.json",
        (
            "tests/fixtures/runtime_extraction/"
            "typed_bridge_acceptance_fail_closed_provider_model_tool_driver_claim.json"
        ),
        (
            "tests/fixtures/runtime_extraction/"
            "typed_bridge_acceptance_fail_closed_browser_file_network_device_robotics_claim.json"
        ),
        "tests/test_typed_bridge_acceptance_preview_only.py",
        "tests/test_typed_bridge_acceptance_fail_closed.py",
    }
    assert expected.issubset(allowed)
    assert fixture["candidate_future_allowed_files_created_by_this_gate"] is False
    for relative_path in expected:
        assert not (REPO_ROOT / relative_path).exists()


def test_v1_g2_gate_forbidden_scope_blocks_runtime_support_and_shell_repos() -> None:
    forbidden = set(_load_fixture()["candidate_forbidden_scope"])
    assert "lima/" in forbidden
    assert "tests/support/" in forbidden
    assert "Sparkbot_shell" in forbidden
    assert "Sparkbot" in forbidden
    assert "Arc-Bot-shell" in forbidden
    assert "adapters/" in forbidden
    assert "drivers/" in forbidden
    assert "persistence/" in forbidden
    assert "runtime_dispatch_paths" in forbidden
    assert "shell_browser_network_file_mutation_paths" in forbidden
    assert "robotics_haptic_device_physical_world_paths" in forbidden


def test_v1_g2_gate_status_mappings_cover_required_shell_packet_states() -> None:
    fixture = _load_fixture()
    assert set(fixture["packet_statuses"]) == {
        "preview_only",
        "explain_plan",
        "blocked",
        "deferred",
    }
    mappings = {
        entry["kernel_status"]: entry["packet_status"]
        for entry in fixture["kernel_status_mappings"]
    }
    assert mappings["proposed"] == "preview_only"
    assert mappings["needs_review"] == "explain_plan"
    assert mappings["blocked"] == "blocked"


def test_v1_g2_gate_required_invariants_fail_closed() -> None:
    invariants = _load_fixture()["required_invariant_flags"]
    assert invariants["non_authoritative"] is True
    assert invariants["safe_by_default"] is True
    assert invariants["local_only"] is True
    assert invariants["deterministic"] is True
    for key in (
        "execution_allowed",
        "dispatch_allowed",
        "persistence_allowed",
        "approval_granted",
        "external_calls_allowed",
        "provider_model_routing_allowed",
        "model_calls_allowed",
        "tool_calls_allowed",
        "driver_calls_allowed",
        "adapter_calls_allowed",
        "browser_file_network_device_robotics_allowed",
        "haptic_device_behavior_allowed",
        "physical_world_allowed",
        "guardian_decision_created",
        "runtime_test_harness_active",
    ):
        assert invariants[key] is False


def test_v1_g2_gate_stop_conditions_and_recommendation_are_explicit() -> None:
    fixture = _load_fixture()
    stop_conditions = set(fixture["stop_conditions"])
    assert "unapproved_lima_change" in stop_conditions
    assert "unapproved_tests_support_change" in stop_conditions
    assert "shell_repo_change" in stop_conditions
    assert "runtime_behavior" in stop_conditions
    assert "runtime_harness_creation_or_activation" in stop_conditions
    assert "guardian_decision_creation" in stop_conditions
    assert "approval_enforcement" in stop_conditions
    assert "execution_dispatch_persistence" in stop_conditions
    assert "provider_model_tool_driver_external_calls" in stop_conditions
    assert "browser_file_network_device_robotics_behavior" in stop_conditions
    assert "haptic_device_behavior" in stop_conditions
    assert "physical_world_behavior" in stop_conditions
    assert (
        fixture["recommended_option"]
        == "approve_v1_g2_docs_tests_fixtures_only_acceptance_proof"
    )
    assert fixture["next_after_v1_g2"] == "V1-G3_destructive_edit_delete_operator_approval_contract"


def test_v1_g2_gate_doc_matches_approval_question_and_boundaries() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "V1-G2`: typed bridge acceptance proof" in text
    assert "Current answer: `not_approved_by_this_gate`." in text
    assert "Does Phil approve implementing V1-G2" in text
    assert "Runtime behavior added: no." in text
    assert "LIMA runtime files changed: no." in text
    assert "`tests/support` changed: no." in text
    assert "Provider/model routing added: no." in text
    assert "GuardianDecision runtime added: no." in text
    assert "Approval enforcement added: no." in text
    assert "Recommended: approve and implement the V1-G2 docs/tests/fixtures-only" in text
