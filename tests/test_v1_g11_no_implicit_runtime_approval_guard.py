"""Retired static guard for V1-G11 no-implicit-approval fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_G11_NO_IMPLICIT_RUNTIME_APPROVAL_GUARD.md"
STATE_PATH = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g11_no_implicit_runtime_approval_guard.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_no_implicit_approval_guard_retired_after_recorded_approval() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert DOC_PATH.exists()
    assert fixture["guard_id"] == "v1_g11_no_implicit_runtime_approval_guard"
    assert fixture["gap_id"] == "V1-G11"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert fixture["guard_status"] == "retired_after_approve_v1_g11_recorded"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["operator_approval_recorded"] is True
    assert fixture["runtime_implementation_approved"] is True


def test_v1_g11_no_implicit_approval_guard_runtime_boundaries_remain_false() -> None:
    fixture = _load_json(FIXTURE_PATH)
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "runtime_exports_changed",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
        "v1_product_ready",
        "production_ready",
    ):
        assert fixture[key] is False


def test_v1_g11_no_implicit_approval_guard_points_to_authoritative_record() -> None:
    fixture = _load_json(FIXTURE_PATH)
    record_ref = fixture["authoritative_approval_record"]
    guarded = _load_json(REPO_ROOT / record_ref["file"])
    decision_record = guarded[record_ref["path"]]
    assert decision_record["recorded_choice"] == record_ref["recorded_choice"]
    assert (
        decision_record["approved_implementation_branch"]
        == record_ref["approved_implementation_branch"]
    )
    assert (
        decision_record["runtime_implementation_approved"]
        is record_ref["runtime_implementation_approved"]
    )


def test_v1_g11_no_implicit_approval_guard_doc_matches_fixture() -> None:
    fixture = _load_json(FIXTURE_PATH)
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    state_text = STATE_PATH.read_text(encoding="utf-8")

    for phrase in fixture["doc_required_phrases"]:
        assert phrase in doc_text

    assert "V1-G11 no implicit runtime approval guard document" in state_text
    assert "Runtime behavior added: no." in doc_text
    assert "Runtime export cleanup approved: no." in doc_text
    assert "Final API freeze approved: no." in doc_text
    assert (
        fixture["recommended_next_step"]
        == "create_approved_v1_g11_implementation_branch"
    )
