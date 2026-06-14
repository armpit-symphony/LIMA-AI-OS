"""Static checks for the V1 readiness gap matrix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_READINESS_GAP_MATRIX.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_readiness_gap_matrix.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_gap_matrix_exists_and_preserves_non_implementation_scope() -> None:
    fixture = _load_fixture()
    assert DOC_PATH.exists()
    assert fixture["document"] == "docs/V1_READINESS_GAP_MATRIX.md"
    assert fixture["source_target"] == "docs/V1_PRODUCT_READINESS_TARGET.md"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["implementation_approved"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["source_commit_before_matrix"] == "57a403cb7ad4aa6f352a3c361a71db575d3de5a1"


def test_v1_gap_matrix_names_first_shell_consumers() -> None:
    assert set(_load_fixture()["first_shell_consumers"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_gap_matrix_covers_expected_gaps() -> None:
    gaps = {gap["id"]: gap for gap in _load_fixture()["gaps"]}
    assert set(gaps) == {f"V1-G{index}" for index in range(10)}
    assert gaps["V1-G1"]["name"] == "sparkbot_shell_thinking_progress_proof"
    assert gaps["V1-G1"]["status"] == "accepted_source_backed_local_shell_evidence"
    assert (
        gaps["V1-G1"]["request_document"]
        == "docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_REQUEST.md"
    )
    assert (
        gaps["V1-G1"]["intake_document"]
        == "docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md"
    )
    assert gaps["V1-G2"]["name"] == "typed_bridge_acceptance_proof"
    assert gaps["V1-G2"]["status"] == "complete_static_docs_tests_fixtures_proof"
    assert (
        gaps["V1-G2"]["gate_document"]
        == "docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF_GATE.md"
    )
    assert (
        gaps["V1-G2"]["proof_document"]
        == "docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md"
    )
    assert gaps["V1-G3"]["name"] == "destructive_edit_delete_approval_contract"
    assert gaps["V1-G4"]["name"] == "real_guardian_decision_and_live_approval_path"
    assert gaps["V1-G4"]["status"] == "complete_static_docs_tests_fixtures_design_gate"
    assert (
        gaps["V1-G4"]["gate_document"]
        == "docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md"
    )
    assert gaps["V1-G5"]["name"] == "provider_model_routing"
    assert (
        gaps["V1-G5"]["status"]
        == "complete_static_docs_tests_fixtures_contract_and_acceptance_test_design"
    )
    assert gaps["V1-G5"]["contract_document"] == "docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md"
    assert gaps["V1-G6"]["name"] == "haptic_intent_metadata"
    assert gaps["V1-G6"]["status"] == "complete_static_docs_tests_fixtures_contract"
    assert (
        gaps["V1-G6"]["contract_document"]
        == "docs/V1_G6_HAPTIC_INTENT_METADATA_CONTRACT.md"
    )
    assert gaps["V1-G7"]["name"] == "first_shell_integration_proof"
    assert gaps["V1-G7"]["status"] == "complete_static_first_shell_integration_evidence"
    assert (
        gaps["V1-G7"]["request_document"]
        == "docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST.md"
    )
    assert (
        gaps["V1-G7"]["consolidated_closeout_document"]
        == "docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_CLOSEOUT.md"
    )
    assert gaps["V1-G7"]["proof_packets_received"] is True
    assert gaps["V1-G7"]["lima_intake_audits_complete"] is True
    assert gaps["V1-G7"]["consolidated_closeout_complete"] is True
    assert gaps["V1-G8"]["name"] == "audit_evidence_persistence"
    assert gaps["V1-G9"]["name"] == "product_release_boundary"


def test_v1_gap_matrix_keeps_runtime_approval_flags_honest() -> None:
    gaps = {gap["id"]: gap for gap in _load_fixture()["gaps"]}
    assert gaps["V1-G1"]["runtime_approval_needed"] is False
    assert gaps["V1-G2"]["runtime_approval_needed"] is False
    assert gaps["V1-G3"]["runtime_approval_needed"] is False
    assert gaps["V1-G3"]["runtime_enforcement_approval_needed"] is True
    assert gaps["V1-G4"]["runtime_approval_needed"] is False
    assert gaps["V1-G4"]["runtime_authority_approval_needed"] is True
    assert gaps["V1-G5"]["runtime_approval_needed"] is False
    assert gaps["V1-G5"]["runtime_routing_approval_needed"] is True
    assert gaps["V1-G6"]["runtime_approval_needed"] is False
    assert gaps["V1-G6"]["device_behavior_approval_needed_in_lima"] is False
    assert gaps["V1-G6"]["shell_device_behavior_remains_shell_owned"] is True
    assert gaps["V1-G7"]["runtime_approval_needed"] is False
    assert gaps["V1-G7"]["runtime_wiring_approval_needed"] is True
    assert gaps["V1-G8"]["runtime_approval_needed"] is True
    assert gaps["V1-G9"]["runtime_approval_needed"] is False


def test_v1_gap_matrix_recommends_haptics_after_provider_model_contract() -> None:
    fixture = _load_fixture()
    assert fixture["recommended_order"][0] == "V1-G1"
    assert fixture["next_smallest_safe_step"] == "V1-G8"
    assert (
        fixture["next_smallest_safe_step_status"]
        == "pending_audit_evidence_persistence_design_request_gate"
    )
    assert (
        fixture["next_smallest_safe_step_reason"]
        == "v1_g7_static_first_shell_evidence_complete_but_audit_persistence_is_missing"
    )


def test_v1_gap_matrix_stop_conditions_cover_forbidden_surfaces() -> None:
    stop_conditions = set(_load_fixture()["stop_conditions"])
    assert "lima_runtime_change" in stop_conditions
    assert "tests_support_runtime_or_harness_helper" in stop_conditions
    assert "shell_repo_modification" in stop_conditions
    assert "provider_model_call" in stop_conditions
    assert "guardian_decision_runtime_creation" in stop_conditions
    assert "approval_enforcement" in stop_conditions
    assert "execution_dispatch_persistence" in stop_conditions
    assert "external_call" in stop_conditions
    assert "shell_browser_network_file_mutation" in stop_conditions
    assert "robotics_or_physical_world_behavior" in stop_conditions
    assert "haptic_device_behavior" in stop_conditions


def test_v1_gap_matrix_boundary_results_add_no_runtime_behavior() -> None:
    boundary = _load_fixture()["boundary_results"]
    assert boundary["operator_approval_contract_added"] is True
    assert boundary["guardian_decision_design_gate_added"] is True
    assert boundary["provider_model_routing_contract_added"] is True
    assert boundary["haptic_intent_metadata_contract_added"] is True
    assert boundary["first_shell_integration_proof_request_gate_added"] is True
    assert boundary["first_shell_integration_proof_complete"] is True
    assert boundary["first_shell_integration_proof_closeout_added"] is True
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "provider_model_routing_added",
        "guardian_decision_runtime_added",
        "approval_enforcement_added",
        "audit_persistence_added",
        "haptic_device_behavior_added",
        "v1_release_claimed",
    ):
        assert boundary[key] is False


def test_v1_gap_matrix_doc_matches_next_step_and_boundaries() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "This matrix turns the V1 product target into an implementation-readiness sequence." in text
    assert "`V1-G1` is accepted as source-backed local shell evidence." in text
    assert "`V1-G2` is complete as static docs/tests/fixtures-only typed bridge acceptance proof." in text
    assert "`V1-G3` is complete as static docs/tests/fixtures-only destructive edit/delete" in text
    assert "`V1-G4` is complete as static docs/tests/fixtures-only real `GuardianDecision`" in text
    assert "`V1-G5` is complete as static docs/tests/fixtures-only provider/model routing" in text
    assert "`V1-G6` is complete as static docs/tests/fixtures-only haptic intent metadata" in text
    assert "`V1-G7` is complete as static docs/tests/fixtures-only first-shell integration evidence." in text
    assert "The next smallest safe step is `V1-G8`" in text
    assert "`Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`" in text
    assert "runtime behavior" in text
    assert "haptic device behavior" in text
