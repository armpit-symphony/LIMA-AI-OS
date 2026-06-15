"""Static checks for the V1-G15 guiderail contract approval request."""

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
    / "v1_g15_shell_harness_guiderail_contract_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g15_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g15_shell_harness_guiderail_contract_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-shell-harness-guiderail-contract-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g15_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_behavior_added"] is False
    assert decision == {
        "recorded_choice": "none",
        "recorded_approval_wording": "none",
        "recorded_revision_request": "none",
        "recorded_pause_reason": "none",
        "approved_implementation_branch": "none",
        "implementation_approved": False,
    }


def test_v1_g15_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G15",
        "Revise-V1-G15",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G15 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g15-shell-harness-guiderail-contract"
    )


def test_v1_g15_required_contract_fields_are_present() -> None:
    fields = set(_load_fixture()["required_contract_fields"])

    assert "capability_profile" in fields
    assert "guardrail_mode" in fields
    assert "approval_policy" in fields
    assert "actor_scope" in fields
    assert "session_scope" in fields
    assert "tenant_scope" in fields
    assert "shell_scope" in fields
    assert "allowed_capability_lanes" in fields
    assert "destructive_edit_delete_policy" in fields
    assert "file_mutation_policy" in fields
    assert "provider_model_policy" in fields
    assert "connector_policy" in fields
    assert "browser_network_policy" in fields
    assert "physical_world_policy" in fields
    assert "emergency_stop_expectations" in fields
    assert "rollback_expectations" in fields
    assert "dry_run_vs_execution_authorized_posture" in fields
    assert "operator_approval_evidence_expectations" in fields
    assert "audit_evidence_linkage_expectations" in fields


def test_v1_g15_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_integration_added"] is False
    assert fixture["provider_model_routing_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["humaninput_bridge_activated"] is False
    assert fixture["connector_behavior_added"] is False
    assert fixture["browser_network_file_device_robotics_physical_world_behavior_added"] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["product_ready"] is False


def test_v1_g15_docs_contain_key_scope_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "capability profile" in approval_text
    assert "guardrail mode" in approval_text
    assert "approval policy" in approval_text
    assert "actor scope" in approval_text
    assert "session scope" in approval_text
    assert "tenant scope" in approval_text
    assert "physical-world policy" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G15" in decision_text
