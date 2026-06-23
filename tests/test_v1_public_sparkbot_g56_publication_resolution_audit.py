"""Static checks for the V1 public Sparkbot G56 publication resolution audit."""

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
    / "v1_public_sparkbot_g56_publication_resolution_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_public_sparkbot_g56_resolution_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == (
        "v1_public_sparkbot_g56_publication_resolution_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "docs-v1-public-sparkbot-g56-publication-resolved"
    assert fixture["source_lima_commit_before_audit"] == "cbc16dc"
    assert fixture["audit_verdict"] == "PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLVED"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_public_sparkbot_g56_resolution_records_remote_ref() -> None:
    remote = _load_fixture()["remote_verification"]

    assert remote["repository"] == "https://github.com/sparkpit-labs/Sparkbot"
    assert remote["branch"] == "v1-g56-runtime-authority-chain-audit"
    assert remote["expected_commit"] == "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    assert remote["verified_remote_ref"] == (
        "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2 "
        "refs/heads/v1-g56-runtime-authority-chain-audit"
    )
    assert remote["main_head"] == "ddaa019272ad11bb56d4660be7d44e81810814a7"
    assert remote["branch_visible"] is True
    assert remote["main_changed"] is False
    assert remote["merged"] is False
    assert remote["tagged"] is False


def test_v1_public_sparkbot_g56_resolution_records_sparkbot_report() -> None:
    fixture = _load_fixture()
    report = fixture["sparkbot_team_report"]
    boundaries = fixture["sparkbot_boundary_confirmation"]

    assert report["bundle_sha256_matched"] is True
    assert report["bundle_sha256"] == (
        "3B366845D4EE78EE43B9F787ECAB2CF7CF4C7848154A49ED4805ED9292A9B69F"
    )
    assert report["git_bundle_verify"] == "pass"
    assert report["python_exact_command_runnable"] is False
    assert report["python3_pytest_result"] == "8 passed"
    assert report["git_diff_check"] == "pass"
    assert report["git_status"] == "clean_on_inspected_branch"

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_public_sparkbot_g56_resolution_records_historical_and_current_blockers() -> None:
    fixture = _load_fixture()

    assert fixture["original_remaining_blockers_at_audit_time"] == {
        "public_sparkbot_publication": False,
        "v1_g57_operator_decision": True,
    }
    assert fixture["current_status_refresh"] == {
        "public_sparkbot_publication": False,
        "v1_g57_through_v1_g60_candidate_gates_completed": True,
        "candidate_harness_quickstart_execution_audit_current": True,
        "active_blocker": (
            "v1_g61_runtime_vendor_sdk_import_execution_proof_operator_decision"
        ),
        "current_quickstart_audit": (
            "docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md"
        ),
        "required_exact_approval_phrase": "Approve-V1-G61",
        "runtime_implementation_approved": False,
    }
    assert fixture["recommended_next_step"] == (
        "record_exactly_one_v1_g61_operator_choice"
    )


def test_v1_public_sparkbot_g56_resolution_preserves_lima_boundaries() -> None:
    boundaries = _load_fixture()["audit_time_boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key

    current = _load_fixture()["current_boundaries_preserved"]
    assert current["v1_g57_through_v1_g60_completed_candidate_only"] is True
    for key, value in current.items():
        if key != "v1_g57_through_v1_g60_completed_candidate_only":
            assert value is False, key


def test_v1_public_sparkbot_g56_resolution_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["publication_resolution_audit"]
    ).read_text(encoding="utf-8")

    assert "# V1 Public Sparkbot G56 Publication Resolution Audit" in text
    assert "PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLVED" in text
    assert "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2" in text
    assert "ddaa019272ad11bb56d4660be7d44e81810814a7" in text
    assert "Public Sparkbot G56 publication blocker: resolved." in text
    assert "Current status refresh" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "Audit-Time Boundaries Preserved" in text
    assert "Current Boundary Refresh" in text
    assert "Active blocker: V1-G61 runtime vendor SDK import execution proof operator decision." in text
    assert "V1-G57 implementation approval recorded: no." in text
    assert "V1-G61 implementation approval recorded: no." in text
    assert "Provider SDK clients added by LIMA: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_public_sparkbot_g56_resolution_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT / fixture["documents"]["publication_resolution_audit"]
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
