"""Static checks for the LIMA-AI-OS V1 product readiness target."""

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
    / "v1_product_readiness_target.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_target_documents_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["target_version"] == "1.0"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["request_stage_lane_label"] == (
        "prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_commit_before_refresh"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


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
    assert reference["copy_sparkbot_code"] is False
    assert reference["import_sparkbot_runtime"] is False
    assert reference["wire_sparkbot_routes"] is False
    assert reference["mutate_consumer_repo_for_g61"] is False


def test_v1_accepts_future_capabilities_without_approving_them_here() -> None:
    fixture = _load_fixture()
    accepted = set(fixture["accepted_future_v1_runtime_capabilities"])

    assert "live_actual_approval_flow" in accepted
    assert "real_guardian_decision_runtime_path" in accepted
    assert "provider_model_routing" in accepted
    assert "shell_haptic_intent_support" in accepted
    assert "first_shell_response_state_parity" in accepted
    assert "bounded_real_provider_sdk_network_egress_authority" in accepted
    assert "consumer_fake_executor_provider_sdk_network_egress_smoke_evidence" in accepted
    assert fixture["product_direction_only"] is True
    assert fixture["runtime_implementation_approved_by_this_fixture"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_destructive_edits_and_deletes_require_operator_approval() -> None:
    policy = _load_fixture()["operator_approval_policy"]

    assert policy["delete_requires_operator_approval"] is True
    assert policy["edit_requires_operator_approval"] is True
    assert policy["overwrite_requires_operator_approval"] is True
    assert policy["destructive_admin_or_connector_action_requires_operator_approval"] is True
    assert policy["applies_to_lima_ai_os"] is True
    assert policy["applies_to_shells"] is True


def test_v1_haptics_remain_shell_owned() -> None:
    haptics = _load_fixture()["haptics_ownership"]

    assert haptics["haptics_acceptable_as_v1_shell_experience_requirement"] is True
    assert haptics["shells_own_haptic_rendering"] is True
    assert haptics["lima_owns_haptic_device_implementation"] is False
    assert haptics["lima_may_define_future_haptic_intent_metadata"] is True
    assert haptics["haptic_implementation_added_here"] is False


def test_v1_current_status_tracks_post_g61_request_lane() -> None:
    current = _load_fixture()["current_status"]

    assert current["latest_completed_gate"] == "V1-G60"
    assert current["latest_authority_chain_audit"] == "V1-G56"
    assert current["latest_readiness_rollup"] == "V1-G60"
    assert (
        current["latest_request_stage_readiness_refresh"]
        == "V1_POST_G61_REQUEST_READINESS_REFRESH"
    )
    assert current["current_gate"] == "V1-G61"
    assert current["v1_g55_operator_approval_recorded"] is True
    assert current["v1_g55_runtime_implementation_approved"] is True
    assert current["v1_g55_wrapper_added"] is True
    assert current["v1_g55_public_api_exports_changed"] is True
    assert current["v1_g55_public_api_change_limited_to_approved_harness_exports"] is True
    assert current["v1_g55_independent_audit_complete"] is True
    assert current["v1_g56_request_packet_prepared"] is True
    assert current["v1_g56_operator_approval_recorded"] is True
    assert current["v1_g56_runtime_implementation_approved"] is True
    assert current["v1_g56_consumer_smoke_added"] is True
    assert current["v1_g56_independent_audit_complete"] is True
    assert current["v1_g57_request_packet_prepared"] is True
    assert current["v1_g57_operator_approval_recorded"] is True
    assert current["v1_g57_runtime_implementation_approved"] is True
    assert current["v1_g60_request_packet_prepared"] is True
    assert current["v1_g60_operator_approval_recorded"] is True
    assert current["v1_g60_runtime_implementation_approved"] is True
    assert current["v1_g60_dependency_manifest_edited"] is True
    assert current["v1_g60_lockfile_edited"] is False
    assert current["v1_g60_independent_audit_complete"] is True
    assert current["v1_g61_request_packet_prepared"] is True
    assert current["v1_g61_request_gate_audit_complete"] is True
    assert current["v1_g61_preapproval_runtime_tree_guard_audit_complete"] is True
    assert current["v1_g61_operator_decision_packet_status_audit_complete"] is True
    assert current["v1_post_g61_request_readiness_refresh_complete"] is True
    assert current["v1_candidate_harness_quickstart_current"] is True
    assert current["v1_candidate_harness_quickstart_verdict"] == (
        "QUICKSTART_READY_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER"
    )
    assert current["v1_candidate_harness_quickstart_execution_audit_complete"] is True
    assert current["v1_candidate_harness_quickstart_execution_audit_verdict"] == (
        "PASS_LOCAL_CANDIDATE_HARNESS_QUICKSTART_WITH_G61_OPERATOR_BLOCKER"
    )
    assert (
        current["v1_candidate_harness_quickstart_post_refresh_public_sparkbot_tests_passed"]
        == 8
    )
    assert (
        current[
            "v1_candidate_harness_quickstart_post_refresh_accessible_sparkbot_tests_passed"
        ]
        == 8
    )
    assert (
        current["v1_candidate_harness_quickstart_post_refresh_arc_bot_shell_tests_passed"]
        == 8
    )
    assert (
        current["v1_candidate_harness_quickstart_post_refresh_lima_focused_tests_passed"]
        == 17
    )
    assert (
        current["v1_candidate_harness_quickstart_post_refresh_lima_broader_tests_passed"]
        == 108
    )
    assert (
        current["v1_candidate_harness_quickstart_post_refresh_lima_full_suite_tests_passed"]
        == 5360
    )
    assert current["v1_consumer_harness_usability_matrix_current"] is True
    assert current["v1_release_candidate_acceptance_checklist_current"] is True
    assert current["v1_release_candidate_acceptance_checklist_verdict"] == (
        "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS"
    )
    assert current["v1_release_candidate_cutover_runbook_current"] is True
    assert current["v1_release_candidate_cutover_runbook_verdict"] == (
        "CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS"
    )
    assert current["v1_current_gate_consistency_audit_complete"] is True
    assert current["v1_current_candidate_validation_refresh_complete"] is True
    assert current["v1_current_validation_focused_current_gate_tests_passed"] == 153
    assert current["v1_current_validation_full_lima_suite_tests_passed"] == 5350
    assert (
        current[
            "v1_current_validation_latest_supplement_focused_final_blocker_index_tests_passed"
        ]
        == 15
    )
    assert (
        current[
            "v1_current_validation_latest_supplement_broader_v1_readiness_tests_passed"
        ]
        == 89
    )
    assert (
        current[
            "v1_current_validation_latest_supplement_full_lima_suite_tests_passed"
        ]
        == 5361
    )
    assert (
        current[
            "v1_current_validation_latest_handoff_supplement_post_g61_request_focused_tests_passed"
        ]
        == 8
    )
    assert (
        current[
            "v1_current_validation_latest_handoff_supplement_post_g61_request_broader_tests_passed"
        ]
        == 117
    )
    assert (
        current[
            "v1_current_validation_latest_handoff_supplement_post_g61_request_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert (
        current[
            "v1_current_validation_latest_handoff_supplement_quickstart_focused_tests_passed"
        ]
        == 7
    )
    assert (
        current[
            "v1_current_validation_latest_handoff_supplement_quickstart_adjacent_tests_passed"
        ]
        == 64
    )
    assert (
        current[
            "v1_current_validation_latest_handoff_supplement_quickstart_broader_tests_passed"
        ]
        == 133
    )
    assert (
        current[
            "v1_current_validation_latest_handoff_supplement_quickstart_full_lima_suite_tests_passed"
        ]
        == 5364
    )
    assert (
        current[
            "v1_current_validation_latest_supplement_release_cutover_final_readiness_or_g61_authority_created"
        ]
        is False
    )
    assert current["v1_post_validation_readiness_change_freshness_audit_complete"] is True
    assert (
        current[
            "v1_post_validation_readiness_change_freshness_full_lima_suite_tests_passed"
        ]
        == 5359
    )
    assert current["v1_latest_quickstart_post_refresh_full_lima_suite_tests_passed"] == 5360
    assert current["v1_latest_final_blocker_index_refresh_focused_tests_passed"] == 15
    assert current["v1_latest_final_blocker_index_refresh_broader_tests_passed"] == 89
    assert (
        current["v1_latest_final_blocker_index_refresh_full_lima_suite_tests_passed"]
        == 5361
    )
    assert (
        current[
            "v1_latest_post_g61_request_readiness_refresh_focused_tests_passed"
        ]
        == 8
    )
    assert (
        current[
            "v1_latest_post_g61_request_readiness_refresh_broader_tests_passed"
        ]
        == 117
    )
    assert (
        current[
            "v1_latest_post_g61_request_readiness_refresh_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert current["v1_latest_quickstart_artifact_refresh_focused_tests_passed"] == 7
    assert current["v1_latest_quickstart_artifact_refresh_adjacent_tests_passed"] == 64
    assert current["v1_latest_quickstart_artifact_refresh_broader_tests_passed"] == 133
    assert current["v1_latest_quickstart_artifact_refresh_full_lima_suite_tests_passed"] == 5364
    assert (
        current[
            "v1_latest_quickstart_artifact_refresh_release_cutover_final_readiness_production_arc_clean_checkpoint_or_g61_authority_created"
        ]
        is False
    )
    assert (
        current[
            "v1_post_validation_readiness_change_freshness_release_authority_created"
        ]
        is False
    )
    assert current["arc_bot_shell_local_drift_exclusion_audit_current"] is True
    assert (
        current["arc_bot_shell_local_drift_exclusion_audit_tracked_modified_file_count"]
        == 7
    )
    assert current[
        "arc_bot_shell_local_drift_exclusion_audit_untracked_file_count"
    ] == 64
    assert (
        current["arc_bot_shell_same_day_recheck_approved_g56_smoke_proof_paths_clean"]
        is True
    )
    assert (
        current[
            "arc_bot_shell_clean_checkpoint_required_before_release_final_branch_tag_cutover_or_readiness_claim"
        ]
        is True
    )
    assert current["arc_bot_shell_clean_checkpoint_proof_recorded"] is False
    assert current["v1_final_readiness_audit_template_current"] is True
    assert current["v1_g61_operator_approval_recorded"] is False
    assert current["v1_g61_runtime_implementation_approved"] is False
    assert current["v1_g61_valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]


def test_v1_current_status_adds_no_new_runtime_sdk_network_or_secret_behavior() -> None:
    current = _load_fixture()["current_status"]

    for key in (
        "runtime_behavior_added_by_refresh",
        "lima_runtime_files_changed_by_refresh",
        "tests_support_changed",
        "shell_repos_changed_by_refresh",
        "g61_runtime_vendor_sdk_import_execution_proof_added",
        "built_in_provider_sdk_client_added",
        "vendor_sdk_import_added_to_lima",
        "provider_endpoint_resolution_by_lima_added",
        "network_call_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
    ):
        assert current[key] is False, key


def test_v1_remaining_blockers_and_next_step_are_g61() -> None:
    fixture = _load_fixture()
    blockers = set(fixture["remaining_blockers"])

    assert "v1_g61_operator_approval_not_recorded" in blockers
    assert "runtime_vendor_sdk_import_execution_proof_not_implemented" in blockers
    assert "lockfile_edits_unapproved" in blockers
    assert "runtime_vendor_sdk_imports_in_lima_unapproved" in blockers
    assert "provider_secrets_and_credential_values_inaccessible_to_lima" in blockers
    assert "fallback_execution_unapproved" in blockers
    assert "consumer_production_runtime_integration_unapproved" in blockers
    assert "release_boundary_not_passed" in blockers
    assert (
        "arc_bot_shell_clean_checkpoint_proof_not_recorded_for_release_final_branch_tag_cutover_or_readiness_claim"
        in blockers
    )
    assert "v1_product_readiness_not_approved" in blockers
    assert "production_behavior_not_approved" in blockers
    assert fixture["recommended_next_step"] == "record_v1_g61_operator_decision"
    assert fixture["recommended_next_gap_id"] == "V1-G61"
    assert (
        fixture["recommended_next_gap_to_close"]
        == "runtime_vendor_sdk_import_execution_proof_request"
    )


def test_v1_product_readiness_doc_matches_post_g60_gate() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["target"]).read_text(encoding="utf-8")

    assert "LIMA remains `CANDIDATE_ONLY`." in text
    assert "first shell consumers" in text
    assert "public `Sparkbot`" in text
    assert "completed implementation evidence is refreshed through `V1-G60`" in text
    assert (
        "Request-stage readiness is refreshed through the post-G61 request readiness refresh."
        in text
    )
    assert "`V1-G60` is complete as approved dependency declaration" in text
    assert "Authoritative completed provider SDK/network and dependency evidence files:" in text
    assert "## Accepted Evidence Through G60 And G61 Request Stage" in text
    assert "Observed workspace branch for this refresh:" in text
    assert "`docs-v1-post-g60-readiness-and-next-lane-matrix`" in text
    assert "The current request-only approval lane label is:" in text
    assert "`prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`" in text
    assert "Authoritative G61 request files:" in text
    assert "`docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md`" in text
    assert "`docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`" in text
    assert "`docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`" in text
    assert "`docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`" in text
    assert "`docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`" in text
    assert "`docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md`" in text
    assert "`docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`" in text
    assert "`docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`" in text
    assert "`docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`" in text
    assert "`docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`" in text
    assert "`docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`" in text
    assert "`docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`" in text
    assert "`docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`" in text
    assert "`docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`" in text
    assert "Valid G61 operator choices are `Approve-V1-G61`, `Revise-V1-G61`, or `Pause`." in text
    assert "Current status remains not V1 product-ready." in text
    assert "V1-G61 preapproval runtime-tree guard audit" in text
    assert "V1-G61 operator decision packet status audit proving the packet is still awaiting one exact valid choice" in text
    assert "V1 candidate harness quickstart with current verdict `QUICKSTART_READY_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER`" in text
    assert "V1 candidate harness quickstart execution audit with current verdict `PASS_LOCAL_CANDIDATE_HARNESS_QUICKSTART_WITH_G61_OPERATOR_BLOCKER`" in text
    assert "V1 candidate harness quickstart post-refresh validation with public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 tests, plus LIMA focused quickstart/handoff 17 tests, broader V1 harness/readiness 108 tests, and full LIMA suite 5360 tests" in text
    assert "V1 consumer harness usability matrix for Sparkbot and Arc-Bot-shell local candidate smoke criteria" in text
    assert "V1 release-candidate acceptance checklist with current verdict `NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS`" in text
    assert "V1 release-candidate cutover runbook with current verdict `CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS`" in text
    assert "V1 current gate consistency audit proving the active gate is G61" in text
    assert "V1 current candidate validation refresh with 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing" in text
    assert "V1 current candidate validation refresh latest LIMA readiness freshness supplement with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests passing" in text
    assert "V1 current candidate validation refresh latest handoff freshness supplement with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests passing" in text
    assert "V1 post-validation readiness-change freshness audit proving same-turn readiness edits after the validation refresh are covered by release/cutover freshness checks, a 5359-test full LIMA suite pass, latest quickstart post-refresh 5360-test full LIMA suite evidence, and latest final blocker/index refresh evidence passing 15 focused final blocker/index tests, 89 broader affected readiness tests, and 5361 full-suite tests" in text
    assert "V1 latest post-G61 request readiness-refresh evidence passing 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and the 5362-test full LIMA suite" in text
    assert "V1 latest quickstart artifact refresh evidence passing 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and the 5364-test full LIMA suite" in text
    assert "V1 Arc-Bot-shell local drift exclusion audit proving current Arc local drift, currently 7 tracked modified files and 64 untracked files, is compatibility-only evidence and excluded from V1 release-candidate/final-readiness proof, with same-day recheck evidence that approved G56 smoke proof paths remain clean" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1 final readiness audit template for the future post-G61 release-candidate audit" in text
    assert "V1 operator unblock action packet for recording exactly one G61 operator decision" in text
    assert "V1 final candidate branch index for saved checkpoint and future branch/tag guard traceability" in text
    assert "Arc-Bot-shell clean-checkpoint gate requiring clean checkpoint proof before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim" in text
    assert "local consumer harness usability criteria" in text
    assert "fake in-process executors, sanitized fixtures, no-network behavior, no-secret access, and no production wiring" in text
    assert "No V1-G61 implementation is approved" in text
    assert "The operator decision packet status audit proves that no V1-G61 choice is recorded yet." in text
    assert "The V1.0.0 release-candidate acceptance checklist is not satisfied and the release-candidate cutover runbook remains blocked" in text
    assert "The operator unblock action packet and final candidate branch index are handoff and traceability evidence only." in text
    assert "The current gate consistency audit, current candidate validation refresh including latest LIMA readiness freshness supplement 15/89/5361 evidence and latest handoff freshness supplement 8/117/5362 plus 7/64/133/5364 evidence, post-validation readiness-change freshness audit including latest final blocker/index 15/89/5361 evidence, latest post-G61 request readiness-refresh 8/117/5362 evidence, and latest quickstart artifact refresh 7/64/133/5364 evidence, current quickstart post-refresh evidence, current Arc drift exclusion audit, and clean Arc-Bot-shell checkpoint proof are required inputs to any future final readiness audit" in text
    assert "built-in provider SDK clients" in text
    assert "secret lookup, credential value access" in text
    assert "consumer repository edits for V1-G61" in text
    assert "V1 product readiness or production readiness claims" in text
    assert "clean Arc-Bot-shell checkpoint proof is not recorded for release-candidate, final-readiness, branch, tag, cutover, or readiness claims" in text
