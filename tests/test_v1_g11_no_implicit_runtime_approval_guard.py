"""Aggregate static guard for V1-G11 no-implicit-approval fixtures."""

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


def _lookup_path(data: Any, dot_path: str) -> Any:
    current = data
    for part in dot_path.split("."):
        assert isinstance(current, dict), f"{dot_path} stopped before {part}"
        current = current[part]
    return current


def _walk_dict_values(data: Any, prefix: str = "") -> list[tuple[str, str, Any]]:
    values: list[tuple[str, str, Any]] = []
    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else key
            values.append((key, path, value))
            values.extend(_walk_dict_values(value, path))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            path = f"{prefix}[{index}]"
            values.extend(_walk_dict_values(value, path))
    return values


def test_v1_g11_no_implicit_approval_guard_fixture_and_doc_exist() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert DOC_PATH.exists()
    assert fixture["guard_id"] == "v1_g11_no_implicit_runtime_approval_guard"
    assert fixture["gap_id"] == "V1-G11"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert fixture["guard_status"] == "active_static_fixture_scan"
    assert fixture["docs_tests_fixtures_only"] is True


def test_v1_g11_no_implicit_approval_guard_boundaries_are_false() -> None:
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


def test_v1_g11_no_guarded_fixture_records_current_runtime_approval() -> None:
    fixture = _load_json(FIXTURE_PATH)
    forbidden_keys = set(fixture["forbidden_true_boolean_keys"])
    allowlist = {
        (item["file"], item["path"]): item["reason"]
        for item in fixture["allowed_true_boolean_paths"]
    }

    observed_allowlisted_true_paths: set[tuple[str, str]] = set()
    for fixture_file in fixture["guarded_fixture_files"]:
        guarded_path = REPO_ROOT / fixture_file
        assert guarded_path.exists(), fixture_file
        guarded = _load_json(guarded_path)

        for key, dot_path, value in _walk_dict_values(guarded):
            if key not in forbidden_keys or value is not True:
                continue
            if (fixture_file, dot_path) in allowlist:
                observed_allowlisted_true_paths.add((fixture_file, dot_path))
                continue
            raise AssertionError(f"{fixture_file}:{dot_path} records forbidden current approval")

    assert observed_allowlisted_true_paths == set(allowlist)


def test_v1_g11_allowed_true_path_is_only_hypothetical_approve_rule() -> None:
    fixture = _load_json(FIXTURE_PATH)
    allowlist = fixture["allowed_true_boolean_paths"]
    assert allowlist == [
        {
            "file": "tests/fixtures/runtime_extraction/v1_g11_operator_decision_packet.json",
            "path": "decision_record_validation_rules.Approve-V1-G11.runtime_implementation_approved",
            "reason": "hypothetical_valid_approve_rule_not_current_decision_record",
        }
    ]

    item = allowlist[0]
    guarded = _load_json(REPO_ROOT / item["file"])
    assert _lookup_path(guarded, item["path"]) is True


def test_v1_g11_required_current_decision_records_remain_empty() -> None:
    fixture = _load_json(FIXTURE_PATH)
    expected = fixture["expected_empty_decision_record"]
    assert expected == {
        "recorded_choice": None,
        "recorded_approval_wording": None,
        "recorded_revision_request": None,
        "recorded_pause_reason": None,
        "approved_implementation_branch": None,
        "runtime_implementation_approved": False,
    }

    for record_ref in fixture["required_empty_decision_records"]:
        guarded = _load_json(REPO_ROOT / record_ref["file"])
        assert _lookup_path(guarded, record_ref["path"]) == expected


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
        == "record_exactly_one_valid_operator_choice_in_decision_record"
    )
