"""Phase 30 runtime slice archive tests for Phase 30.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_30_4_PHASE_30_RUNTIME_SLICE_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_30_4_phase_30_runtime_slice_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_30_4_archives_completed_runtime_slice() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "30.4"
    assert fixture["phase_29_audit_result"] == "PASS"
    assert fixture["runtime_code_modified"] is False
    assert fixture["completed_phases"] == ["30.0", "30.1", "30.2", "30.3"]
    assert "completed narrow read-only runtime state inspection slice" in phase_doc


def test_archive_records_exact_runtime_files_changed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_files_changed_in_phase_30"] == [
        "lima/kernel/runtime_state.py",
        "lima/kernel/__init__.py",
    ]
    assert fixture["runtime_state_py_added"] is True
    assert fixture["kernel_init_changed"] is True
    assert fixture["kernel_init_change_reason"] == (
        "safe_public_export_required_by_existing_kernel_package_convention"
    )
    assert fixture["forbidden_lima_files_changed"] is False
    assert fixture["tests_support_changed"] is False


def test_approved_runtime_behavior_remains_read_only_and_non_executing() -> None:
    behavior = _load_json(PHASE_FIXTURE_PATH)["approved_runtime_behavior"]
    assert behavior["read_only_runtime_state_inspection"] is True
    assert behavior["deterministic"] is True
    assert behavior["local_only"] is True
    assert behavior["read_only"] is True
    assert behavior["non_authoritative"] is True
    assert behavior["non_executing"] is True
    assert behavior["side_effect_free"] is True
    assert behavior["safe_missing_input"] is True
    assert behavior["safe_malformed_input"] is True
    assert behavior["safe_unknown_values"] is True
    assert behavior["safe_bypass_wording"] is True
    assert behavior["phase_5_runtime_bridge_remains_gated"] is True


def test_forbidden_behavior_remains_absent() -> None:
    absent = _load_json(PHASE_FIXTURE_PATH)["forbidden_behavior_absent"]
    assert absent["humaninput_runtime_bridge"] is True
    assert absent["sparkbot_wiring_imports"] is True
    assert absent["live_adapter"] is True
    assert absent["intentcompiler_runtime_behavior"] is True
    assert absent["guardiandecision_runtime_behavior"] is True
    assert absent["approval_enforcement"] is True
    assert absent["execution"] is True
    assert absent["dispatch"] is True
    assert absent["audit_persistence"] is True
    assert absent["shell_browser_network_file_mutation"] is True
    assert absent["robotics_physical_world_behavior"] is True
    assert absent["external_service_calls"] is True
    assert (
        absent[
            "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects"
        ]
        is True
    )


def test_phase_31_gate_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    question = fixture["phase_31_approval_question"]
    assert fixture["recommended_phase_31_direction"] == (
        "docs_tests_fixtures_only_audit_archive_and_next_lane_decision"
    )
    assert "Do you approve Phase 31" in question
    assert "docs/tests/fixtures-only audit/archive" in question
    assert "runtime implementation changes" in question
    assert "new `lima/` changes" in question
    assert "`tests/support/` changes" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge behavior" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "hidden side effects" in question


def test_no_phase_30_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_30_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_30_4*"))
