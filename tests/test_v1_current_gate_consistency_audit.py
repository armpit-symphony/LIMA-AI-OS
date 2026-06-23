"""Static checks for the V1 current gate consistency audit."""

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
    / "v1_current_gate_consistency_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_current_gate_consistency_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_current_gate_consistency_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-22"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["audit_verdict"] == "PASS_CURRENT_GATE_POST_G61_RELEASE_READINESS"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_current_gate_consistency_records_current_state() -> None:
    state = _load_fixture()["required_current_state"]

    assert state == {
        "current_gate": "V1-G61",
        "required_next_action": (
            "record_clean_arc_bot_shell_checkpoint_proof_then_execute_future_final_readiness_audit"
        ),
        "valid_operator_choices": [
            "Approve-V1-G61",
            "Revise-V1-G61",
            "Pause",
        ],
        "implementation_approval_recorded": True,
        "runtime_vendor_sdk_import_execution_proof_implemented": True,
        "public_sparkbot_g56_publication_blocker_resolved": True,
        "candidate_harness_quickstart_execution_audit_current": True,
        "g61_operator_decision_packet_status_audit_current": True,
        "g61_operator_decision_packet_approved": True,
        "release_candidate_acceptance_checklist_blocked_pending_arc_checkpoint_and_final_readiness": True,
        "release_candidate_cutover_runbook_blocked_pending_checklist_final_readiness_and_arc_checkpoint": True,
        "final_readiness_audit_template_waits_for_arc_clean_checkpoint": True,
        "post_validation_readiness_change_freshness_audit_current": True,
        "arc_bot_shell_local_drift_gate_current": True,
        "arc_bot_shell_local_drift_exclusion_audit_current": True,
        "arc_bot_shell_local_drift_exclusion_audit_tracked_modified_file_count": 7,
        "arc_bot_shell_local_drift_exclusion_audit_untracked_file_count": 64,
        "arc_bot_shell_clean_checkpoint_required_before_release_final_branch_tag_cutover_or_readiness_claim": True,
        "long_range_roadmap_v1_section_current": True,
        "decision_log_v1_current_gate_current": True,
        "historical_consumer_docs_current_status_refresh_current": True,
        "current_validation_refresh_full_lima_suite_tests_passed": 5350,
        "current_validation_latest_handoff_freshness_post_g61_request_focused_tests_passed": 8,
        "current_validation_latest_handoff_freshness_post_g61_request_broader_tests_passed": 117,
        "current_validation_latest_handoff_freshness_post_g61_request_full_lima_suite_tests_passed": 5362,
        "current_validation_latest_handoff_freshness_quickstart_focused_tests_passed": 7,
        "current_validation_latest_handoff_freshness_quickstart_adjacent_tests_passed": 64,
        "current_validation_latest_handoff_freshness_quickstart_broader_tests_passed": 133,
        "current_validation_latest_handoff_freshness_quickstart_full_lima_suite_tests_passed": 5364,
        "post_validation_same_turn_full_lima_suite_tests_passed": 5359,
        "latest_quickstart_post_refresh_full_lima_suite_tests_passed": 5360,
        "latest_final_blocker_index_refresh_focused_tests_passed": 15,
        "latest_final_blocker_index_refresh_broader_tests_passed": 89,
        "latest_final_blocker_index_refresh_full_lima_suite_tests_passed": 5361,
        "latest_post_g61_request_readiness_refresh_focused_tests_passed": 8,
        "latest_post_g61_request_readiness_refresh_broader_tests_passed": 117,
        "latest_post_g61_request_readiness_refresh_full_lima_suite_tests_passed": 5362,
        "latest_quickstart_artifact_refresh_focused_tests_passed": 7,
        "latest_quickstart_artifact_refresh_adjacent_tests_passed": 64,
        "latest_quickstart_artifact_refresh_broader_tests_passed": 133,
        "latest_quickstart_artifact_refresh_full_lima_suite_tests_passed": 5364,
    }


def test_v1_current_gate_consistency_required_snippets_are_present() -> None:
    fixture = _load_fixture()

    for document_key, snippets in fixture["required_snippets_by_document"].items():
        relative_path = fixture["documents"][document_key]
        text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for snippet in snippets:
            assert snippet in text, f"{snippet!r} missing from {relative_path}"


def test_v1_current_gate_consistency_rejects_stale_current_state_language() -> None:
    fixture = _load_fixture()
    current_document_keys = [
        "readme",
        "current_project_state",
        "long_range_roadmap",
        "decisions",
        "product_readiness_target",
        "readiness_gap_matrix",
        "final_blocker_register",
        "operator_unblock_packet",
        "final_candidate_branch_index",
        "release_candidate_acceptance_checklist",
        "release_candidate_cutover_runbook",
        "final_readiness_audit_template",
        "consumer_target_state_after_arc_readiness_integration",
        "consumer_testability_matrix_through_work_settings",
        "current_candidate_validation_refresh_audit",
        "post_validation_readiness_change_freshness_audit",
        "g61_operator_decision_packet_status_audit",
        "arc_bot_shell_local_drift_exclusion_audit",
        "candidate_harness_quickstart",
        "candidate_harness_quickstart_execution_audit",
    ]
    combined_text = "\n".join(
        (REPO_ROOT / fixture["documents"][document_key]).read_text(encoding="utf-8")
        for document_key in current_document_keys
    )

    for forbidden in fixture["forbidden_current_state_phrases"]:
        assert forbidden not in combined_text


def test_v1_current_gate_consistency_public_sparkbot_audit_has_current_refresh() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT
        / fixture["documents"]["public_sparkbot_g56_publication_resolution_audit"]
    ).read_text(encoding="utf-8")

    assert "Original Residual Blocker At Audit Time" in text
    assert "Current Status Refresh" in text
    assert "Public Sparkbot G56 publication blocker: resolved." in text
    assert (
        "Active blocker: V1-G61 runtime vendor SDK import execution proof "
        "operator decision."
    ) in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" not in text


def test_v1_current_gate_consistency_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    assert boundaries["v1_g61_operator_approval_recorded_by_audit"] is True
    assert (
        boundaries[
            "v1_g61_runtime_vendor_sdk_import_execution_proof_implemented_by_audit"
        ]
        is True
    )

    for key, value in boundaries.items():
        if key in {
            "v1_g61_operator_approval_recorded_by_audit",
            "v1_g61_runtime_vendor_sdk_import_execution_proof_implemented_by_audit",
        }:
            continue
        assert value is False, key


def test_v1_current_gate_consistency_audit_doc_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Current Gate Consistency Audit" in text
    assert fixture["audit_verdict"] in text
    assert "Current active gate: `V1-G61`." in text
    assert "`docs/LIMA_LONG_RANGE_ROADMAP.md`" in text
    assert "`docs/DECISIONS.md`" in text
    assert (
        "`docs/readiness/V1_CONSUMER_TARGET_STATE_AFTER_ARC_READINESS_INTEGRATION.md`"
        in text
    )
    assert (
        "`docs/readiness/V1_CONSUMER_TESTABILITY_MATRIX_THROUGH_WORK_SETTINGS.md`"
        in text
    )
    assert "Current long-range roadmap V1 section: aligned to G61 operator-decision blocker." in text
    assert "Current decision log: includes ADR-0340 recording V1-G61 as the current blocker and earlier V1 ADRs as historical." in text
    assert "Historical consumer target/testability docs: include current-status refreshes pointing to G61 and preserving G55 as audit-time evidence only." in text
    assert "Current G61 operator decision packet status audit: pass and approved for the bounded import proof." in text
    assert "Current release-candidate acceptance checklist: blocked pending final readiness audit and clean Arc checkpoint proof." in text
    assert "Current release-candidate cutover runbook: blocked pending checklist satisfaction, final readiness audit, and clean Arc checkpoint proof." in text
    assert "Current final readiness audit template: ready to run after clean Arc checkpoint proof." in text
    assert "Current post-validation readiness-change freshness audit: current" in text
    assert "Current Arc-Bot-shell local drift posture: `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md` records 7 tracked modified files and 64 untracked files as compatibility evidence only; excluded drift is not clean-checkpoint proof." in text
    assert "Current Arc-Bot-shell clean-checkpoint gate: clean checkpoint proof is required before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim." in text
    assert "Current validation-refresh full LIMA suite evidence: 5350 tests passed." in text
    assert "Current validation-refresh latest LIMA readiness freshness supplement: 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests passed." in text
    assert "Current validation-refresh latest handoff freshness supplement: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests passed." in text
    assert "Current post-validation same-turn full LIMA suite evidence: 5359 tests passed." in text
    assert "Latest quickstart post-refresh full LIMA suite evidence: 5360 tests passed." in text
    assert "Latest final blocker/index freshness evidence: 15 focused final blocker/index tests, 89 broader affected readiness tests, and 5361 full-suite tests passed." in text
    assert "Latest post-G61 request readiness-refresh evidence: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests passed." in text
    assert "Latest quickstart artifact refresh evidence: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests passed." in text
    assert "public Sparkbot publication blocked by GitHub 403" in text
    assert "active V1-G57 operator-decision blocker" in text
    assert "release-candidate branch, tag, cutover, or readiness action before checklist satisfaction, clean Arc-Bot-shell checkpoint proof, and final-readiness audit pass" in text
    assert "release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim that treats excluded Arc-Bot-shell drift as clean-checkpoint proof" in text
    assert "Arc-Bot-shell smoke evidence described as clean-checkpoint evidence while unrelated local drift remains unexcluded" in text
    assert "Recorded choice: Approve-V1-G61" in text
    assert "V1-G61 operator approval recorded by this audit: yes." in text
    assert fixture["next_recommended_step"] in text


def test_v1_current_gate_consistency_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

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
