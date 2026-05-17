"""Phase 38.4 alignment archive closeout tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_38_4_PHASE_38_ALIGNMENT_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_38_4_phase_38_alignment_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_38_4_archives_all_phase_38_phases() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "38.4"
    assert fixture["completed_phases"] == ["38.0", "38.1", "38.2", "38.3", "38.4"]
    assert "Phase 38 completed:" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_38_4_records_sparkbot_sources_reviewed() -> None:
    sources = set(_load_json(PHASE_FIXTURE_PATH)["sparkbot_sources_reviewed"])
    assert "README.md" in sources
    assert "SECURITY.md" in sources
    assert "docs/capabilities.md" in sources
    assert "docs/lima-robo-os-integration.md" in sources
    assert "docs/guardian-spine.md" in sources
    assert "docs/release-notes/v1.6.42.txt" in sources
    assert "docs/release-notes/v1.6.80.txt" in sources


def test_phase_38_4_records_concepts_added_to_planning() -> None:
    concepts = set(_load_json(PHASE_FIXTURE_PATH)["concepts_added_to_planning"])
    assert "owner_local_posture" in concepts
    assert "strict_security_posture" in concepts
    assert "policy_simulation_explain_plan" in concepts
    assert "agent_identity_kill_switch" in concepts
    assert "memory_trust_metadata" in concepts
    assert "mcp_robo_os_manifest_posture" in concepts
    assert "robotics_simulation_real_hardware_blocked_posture" in concepts


def test_phase_38_4_confirms_all_boundaries_stayed_closed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["phase_5_runtime_bridge_gated"] is True
    assert fixture["execution_approval_dispatch_persistence_absent"] is True
    assert fixture["sparkbot_wiring_imports_absent"] is True
    assert fixture["live_adapters_absent"] is True
    assert fixture["robotics_physical_world_behavior_absent"] is True


def test_phase_38_4_recommends_phase_39_test_only_hardening() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == ["candidate_preview_needs_sparkbot_shaped_fixture_hardening"]
    assert (
        fixture["recommended_next_direction"]
        == "phase_39_test_only_candidate_preview_hardening_with_sparkbot_shaped_fixtures"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["phil_approval_required_for_recommended_next_direction"] is False


def test_phase_38_4_files_are_not_under_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_38_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_38_4*"))
