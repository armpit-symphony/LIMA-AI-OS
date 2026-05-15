"""Static checks for Phase 13.3 threat fixture matrix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_13_3_THREAT_FIXTURE_MATRIX.md"
PHASE_FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction" / "phase_13_3_threat_fixture_matrix.json"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_fixture_requirements_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "13.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_fixture_families_cover_required_threats() -> None:
    families = set(_load_json(PHASE_FIXTURE_PATH)["future_fixture_families"])
    for expected in {
        "malformed_candidate",
        "unknown_status",
        "stale_candidate",
        "replayed_candidate",
        "approval_bypass_wording",
        "shell_command_attempt",
        "browser_or_network_attempt",
        "file_mutation_attempt",
        "robotics_or_physical_world_attempt",
        "sparkbot_integration_attempt",
        "humaninput_bridge_attempt",
    }:
        assert expected in families


def test_fixture_requirements_are_synthetic_inert_and_non_authorizing() -> None:
    requirements = _load_json(PHASE_FIXTURE_PATH)["fixture_requirements"]
    assert requirements["synthetic"] is True
    assert requirements["inert"] is True
    assert requirements["non_executing"] is True
    assert requirements["test_only"] is True
    assert requirements["authorization_implied"] is False
    assert requirements["execution_implied"] is False


def test_phase_document_blocks_runtime_fixture_behavior() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not add production fixtures for runtime execution" in phase_doc
    assert "synthetic, inert, non-executing" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["production_fixture_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_thirteen_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_13_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_13_3*"))
