"""Phase 40.0 Arc Bot consumer boundary clarification tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_40_0_ARC_BOT_CONSUMER_BOUNDARY_CLARIFICATION.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_40_0_arc_bot_consumer_boundary_clarification.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_40_0_records_sparkbot_as_reference_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "40.0"
    assert fixture["sparkbot_reference_evidence_only"] is True
    assert fixture["primary_guarded_task_consumer"] == "arc_bot_lima_ai_office"
    assert fixture["lima_ai_os_runtime_main_target"] is True
    doc_text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Sparkbot v1.6.80 remains reference evidence" in doc_text
    assert "not the primary future consumer to wire next" in doc_text


def test_phase_40_0_classifies_required_concept_buckets() -> None:
    classification = _load_json(PHASE_FIXTURE_PATH)["concept_classification"]
    assert "command_center_operator_hub" in classification["adopt_into_lima_ai_os_planning_vocabulary"]
    assert "owner_local_routine_read_posture" in classification[
        "adapt_for_arc_bot_lima_office_with_stricter_defaults"
    ]
    assert "broad_shell_browser_live_terminal_code_execution" in classification[
        "keep_as_sparkbot_only_product_behavior"
    ]
    assert "direct_sparkbot_integration" in classification["defer_until_future_integration_planning"]
    assert "sparkbot_owner_local_execution_inheritance" in classification[
        "reject_from_lima_runtime_safety_model"
    ]


def test_phase_40_0_records_arc_bot_office_needs() -> None:
    needs = set(_load_json(PHASE_FIXTURE_PATH)["arc_bot_needs"])
    assert "task_oriented_office_workflow" in needs
    assert "operator_approval_boundaries" in needs
    assert "policy_simulation_explain_plan_before_action" in needs
    assert "run_states" in needs
    assert "durable_audit_evidence_model" in needs
    assert "agent_identity_kill_switch" in needs
    assert "memory_trust_verification_redaction" in needs
    assert "guarded_scheduled_work" in needs
    assert "connector_health_setup_posture" in needs
    assert "strict_defaults_for_external_writes_secrets_admin_physical_world" in needs


def test_phase_40_0_rejects_direct_implementation_recommendations() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["direct_sparkbot_integration_recommended"] is False
    assert fixture["arc_bot_implementation_recommended"] is False
    assert fixture["humaninput_bridge_implementation_recommended"] is False
    assert (
        fixture["recommended_next_direction"]
        == "docs_tests_fixtures_only_arc_bot_lima_office_consumer_boundary_review_or_arc_bot_shaped_candidate_preview_hardening"
    )


def test_phase_40_0_stays_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["forbidden_scope_touched"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_40_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_40_0*"))
