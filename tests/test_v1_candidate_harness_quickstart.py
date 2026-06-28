"""Static checks for the V1 candidate harness quickstart."""

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
    / "v1_candidate_harness_quickstart.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_candidate_harness_quickstart_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["quickstart_id"] == "v1_candidate_harness_quickstart"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-21"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_quickstart"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["quickstart_verdict"] == (
        "QUICKSTART_READY_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_candidate_harness_quickstart_commands_cover_all_repos() -> None:
    commands = _load_fixture()["commands"]

    assert commands["public_sparkbot"][0] == "Set-Location C:\\Users\\limap\\Sparkbot-public"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["public_sparkbot"][1]
    assert commands["public_sparkbot"][2] == "git diff --check"
    assert commands["accessible_sparkbot"][0] == "Set-Location C:\\Users\\limap\\Sparkbot"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["accessible_sparkbot"][1]
    assert commands["arc_bot_shell"][0] == "Set-Location C:\\Users\\limap\\Arc-Bot-shell"
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in commands["arc_bot_shell"][1]
    assert commands["lima_ai_os"] == [
        "Set-Location C:\\Users\\limap\\LIMA-AI-OS",
        "python -m compileall lima",
        "python -m pytest -q tests -p no:cacheprovider",
        "git diff --check",
        "git diff --cached --check",
    ]


def test_v1_candidate_harness_quickstart_pass_meaning_is_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["pass_means"] == [
        "public_sparkbot_fake_executor_smoke_passes",
        "accessible_sparkbot_fake_executor_smoke_passes",
        "arc_bot_shell_fake_executor_smoke_passes",
        "lima_compile_full_suite_and_diff_hygiene_pass",
        "g61_operator_decision_packet_status_audit_awaiting_choice",
        "current_gate_consistency_audit_rejects_release_candidate_claims_before_final_readiness_pass_and_clean_arc_checkpoint_proof",
        "candidate_remains_local_harness_smoke_only",
    ]
    assert fixture["pass_does_not_mean"] == [
        "v1_g61_approved",
        "runtime_vendor_sdk_import_execution_proven",
        "runtime_vendor_sdk_imports_in_lima_approved",
        "future_final_readiness_audit_executed_or_passed",
        "release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim_authorized",
        "arc_bot_shell_clean_checkpoint_proven_for_release_claims_while_local_drift_excluded",
        "built_in_provider_sdk_clients_approved",
        "provider_client_construction_approved",
        "endpoint_resolution_network_credential_fallback_connector_or_consumer_production_behavior_approved",
        "physical_world_v1_product_or_production_readiness_approved",
    ]


def test_v1_candidate_harness_quickstart_records_current_evidence_to_preserve() -> None:
    evidence = _load_fixture()["current_evidence_to_preserve"]

    assert evidence == {
        "public_sparkbot_smoke_tests_passed": 8,
        "accessible_sparkbot_smoke_tests_passed": 8,
        "arc_bot_shell_smoke_tests_passed": 8,
        "lima_quickstart_focused_tests_passed": 17,
        "lima_quickstart_broader_v1_harness_readiness_tests_passed": 108,
        "lima_quickstart_full_suite_tests_passed": 5360,
        "latest_final_blocker_index_focused_tests_passed": 15,
        "latest_final_blocker_index_broader_tests_passed": 89,
        "latest_final_blocker_index_full_suite_tests_passed": 5361,
        "latest_post_g61_request_readiness_refresh_focused_tests_passed": 8,
        "latest_post_g61_request_readiness_refresh_broader_tests_passed": 117,
        "latest_post_g61_request_readiness_refresh_full_suite_tests_passed": 5362,
        "latest_quickstart_artifact_refresh_focused_tests_passed": 7,
        "latest_quickstart_artifact_refresh_adjacent_tests_passed": 64,
        "latest_quickstart_artifact_refresh_broader_tests_passed": 133,
        "latest_quickstart_artifact_refresh_full_suite_tests_passed": 5364,
        "release_cutover_final_readiness_production_or_g61_authority_created": False,
        "arc_bot_shell_clean_checkpoint_authority_created": False,
    }


def test_v1_candidate_harness_quickstart_preserves_false_boundaries() -> None:
    for key, value in _load_fixture()["required_false_boundaries"].items():
        assert value is False, key


def test_v1_candidate_harness_quickstart_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["quickstart"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Candidate Harness Quickstart" in text
    assert fixture["source_lima_commit_before_quickstart"] in text
    assert "QUICKSTART_READY_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER" in text
    assert "shortest safe path to run the current Sparkbot and Arc-Bot-shell V1 candidate smoke checks" in text
    assert "Set-Location C:\\Users\\limap\\Sparkbot-public" in text
    assert "Set-Location C:\\Users\\limap\\Sparkbot" in text
    assert "Set-Location C:\\Users\\limap\\Arc-Bot-shell" in text
    assert "Set-Location C:\\Users\\limap\\LIMA-AI-OS" in text
    assert "What A Pass Does Not Mean" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CONSUMER_HARNESS_USABILITY_MATRIX.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "current committed proof that `Approve-V1-G61` is recorded for bounded local import-proof evidence only" in text
    assert "current harness-usability and freshness evidence before using this quickstart as handoff proof" in text
    assert "stale blocker or release-candidate claims are rejected" in text
    assert "this quickstart does not execute or pass that audit" in text
    assert "Arc-Bot-shell smoke as compatibility evidence only" in text
    assert "clean-checkpoint proof is recorded before release-candidate, final-readiness, branch, tag, cutover, or readiness claims" in text
    assert "release-candidate claims before a final-readiness pass and clean Arc-Bot-shell checkpoint proof" in text
    assert "Consumer smoke freshness: public Sparkbot 8 tests, accessible Sparkbot 8 tests, and Arc-Bot-shell 8 tests." in text
    assert "LIMA quickstart freshness: 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests." in text
    assert "Final blocker/index freshness: 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests." in text
    assert "Latest post-G61 request readiness-refresh: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests." in text
    assert "Latest quickstart artifact refresh: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "These evidence counts keep this quickstart current for local harness handoff only." in text
    assert "It does not approve V1-G61." in text
    assert "It does not execute or pass the future final readiness audit." in text
    assert "It does not authorize a release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim." in text
    assert "It does not turn Arc-Bot-shell compatibility smoke into release, final-readiness, branch, tag, cutover, or readiness authority; clean-checkpoint proof is recorded separately as release-gate input evidence." in text
    assert "Arc-Bot-shell clean-checkpoint evidence claimed by this quickstart: false." in text
    assert "V1 release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim authorized by this quickstart: false." in text
    assert "V1.0 completion, product-readiness, or production-readiness claimed: false." in text
    assert "Do not add more G61 implementation or create release-candidate artifacts from this quickstart." in text


def test_v1_candidate_harness_quickstart_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["quickstart"]).read_text(
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
