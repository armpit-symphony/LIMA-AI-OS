"""Static checks for the LIMA-AI-OS V1 product readiness target."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_PRODUCT_READINESS_TARGET.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_product_readiness_target.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_target_document_and_fixture_exist() -> None:
    assert DOC_PATH.exists()
    assert FIXTURE_PATH.exists()
    fixture = _load_fixture()
    assert fixture["target_version"] == "1.0"
    assert fixture["document"] == "docs/V1_PRODUCT_READINESS_TARGET.md"
    assert fixture["readiness_gap_matrix"] == "docs/V1_READINESS_GAP_MATRIX.md"
    assert fixture["v1_g1_request_document"] == "docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_REQUEST.md"
    assert fixture["v1_g1_intake_document"] == "docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md"
    assert fixture["v1_g2_gate_document"] == "docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF_GATE.md"
    assert fixture["v1_g2_proof_document"] == "docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md"
    assert (
        fixture["v1_g3_contract_document"]
        == "docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CONTRACT.md"
    )
    assert (
        fixture["v1_g3_audit_document"]
        == "docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_AUDIT.md"
    )
    assert (
        fixture["v1_g3_closeout_document"]
        == "docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CLOSEOUT.md"
    )
    assert (
        fixture["v1_g4_gate_document"]
        == "docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md"
    )
    assert (
        fixture["v1_g4_audit_document"]
        == "docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_AUDIT.md"
    )
    assert (
        fixture["v1_g4_closeout_document"]
        == "docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_CLOSEOUT.md"
    )
    assert fixture["v1_g5_contract_document"] == "docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md"
    assert fixture["v1_g5_audit_document"] == "docs/V1_G5_PROVIDER_MODEL_ROUTING_AUDIT.md"
    assert fixture["v1_g5_closeout_document"] == "docs/V1_G5_PROVIDER_MODEL_ROUTING_CLOSEOUT.md"
    assert fixture["v1_g6_contract_document"] == "docs/V1_G6_HAPTIC_INTENT_METADATA_CONTRACT.md"
    assert fixture["v1_g6_audit_document"] == "docs/V1_G6_HAPTIC_INTENT_METADATA_AUDIT.md"
    assert fixture["v1_g6_closeout_document"] == "docs/V1_G6_HAPTIC_INTENT_METADATA_CLOSEOUT.md"
    assert fixture["v1_g7_request_document"] == "docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST.md"
    assert (
        fixture["v1_g7_audit_criteria_document"]
        == "docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_AUDIT_CRITERIA.md"
    )
    assert (
        fixture["v1_g7_closeout_document"]
        == "docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_CLOSEOUT.md"
    )
    assert (
        fixture["v1_g7_request_closeout_document"]
        == "docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST_CLOSEOUT.md"
    )
    assert (
        fixture["v1_g8_request_document"]
        == "docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_REQUEST_GATE.md"
    )
    assert (
        fixture["v1_g8_audit_criteria_document"]
        == "docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_AUDIT_CRITERIA.md"
    )
    assert (
        fixture["v1_g8_request_closeout_document"]
        == "docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_REQUEST_CLOSEOUT.md"
    )
    assert (
        fixture["v1_g8_contract_document"]
        == "docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_CONTRACT.md"
    )
    assert (
        fixture["v1_g8_threat_model_document"]
        == "docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_THREAT_MODEL.md"
    )
    assert (
        fixture["v1_g8_closeout_document"]
        == "docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md"
    )
    assert fixture["v1_g9_audit_document"] == "docs/V1_G9_PRODUCT_RELEASE_BOUNDARY_AUDIT.md"
    assert fixture["v1_g9_closeout_document"] == "docs/V1_G9_PRODUCT_RELEASE_BOUNDARY_CLOSEOUT.md"
    assert (
        fixture["v1_g10_gate_document"]
        == "docs/V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_GATE.md"
    )
    assert (
        fixture["v1_g10_closeout_document"]
        == "docs/V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_CLOSEOUT.md"
    )
    assert fixture["product_direction_only"] is True
    assert fixture["runtime_implementation_approved_by_this_fixture"] is False
    assert fixture["phase_48_2_implementation_approved"] is False


def test_v1_first_shell_consumers_and_sparkbot_reference_are_explicit() -> None:
    fixture = _load_fixture()
    assert set(fixture["first_shell_consumers"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }
    reference = fixture["shell_behavior_reference"]
    assert reference["reference_repo"] == "Sparkbot"
    assert reference["reference_role"] == "r_and_d_shell_behavior_source"
    assert reference["local_checkout_present"] is True
    assert reference["git_revision_recorded"] is False
    assert (
        reference["git_revision_unavailable_reason"]
        == "git_safe_directory_ownership_check_blocked_revision_read"
    )
    docs_checked = set(reference["read_only_reference_docs_checked"])
    assert "Sparkbot/AGENTS.md" in docs_checked
    assert "Sparkbot/docs/capabilities.md" in docs_checked
    assert "Sparkbot/docs/PUBLIC_RELEASE_CAPABILITY_MODEL.md" in docs_checked
    assert reference["copy_sparkbot_code"] is False
    assert reference["import_sparkbot_runtime"] is False
    assert reference["wire_sparkbot_routes"] is False


def test_v1_accepts_future_runtime_capabilities_without_implementing_them_here() -> None:
    fixture = _load_fixture()
    accepted = set(fixture["accepted_future_v1_runtime_capabilities"])
    assert "live_actual_approval_flow" in accepted
    assert "real_guardian_decision_runtime_path" in accepted
    assert "provider_model_routing" in accepted
    assert "shell_haptic_intent_support" in accepted
    assert "first_shell_response_state_parity" in accepted
    current = fixture["current_status"]
    assert current["provider_model_routing_added"] is False
    assert current["guardian_decision_runtime_added"] is False
    assert current["approval_enforcement_added"] is False
    assert current["runtime_behavior_added"] is False


def test_v1_destructive_edits_and_deletes_require_operator_approval() -> None:
    policy = _load_fixture()["operator_approval_policy"]
    assert policy["delete_requires_operator_approval"] is True
    assert policy["edit_requires_operator_approval"] is True
    assert policy["overwrite_requires_operator_approval"] is True
    assert policy["destructive_admin_or_connector_action_requires_operator_approval"] is True
    assert policy["applies_to_lima_ai_os"] is True
    assert policy["applies_to_shells"] is True
    destructive = set(_load_fixture()["destructive_action_classes"])
    assert "delete_file_or_record" in destructive
    assert "edit_or_mutate_file_or_record" in destructive
    assert "overwrite_existing_content" in destructive
    assert "destructive_admin_or_connector_action" in destructive


def test_v1_haptics_remain_shell_owned_with_lima_intent_metadata_only() -> None:
    haptics = _load_fixture()["haptics_ownership"]
    assert haptics["haptics_acceptable_as_v1_shell_experience_requirement"] is True
    assert haptics["shells_own_haptic_rendering"] is True
    assert haptics["lima_owns_haptic_device_implementation"] is False
    assert haptics["lima_may_define_future_haptic_intent_metadata"] is True
    assert haptics["haptic_intent_metadata_contract_added"] is True
    assert haptics["haptic_implementation_added_here"] is False


def test_v1_current_status_and_blockers_stay_honest() -> None:
    fixture = _load_fixture()
    current = fixture["current_status"]
    assert current["v1_product_ready"] is False
    assert current["phase_48_2_docs_tests_fixtures_only"] is True
    assert current["lima_runtime_files_changed"] is False
    assert current["tests_support_changed"] is False
    assert current["shell_repos_changed"] is False
    assert current["sparkbot_code_copied"] is False
    assert current["sparkbot_import_added"] is False
    assert current["haptic_intent_metadata_contract_added"] is True
    assert current["haptic_device_behavior_added"] is False
    assert current["first_shell_integration_proof_request_gate_added"] is True
    assert current["first_shell_integration_proof_complete"] is True
    assert current["first_shell_integration_proof_static_only"] is True
    assert current["audit_evidence_persistence_request_gate_added"] is True
    assert current["audit_evidence_persistence_static_contract_added"] is True
    assert current["audit_evidence_persistence_threat_model_added"] is True
    assert current["product_release_boundary_audit_added"] is True
    assert current["product_release_boundary_passed"] is False
    assert current["minimum_runtime_implementation_gate_added"] is True
    assert current["minimum_runtime_implementation_gate_approved_runtime"] is False
    assert current["v1_g11_runtime_implementation_approved"] is False
    assert current["durable_audit_persistence_implemented"] is False
    accepted = fixture["accepted_shell_evidence"]
    assert accepted["sparkbot_shell_thinking_proof_accepted"] is True
    assert accepted["sparkbot_shell_thinking_proof_scope"] == "source_backed_local_shell_evidence_only"
    assert accepted["sparkbot_shell_live_streaming_parity_proven"] is False
    static_evidence = fixture["accepted_static_lima_evidence"]
    assert static_evidence["v1_g2_typed_bridge_acceptance_proof_accepted"] is True
    assert static_evidence["v1_g2_typed_bridge_acceptance_proof_scope"] == "static_docs_tests_fixtures_only"
    assert static_evidence["v1_g2_runtime_bridge_behavior_proven"] is False
    assert static_evidence["v1_g3_destructive_operator_approval_contract_accepted"] is True
    assert (
        static_evidence["v1_g3_destructive_operator_approval_contract_scope"]
        == "static_docs_tests_fixtures_only"
    )
    assert static_evidence["v1_g3_runtime_approval_enforcement_proven"] is False
    assert static_evidence["v1_g4_guardian_decision_live_approval_path_gate_accepted"] is True
    assert (
        static_evidence["v1_g4_guardian_decision_live_approval_path_gate_scope"]
        == "static_docs_tests_fixtures_only"
    )
    assert static_evidence["v1_g4_runtime_guardian_decision_authority_proven"] is False
    assert static_evidence["v1_g5_provider_model_routing_contract_accepted"] is True
    assert (
        static_evidence["v1_g5_provider_model_routing_contract_scope"]
        == "static_docs_tests_fixtures_only"
    )
    assert static_evidence["v1_g5_runtime_provider_model_routing_proven"] is False
    assert static_evidence["v1_g6_haptic_intent_metadata_contract_accepted"] is True
    assert (
        static_evidence["v1_g6_haptic_intent_metadata_contract_scope"]
        == "static_docs_tests_fixtures_only"
    )
    assert static_evidence["v1_g6_haptic_device_behavior_proven"] is False
    assert static_evidence["v1_g6_shell_rendering_parity_proven"] is False
    assert static_evidence["v1_g7_first_shell_integration_proof_request_gate_completed"] is True
    assert static_evidence["v1_g7_first_shell_integration_proof_packets_received"] is True
    assert static_evidence["v1_g7_sparkbot_shell_intake_accepted"] is True
    assert static_evidence["v1_g7_sparkbot_intake_accepted"] is True
    assert static_evidence["v1_g7_arc_bot_shell_intake_accepted"] is True
    assert static_evidence["v1_g7_first_shell_integration_proof_accepted"] is True
    assert static_evidence["v1_g7_first_shell_integration_proof_scope"] == (
        "static_docs_tests_fixtures_only"
    )
    assert static_evidence["v1_g7_live_runtime_parity_proven"] is False
    assert static_evidence["v1_g8_audit_evidence_persistence_request_gate_completed"] is True
    assert static_evidence["v1_g8_audit_evidence_persistence_static_contract_completed"] is True
    assert static_evidence["v1_g8_audit_evidence_persistence_threat_model_completed"] is True
    assert static_evidence["v1_g8_audit_evidence_persistence_scope"] == (
        "static_docs_tests_fixtures_only_no_runtime_persistence"
    )
    assert static_evidence["v1_g8_durable_audit_persistence_proven"] is False
    assert static_evidence["v1_g9_product_release_boundary_audit_completed"] is True
    assert static_evidence["v1_g9_product_release_boundary_scope"] == (
        "static_docs_tests_fixtures_only_no_release_approval"
    )
    assert static_evidence["v1_g9_product_release_boundary_passed"] is False
    assert static_evidence["v1_g10_minimum_runtime_implementation_gate_completed"] is True
    assert static_evidence["v1_g10_minimum_runtime_implementation_gate_scope"] == (
        "docs_tests_fixtures_only_no_runtime_approval"
    )
    assert static_evidence["v1_g10_runtime_implementation_approved"] is False
    blockers = set(fixture["remaining_blockers"])
    assert "v1_g11_implementation_approval_required" in blockers
    assert "runtime_implementation_scope_gate_defined_but_runtime_unapproved" in blockers
    assert "real_guardian_decision_runtime_path_not_implemented" in blockers
    assert "live_approval_enforcement_not_implemented" in blockers
    assert "provider_model_routing_not_implemented" in blockers
    assert "sparkbot_shell_real_thinking_state_proof_missing" not in blockers
    assert "first_shell_integration_proof_static_only_live_runtime_parity_not_proven" in blockers
    assert "live_model_streaming_parity_not_proven" in blockers
    assert "haptic_device_rendering_proof_remains_shell_owned" in blockers
    assert "audit_persistence_request_gate_exists_but_durable_persistence_not_implemented" in blockers
    assert "destructive_edit_delete_approval_enforcement_not_implemented" in blockers
    assert "product_release_boundary_audit_complete_but_not_passed" in blockers
    assert "runtime_export_cleanup_unapproved" in blockers
    assert "final_api_freeze_unapproved" in blockers
    assert "production_behavior_not_approved" in blockers
    assert (
        fixture["recommended_first_gap_closed"]
        == "sparkbot_shell_source_backed_thinking_progress_state"
    )
    assert (
        fixture["recommended_next_step"]
        == "implement_v1_g11_typed_request_guardian_decision_preflight_after_explicit_approval"
    )
    assert fixture["recommended_second_gap_closed"] == "typed_bridge_acceptance_proof_static_evidence"
    assert (
        fixture["recommended_third_gap_closed"]
        == "destructive_edit_delete_operator_approval_contract_static_evidence"
    )
    assert (
        fixture["recommended_fourth_gap_closed"]
        == "real_guardian_decision_live_approval_path_static_design_gate"
    )
    assert (
        fixture["recommended_fifth_gap_closed"]
        == "provider_model_routing_static_contract_and_acceptance_test_design"
    )
    assert (
        fixture["recommended_sixth_gap_closed"]
        == "haptic_intent_metadata_static_contract_and_shell_fixture_proof"
    )
    assert (
        fixture["recommended_seventh_gap_request_gate"]
        == "first_shell_integration_proof_request_gate_complete"
    )
    assert (
        fixture["recommended_seventh_gap_closed"]
        == "first_shell_integration_proof_static_evidence"
    )
    assert (
        fixture["recommended_eighth_gap_request_gate"]
        == "audit_evidence_persistence_request_gate_complete"
    )
    assert (
        fixture["recommended_eighth_gap_closed"]
        == "audit_evidence_persistence_static_contract_and_threat_model"
    )
    assert (
        fixture["recommended_ninth_gap_closed"]
        == "product_release_boundary_audit_complete_boundary_not_passed"
    )
    assert (
        fixture["recommended_tenth_gap_closed"]
        == "minimum_runtime_implementation_gate_defined_runtime_not_approved"
    )
    assert fixture["recommended_next_gap_id"] == "V1-G11"
    assert (
        fixture["recommended_next_gap_to_close"]
        == "typed_request_guardian_decision_preflight_runtime_slice"
    )
