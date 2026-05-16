"""Static checks for Phase 20.2 exact file-touch map."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_20_2_EXACT_FILE_TOUCH_MAP_FOR_CANDIDATE_SLICE.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_20_2_exact_file_touch_map_for_candidate_slice.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "20.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_future_eligible_runtime_files_are_exact() -> None:
    files = _load_json(PHASE_FIXTURE_PATH)["future_eligible_runtime_files"]
    assert files == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    ]


def test_future_forbidden_runtime_files_exclude_public_export_and_new_module() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["future_forbidden_runtime_files"])
    assert "lima/kernel/__init__.py" in forbidden
    assert "lima/kernel/candidate_provenance.py" in forbidden
    assert "any_other_lima_file" in forbidden
    assert "tests/support" in forbidden
    assert "sparkbot_files" in forbidden


def test_future_touch_intent_is_provenance_only() -> None:
    intent = _load_json(PHASE_FIXTURE_PATH)["future_touch_intent"]
    assert set(intent) == {
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    }
    assert "define_provenance_shape_requirements_for_candidate_construction" in intent[
        "lima/kernel/intake_candidate.py"
    ]
    assert "validate_or_normalize_provenance_metadata_for_existing_candidates" in intent[
        "lima/kernel/candidate_status.py"
    ]


def test_phase_document_preserves_exact_file_map_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "`lima/kernel/intake_candidate.py`" in phase_doc
    assert "`lima/kernel/candidate_status.py`" in phase_doc
    assert "`lima/kernel/__init__.py`" in phase_doc
    assert "Phase 20.2 does not approve Phase 21" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_twenty_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_20_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_20_2*"))
