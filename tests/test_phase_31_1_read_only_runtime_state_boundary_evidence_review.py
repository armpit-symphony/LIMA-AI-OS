"""Read-only runtime state boundary evidence review tests for Phase 31.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_31_1_READ_ONLY_RUNTIME_STATE_BOUNDARY_EVIDENCE_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_31_1_read_only_runtime_state_boundary_evidence_review.json"
)
RUNTIME_STATE_PATH = REPO_ROOT / "lima" / "kernel" / "runtime_state.py"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_31_1_is_evidence_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "31.1"
    assert fixture["runtime_code_modified"] is False
    assert "evidence review only" in phase_doc
    assert "does not implement new runtime behavior" in phase_doc


def test_phase_31_1_records_no_runtime_file_changes() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_state_py_changed_in_phase_31"] is False
    assert fixture["kernel_init_changed_in_phase_31"] is False


def test_boundary_evidence_preserves_read_only_invariants() -> None:
    evidence = _load_json(PHASE_FIXTURE_PATH)["boundary_evidence"]
    assert evidence["deterministic_identical_input"] is True
    assert evidence["does_not_mutate_input"] is True
    assert evidence["missing_input_safe"] is True
    assert evidence["malformed_input_safe"] is True
    assert evidence["unknown_status_blocked"] is True
    assert evidence["bypass_wording_blocked"] is True
    assert evidence["non_authoritative_advisory_output"] is True
    assert evidence["read_only_local_only_output"] is True


def test_boundary_evidence_preserves_authority_free_outputs() -> None:
    evidence = _load_json(PHASE_FIXTURE_PATH)["boundary_evidence"]
    assert evidence["execution_allowed_false"] is True
    assert evidence["side_effects_allowed_false"] is True
    assert evidence["approved_false"] is True
    assert evidence["approval_state_not_approved"] is True
    assert evidence["dispatch_disallowed"] is True
    assert evidence["persistence_disallowed"] is True
    assert evidence["phase_5_runtime_bridge_gated"] is True
    assert evidence["sparkbot_wiring_absent"] is True
    assert evidence["live_adapter_absent"] is True
    assert evidence["intent_envelope_creation_absent"] is True
    assert evidence["guardian_decision_creation_absent"] is True


def test_forbidden_behavior_evidence_remains_absent() -> None:
    evidence = _load_json(PHASE_FIXTURE_PATH)["forbidden_behavior_evidence"]
    assert evidence["shell_browser_network_file_mutation_absent"] is True
    assert evidence["subprocess_thread_queue_daemon_absent"] is True
    assert evidence["database_write_absent"] is True
    assert evidence["external_service_calls_absent"] is True
    assert evidence["robotics_physical_world_behavior_absent"] is True
    assert evidence["hidden_side_effects_absent"] is True


def test_runtime_state_source_contains_no_phase_31_edits_or_markers() -> None:
    source = RUNTIME_STATE_PATH.read_text(encoding="utf-8")
    assert "phase_31" not in source.lower()
    assert "PHASE_31" not in source


def test_no_phase_31_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_31_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_31_1*"))
