"""Static checks for the V1 candidate handoff manifest execution audit."""

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
    / "v1_candidate_test_handoff_manifest_execution_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_candidate_handoff_execution_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == (
        "v1_candidate_test_handoff_manifest_execution_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_lima_commit_before_audit"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["audit_verdict"] == "PASS_WITH_G61_OPERATOR_BLOCKER"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_candidate_handoff_execution_audit_records_checkpoints() -> None:
    checkpoints = _load_fixture()["executed_checkpoints"]

    assert checkpoints["lima_ai_os"] == {
        "local_path": "C:\\Users\\limap\\LIMA-AI-OS",
        "branch": "docs-v1-post-g60-readiness-and-next-lane-matrix",
        "commit": "37626bf236bf96c8a57a3ca351668e90eeb0e651",
        "current_readiness_updates_present": True,
    }
    assert checkpoints["public_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "branch": "v1-g56-runtime-authority-chain-audit",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "clean": True,
        "target_repository": "sparkpit-labs/Sparkbot",
        "target_branch_published": True,
        "publication_resolved_by_audit": True,
    }
    assert checkpoints["accessible_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ddaa4ccaacd328ddcc1f00a040c2c140abee428e",
        "clean": True,
        "tracks_origin": True,
    }
    assert checkpoints["arc_bot_shell"] == {
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0",
        "clean": False,
        "local_drift_excluded_from_v1_proof": True,
        "tracks_origin": True,
    }


def test_v1_candidate_handoff_execution_audit_records_validation_results() -> None:
    validation = _load_fixture()["validation_results"]

    for key in (
        "public_sparkbot_g56_smoke",
        "accessible_sparkbot_g56_smoke",
        "arc_bot_shell_g56_smoke",
    ):
        assert validation[key]["passed"] is True
        assert validation[key]["tests_passed"] == 8

    assert validation["lima_focused_candidate_harness_quickstart_execution_readiness_set"] == {
        "passed": True,
        "tests_passed": 73,
    }
    assert validation["lima_focused_current_gate_release_readiness_set"] == {
        "passed": True,
        "tests_passed": 153,
    }
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"] == {
        "command": "python -m pytest -q tests -p no:cacheprovider",
        "passed": True,
        "tests_passed": 5359,
    }
    assert validation["lima_diff_check"] == {
        "command": "git diff --check",
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert validation["lima_cached_diff_check"] == {
        "command": "git diff --cached --check",
        "passed": True,
    }


def test_v1_candidate_handoff_execution_audit_accepts_expected_evidence() -> None:
    fixture = _load_fixture()

    assert fixture["evidence_accepted"] == [
        "public_sparkbot_local_g56_fake_executor_smoke_passed",
        "public_sparkbot_g56_publication_resolved",
        "accessible_sparkbot_g56_fake_executor_smoke_passed",
        "arc_bot_shell_g56_fake_executor_smoke_passed_with_local_drift_excluded",
        "v1_candidate_harness_quickstart_current",
        "v1_candidate_harness_quickstart_execution_audit_current_with_consumer_8_each_lima_73_5359",
        "v1_candidate_harness_quickstart_execution_audit_same_turn_consumer_refresh_2026_06_21_public_accessible_arc_8_each",
        "v1_candidate_harness_quickstart_execution_audit_post_refresh_lima_17_108_5360",
        "v1_post_g61_request_readiness_refresh_records_latest_handoff_freshness_lima_8_117_5362",
        "v1_latest_quickstart_artifact_refresh_records_current_evidence_to_preserve_lima_7_64_133_5364",
        "v1_consumer_harness_usability_matrix_current",
        "v1_current_gate_consistency_audit_current",
        "v1_current_gate_consistency_audit_committed_stale_claim_rejection_proof",
        "v1_g61_operator_decision_packet_status_audit_current_awaiting_choice",
        "v1_release_candidate_acceptance_checklist_current_blocked_not_authority",
        "v1_release_candidate_cutover_runbook_current_blocked_not_authority",
        "v1_final_readiness_audit_template_current_not_executed",
        "arc_bot_shell_candidate_smoke_not_clean_checkpoint_proof",
        "lima_handoff_final_blocker_final_index_final_template_g61_request_guard_status_assertions_aligned",
        "full_lima_suite_5359_passed_at_current_manifest_checkpoint",
    ]


def test_v1_candidate_handoff_execution_audit_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_candidate_handoff_execution_audit_records_blockers_and_stops() -> None:
    fixture = _load_fixture()

    assert fixture["current_blockers"] == {
        "v1_g61_implementation": "requires_exact_operator_choice",
        "runtime_import_execution_proof": "blocked_until_v1_g61_approved",
        "release_candidate_branch_or_tag_authority": (
            "blocked_until_acceptance_checklist_passes_after_g61_resolution"
        ),
        "release_candidate_cutover": (
            "blocked_until_cutover_runbook_executes_after_release_candidate_acceptance"
        ),
        "final_readiness": "blocked_until_final_readiness_audit_executes_and_passes",
        "arc_bot_shell_clean_checkpoint_proof": (
            "blocked_until_clean_checkpoint_proof_recorded_after_local_drift_absent_or_resolved_and_revalidated_before_release_final_branch_tag_cutover_or_readiness_claim"
        ),
        "post_g61_authorities": (
            "lockfile_runtime_import_client_credentials_endpoint_network_fallback_consumer_production_and_product_readiness_remain_separate_blocked_gates"
        ),
    }
    assert fixture["stop_conditions_preserved"] == [
        "v1_g61_implementation_without_exact_approval",
        "treat_this_audit_as_g61_approval",
        "treat_this_audit_as_release_candidate_branch_or_tag_authority",
        "treat_this_audit_as_passed_final_readiness_audit",
        "treat_arc_candidate_smoke_as_clean_checkpoint_proof_while_local_drift_excluded",
        "consumer_repo_edit_from_execution_audit_lane",
        "runtime_or_public_api_change_from_execution_audit_lane",
        "runtime_vendor_sdk_import_lockfile_secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]
    assert fixture["recommended_next_step"] == (
        "record_exactly_one_v1_g61_operator_choice"
    )


def test_v1_candidate_handoff_execution_audit_records_latest_freshness_supplements() -> None:
    fixture = _load_fixture()
    supplements = fixture["latest_handoff_freshness_supplements"]
    text = (REPO_ROOT / fixture["documents"]["execution_audit"]).read_text(
        encoding="utf-8"
    )

    assert supplements == {
        "latest_post_g61_request_refresh_focused_tests_passed": 8,
        "latest_post_g61_request_refresh_broader_tests_passed": 117,
        "latest_post_g61_request_refresh_full_lima_suite_tests_passed": 5362,
        "latest_quickstart_artifact_refresh_focused_tests_passed": 7,
        "latest_quickstart_artifact_refresh_adjacent_tests_passed": 64,
        "latest_quickstart_artifact_refresh_broader_tests_passed": 133,
        "latest_quickstart_artifact_refresh_full_lima_suite_tests_passed": 5364,
        "implementation_authority_created": False,
        "release_candidate_authority_created": False,
        "final_readiness_authority_created": False,
        "cutover_authority_created": False,
        "consumer_production_integration_authority_created": False,
        "arc_clean_checkpoint_authority_created": False,
        "product_or_production_readiness_authority_created": False,
    }
    assert "V1 post-G61 request readiness-refresh supplement records later handoff freshness with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests." in text
    assert "V1 latest quickstart artifact refresh records current evidence-to-preserve assertions with 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "Latest handoff freshness supplements remain evidence-only and do not create G61 implementation, release-candidate, final-readiness, cutover, consumer production integration, Arc clean-checkpoint, product-readiness, or production-readiness authority." in text


def test_v1_candidate_handoff_execution_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["execution_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Candidate Test Handoff Manifest Execution Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert "PASS_WITH_G61_OPERATOR_BLOCKER" in text
    assert "153 passed" in text
    assert "73 passed" in text
    assert "5359 passed" in text
    assert "focused candidate harness quickstart execution/readiness pytest set" in text
    assert "focused current-gate/release-readiness pytest set" in text
    assert "V1 candidate harness quickstart is current" in text
    assert "V1 candidate harness quickstart execution audit is current" in text
    assert "smoke reruns as 8 passed each" in text
    assert (
        "same-turn 2026-06-21 consumer smoke refresh with all three consumers "
        "still passing 8 tests each"
    ) in text
    assert "LIMA focused handoff/current-gate pytest rerun as 73 passed" in text
    assert "full LIMA suite validation as 5359 passed at the original audit checkpoint" in text
    assert (
        "post-refresh LIMA validation passing 17 focused quickstart/handoff "
        "tests, 108 broader V1 harness/readiness tests, and 5360 full-suite "
        "tests after the same-turn refresh assertions"
    ) in text
    assert "V1 post-G61 request readiness-refresh supplement records later handoff freshness" in text
    assert "V1 latest quickstart artifact refresh records current evidence-to-preserve assertions" in text
    assert "V1 consumer harness usability matrix is current" in text
    assert "V1 current gate consistency audit is current" in text
    assert "committed proof that stale public Sparkbot publication" in text
    assert "V1-G61 operator decision packet status audit is current" in text
    assert "awaiting exactly one valid operator choice" in text
    assert "V1 release-candidate acceptance checklist is current" in text
    assert "blocked evidence, not release authority" in text
    assert "V1 release-candidate cutover runbook is current" in text
    assert "blocked evidence, not cutover authority" in text
    assert "V1 final readiness audit template is current as future audit scaffolding only" in text
    assert "not clean-checkpoint proof while unrelated Arc local drift remains excluded" in text
    assert "G61 preapproval runtime-tree guard audit" in text
    assert "G61 operator decision packet status audit" in text
    assert "post-G61 readiness assertions remain aligned" in text
    assert "Full LIMA static/runtime-test suite passes at the current manifest checkpoint with 5359 tests." in text
    assert "Public Sparkbot G56 publication is resolved" in text
    assert "unrelated local worktree drift is excluded from V1 proof" in text
    assert "V1-G61 remains unapproved" in text
    assert "V1-G61 implementation approval recorded: no." in text
    assert "Release-candidate branch or tag authority created by this audit: no." in text
    assert "Final readiness audit executed or passed by this audit: no." in text
    assert "Arc-Bot-shell clean-checkpoint proof claimed by this audit: no." in text
    assert "treat this audit as release-candidate branch or tag authority" in text
    assert "treat this audit as a passed final readiness audit" in text
    assert "treat Arc-Bot-shell local candidate smoke evidence as clean-checkpoint proof" in text
    assert "Public Sparkbot remote publication remains blocked" not in text
    assert "V1-G57 remains unapproved" not in text
    assert "Provider SDK clients added: no." in text
    assert "V1.0 completion, product-readiness, or production-readiness claimed: no." in text


def test_v1_candidate_handoff_execution_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["execution_audit"]).read_text(
        encoding="utf-8"
    )

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
