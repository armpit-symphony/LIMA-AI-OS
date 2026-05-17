"""Candidate preview boundary evidence review tests for Phase 37.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_37_1_CANDIDATE_PREVIEW_BOUNDARY_EVIDENCE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_37_1_candidate_preview_boundary_evidence_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_37_1_adds_no_runtime_behavior() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "37.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_behavior_added_in_phase_37_1"] is False
    assert fixture["runtime_files_changed_in_phase_37_1"] == []
    assert "does not modify `lima/`" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_evidence_review_covers_input_safety_cases() -> None:
    evidence = set(_load_json(PHASE_FIXTURE_PATH)["evidence_reviewed"])
    assert "benign_input_safe" in evidence
    assert "missing_input_safe" in evidence
    assert "malformed_input_safe" in evidence
    assert "unknown_values_safe" in evidence
    assert "suspicious_values_safe" in evidence
    assert "nested_suspicious_metadata_safe" in evidence
    assert "bypass_wording_no_authority" in evidence


def test_inert_output_flags_preserve_non_executing_boundary() -> None:
    flags = _load_json(PHASE_FIXTURE_PATH)["inert_output_flags"]
    assert flags["non_authoritative"] is True
    assert flags["read_only"] is True
    assert flags["local_only"] is True
    assert flags["deterministic"] is True
    assert flags["safe_by_default"] is True
    assert flags["execution_allowed"] is False
    assert flags["side_effects_allowed"] is False
    assert flags["approval_granted"] is False
    assert flags["dispatch_allowed"] is False
    assert flags["persistence_allowed"] is False
    assert flags["phase_5_humaninput_runtime_bridge_gated"] is True
    assert flags["physical_world_allowed"] is False


def test_static_scan_result_preserves_absent_integrations() -> None:
    scan = _load_json(PHASE_FIXTURE_PATH)["static_scan_result"]
    assert scan["forbidden_imports_absent"] is True
    assert scan["forbidden_calls_absent"] is True
    assert scan["sparkbot_imports_absent"] is True
    assert scan["humaninput_bridge_behavior_absent"] is True
    assert scan["live_adapter_behavior_absent"] is True
    assert scan["intentcompiler_calls_absent"] is True
    assert scan["guardiandecision_calls_absent"] is True
    assert scan["robotics_physical_world_behavior_absent"] is True


def test_no_phase_37_1_files_exist_under_lima_tests_support_or_old_phase_tests() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_37_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_37_1*"))
    assert not list((REPO_ROOT / "tests").glob("test_phase_35_*phase_37_1*"))
