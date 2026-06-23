"""Static checks for the V1 candidate test handoff manifest."""

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
    / "v1_candidate_test_handoff_manifest.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_candidate_test_handoff_manifest_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["manifest_id"] == "v1_candidate_test_handoff_manifest"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_lima_commit_before_manifest"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["handoff_verdict"] == (
        "READY_FOR_LOCAL_CANDIDATE_TESTING_WITH_G61_OPERATOR_BLOCKER"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_candidate_test_handoff_manifest_records_repo_checkpoints() -> None:
    checkpoints = _load_fixture()["repository_checkpoints"]

    assert checkpoints["lima_ai_os"] == {
        "local_path": "C:\\Users\\limap\\LIMA-AI-OS",
        "branch": "docs-v1-post-g60-readiness-and-next-lane-matrix",
        "commit": "37626bf236bf96c8a57a3ca351668e90eeb0e651",
        "current_readiness_updates_present": True,
    }
    assert checkpoints["public_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "repository": "sparkpit-labs/Sparkbot",
        "branch": "v1-g56-runtime-authority-chain-audit",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "local_dirty_state": "clean",
        "target_publication_resolved": True,
    }
    assert checkpoints["accessible_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot",
        "repository": "armpit-symphony/Sparkbot",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ddaa4ccaacd328ddcc1f00a040c2c140abee428e",
        "tracks_origin": True,
        "local_dirty_state": "clean",
    }
    assert checkpoints["arc_bot_shell"] == {
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0",
        "tracks_origin": True,
        "local_dirty_state": "dirty_unrelated_local_worktree_drift_excluded_from_v1_proof",
    }


def test_v1_candidate_test_handoff_manifest_validation_commands_are_complete() -> None:
    commands = _load_fixture()["validation_commands"]

    assert [item["step"] for item in commands] == list(range(1, 11))
    assert commands[0]["repo"] == "C:\\Users\\limap\\Sparkbot-public"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands[0]["command"]
    assert commands[0]["expected_result"] == "8 passed"
    assert commands[2]["repo"] == "C:\\Users\\limap\\Sparkbot"
    assert commands[2]["expected_result"] == "8 passed"
    assert commands[4]["repo"] == "C:\\Users\\limap\\Arc-Bot-shell"
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in commands[4]["command"]
    assert commands[6]["repo"] == "C:\\Users\\limap\\LIMA-AI-OS"
    assert "test_v1_candidate_harness_quickstart.py" in commands[6]["command"]
    assert "test_v1_candidate_test_handoff_manifest.py" in commands[6]["command"]
    assert "test_v1_consumer_harness_usability_matrix.py" in commands[6]["command"]
    assert "test_v1_current_gate_consistency_audit.py" in commands[6]["command"]
    assert "test_v1_final_blocker_register.py" in commands[6]["command"]
    assert "test_v1_g61_operator_decision_packet_status_audit.py" in commands[6]["command"]
    assert "test_v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request.py" in commands[6]["command"]
    assert commands[7]["command"] == "python -m compileall lima"
    assert commands[8]["command"] == "python -m pytest -q tests -p no:cacheprovider"
    assert commands[9]["command"] == "git diff --check"


def test_v1_candidate_test_handoff_manifest_scope_and_boundaries_are_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["candidate_scope_proven"] == [
        "public_sparkbot_local_fake_executor_g55_wrapper_smoke",
        "accessible_sparkbot_pushed_g56_fake_executor_smoke_checkpoint",
        "arc_bot_shell_pushed_g56_fake_executor_smoke_checkpoint_with_local_drift_excluded",
        "candidate_harness_quickstart_defines_operator_smoke_path",
        "candidate_harness_quickstart_execution_audit_records_current_consumer_smoke_and_lima_73_5359_validation",
        "post_g61_request_readiness_refresh_records_latest_handoff_freshness_lima_8_117_5362",
        "latest_quickstart_artifact_refresh_records_current_evidence_to_preserve_lima_7_64_133_5364",
        "consumer_harness_usability_matrix_defines_candidate_smoke_boundary",
        "current_gate_consistency_audit_locks_active_g61_gate",
        "release_candidate_checklist_and_cutover_blocked_until_g61_final_audit_and_clean_arc_checkpoint_proof",
        "final_readiness_audit_template_not_executed_by_manifest",
        "g61_operator_decision_packet_status_audit_confirms_awaiting_exactly_one_valid_choice",
        "lima_runtime_authority_chain_complete_through_g56",
        "v1_g57_through_v1_g60_candidate_only_evidence_complete",
        "g61_request_only_operator_gate_recorded",
    ]

    for key, value in fixture["required_false_boundaries"].items():
        assert value is False, key


def test_v1_candidate_test_handoff_manifest_records_blockers_and_stop_conditions() -> None:
    fixture = _load_fixture()

    assert fixture["current_blockers"] == {
        "v1_g61_implementation": "requires_exact_operator_choice",
        "runtime_import_execution_proof": "blocked_until_v1_g61_approved",
        "release_candidate_branch_tag_authority": (
            "blocked_until_release_candidate_checklist_final_readiness_audit_and_clean_arc_checkpoint_proof_pass_under_separate_approval"
        ),
        "arc_bot_shell_clean_checkpoint_proof": (
            "blocked_while_unrelated_local_drift_remains_excluded_from_current_v1_proof"
        ),
        "post_g61_authorities": (
            "lockfile_runtime_import_client_credentials_endpoint_network_fallback_consumer_production_and_product_readiness_remain_separate_blocked_gates"
        ),
    }
    assert fixture["stop_conditions"] == [
        "v1_g61_implementation_without_exact_approval",
        "treat_manifest_as_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim_authority",
        "treat_arc_bot_shell_compatibility_evidence_as_clean_checkpoint_for_release_final_branch_tag_cutover_or_readiness_claims_while_local_drift_excluded",
        "consumer_repo_edit_from_manifest_lane",
        "runtime_or_public_api_change_from_manifest_lane",
        "runtime_vendor_sdk_import_lockfile_secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]
    assert fixture["next_operator_actions"] == [
        "record_exactly_one_v1_g61_operator_choice",
        "if_g61_is_approved_implement_only_runtime_vendor_sdk_import_execution_proof_scope",
    ]


def test_v1_candidate_test_handoff_manifest_records_latest_freshness_supplements() -> None:
    fixture = _load_fixture()
    supplements = fixture["latest_handoff_freshness_supplements"]
    text = (REPO_ROOT / fixture["documents"]["manifest"]).read_text(
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
    assert "post-G61 request readiness-refresh supplement records later handoff freshness with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "latest quickstart artifact refresh records current quickstart evidence-to-preserve assertions with 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "Latest handoff freshness supplements: evidence only; they do not approve V1-G61 implementation, release-candidate acceptance, final readiness, cutover, consumer production integration, Arc-Bot-shell clean-checkpoint proof, product readiness, or production readiness." in text


def test_v1_candidate_test_handoff_manifest_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["manifest"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Candidate Test Handoff Manifest" in text
    assert fixture["source_lima_commit_before_manifest"] in text
    assert "READY_FOR_LOCAL_CANDIDATE_TESTING_WITH_G61_OPERATOR_BLOCKER" in text
    assert "public Sparkbot" in text
    assert "Arc-Bot-shell" in text
    assert "unrelated local worktree drift excluded from current V1 proof" in text
    assert "not clean-checkpoint evidence" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART.md" in text
    assert "shortest safe local smoke command path" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "G56 smoke reruns as 8 passed each" in text
    assert "LIMA focused handoff/current-gate pytest rerun as 73 passed" in text
    assert "full LIMA suite validation as 5359 passed" in text
    assert "post-G61 request readiness-refresh supplement records later handoff freshness" in text
    assert "latest quickstart artifact refresh records current quickstart evidence-to-preserve assertions" in text
    assert "V1_CONSUMER_HARNESS_USABILITY_MATRIX.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "locks current-facing handoff, readiness, and release artifacts to the active G61 operator-decision gate" in text
    assert "release-candidate checklist and cutover runbook remain blocked" in text
    assert "clean Arc-Bot-shell checkpoint proof is recorded" in text
    assert "final readiness audit template has not been executed by this manifest" in text
    assert "status audit proves the packet is still awaiting exactly one valid choice" in text
    assert "fake in-process executor, sanitized fixture, no-network, no-secret, no-production-wiring evidence only" in text
    assert "public G56 target publication resolved by audit" in text
    assert "V1-G61 remains unapproved" in text
    assert "No" not in text[:300]
    assert "does not approve V1-G61 implementation" in text
    assert "V1.0.0 release-candidate branch or tag authorized by this manifest" in text
    assert "release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim authorized by this manifest" in text
    assert "Arc-Bot-shell clean-checkpoint evidence claimed by this manifest" in text
    assert "Release-candidate branch/tag authority: blocked" in text
    assert "Arc-Bot-shell clean-checkpoint proof: blocked" in text
    assert "clean-checkpoint proof for release, final-readiness, branch, tag, cutover, or readiness claims" in text
    assert "claim V1.0 completion, product readiness, or production readiness" in text


def test_v1_candidate_test_handoff_manifest_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["manifest"]).read_text(
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
