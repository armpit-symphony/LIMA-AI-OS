"""Static checks for the V1 consumer harness usability matrix."""

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
    / "v1_consumer_harness_usability_matrix.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_consumer_harness_usability_matrix_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["matrix_id"] == "v1_consumer_harness_usability_matrix"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-21"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_matrix"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["matrix_verdict"] == (
        "HARNESS_USABLE_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_consumer_harness_usability_matrix_criteria_are_bounded() -> None:
    assert _load_fixture()["usability_criteria"] == [
        "approved_candidate_public_wrapper_symbols_only",
        "fake_in_process_provider_sdk_network_executor_injected_by_harness",
        "sanitized_request_metadata_only",
        "candidate_call_shape_and_authority_metadata_only",
        "no_lima_owned_dns_http_socket_network_call",
        "no_provider_endpoint_resolution_credential_token_fallback_connector_browser_file_device_robotics_or_physical_world_action",
        "g61_operator_decision_packet_status_audit_current_awaiting_choice",
        "current_gate_consistency_audit_current_rejects_stale_release_claims",
        "current_validation_post_validation_freshness_post_g61_request_refresh_and_quickstart_artifact_refresh_current_for_harness_handoff",
        "release_candidate_checklist_and_cutover_blocked_until_g61_final_audit_and_clean_arc_checkpoint_proof",
        "arc_bot_shell_smoke_is_compatibility_evidence_not_clean_checkpoint_until_clean_checkpoint_proof_recorded_before_release_claims",
        "stop_before_g61_implementation_without_exact_approval",
    ]


def test_v1_consumer_harness_usability_matrix_names_expected_consumers() -> None:
    consumers = _load_fixture()["consumers"]

    assert set(consumers) == {
        "public_sparkbot",
        "accessible_sparkbot",
        "arc_bot_shell",
    }
    assert consumers["public_sparkbot"]["repository"] == "sparkpit-labs/Sparkbot"
    assert consumers["accessible_sparkbot"]["repository"] == "armpit-symphony/Sparkbot"
    assert consumers["arc_bot_shell"]["repository"] == "armpit-symphony/Arc-Bot-shell"
    assert consumers["public_sparkbot"]["expected_result"] == "8 passed"
    assert consumers["accessible_sparkbot"]["expected_result"] == "8 passed"
    assert consumers["arc_bot_shell"]["expected_result"] == "8 passed"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in consumers["public_sparkbot"]["command"]
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in consumers["arc_bot_shell"]["command"]


def test_v1_consumer_harness_usability_matrix_keeps_consumers_candidate_only() -> None:
    consumers = _load_fixture()["consumers"]

    for name, consumer in consumers.items():
        assert consumer["usable_path"] == (
            "g56_fake_executor_provider_sdk_network_egress_smoke"
        ), name
        assert consumer["candidate_smoke_only"] is True, name
        if name == "arc_bot_shell":
            assert consumer["clean_checkpoint_evidence"] is False
        assert consumer["production_wiring_approved"] is False, name
        assert consumer["provider_egress_approved"] is False, name


def test_v1_consumer_harness_usability_matrix_records_current_freshness_evidence() -> None:
    freshness = _load_fixture()["current_freshness_evidence"]

    assert freshness == {
        "current_candidate_validation_focused_tests_passed": 153,
        "current_candidate_validation_full_lima_suite_tests_passed": 5350,
        "candidate_harness_quickstart_public_sparkbot_tests_passed": 8,
        "candidate_harness_quickstart_accessible_sparkbot_tests_passed": 8,
        "candidate_harness_quickstart_arc_bot_shell_tests_passed": 8,
        "candidate_harness_quickstart_lima_focused_tests_passed": 17,
        "candidate_harness_quickstart_lima_broader_v1_tests_passed": 108,
        "candidate_harness_quickstart_lima_full_suite_tests_passed": 5360,
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
        "release_cutover_final_readiness_or_g61_authority_created": False,
        "arc_bot_shell_clean_checkpoint_proof_created": False,
    }


def test_v1_consumer_harness_usability_matrix_preserves_required_false_boundaries() -> None:
    for key, value in _load_fixture()["required_false_boundaries"].items():
        assert value is False, key


def test_v1_consumer_harness_usability_matrix_records_stop_conditions() -> None:
    fixture = _load_fixture()

    assert fixture["stop_conditions"] == [
        "v1_g61_implementation_without_exact_approval",
        "treat_matrix_as_g61_approval",
        "treat_matrix_as_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim_authority",
        "treat_arc_bot_shell_compatibility_smoke_as_clean_checkpoint_for_release_final_branch_tag_cutover_or_readiness_claims_while_local_drift_excluded",
        "consumer_repo_edit_from_matrix_lane",
        "runtime_or_public_api_change_from_matrix_lane",
        "runtime_vendor_sdk_import_lockfile_secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]
    assert fixture["next_operator_action"] == (
        "record_exactly_one_v1_g61_operator_choice"
    )


def test_v1_consumer_harness_usability_matrix_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["matrix"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Consumer Harness Usability Matrix" in text
    assert fixture["source_lima_commit_before_matrix"] in text
    assert "HARNESS_USABLE_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER" in text
    assert "Sparkbot and Arc-Bot-shell harnesses remain usable" in text
    assert "fake in-process executors and sanitized fixtures" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART.md" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "G61 operator decision packet status audit remains current" in text
    assert "current candidate validation refresh, post-validation readiness-change freshness audit, latest post-G61 request readiness-refresh supplement, and latest quickstart artifact refresh evidence remain current for the harness handoff" in text
    assert "release-candidate acceptance checklist and cutover runbook remain blocked" in text
    assert "clean Arc-Bot-shell checkpoint proof is recorded" in text
    assert "Arc-Bot-shell smoke evidence is treated as compatibility evidence only" in text
    assert "clean-checkpoint proof is recorded before release-candidate, final-readiness, branch, tag, cutover, or readiness claims" in text
    assert "Public Sparkbot target checkout" in text
    assert "Accessible Sparkbot checkpoint" in text
    assert "Arc-Bot-shell" in text
    assert "Current candidate validation refresh: 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests." in text
    assert "Candidate harness quickstart execution refresh: public Sparkbot 8 tests, accessible Sparkbot 8 tests, Arc-Bot-shell 8 tests, LIMA 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests." in text
    assert "Latest final blocker/index readiness refresh: 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests." in text
    assert "Latest post-G61 request readiness-refresh: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests." in text
    assert "Latest quickstart artifact refresh: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "These freshness results keep the local harness handoff current only." in text
    assert "V1-G61 implementation approval recorded: false." in text
    assert "V1 release-candidate branch or tag authorized by harness usability: false." in text
    assert "V1 release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim authorized by harness usability: false." in text
    assert "Arc-Bot-shell clean-checkpoint evidence claimed from local smoke: false." in text
    assert "Release, cutover, final-readiness, or G61 implementation authority created by freshness evidence: false." in text
    assert "Consumer production runtime integration approved: false." in text
    assert "V1.0 completion, product-readiness, or production-readiness claimed: false." in text
    assert "Record exactly one V1-G61 operator choice" in text


def test_v1_consumer_harness_usability_matrix_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["matrix"]).read_text(
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
