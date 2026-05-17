"""Phase 38.2 LIMA consumer boundary vocabulary tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_38_2_LIMA_CONSUMER_BOUNDARY_VOCABULARY_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_38_2_lima_consumer_boundary_vocabulary_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_38_2_defines_required_vocabulary_groups() -> None:
    vocabulary = _load_json(PHASE_FIXTURE_PATH)["vocabulary"]
    assert "sparkbot" in vocabulary["consumer_kind"]
    assert "owner_local" in vocabulary["operator_posture"]
    assert "strict_security" in vocabulary["operator_posture"]
    assert "robot_motion" in vocabulary["action_class"]
    assert "breakglass_required" in vocabulary["approval_posture"]
    assert "explain_plan_required" in vocabulary["dry_run_posture"]
    assert "real_hardware_blocked" in vocabulary["robotics_posture"]


def test_phase_38_2_keeps_vocabulary_non_authoritative() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    invariants = fixture["safe_by_default_invariants"]
    assert all(value is False for value in invariants.values())
    assert fixture["owner_local_is_runtime_permission"] is False
    assert fixture["strict_security_enforced_in_phase_38"] is False
    assert "These names do not approve, execute, dispatch, persist" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_38_2_models_explain_plan_without_execution() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["explain_plan_executes_tools"] is False
    assert fixture["dry_run_connects_to_mcp"] is False
    doc_text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "`dry_run_posture=explain_plan_required`" in doc_text
    assert "`approval_posture=blocked`" in doc_text


def test_phase_38_2_keeps_scope_closed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_38_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_38_2*"))
