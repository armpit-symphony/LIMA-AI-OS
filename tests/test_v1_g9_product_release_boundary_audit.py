"""Static checks for the V1-G9 product release boundary audit."""

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
    / "v1_g9_product_release_boundary_audit.json"
)
DOCS = {
    "audit": REPO_ROOT / "docs" / "V1_G9_PRODUCT_RELEASE_BOUNDARY_AUDIT.md",
    "closeout": REPO_ROOT / "docs" / "V1_G9_PRODUCT_RELEASE_BOUNDARY_CLOSEOUT.md",
}


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g9_documents_exist_and_stay_candidate_only() -> None:
    fixture = _load_fixture()
    assert FIXTURE_PATH.exists()
    for path in DOCS.values():
        assert path.exists()

    assert fixture["gap_id"] == "V1-G9"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g9-product-release-boundary-audit"
    assert fixture["release_boundary_audit_completed"] is True
    assert fixture["release_boundary_passed"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_g9_boundary_adds_no_runtime_behavior() -> None:
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


def test_v1_g9_accepts_static_evidence_stack_only() -> None:
    fixture = _load_fixture()
    accepted = set(fixture["accepted_static_evidence"])
    assert "v1_target_explicit" in accepted
    assert "sparkbot_shell_thinking_source_backed_local_evidence" in accepted
    assert "typed_bridge_static_proof" in accepted
    assert "destructive_edit_delete_operator_approval_static_contract" in accepted
    assert "guardian_decision_live_approval_static_design_gate" in accepted
    assert "provider_model_routing_static_contract" in accepted
    assert "haptic_intent_metadata_static_contract_shell_owned" in accepted
    assert "first_shell_integration_static_evidence" in accepted
    assert "audit_evidence_persistence_static_contract_and_threat_model" in accepted
    assert set(fixture["first_shell_consumers"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_g9_release_gates_do_not_pass_from_static_evidence() -> None:
    fixture = _load_fixture()
    gates = {gate["id"]: gate for gate in fixture["release_gates"]}
    expected = {
        "api_status_release_candidate",
        "runtime_typed_bridge",
        "guardian_decision_runtime_authority",
        "live_approval_enforcement",
        "provider_model_runtime_routing",
        "durable_audit_evidence_persistence",
        "first_shell_runtime_wiring",
        "haptic_shell_rendering_proof_if_claimed",
        "runtime_export_cleanup",
        "final_api_freeze",
        "production_readiness",
    }
    assert expected <= set(gates)
    for gate_id in expected:
        assert gates[gate_id]["passed"] is False


def test_v1_g9_rejects_release_freeze_and_runtime_claims() -> None:
    fixture = _load_fixture()
    rejected = set(fixture["rejected_claims"])
    assert "v1_product_readiness" in rejected
    assert "production_readiness" in rejected
    assert "runtime_parity" in rejected
    assert "shell_runtime_wiring" in rejected
    assert "real_runtime_guardian_decision" in rejected
    assert "live_approval_enforcement" in rejected
    assert "provider_model_runtime_routing" in rejected
    assert "durable_audit_evidence_persistence" in rejected
    assert "runtime_export_cleanup_approval" in rejected
    assert "final_api_freeze" in rejected


def test_v1_g9_blockers_and_next_gate_are_explicit() -> None:
    fixture = _load_fixture()
    blockers = set(fixture["remaining_release_blockers"])
    assert "runtime_implementation_scope_gate_missing" in blockers
    assert "typed_bridge_runtime_behavior_not_implemented" in blockers
    assert "real_lima_guardian_decision_runtime_authority_missing" in blockers
    assert "live_approval_enforcement_missing" in blockers
    assert "destructive_edit_delete_enforcement_not_implemented" in blockers
    assert "provider_model_runtime_routing_missing" in blockers
    assert "durable_lima_audit_evidence_persistence_not_implemented" in blockers
    assert "shell_runtime_wiring_missing" in blockers
    assert "first_shell_live_runtime_parity_missing" in blockers
    assert "final_api_freeze_unapproved" in blockers

    future_gates = set(fixture["required_future_release_gates"])
    assert "runtime_implementation_scope_gate_with_exact_file_touch_map" in future_gates
    assert "runtime_typed_bridge_or_approved_equivalent" in future_gates
    assert "real_guardian_decision_runtime_path" in future_gates
    assert "live_approval_enforcement_for_destructive_edit_delete" in future_gates
    assert "durable_audit_evidence_persistence" in future_gates

    assert fixture["recommended_next_gap_id"] == "V1-G10"
    assert (
        fixture["recommended_next_step"]
        == "create_minimum_runtime_implementation_gate_and_exact_file_touch_rollback_plan"
    )
    assert (
        fixture["recommended_next_step_scope"]
        == "docs_tests_fixtures_only_gate_before_any_lima_runtime_change"
    )


def test_v1_g9_docs_state_boundary_not_passed() -> None:
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")

    assert "Release boundary verdict: `not_passed`" in audit_text
    assert "V1-G1 through V1-G8 give LIMA a strong static" in audit_text
    assert "Runtime export cleanup, final API freeze" in audit_text
    assert "Verdict: `release_boundary_audit_complete_boundary_not_passed`" in closeout_text
    assert "Recommended: `V1-G10`." in closeout_text
