"""Static checks for the V1-G17 file mutation preview/diff request."""

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
    / "v1_g17_file_mutation_preview_diff_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g17_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g17_file_mutation_preview_diff_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-file-mutation-preview-diff-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g17_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["preview_diff_runtime_behavior_added"] is False
    assert fixture["actual_file_mutation_execution_approved"] is False
    assert fixture["actual_file_mutation_execution_added"] is False
    assert fixture["runtime_behavior_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g17_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G17",
        "Revise-V1-G17",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G17 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g17-file-mutation-preview-diff"
    )


def test_v1_g17_distinguishes_policy_preview_and_execution() -> None:
    distinctions = set(_load_fixture()["distinctions"])

    assert "v1_g16_guarded_file_mutation_policy" in distinctions
    assert "preview_dry_run_metadata_behavior" in distinctions
    assert "actual_file_mutation_execution" in distinctions


def test_v1_g17_required_preview_diff_topics_are_present() -> None:
    topics = set(_load_fixture()["required_preview_diff_topics"])

    assert "dry_run_file_mutation_preview" in topics
    assert "redacted_diff_patch_preview_metadata" in topics
    assert "no_raw_file_content_persistence" in topics
    assert "no_actual_file_write_delete" in topics
    assert "path_scope_workspace_root_validation" in topics
    assert "path_traversal_rejection" in topics
    assert "rollback_plan_metadata" in topics
    assert "approval_evidence_linkage" in topics
    assert "user_operator_confirmation_linkage" in topics
    assert "shell_harness_policy_linkage" in topics
    assert "audit_evidence_linkage" in topics
    assert "test_coverage_expectations" in topics
    assert "stop_conditions" in topics


def test_v1_g17_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_integration_added"] is False
    assert fixture["provider_model_routing_added"] is False
    assert fixture["connector_browser_network_device_robotics_physical_world_behavior_added"] is False
    assert fixture["actual_file_mutation_execution_added"] is False
    assert fixture["preview_diff_runtime_behavior_added"] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["product_ready"] is False


def test_v1_g17_docs_contain_execution_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "redacted diff/patch preview metadata" in approval_text
    assert "no raw file content persistence" in approval_text
    assert "no actual file write/delete" in approval_text
    assert "Actual file mutation execution remains unapproved" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G17" in decision_text
