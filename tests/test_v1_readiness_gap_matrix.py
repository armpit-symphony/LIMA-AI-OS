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
    assert fixture["current_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["request_stage_lane_label"] == (
        "prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_commit_before_matrix_refresh"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["implementation_approved"] is False
    assert fixture["v1_product_ready"] is False


def test_v1_gap_matrix_names_first_shell_consumers() -> None:
    assert set(_load_fixture()["first_shell_consumers"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_gap_matrix_current_anchor_is_g61_request_prep() -> None:
    anchor = _load_fixture()["current_anchor"]

    assert anchor["latest_completed_gate"] == "V1-G60"
    assert anchor["current_gate"] == "V1-G61"
    assert anchor["g55_operator_approval_recorded"] is True
    assert anchor["g55_runtime_implementation_approved"] is True
    assert anchor["g55_independent_audit_complete"] is True
    assert anchor["g56_request_packet_prepared"] is True
    assert anchor["g56_operator_approval_recorded"] is True
    assert anchor["g56_runtime_implementation_approved"] is True
    assert anchor["g56_independent_audit_complete"] is True
    assert anchor["g57_request_packet_prepared"] is True
    assert anchor["g57_operator_approval_recorded"] is True
    assert anchor["g57_runtime_implementation_approved"] is True
    assert anchor["g60_request_packet_prepared"] is True
    assert anchor["g60_operator_approval_recorded"] is True
    assert anchor["g60_runtime_implementation_approved"] is True
    assert anchor["g60_dependency_manifest_edited"] is True
    assert anchor["g60_lockfile_edited"] is False
    assert anchor["g60_independent_audit_complete"] is True
    assert anchor["g61_request_packet_prepared"] is True
    assert anchor["g61_request_gate_audit_complete"] is True
    assert anchor["g61_preapproval_runtime_tree_guard_audit_complete"] is True
    assert anchor["g61_operator_decision_packet_status_audit_complete"] is True
    assert anchor["g61_operator_decision_packet_status_audit_document"] == (
        "docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md"
    )
    assert anchor["post_g61_request_readiness_refresh_complete"] is True
    assert anchor["candidate_harness_quickstart_current"] is True
    assert anchor["candidate_harness_quickstart_document"] == (
        "docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md"
    )
    assert anchor["candidate_harness_quickstart_execution_audit_current"] is True
    assert anchor["candidate_harness_quickstart_execution_audit_document"] == (
        "docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md"
    )
    assert anchor["consumer_harness_usability_matrix_current"] is True
    assert anchor["release_candidate_acceptance_checklist_current"] is True
    assert anchor["release_candidate_acceptance_checklist_verdict"] == (
        "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS"
    )
    assert anchor["release_candidate_cutover_runbook_current"] is True
    assert anchor["release_candidate_cutover_runbook_verdict"] == (
        "CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS"
    )
    assert anchor["arc_bot_shell_local_drift_excluded_from_v1_proof"] is True
    assert anchor["arc_bot_shell_local_drift_exclusion_audit_current"] is True
    assert anchor["arc_bot_shell_local_drift_exclusion_audit_document"] == (
        "docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md"
    )
    assert (
        anchor["arc_bot_shell_local_drift_exclusion_audit_tracked_modified_file_count"]
        == 7
    )
    assert (
        anchor["arc_bot_shell_local_drift_exclusion_audit_untracked_file_count"] == 64
    )
    assert (
        anchor["arc_bot_shell_same_day_recheck_approved_g56_smoke_proof_paths_clean"]
        is True
    )
    assert anchor["arc_bot_shell_clean_checkpoint_evidence"] is False
    assert (
        anchor[
            "arc_bot_shell_clean_checkpoint_required_before_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim"
        ]
        is True
    )
    assert anchor["current_gate_consistency_audit_complete"] is True
    assert anchor["current_gate_consistency_audit_document"] == (
        "docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md"
    )
    assert anchor["current_candidate_validation_refresh_complete"] is True
    assert anchor["current_candidate_validation_refresh_audit_document"] == (
        "docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md"
    )
    assert anchor["current_validation_focused_current_gate_tests_passed"] == 153
    assert anchor["current_validation_full_lima_suite_tests_passed"] == 5350
    assert (
        anchor[
            "current_validation_latest_supplement_focused_final_blocker_index_tests_passed"
        ]
        == 15
    )
    assert (
        anchor["current_validation_latest_supplement_broader_v1_readiness_tests_passed"]
        == 89
    )
    assert (
        anchor["current_validation_latest_supplement_full_lima_suite_tests_passed"]
        == 5361
    )
    assert (
        anchor[
            "current_validation_latest_handoff_supplement_post_g61_request_focused_tests_passed"
        ]
        == 8
    )
    assert (
        anchor[
            "current_validation_latest_handoff_supplement_post_g61_request_broader_tests_passed"
        ]
        == 117
    )
    assert (
        anchor[
            "current_validation_latest_handoff_supplement_post_g61_request_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert (
        anchor[
            "current_validation_latest_handoff_supplement_quickstart_focused_tests_passed"
        ]
        == 7
    )
    assert (
        anchor[
            "current_validation_latest_handoff_supplement_quickstart_adjacent_tests_passed"
        ]
        == 64
    )
    assert (
        anchor[
            "current_validation_latest_handoff_supplement_quickstart_broader_tests_passed"
        ]
        == 133
    )
    assert (
        anchor[
            "current_validation_latest_handoff_supplement_quickstart_full_lima_suite_tests_passed"
        ]
        == 5364
    )
    assert anchor["post_validation_readiness_change_freshness_audit_current"] is True
    assert anchor["post_validation_readiness_change_freshness_audit_document"] == (
        "docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md"
    )
    assert anchor["post_validation_same_turn_full_lima_suite_tests_passed"] == 5359
    assert anchor["latest_quickstart_post_refresh_public_sparkbot_tests_passed"] == 8
    assert (
        anchor["latest_quickstart_post_refresh_accessible_sparkbot_tests_passed"] == 8
    )
    assert anchor["latest_quickstart_post_refresh_arc_bot_shell_tests_passed"] == 8
    assert anchor["latest_quickstart_post_refresh_focused_tests_passed"] == 17
    assert anchor["latest_quickstart_post_refresh_broader_v1_tests_passed"] == 108
    assert (
        anchor["latest_quickstart_post_refresh_full_lima_suite_tests_passed"] == 5360
    )
    assert anchor["latest_final_blocker_index_refresh_focused_tests_passed"] == 15
    assert anchor["latest_final_blocker_index_refresh_broader_tests_passed"] == 89
    assert (
        anchor["latest_final_blocker_index_refresh_full_lima_suite_tests_passed"]
        == 5361
    )
    assert anchor["latest_post_g61_request_readiness_refresh_focused_tests_passed"] == 8
    assert anchor["latest_post_g61_request_readiness_refresh_broader_tests_passed"] == 117
    assert (
        anchor["latest_post_g61_request_readiness_refresh_full_lima_suite_tests_passed"]
        == 5362
    )
    assert anchor["latest_quickstart_artifact_refresh_focused_tests_passed"] == 7
    assert anchor["latest_quickstart_artifact_refresh_adjacent_tests_passed"] == 64
    assert anchor["latest_quickstart_artifact_refresh_broader_tests_passed"] == 133
    assert anchor["latest_quickstart_artifact_refresh_full_lima_suite_tests_passed"] == 5364
    assert anchor["final_readiness_audit_template_current"] is True
    assert anchor["final_readiness_audit_template_document"] == (
        "docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md"
    )
    assert anchor["g61_operator_approval_recorded"] is False
    assert anchor["g61_runtime_implementation_approved"] is False
    assert anchor["next_required_artifact"] == (
        "v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request"
    )
    assert anchor["next_required_action"] == "record_v1_g61_operator_decision"
    assert anchor["valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]


def test_v1_gap_matrix_covers_expected_gap_groups() -> None:
    groups = {group["ids"]: group for group in _load_fixture()["gap_groups"]}

    assert set(groups) == {
        "V1-G1..V1-G10",
        "V1-G11..V1-G17",
        "V1-G18..V1-G28",
        "V1-G29..V1-G42",
        "V1-G43..V1-G56",
        "V1-G57..V1-G60",
        "V1-G61",
    }
    assert groups["V1-G1..V1-G10"]["status"] == (
        "complete_historical_candidate_only_evidence"
    )
    assert groups["V1-G43..V1-G56"]["status"] == (
        "complete_prior_approved_provider_authority_fake_egress_g55_wrapper_and_g56_consumer_smoke_evidence"
    )
    assert (
        groups["V1-G43..V1-G56"]["consumer_harness_usability_matrix_document"]
        == "docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md"
    )
    assert groups["V1-G43..V1-G56"]["consumer_harness_usability_matrix_current"] is True
    complete = groups["V1-G57..V1-G60"]
    assert complete["status"] == (
        "complete_prior_approved_provider_hardening_sdk_authority_dependency_and_import_boundary_evidence"
    )
    assert complete["runtime_approval_needed"] is False

    g61 = groups["V1-G61"]
    assert g61["status"] == (
        "approval_request_prepared_awaiting_operator_decision_implementation_not_approved"
    )
    assert (
        g61["approval_request_document"]
        == "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md"
    )
    assert (
        g61["operator_decision_packet_document"]
        == "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md"
    )
    assert (
        g61["request_gate_audit_document"]
        == "docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md"
    )
    assert (
        g61["preapproval_runtime_tree_guard_audit_document"]
        == "docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md"
    )
    assert (
        g61["operator_decision_packet_status_audit_document"]
        == "docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md"
    )
    assert (
        g61["post_g61_request_readiness_refresh_document"]
        == "docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md"
    )
    assert (
        g61["current_gate_consistency_audit_document"]
        == "docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md"
    )
    assert (
        g61["current_candidate_validation_refresh_audit_document"]
        == "docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md"
    )
    assert (
        g61["post_validation_readiness_change_freshness_audit_document"]
        == "docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md"
    )
    assert (
        g61["final_readiness_audit_template_document"]
        == "docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md"
    )
    assert (
        g61["next_lane_matrix_document"]
        == "docs/readiness/V1_POST_G60_NEXT_LANE_DECISION_MATRIX.md"
    )
    assert (
        g61["g60_audit_document"]
        == "docs/audits/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUDIT.md"
    )
    assert (
        g61["g60_rollup_document"]
        == "docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G60.md"
    )
    assert g61["g61_request_packet_prepared"] is True
    assert g61["g61_request_gate_audit_complete"] is True
    assert g61["g61_preapproval_runtime_tree_guard_audit_complete"] is True
    assert g61["g61_operator_decision_packet_status_audit_complete"] is True
    assert g61["post_g61_request_readiness_refresh_complete"] is True
    assert g61["current_gate_consistency_audit_complete"] is True
    assert g61["current_candidate_validation_refresh_complete"] is True
    assert g61["current_validation_focused_current_gate_tests_passed"] == 153
    assert g61["current_validation_full_lima_suite_tests_passed"] == 5350
    assert (
        g61[
            "current_validation_latest_supplement_focused_final_blocker_index_tests_passed"
        ]
        == 15
    )
    assert (
        g61["current_validation_latest_supplement_broader_v1_readiness_tests_passed"]
        == 89
    )
    assert (
        g61["current_validation_latest_supplement_full_lima_suite_tests_passed"]
        == 5361
    )
    assert (
        g61[
            "current_validation_latest_handoff_supplement_post_g61_request_focused_tests_passed"
        ]
        == 8
    )
    assert (
        g61[
            "current_validation_latest_handoff_supplement_post_g61_request_broader_tests_passed"
        ]
        == 117
    )
    assert (
        g61[
            "current_validation_latest_handoff_supplement_post_g61_request_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert (
        g61[
            "current_validation_latest_handoff_supplement_quickstart_focused_tests_passed"
        ]
        == 7
    )
    assert (
        g61[
            "current_validation_latest_handoff_supplement_quickstart_adjacent_tests_passed"
        ]
        == 64
    )
    assert (
        g61[
            "current_validation_latest_handoff_supplement_quickstart_broader_tests_passed"
        ]
        == 133
    )
    assert (
        g61[
            "current_validation_latest_handoff_supplement_quickstart_full_lima_suite_tests_passed"
        ]
        == 5364
    )
    assert g61["post_validation_readiness_change_freshness_audit_current"] is True
    assert g61["post_validation_same_turn_full_lima_suite_tests_passed"] == 5359
    assert g61["latest_quickstart_post_refresh_public_sparkbot_tests_passed"] == 8
    assert g61["latest_quickstart_post_refresh_accessible_sparkbot_tests_passed"] == 8
    assert g61["latest_quickstart_post_refresh_arc_bot_shell_tests_passed"] == 8
    assert g61["latest_quickstart_post_refresh_focused_tests_passed"] == 17
    assert g61["latest_quickstart_post_refresh_broader_v1_tests_passed"] == 108
    assert g61["latest_quickstart_post_refresh_full_lima_suite_tests_passed"] == 5360
    assert g61["latest_final_blocker_index_refresh_focused_tests_passed"] == 15
    assert g61["latest_final_blocker_index_refresh_broader_tests_passed"] == 89
    assert g61["latest_final_blocker_index_refresh_full_lima_suite_tests_passed"] == 5361
    assert g61["latest_post_g61_request_readiness_refresh_focused_tests_passed"] == 8
    assert g61["latest_post_g61_request_readiness_refresh_broader_tests_passed"] == 117
    assert (
        g61["latest_post_g61_request_readiness_refresh_full_lima_suite_tests_passed"]
        == 5362
    )
    assert g61["latest_quickstart_artifact_refresh_focused_tests_passed"] == 7
    assert g61["latest_quickstart_artifact_refresh_adjacent_tests_passed"] == 64
    assert g61["latest_quickstart_artifact_refresh_broader_tests_passed"] == 133
    assert g61["latest_quickstart_artifact_refresh_full_lima_suite_tests_passed"] == 5364
    assert (
        g61["arc_bot_shell_same_day_recheck_approved_g56_smoke_proof_paths_clean"]
        is True
    )
    assert g61["final_readiness_audit_template_current"] is True
    assert g61["g61_operator_approval_recorded"] is False
    assert g61["runtime_implementation_added"] is False
    assert g61["runtime_approval_needed"] is True


def test_v1_gap_matrix_recommends_g61_request_preparation() -> None:
    fixture = _load_fixture()

    assert fixture["next_smallest_safe_step"] == "record_v1_g61_operator_decision"
    assert fixture["next_smallest_safe_step_status"] == "pending_operator_decision"
    assert fixture["next_smallest_safe_step_reason"] == (
        "g60_dependency_declaration_is_audited_and_next_runtime_import_execution_proof_should_remain_test_scoped_request_only"
    )


def test_v1_gap_matrix_stop_conditions_cover_forbidden_g61_surfaces() -> None:
    stop_conditions = set(_load_fixture()["stop_conditions"])

    assert "g61_runtime_vendor_sdk_import_execution_proof_implementation_without_exact_approval" in stop_conditions
    assert "file_scope_outside_future_g61_request" in stop_conditions
    assert "sparkbot_or_arc_bot_shell_modification_for_g61_without_exact_approval" in stop_conditions
    assert (
        "release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim_with_arc_drift_only_excluded"
        in stop_conditions
    )
    assert "dependency_manifest_or_lockfile_edit_without_exact_approval" in stop_conditions
    assert "runtime_vendor_sdk_import_in_lima" in stop_conditions
    assert "credential_handling_or_real_provider_sdk_network_egress_in_import_execution_proof_lane" in stop_conditions
    assert "built_in_provider_sdk_client" in stop_conditions
    assert "provider_client_construction" in stop_conditions
    assert "endpoint_resolution_by_lima" in stop_conditions
    assert "dns_http_socket_network_calls_by_lima" in stop_conditions
    assert "direct_provider_egress_by_lima" in stop_conditions
    assert "secret_lookup_or_credential_value_access" in stop_conditions
    assert "provider_configuration_change" in stop_conditions
    assert "fallback_execution" in stop_conditions
    assert "consumer_production_runtime_integration" in stop_conditions
    assert (
        "connector_browser_network_file_device_robotics_physical_world_behavior"
        in stop_conditions
    )
    assert "v1_product_or_production_readiness_claim" in stop_conditions


def test_v1_gap_matrix_boundary_results_add_no_new_runtime_behavior() -> None:
    boundary = _load_fixture()["boundary_results"]

    assert boundary["v1_g56_request_packet_added"] is True
    assert boundary["v1_g56_operator_approval_recorded"] is True
    assert boundary["v1_g56_runtime_implementation_added"] is True
    assert boundary["v1_g57_request_packet_added"] is True
    assert boundary["v1_g57_operator_approval_recorded"] is True
    assert boundary["v1_g57_runtime_implementation_added"] is True
    assert boundary["v1_g60_request_packet_added"] is True
    assert boundary["v1_g60_operator_approval_recorded"] is True
    assert boundary["v1_g60_runtime_implementation_added"] is True
    assert boundary["v1_g60_dependency_manifest_edited"] is True
    assert boundary["v1_g60_lockfile_edited"] is False
    assert boundary["v1_g61_request_packet_added"] is True
    assert boundary["v1_g61_preapproval_runtime_tree_guard_added"] is True
    assert boundary["v1_g61_operator_decision_packet_status_audit_added"] is True
    assert (
        boundary[
            "v1_g61_operator_decision_packet_status_audit_not_implementation_approval"
        ]
        is True
    )
    assert boundary["v1_candidate_harness_quickstart_added"] is True
    assert boundary["v1_candidate_harness_quickstart_execution_audit_added"] is True
    assert boundary["v1_consumer_harness_usability_matrix_added"] is True
    assert boundary["v1_g61_operator_approval_recorded"] is False
    assert boundary["v1_g61_runtime_implementation_added"] is False

    for key in (
        "runtime_behavior_added_by_refresh",
        "lima_runtime_files_changed_by_refresh",
        "tests_support_changed",
        "shell_repos_changed_by_refresh",
        "built_in_provider_sdk_client_added",
        "provider_client_construction_added",
        "runtime_vendor_sdk_import_added_to_lima",
        "provider_endpoint_resolution_by_lima_added",
        "network_call_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "v1_release_claimed",
    ):
        assert boundary[key] is False, key


def test_v1_gap_matrix_doc_matches_g61_next_step_and_boundaries() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "This matrix turns the V1 product target into the current implementation-readiness sequence." in text
    assert "Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`" in text
    assert "Request-stage lane label: `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`" in text
    assert "Current active gate: `V1-G61`" in text
    assert "Current request-stage audit: `docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`" in text
    assert "Current preapproval runtime-tree guard audit: `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`" in text
    assert "docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "Current request-stage readiness refresh: `docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`" in text
    assert "Current candidate harness quickstart: `docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md`" in text
    assert "Current candidate harness quickstart execution audit: `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`" in text
    assert "Current consumer harness usability matrix: `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`" in text
    assert "Current release-candidate acceptance checklist: `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`" in text
    assert "Current release-candidate cutover runbook: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`" in text
    assert "Current Arc-Bot-shell local drift stance: smoke compatibility evidence only" in text
    assert "unrelated local worktree drift is excluded from V1 proof" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "7 tracked modified files and 64 untracked files excluded from V1 release-candidate/final-readiness proof" in text
    assert "same-day recheck proving approved G56 smoke proof paths remain clean" in text
    assert "not clean-checkpoint evidence" in text
    assert "Any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim requires a clean Arc-Bot-shell checkpoint proof." in text
    assert "Current gate consistency audit: `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`" in text
    assert "Current candidate validation refresh audit: `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`" in text
    assert "Current post-validation readiness-change freshness audit: `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`" in text
    assert "Current final readiness audit template: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`" in text
    assert "Current validation evidence: 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing" in text
    assert "Current validation latest LIMA readiness freshness supplement: 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and full LIMA suite passing with 5361 tests" in text
    assert "Current post-validation freshness evidence: same-turn release/cutover freshness validation and full LIMA suite passing with 5359 tests" in text
    assert "Latest quickstart post-refresh evidence: public Sparkbot 8 tests, accessible Sparkbot 8 tests, Arc-Bot-shell 8 tests, LIMA focused quickstart/handoff 17 tests, broader V1 harness/readiness 108 tests, and full LIMA suite 5360 tests" in text
    assert "Latest final blocker/index freshness evidence: 15 focused final blocker/index tests, 89 broader affected readiness tests, and full LIMA suite 5361 tests passing" in text
    assert "Latest post-G61 request readiness-refresh evidence: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and full LIMA suite 5362 tests passing" in text
    assert "Latest quickstart artifact refresh evidence: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and full LIMA suite 5364 tests passing" in text
    assert "`V1-G43` through `V1-G56`" in text
    assert "defines current Sparkbot and Arc-Bot-shell harness usability as local candidate smoke only" in text
    assert "`V1-G57` through `V1-G60`" in text
    assert "`V1-G61`" in text
    assert "request-gate audit passes; preapproval runtime-tree guard audit passes; operator decision packet status audit proves the packet is still awaiting one exact valid choice; post-G61 request readiness refresh is complete" in text
    assert "current gate consistency rejects stale G56/G57 blocker language" in text
    assert "Arc drift exclusion evidence records current dirty Arc local state as compatibility-only evidence, same-day approved G56 smoke proof paths clean, and not clean-checkpoint proof" in text
    assert "current validation refresh records 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing plus latest LIMA readiness freshness supplement evidence with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests plus latest handoff freshness supplement evidence with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests" in text
    assert "post-validation readiness-change freshness evidence records same-turn validation requirements for later readiness docs, fixtures, or tests with full LIMA suite passing 5359 tests, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request readiness-refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "candidate harness quickstart execution evidence records consumers 8/8/8 and LIMA 17/108/5360 plus latest quickstart artifact refresh 7/64/133/5364" in text
    assert "same-day approved G56 smoke proof paths clean" in text
    assert "Awaiting operator decision; implementation not approved" in text
    assert "V1-G61 runtime vendor SDK import execution proof implementation without exact approval" in text
    assert "credential handling or real provider SDK/network egress in an import execution proof lane" in text
    assert "built-in provider SDK clients" in text
    assert "LIMA-owned DNS, HTTP, socket, network calls" in text
    assert "secret lookup, credential value access" in text
    assert "V1 product readiness, production readiness" in text
    assert "protected by the preapproval runtime-tree guard audit, checked by the operator decision packet status audit" in text
    assert "Treat the V1 candidate harness quickstart as the shortest safe local Sparkbot and Arc-Bot-shell smoke command path only" in text
    assert "Treat the V1 candidate harness quickstart execution audit as current local public Sparkbot, accessible Sparkbot, and Arc-Bot-shell smoke pass evidence only, including latest consumers 8/8/8 and LIMA 17/108/5360 post-refresh validation, not production integration authority or clean-checkpoint proof for Arc-Bot-shell." in text
    assert "Treat the V1 current gate consistency audit as the active-gate guardrail" in text
    assert "Treat the V1 current candidate validation refresh as current validation evidence only: 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing, plus latest LIMA readiness freshness supplement evidence with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, and latest handoff freshness supplement evidence with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests." in text
    assert "Treat the V1 post-validation readiness-change freshness audit as same-turn freshness evidence for later readiness docs, fixtures, or tests, including 5359 release/cutover freshness proof, latest quickstart 5360 full-suite proof, latest final blocker/index 15/89/5361 proof, latest post-G61 request readiness-refresh 8/117/5362 proof, and latest quickstart artifact refresh 7/64/133/5364 proof, not a release approval." in text
    assert "Treat the V1 release-candidate cutover runbook as the future branch/tag procedure only, with current verdict `CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS`; excluded Arc-Bot-shell drift is compatibility-only evidence recorded by `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`, and any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim requires a clean Arc-Bot-shell checkpoint proof." in text
    assert "release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim while Arc-Bot-shell drift is only excluded rather than resolved with clean-checkpoint proof" in text
    assert "Treat the V1 final readiness audit template as a future post-G61 release-candidate audit input" in text
    assert "the G61 preapproval runtime-tree guard audit, the G61 operator decision packet status audit, the post-G61 request readiness refresh" in text
    assert (
        "completed implementation evidence chain through G60, request-stage readiness through the post-G61 refresh, current consumer harness usability criteria and quickstart execution evidence for Sparkbot and Arc-Bot-shell local candidate smoke tests, a release-candidate acceptance checklist, a cutover runbook, a current gate consistency audit, a current candidate validation refresh with 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing plus latest LIMA readiness freshness supplement evidence with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests plus latest handoff freshness supplement evidence with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests, a post-validation readiness-change freshness audit with same-turn full LIMA suite evidence passing 5359 tests, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request readiness-refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests, an Arc drift exclusion audit proving current Arc dirty state is compatibility-only evidence with approved G56 smoke proof paths clean, and a final readiness audit template"
        in text
    )
    assert "post-validation readiness-change freshness audit with same-turn full LIMA suite evidence passing 5359 tests, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request readiness-refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "The next smallest safe step is to record exactly one operator choice in the V1-G61 runtime vendor SDK import execution proof operator decision packet." in text
