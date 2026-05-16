"""Read-only runtime state inspection acceptance design tests for Phase 30.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_30_1_READ_ONLY_RUNTIME_STATE_INSPECTION_ACCEPTANCE_DESIGN.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_30_1_read_only_runtime_state_inspection_acceptance_design.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_30_1_is_acceptance_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "30.1"
    assert fixture["runtime_code_modified"] is False
    assert "acceptance design only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_required_contract_preserves_read_only_runtime_boundaries() -> None:
    contract = _load_json(PHASE_FIXTURE_PATH)["required_runtime_contract"]
    assert contract["deterministic_output_for_identical_input"] is True
    assert contract["safe_default_output_for_missing_input"] is True
    assert contract["safe_output_for_malformed_input"] is True
    assert contract["safe_output_for_unknown_status_values"] is True
    assert contract["bypass_wording_does_not_change_safety_outcome"] is True
    assert contract["non_authoritative_output"] is True
    assert contract["execution_allowed_false"] is True
    assert contract["side_effects_allowed_false"] is True
    assert contract["approval_not_approved"] is True
    assert contract["dispatch_disallowed"] is True
    assert contract["persistence_disallowed"] is True
    assert contract["phase_5_runtime_bridge_gated"] is True


def test_required_contract_excludes_integrations_and_side_effects() -> None:
    contract = _load_json(PHASE_FIXTURE_PATH)["required_runtime_contract"]
    assert contract["no_sparkbot_wiring_imports"] is True
    assert contract["no_live_adapter_behavior"] is True
    assert contract["no_shell_browser_network_file_mutation_behavior"] is True
    assert contract["no_robotics_physical_world_behavior"] is True
    assert contract["no_background_worker_thread_subprocess_queue_daemon_behavior"] is True


def test_required_test_families_cover_acceptance_obligations() -> None:
    test_families = set(_load_json(PHASE_FIXTURE_PATH)["required_test_families"])
    assert "deterministic_snapshots" in test_families
    assert "missing_input_safe_defaults" in test_families
    assert "malformed_input_safe_defaults" in test_families
    assert "unknown_status_safe_defaults" in test_families
    assert "bypass_wording_resistance" in test_families
    assert "non_execution_invariants" in test_families
    assert "non_authoritative_advisory_output" in test_families
    assert "no_mutation_of_caller_input" in test_families
    assert "forbidden_import_and_behavior_absence" in test_families
    assert "phase_5_runtime_bridge_remains_gated" in test_families


def test_required_fixtures_cover_risky_runtime_state_examples() -> None:
    fixtures = set(_load_json(PHASE_FIXTURE_PATH)["required_synthetic_fixtures"])
    assert "valid_non_executing_candidate_state" in fixtures
    assert "missing_candidate_state" in fixtures
    assert "malformed_candidate_state" in fixtures
    assert "unknown_candidate_status" in fixtures
    assert "bypass_wording_candidate_text" in fixtures
    assert "shell_browser_network_file_robotics_physical_world_attempt_metadata" in fixtures
    assert "sparkbot_integration_attempt_metadata" in fixtures
    assert "humaninput_bridge_attempt_metadata" in fixtures


def test_no_phase_30_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_30_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_30_1*"))
