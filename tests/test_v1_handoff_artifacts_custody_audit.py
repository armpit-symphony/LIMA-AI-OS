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
    assert fixture["branch"] == "docs-v1-handoff-artifacts-custody"
    assert fixture["source_lima_commit_before_audit"] == (
        "81102ed39eccc6781c2d3c74d2b54ab757ea20ac"
    )
    assert fixture["audit_verdict"] == (
        "LOCAL_HANDOFF_PAYLOAD_EXCLUDED_FROM_REPOSITORY_PROOF"
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
    assert decision["public_sparkbot_publication_proven_by_artifacts"] is False
    assert decision["v1_g57_decision_recorded_by_artifacts"] is False


def test_v1_handoff_artifacts_custody_interpretation_keeps_blockers() -> None:
    assert _load_fixture()["evidence_interpretation"] == [
        "directory_is_local_operator_transfer_material_only",
        "directory_does_not_prove_publication_to_sparkpit_labs_sparkbot",
        "directory_does_not_replace_public_sparkbot_write_credential_gate",
        "directory_does_not_record_v1_g57_operator_decision",
        "directory_excluded_from_final_v1_readiness_proof_without_later_artifact_publication_gate",
    ]


def test_v1_handoff_artifacts_custody_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_handoff_artifacts_custody_stop_conditions_are_bounded() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "raw_handoff_payload_commit_without_artifact_publication_approval",
        "treat_local_handoff_artifacts_as_public_sparkbot_publication_proof",
        "public_sparkbot_push_without_write_credentials",
        "v1_g57_implementation_without_exact_approval",
        "treat_this_audit_as_g57_approval",
        "consumer_repo_edit_from_audit_lane",
        "runtime_or_public_api_change_from_audit_lane",
        "secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_handoff_artifacts_custody_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["handoff_artifacts_custody_audit"]
    ).read_text(encoding="utf-8")

    assert "# V1 Handoff Artifacts Custody Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert "LOCAL_HANDOFF_PAYLOAD_EXCLUDED_FROM_REPOSITORY_PROOF" in text
    assert "`handoff_artifacts/` is added to `.gitignore`" in text
    assert "The raw payload contents are not persisted" in text
    assert "Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot` by this audit: no." in text
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
