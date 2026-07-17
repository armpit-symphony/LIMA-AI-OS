"""Static checks for the V1-G11 runtime request decision gate work order."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g11_runtime_request_decision_gate_work_order.json"
)
DOC_PATH = REPO_ROOT / "docs" / "V1_G11_RUNTIME_REQUEST_DECISION_GATE_WORK_ORDER.md"


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_work_order_exists_without_approval() -> None:
    fixture = _load_fixture()
    assert DOC_PATH.exists()
    assert FIXTURE_PATH.exists()
    assert fixture["work_order_id"] == "v1_g11_runtime_request_decision_gate_work_order"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert fixture["source_commit"] == "3f844a5097e2be60653e2b85bbbec9ce758cbc48"
    assert fixture["document"] == "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_WORK_ORDER.md"
    assert (
        fixture["approval_request_document"]
        == "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md"
    )
    assert fixture["work_order_ready"] is True
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False


def test_v1_g11_work_order_adds_no_runtime_behavior() -> None:
    fixture = _load_fixture()
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_code_copied",
        "sparkbot_import_added",
        "provider_model_routing_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False


def test_v1_g11_work_order_reuses_existing_contract_shapes() -> None:
    shapes = set(_load_fixture()["existing_shapes_to_reuse"])
    assert "lima.contracts.guardian.ConsequentialActionRequest" in shapes
    assert "lima.contracts.guardian.ConsequentialActionType" in shapes
    assert "lima.contracts.guardian.GuardianDecision" in shapes
    assert "lima.contracts.guardian.GuardianDecisionStatus" in shapes
    assert "lima.kernel.validate_candidate" in shapes
    assert "lima.kernel.normalize_candidate_status" in shapes


def test_v1_g11_work_order_locks_future_file_and_symbol_scope() -> None:
    fixture = _load_fixture()
    assert set(fixture["approved_runtime_files_if_operator_approves"]) == {
        "lima/kernel/v1_runtime_request.py",
        "lima/kernel/__init__.py",
        "lima/guardian/v1_decision_gate.py",
        "lima/guardian/__init__.py",
    }
    symbols = set(fixture["candidate_symbols_if_approved"])
    assert "V1RuntimeRequestError" in symbols
    assert "build_v1_runtime_request" in symbols
    assert "V1GuardianDecisionGateError" in symbols
    assert "review_v1_runtime_request" in symbols


def test_v1_g11_work_order_mapping_rules_keep_execution_blocked() -> None:
    rules = _load_fixture()["required_mapping_rules_if_approved"]
    assert rules["informational"] == "reviewed_non_executing_no_approval_token"
    assert rules["planning"] == "reviewed_non_executing_no_approval_token"
    assert rules["drafting"] == "reviewed_non_executing_no_approval_token"
    assert rules["file_mutation"] == "approval_required_non_executing"
    assert rules["destructive_edit"] == "approval_required_non_executing"
    assert rules["destructive_delete"] == "approval_required_non_executing"
    assert rules["model_call"] == "blocked_or_future_policy_required_no_routing"
    assert rules["tool_call"] == "blocked_or_future_policy_required_no_execution"
    assert rules["browser_network"] == "blocked_or_future_policy_required_no_browser_network_action"
    assert rules["robotics_physical_world"] == (
        "blocked_or_future_policy_required_no_physical_action"
    )
    assert rules["unknown"] == "denied_or_blocked"


def test_v1_g11_work_order_outputs_and_stop_conditions_are_safe() -> None:
    fixture = _load_fixture()
    allowed_outputs = set(fixture["allowed_outputs_if_approved"])
    assert "typed_request_metadata" in allowed_outputs
    assert "guardian_decision_metadata" in allowed_outputs
    assert "non_persistent_audit_evidence_linkage_metadata" in allowed_outputs

    forbidden_outputs = set(fixture["forbidden_outputs"])
    assert "raw_secrets" in forbidden_outputs
    assert "raw_prompts" in forbidden_outputs
    assert "raw_file_contents" in forbidden_outputs
    assert "approval_pins" in forbidden_outputs
    assert "approval_tokens" in forbidden_outputs
    assert "provider_credentials" in forbidden_outputs
    assert "executable_commands" in forbidden_outputs
    assert "mutation_instructions_marked_approved" in forbidden_outputs

    stops = set(fixture["stop_conditions"])
    assert "files_outside_approved_v1_g11_file_map" in stops
    assert "raw_natural_language_parsing" in stops
    assert "execution_dispatch_persistence_workers_or_subprocesses" in stops
    assert "provider_model_calls_or_routing" in stops
    assert "shell_runtime_wiring" in stops
    assert "sparkbot_sparkbot_shell_arc_bot_shell_imports_or_code_copy" in stops
    assert "approval_token_issuance" in stops
    assert "destructive_edit_delete_approved_without_operator_approval_evidence" in stops
    assert "browser_file_network_device_robotics_physical_world_behavior" in stops
    assert "runtime_export_cleanup" in stops
    assert "final_api_freeze" in stops


def test_v1_g11_work_order_doc_matches_fixture() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Work order verdict: `ready_if_operator_approves_runtime`" in text
    assert "This is a work order only." in text
    assert "V1-G11 implementation may start only after the operator explicitly approves" in text
    assert "Do not create a parallel Guardian request model" in text
    assert "`informational` -> reviewed, non-executing, no approval token" in text
    assert "`file_mutation` -> approval-required, non-executing" in text
    assert "Operator decision on the exact V1-G11 approval request." in text
