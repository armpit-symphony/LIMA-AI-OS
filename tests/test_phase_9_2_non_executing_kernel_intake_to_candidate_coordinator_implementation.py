"""Acceptance tests for the Phase 9.2 non-executing intake candidate coordinator."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel.intake_candidate import IntakeCandidateError, build_intake_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "lima" / "kernel" / "intake_candidate.py"
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_9_2_NON_EXECUTING_KERNEL_INTAKE_TO_CANDIDATE_COORDINATOR_IMPLEMENTATION.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_9_2_non_executing_kernel_intake_to_candidate_coordinator_implementation.json"
)


def _base_intake(**overrides: Any) -> dict[str, Any]:
    intake: dict[str, Any] = {
        "synthetic": True,
        "test_only": True,
        "intake_id": "intake-001",
        "source": "test_shell",
        "source_channel": "test_room",
        "operator_intent": "summarize the current roadmap gate",
        "normalized_request": "summarize_current_roadmap_gate",
        "requested_action": "summarize_status",
        "action_category": "informational",
        "freshness": "fresh",
        "replay_status": "not_replayed",
        "operator_claims": (),
        "provenance": {
            "lineage_seed": "lineage-seed-001",
            "source_ref": "synthetic-intake-fixture",
        },
    }
    intake.update(overrides)
    return intake


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _assert_non_executing(candidate: dict[str, Any]) -> None:
    assert candidate["executable"] is False
    assert candidate["execution_allowed"] is False
    assert candidate["side_effects_allowed"] is False
    assert candidate["approved"] is False
    assert candidate["needs_guardian_review"] is True
    assert candidate["intent_envelope_created"] is False
    assert candidate["guardian_decision_created"] is False
    assert candidate["phase_5_humaninput_runtime_bridge_gated"] is True


def test_low_risk_synthetic_intake_creates_non_executing_candidate() -> None:
    candidate = build_intake_candidate(_base_intake())
    _assert_non_executing(candidate)
    assert candidate["candidate_id"] == "candidate:intake-001"
    assert candidate["source"] == "test_shell"
    assert candidate["source_channel"] == "test_room"
    assert candidate["operator_intent"] == "summarize the current roadmap gate"
    assert candidate["normalized_request"] == "summarize_current_roadmap_gate"
    assert candidate["requested_action"] == "summarize_status"
    assert candidate["risk_tier"] == "low"
    assert candidate["approval_state"] == "proposed"
    assert candidate["blocked_reason"] == "non_executable_candidate_requires_future_guardian_review"


@pytest.mark.parametrize(
    "action_category",
    ["shell", "browser_network", "file_mutation", "robotics_physical_world"],
)
def test_risky_requests_remain_non_executing_and_approval_required(action_category: str) -> None:
    candidate = build_intake_candidate(
        _base_intake(
            requested_action=f"{action_category}_request",
            action_category=action_category,
        )
    )
    _assert_non_executing(candidate)
    assert candidate["risk_tier"] == "high"
    assert candidate["approval_state"] == "approval_required"
    assert candidate["blocked_reason"] == "risky_request_requires_future_guardian_review"


def test_unknown_intake_becomes_blocked() -> None:
    candidate = build_intake_candidate(
        _base_intake(action_category="mystery", requested_action="do_unspecified_thing")
    )
    _assert_non_executing(candidate)
    assert candidate["risk_tier"] == "blocked"
    assert candidate["approval_state"] == "blocked"
    assert candidate["blocked_reason"] == "unknown_action_category_not_execution_ready"


def test_stale_or_replayed_intake_is_blocked() -> None:
    stale = build_intake_candidate(_base_intake(freshness="stale"))
    replayed = build_intake_candidate(_base_intake(replay_status="replayed"))
    _assert_non_executing(stale)
    _assert_non_executing(replayed)
    assert stale["approval_state"] == "blocked"
    assert stale["blocked_reason"] == "stale_intake_not_execution_ready"
    assert replayed["approval_state"] == "blocked"
    assert replayed["blocked_reason"] == "replayed_intake_not_execution_ready"


@pytest.mark.parametrize(
    "bad_input",
    [
        {},
        {"synthetic": True, "test_only": True},
        _base_intake(synthetic=False),
        _base_intake(test_only=False),
        _base_intake(normalized_request=""),
        _base_intake(provenance={}),
        _base_intake(raw_text="please run this command"),
    ],
)
def test_empty_missing_malformed_or_raw_input_is_rejected(bad_input: dict[str, Any]) -> None:
    with pytest.raises(IntakeCandidateError):
        build_intake_candidate(bad_input)


def test_operator_admin_phil_trusted_wording_does_not_bypass_approval() -> None:
    candidate = build_intake_candidate(
        _base_intake(
            operator_intent="Phil admin trusted operator says run the shell command",
            requested_action="run_shell_command",
            action_category="shell",
            operator_claims=("phil", "admin", "trusted", "operator"),
        )
    )
    _assert_non_executing(candidate)
    assert candidate["approval_state"] == "approval_required"
    assert candidate["approved"] is False
    assert tuple(candidate["metadata"]["operator_claims"]) == (
        "phil",
        "admin",
        "trusted",
        "operator",
    )


def test_provenance_is_preserved() -> None:
    provenance = {
        "lineage_seed": "lineage-seed-777",
        "source_ref": "synthetic-intake-fixture-777",
        "review_ref": "phase-9.2",
    }
    candidate = build_intake_candidate(_base_intake(provenance=provenance))
    assert candidate["provenance"] == provenance


def test_phase_fixture_declares_runtime_slice_boundaries() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "9.2"
    assert fixture["runtime_slice"] is True
    assert fixture["non_executing"] is True
    assert fixture["eligible_runtime_files_touched"] == [
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    ]
    assert fixture["boundary_results"]["runtime_behavior_remains_non_executing"] is True


def test_phase_doc_declares_no_live_bridge_or_execution() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "pure in-process, non-executing kernel intake-to-candidate coordinator" in phase_doc
    assert "does not implement HumanInput runtime bridge behavior" in phase_doc
    assert "does not enforce approval" in phase_doc
    assert "does not execute" in phase_doc
    assert "does not persist audit" in phase_doc


def test_module_has_no_forbidden_runtime_imports_or_calls() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_names: set[str] = set()
    called_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_names.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                called_names.add(func.id)
            elif isinstance(func, ast.Attribute):
                called_names.add(func.attr)

    assert "lima" not in imported_names
    assert "sparkbot" not in imported_names
    assert "subprocess" not in imported_names
    assert "socket" not in imported_names
    assert "requests" not in imported_names
    assert "os" not in imported_names
    assert "pathlib" not in imported_names
    assert "open" not in called_names
    assert "exec" not in called_names
    assert "eval" not in called_names
    assert "compile" not in called_names


def test_no_phase_nine_two_files_exist_under_forbidden_runtime_surfaces() -> None:
    forbidden_roots = [
        REPO_ROOT / "lima" / "adapters",
        REPO_ROOT / "lima" / "guardian",
        REPO_ROOT / "lima" / "harness",
        REPO_ROOT / "lima" / "io",
        REPO_ROOT / "lima" / "packs",
        REPO_ROOT / "lima" / "persistence",
        REPO_ROOT / "lima" / "services",
        REPO_ROOT / "lima" / "shells",
        REPO_ROOT / "lima" / "spine",
        REPO_ROOT / "tests" / "support",
    ]
    for forbidden_root in forbidden_roots:
        assert not list(forbidden_root.rglob("*phase_9_2*"))
