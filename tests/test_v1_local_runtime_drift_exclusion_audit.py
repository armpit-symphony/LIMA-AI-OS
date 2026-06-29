"""Static checks for the V1 local runtime drift closure audit."""

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
    / "v1_local_runtime_drift_exclusion_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_local_runtime_drift_closure_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_local_runtime_drift_exclusion_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["original_observed_lima_commit"] == (
        "f554a2f048c6231a2b321390e1a309101bee02c9"
    )
    assert fixture["superseding_lima_commit"] == (
        "bc63ed3b00055976b1728d80124137d7ce15d871"
    )
    assert fixture["audit_verdict"] == (
        "LOCAL_RUNTIME_DRIFT_SUPERSEDED_BY_COMMITTED_CANDIDATE_HARNESS_AUDIT"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_local_runtime_drift_records_superseded_artifacts() -> None:
    artifacts = _load_fixture()["originally_observed_artifacts"]

    assert [artifact["path"] for artifact in artifacts] == [
        "docs/readiness/V1_LOCAL_INSTALL_AND_DOCUMENT_HARNESS_QUICKSTART.md",
        "lima/harness/v1_local_document_harness.py",
        "scripts/download_lima_ai_os_candidate.ps1",
        "scripts/install_lima_ai_os_candidate.ps1",
        "tests/test_v1_local_document_harness.py",
    ]
    for artifact in artifacts:
        assert artifact["original_git_state"] == "untracked"
        assert artifact["current_git_state"] == "tracked"
        treatment = artifact["current_release_proof_treatment"]
        assert treatment in {
            "candidate_only_not_release_authority",
            "candidate_only_not_production_runtime_authority",
            "operator_run_utility_not_validation_authority",
            "committed_candidate_only_test_evidence",
        }

    downloader = artifacts[2]
    installer = artifacts[3]
    assert downloader["network_capable_unless_dry_run"] is True
    assert installer["writes_install_root_unless_dry_run"] is True


def test_v1_local_runtime_drift_records_release_impact_and_boundaries() -> None:
    fixture = _load_fixture()
    impact = fixture["closure_release_impact"]

    assert impact == {
        "original_drift_resolved_as_tracked_content": True,
        "local_worktree_can_be_clean_with_artifacts_present": True,
        "cutover_blocker_changed_by_closure": False,
        "required_cutover_action": "record_exactly_one_valid_cutover_operator_choice",
    }
    boundaries = fixture["boundaries_preserved"]
    assert boundaries["runtime_install_artifacts_committed_after_original_audit"] is True
    for key, value in boundaries.items():
        if key == "runtime_install_artifacts_committed_after_original_audit":
            continue
        assert value is False, key
    assert fixture["next_required_action"] == (
        "use_committed_feature_audit_and_record_cutover_choice_before_release_claim"
    )


def test_v1_local_runtime_drift_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Local Runtime Drift Exclusion Audit" in text
    assert fixture["original_observed_lima_commit"] in text
    assert fixture["superseding_lima_commit"] in text
    assert fixture["audit_verdict"] in text
    assert "closure record" in text
    assert "no longer untracked workspace drift" in text
    assert "V1_LOCAL_DOCUMENT_HARNESS_INSTALL_COMMITTED_FEATURE_AUDIT.md" in text
    assert "lima/harness/v1_local_document_harness.py" in text
    assert "scripts/download_lima_ai_os_candidate.ps1" in text
    assert "scripts/install_lima_ai_os_candidate.ps1" in text
    assert "tests/test_v1_local_document_harness.py" in text
    assert "Network behavior approved by this closure: no." in text
    assert "Cutover operator choice recorded by this closure: no." in text
    assert "Product or production readiness claimed by this closure: no." in text


def test_v1_local_runtime_drift_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["audit"]).read_text(
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
