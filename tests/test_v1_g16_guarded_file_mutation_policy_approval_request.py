"""Static checks for the V1-G16 guarded file mutation policy request."""

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
    / "v1_g16_guarded_file_mutation_policy_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g16_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g16_guarded_file_mutation_policy_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-guarded-file-mutation-policy-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g16_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["actual_file_mutation_execution_approved"] is False
    assert fixture["runtime_behavior_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g16_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G16",
        "Revise-V1-G16",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G16 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g16-guarded-file-mutation-policy"
    )


def test_v1_g16_distinguishes_policy_preview_and_execution() -> None:
    distinctions = set(_load_fixture()["distinctions"])

    assert "policy_authority_contract" in distinctions
    assert "preview_dry_run_behavior" in distinctions
    assert "actual_file_mutation_execution" in distinctions


def test_v1_g16_required_policy_topics_are_present() -> None:
    topics = set(_load_fixture()["required_policy_topics"])

    assert "file_edit_delete_request_classification" in topics
    assert "file_mutation_intent_scope" in topics
    assert "shell_harness_provided_file_authority" in topics
    assert "user_operator_approval_evidence" in topics
    assert "workspace_root_boundary" in topics
    assert "path_traversal_rejection" in topics
    assert "destructive_delete_confirmation" in topics
    assert "rollback_expectations" in topics
    assert "dry_run_preview_expectations" in topics
    assert "diff_patch_preview_expectations" in topics
    assert "audit_evidence_linkage" in topics
    assert "no_raw_secret_file_content_persistence" in topics
    assert "no_mutation_without_approval" in topics
    assert "no_mutation_outside_approved_scope" in topics
    assert "no_consumer_integration" in topics


def test_v1_g16_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_integration_added"] is False
    assert fixture["provider_model_routing_added"] is False
    assert fixture["connector_browser_network_device_robotics_physical_world_behavior_added"] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["product_ready"] is False


def test_v1_g16_docs_contain_execution_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "policy/authority contract" in approval_text
    assert "preview/dry-run behavior" in approval_text
    assert "actual file mutation execution" in approval_text
    assert "path traversal rejection" in approval_text
    assert "no mutation without approval" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G16" in decision_text
