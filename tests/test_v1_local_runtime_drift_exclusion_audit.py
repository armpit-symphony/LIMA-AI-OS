"""Static checks for the V1 local runtime drift exclusion audit."""

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


def test_v1_local_runtime_drift_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_local_runtime_drift_exclusion_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["observed_lima_commit"] == (
        "f554a2f048c6231a2b321390e1a309101bee02c9"
    )
    assert fixture["audit_verdict"] == (
        "LOCAL_RUNTIME_DRIFT_EXCLUDED_FROM_V1_RELEASE_PROOF"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_local_runtime_drift_records_untracked_artifacts() -> None:
    artifacts = _load_fixture()["observed_untracked_artifacts"]

    assert [artifact["path"] for artifact in artifacts] == [
        "docs/readiness/V1_LOCAL_INSTALL_AND_DOCUMENT_HARNESS_QUICKSTART.md",
        "lima/harness/v1_local_document_harness.py",
        "scripts/download_lima_ai_os_candidate.ps1",
        "scripts/install_lima_ai_os_candidate.ps1",
        "tests/test_v1_local_document_harness.py",
    ]
    for artifact in artifacts:
        assert artifact["git_state"] == "untracked"
        assert artifact["release_proof_treatment"] == "excluded"

    harness = artifacts[1]
    assert harness["observed_size_bytes"] == 11113
    assert harness["py_compile_passed"] is True
    fixture = _load_fixture()
    assert fixture["missing_referenced_tests"] == []
    assert fixture["present_untracked_tests"] == [
        "tests/test_v1_local_document_harness.py"
    ]


def test_v1_local_runtime_drift_records_release_impact_and_boundaries() -> None:
    fixture = _load_fixture()
    impact = fixture["release_impact"]

    assert impact == {
        "pushed_branch_synced": True,
        "local_worktree_clean": False,
        "local_clean_checkpoint_claim_allowed": False,
        "cutover_blocker_changed_by_audit": False,
        "required_cutover_action": "record_exactly_one_valid_cutover_operator_choice",
    }
    for key, value in fixture["boundaries_preserved"].items():
        assert value is False, key
    assert fixture["next_required_action"] == (
        "exclude_or_resolve_local_runtime_drift_before_clean_checkpoint_claim"
    )


def test_v1_local_runtime_drift_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Local Runtime Drift Exclusion Audit" in text
    assert fixture["observed_lima_commit"] in text
    assert fixture["audit_verdict"] in text
    assert "lima/harness/v1_local_document_harness.py" in text
    assert "scripts/download_lima_ai_os_candidate.ps1" in text
    assert "scripts/install_lima_ai_os_candidate.ps1" in text
    assert "tests/test_v1_local_document_harness.py" in text
    assert "Invoke-WebRequest" in text
    assert "pip install -e" in text
    assert "not part of the committed V1 evidence chain" in text
    assert "local worktree is not clean" in text
    assert "Runtime/install artifacts committed by this audit: no." in text
    assert "Cutover operator choice recorded by this audit: no." in text
    assert "Product or production readiness claimed by this audit: no." in text


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
