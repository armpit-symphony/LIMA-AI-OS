"""Static checks for the V1 handoff artifacts custody audit."""

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
    / "v1_handoff_artifacts_custody_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_handoff_artifacts_custody_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_handoff_artifacts_custody_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_lima_commit_before_refresh"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["audit_verdict"] == (
        "LOCAL_HANDOFF_PAYLOAD_EXCLUDED_FROM_REPOSITORY_PROOF_WITH_G61_BLOCKER"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_handoff_artifacts_custody_records_inventory_without_raw_payloads() -> None:
    inventory = _load_fixture()["local_payload_inventory"]

    assert inventory == {
        "directory": "handoff_artifacts/",
        "archive_count": 1,
        "patch_file_count": 2,
        "bundle_count": 1,
        "raw_payload_contents_committed": False,
    }


def test_v1_handoff_artifacts_custody_gitignore_rule_is_present() -> None:
    fixture = _load_fixture()
    decision = fixture["repository_hygiene_decision"]
    gitignore = (REPO_ROOT / fixture["documents"]["gitignore"]).read_text(
        encoding="utf-8"
    )

    assert decision["ignore_rule_added"] == "handoff_artifacts/"
    assert "handoff_artifacts/" in gitignore.splitlines()
    assert decision["public_sparkbot_write_credential_blocker_active"] is False
    assert decision["v1_g61_decision_recorded_by_artifacts"] is False


def test_v1_handoff_artifacts_custody_interpretation_keeps_blockers() -> None:
    assert _load_fixture()["evidence_interpretation"] == [
        "directory_is_local_operator_transfer_material_only",
        "public_sparkbot_write_credential_blocker_resolved_elsewhere",
        "directory_does_not_replace_g61_request_stage_artifacts",
        "directory_does_not_replace_current_gate_or_release_candidate_artifacts",
        "directory_does_not_replace_candidate_handoff_quickstart_or_usability_artifacts",
        "latest_handoff_freshness_remains_committed_docs_tests_fixtures_evidence_lima_8_117_5362_and_7_64_133_5364",
        "directory_does_not_record_approve_v1_g61_operator_decision",
        "g61_operator_decision_packet_status_audit_remains_committed_awaiting_choice_evidence",
        "release_candidate_branch_tag_work_remains_blocked_at_g61_operator_decision",
        "directory_excluded_from_final_v1_readiness_proof_without_later_artifact_publication_gate",
    ]


def test_v1_handoff_artifacts_custody_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_handoff_artifacts_custody_stop_conditions_are_bounded() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "raw_handoff_payload_commit_without_artifact_publication_approval",
        "treat_local_handoff_artifacts_as_g61_approval_or_v1_readiness_proof",
        "treat_local_handoff_artifacts_as_release_candidate_branch_or_tag_authority",
        "v1_g61_implementation_without_exact_approval",
        "treat_this_audit_as_g61_approval",
        "consumer_repo_edit_from_audit_lane",
        "runtime_or_public_api_change_from_audit_lane",
        "secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_handoff_artifacts_custody_records_latest_committed_freshness() -> None:
    fixture = _load_fixture()
    freshness = fixture["latest_committed_handoff_freshness_evidence"]
    text = (
        REPO_ROOT / fixture["documents"]["handoff_artifacts_custody_audit"]
    ).read_text(encoding="utf-8")

    assert freshness == {
        "latest_post_g61_request_refresh_focused_tests_passed": 8,
        "latest_post_g61_request_refresh_broader_tests_passed": 117,
        "latest_post_g61_request_refresh_full_lima_suite_tests_passed": 5362,
        "latest_quickstart_artifact_refresh_focused_tests_passed": 7,
        "latest_quickstart_artifact_refresh_adjacent_tests_passed": 64,
        "latest_quickstart_artifact_refresh_broader_tests_passed": 133,
        "latest_quickstart_artifact_refresh_full_lima_suite_tests_passed": 5364,
        "artifact_publication_authority_created": False,
        "v1_readiness_proof_created_from_local_payloads": False,
        "g61_implementation_authority_created": False,
        "release_candidate_authority_created": False,
        "product_or_production_readiness_authority_created": False,
    }
    assert "does not replace the committed candidate test handoff manifest" in text
    assert "post-G61 request readiness-refresh supplement, or latest quickstart artifact refresh evidence" in text
    assert "Latest committed handoff freshness remains in docs/tests/fixtures evidence, including 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "Latest handoff freshness supplements converted into artifact-publication authority by this audit: no." in text
    assert "Local `handoff_artifacts/` directory accepted as a substitute for committed docs/tests/fixtures evidence by this audit: no." in text


def test_v1_handoff_artifacts_custody_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["handoff_artifacts_custody_audit"]
    ).read_text(encoding="utf-8")

    assert "# V1 Handoff Artifacts Custody Audit" in text
    assert fixture["source_lima_commit_before_refresh"] in text
    assert "LOCAL_HANDOFF_PAYLOAD_EXCLUDED_FROM_REPOSITORY_PROOF_WITH_G61_BLOCKER" in text
    assert "`handoff_artifacts/` is added to `.gitignore`" in text
    assert "The raw payload contents are not persisted" in text
    assert "operator decision packet status audit" in text
    assert "status audit remains the committed evidence that `Approve-V1-G61` is recorded for bounded local import-proof evidence only" in text
    assert "does not replace the current-gate consistency audit, release-candidate acceptance checklist, release-candidate cutover runbook, or final readiness audit template" in text
    assert "does not replace the committed candidate test handoff manifest" in text
    assert "Latest committed handoff freshness remains in docs/tests/fixtures evidence" in text
    assert "V1 branch/tag work is blocked at the G61 operator decision" in text
    assert "Exact `Approve-V1-G61` operator decision recorded by this audit: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_handoff_artifacts_custody_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT / fixture["documents"]["handoff_artifacts_custody_audit"]
    ).read_text(encoding="utf-8")

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
