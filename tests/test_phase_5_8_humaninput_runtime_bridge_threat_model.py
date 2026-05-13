"""Static checks for Phase 5.8 HumanInput runtime bridge threat model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_5_8_HUMANINPUT_RUNTIME_BRIDGE_THREAT_MODEL.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_8_humaninput_runtime_bridge_threat_model.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_fixture_declares_threat_model_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "5.8"
    assert fixture["status"] == "humaninput_runtime_bridge_threat_model"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["threat_model_only"] is True


def test_doc_says_no_runtime_or_helper_behavior_is_added() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement a runtime bridge" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change the Phase 5.4 helper" in phase_doc


def test_required_threats_are_modeled() -> None:
    threat_ids = {threat["id"] for threat in _load_json(PHASE_FIXTURE_PATH)["threats"]}
    assert {
        "prompt_injection",
        "operator_impersonation",
        "trust_bypass",
        "accidental_execution",
        "side_effect_escalation",
        "audit_gaps",
        "approval_confusion",
        "helper_classifier_misuse",
        "unsafe_test_code_reuse",
        "malformed_input",
        "replayed_input",
        "ambiguous_commands",
    } <= threat_ids


def test_mitigations_keep_humaninput_non_executing_and_guardian_gated() -> None:
    mitigations = set(_load_json(PHASE_FIXTURE_PATH)["required_mitigations"])
    assert "humaninput_is_intent_context_only" in mitigations
    assert "provenance_required_before_candidate_creation" in mitigations
    assert "candidates_default_non_executable" in mitigations
    assert "side_effect_categories_require_approval_required_or_blocked" in mitigations
    assert "operator_admin_phil_trusted_wording_cannot_bypass_approval" in mitigations


def test_helper_and_tests_support_reuse_are_explicitly_mitigated() -> None:
    mitigations = set(_load_json(PHASE_FIXTURE_PATH)["required_mitigations"])
    assert "phase_5_4_helper_remains_test_only" in mitigations
    assert "production_runtime_must_not_import_tests_support" in mitigations
    assert "future_runtime_design_required_before_implementation" in mitigations


def test_residual_risk_requires_future_runtime_review_before_live_behavior() -> None:
    residual = _load_json(PHASE_FIXTURE_PATH)["residual_risk"]
    assert residual["static_model_only"] is True
    assert residual["runtime_safety_proven"] is False
    assert residual["requires_future_runtime_design_review"] is True
    assert residual["requires_future_semantic_tests"] is True
    assert residual["requires_future_guardian_gate_review"] is True
    assert residual["requires_explicit_operator_approval_before_live_behavior"] is True


def test_blocked_scope_preserves_runtime_boundaries() -> None:
    blocked = _load_json(PHASE_FIXTURE_PATH)["blocked_scope"]
    assert all(blocked.values())
    assert blocked["runtime_bridge_implementation"] is True
    assert blocked["live_adapter_code"] is True
    assert blocked["files_under_lima"] is True
    assert blocked["tests_support_changes"] is True
    assert blocked["approval_enforcement"] is True
    assert blocked["execution"] is True
    assert blocked["physical_world_action"] is True


def test_ready_only_for_phase_five_nine_validation_matrix() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_5_9_docs_tests_fixtures_only_boundary_validation_matrix"
    ]
    assert "runtime_bridge_implementation" in fixture["not_ready_for"]
    assert "phase_5_4_helper_runtime_reuse" in fixture["not_ready_for"]


def test_boundary_results_show_no_runtime_or_helper_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["runtime_bridge_added"] is False


def test_no_phase_five_eight_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_5_8*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_5_8*"))
