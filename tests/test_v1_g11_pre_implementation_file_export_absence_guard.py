"""Static guard for V1-G11 pre-approval file/export absence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import lima.guardian as guardian
import lima.kernel as kernel


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    REPO_ROOT / "docs" / "V1_G11_PRE_IMPLEMENTATION_FILE_EXPORT_ABSENCE_GUARD.md"
)
STATE_PATH = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g11_pre_implementation_file_export_absence_guard.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_pre_implementation_guard_fixture_and_doc_exist() -> None:
    fixture = _load_fixture()

    assert DOC_PATH.exists()
    assert fixture["guard_id"] == "v1_g11_pre_implementation_file_export_absence_guard"
    assert fixture["gap_id"] == "V1-G11"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert fixture["guard_status"] == "active_static_file_export_absence_scan"
    assert fixture["docs_tests_fixtures_only"] is True


def test_v1_g11_pre_implementation_approval_boundaries_are_false() -> None:
    fixture = _load_fixture()

    for key in (
        "runtime_implementation_approved",
        "operator_approval_recorded",
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_import_added",
        "sparkbot_shell_import_added",
        "arc_bot_shell_import_added",
        "sparkbot_code_copied",
        "provider_model_routing_added",
        "shell_wiring_added",
        "persistence_added",
        "haptic_device_behavior_added",
        "browser_file_network_device_robotics_physical_world_added",
        "runtime_exports_changed",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
        "v1_product_ready",
        "production_ready",
    ):
        assert fixture[key] is False


def test_v1_g11_current_decision_record_is_empty() -> None:
    fixture = _load_fixture()

    assert fixture["current_decision_record_empty"] is True
    assert fixture["approved_implementation_branch"] is None
    assert fixture["current_decision_record"] == {
        "recorded_choice": None,
        "recorded_approval_wording": None,
        "recorded_revision_request": None,
        "recorded_pause_reason": None,
        "approved_implementation_branch": None,
        "runtime_implementation_approved": False,
    }


def test_v1_g11_forbidden_pre_approval_files_are_absent() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["currently_forbidden_pre_approval_files"]:
        assert not (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g11_current_kernel_exports_remain_unchanged() -> None:
    fixture = _load_fixture()

    assert list(kernel.__all__) == fixture["current_kernel_exports"]


def test_v1_g11_current_guardian_exports_remain_unchanged() -> None:
    fixture = _load_fixture()

    assert list(guardian.__all__) == fixture["current_guardian_exports"]


def test_v1_g11_future_symbols_are_not_exported_before_approval() -> None:
    fixture = _load_fixture()
    exported_symbols = set(kernel.__all__) | set(guardian.__all__)

    for symbol in fixture["proposed_future_symbols_if_approved"]:
        assert symbol not in exported_symbols


def test_v1_g11_pre_implementation_guard_doc_and_state_match_fixture() -> None:
    fixture = _load_fixture()
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    state_text = STATE_PATH.read_text(encoding="utf-8")

    for phrase in fixture["doc_required_phrases"]:
        assert phrase in doc_text

    assert fixture["state_required_phrase"] in state_text
    assert "Runtime export cleanup approved: no." in doc_text
    assert "Final API freeze approved: no." in doc_text
    assert (
        fixture["recommended_next_step"]
        == "record_exactly_one_valid_operator_choice_in_decision_record"
    )
