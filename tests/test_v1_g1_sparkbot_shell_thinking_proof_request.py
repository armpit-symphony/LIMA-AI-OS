"""Static checks for the V1-G1 Sparkbot_shell thinking proof request."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_G1_SPARKBOT_SHELL_THINKING_PROOF_REQUEST.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g1_sparkbot_shell_thinking_proof_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g1_request_document_and_fixture_exist() -> None:
    fixture = _load_fixture()
    assert DOC_PATH.exists()
    assert fixture["gap_id"] == "V1-G1"
    assert fixture["gap_name"] == "sparkbot_shell_thinking_progress_proof"
    assert fixture["request_document"] == "docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_REQUEST.md"
    assert fixture["source_target"] == "docs/V1_PRODUCT_READINESS_TARGET.md"
    assert fixture["gap_matrix"] == "docs/V1_READINESS_GAP_MATRIX.md"
    assert fixture["request_status"] == "created_waiting_on_sparkbot_shell"
    assert fixture["proof_requested"] is True
    assert fixture["proof_received"] is False


def test_v1_g1_request_targets_sparkbot_shell_thinking_state() -> None:
    fixture = _load_fixture()
    assert fixture["requested_consumer_repo"] == "Sparkbot_shell"
    assert fixture["requested_proof_branch"] == "sparkbot-shell-thinking-state-proof-packet"
    assert fixture["required_state"] == "thinking"
    assert fixture["source_backed_thinking_required"] is True
    assert fixture["docs_fixture_only_thinking_acceptable"] is False


def test_v1_g1_requested_files_are_explicit() -> None:
    requested = set(_load_fixture()["requested_proof_files"])
    assert "docs/proof_packets/SPARKBOT_SHELL_THINKING_STATE_PROOF_PACKET.md" in requested
    assert "docs/audits/SPARKBOT_SHELL_THINKING_STATE_PROOF_AUDIT.md" in requested
    assert "tests/fixtures/sparkbot_shell_thinking_state_proof_packet.json" in requested
    assert "tests/test_sparkbot_shell_thinking_state_proof_packet.py" in requested


def test_v1_g1_required_evidence_covers_state_transitions_and_shell_review() -> None:
    evidence = set(_load_fixture()["required_evidence"])
    assert "thinking_source_files" in evidence
    assert "thinking_render_entrypoints" in evidence
    assert "received_to_thinking_transition" in evidence
    assert "thinking_to_terminal_or_preview_transition" in evidence
    assert "desktop_behavior_notes" in evidence
    assert "mobile_behavior_notes" in evidence
    assert "haptics_notes" in evidence
    assert "static_tests_or_fixture_checks" in evidence
    assert "no_lima_runtime_behavior_boundary" in evidence


def test_v1_g1_machine_readable_fields_keep_boundaries_explicit() -> None:
    fields = set(_load_fixture()["required_machine_readable_fields"])
    assert "proof_gap_id" in fields
    assert "state_name" in fields
    assert "source_backed_thinking" in fields
    assert "docs_fixture_only_thinking" in fields
    assert "haptics_shell_owned" in fields
    assert "lima_owns_haptics" in fields
    assert "lima_runtime_behavior_added" in fields
    assert "provider_model_routing_added" in fields
    assert "guardian_decision_runtime_added" in fields
    assert "approval_enforcement_added" in fields
    assert "production_readiness_claimed" in fields


def test_v1_g1_acceptance_and_rejection_criteria_are_fail_closed() -> None:
    fixture = _load_fixture()
    acceptance = fixture["acceptance_criteria"]
    assert acceptance["thinking_source_backed"] is True
    assert acceptance["haptics_shell_owned"] is True
    assert acceptance["lima_owns_haptics"] is False
    assert acceptance["lima_runtime_behavior_added"] is False
    assert acceptance["provider_model_routing_added"] is False
    assert acceptance["guardian_decision_runtime_added"] is False
    assert acceptance["approval_enforcement_added"] is False
    assert acceptance["production_readiness_claimed"] is False
    rejection = set(fixture["rejection_criteria"])
    assert "thinking_docs_fixture_only" in rejection
    assert "lima_runtime_integration_claimed" in rejection
    assert "guardian_decision_runtime_claimed" in rejection
    assert "approval_enforcement_claimed" in rejection
    assert "provider_model_routing_through_lima_claimed" in rejection
    assert "production_readiness_claimed" in rejection


def test_v1_g1_lima_boundary_results_add_no_runtime_or_shell_changes() -> None:
    boundary = _load_fixture()["lima_boundary_results"]
    assert boundary["docs_tests_fixtures_only"] is True
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repo_changed",
        "sparkbot_shell_wiring_added",
        "sparkbot_shell_import_added",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "runtime_exports_changed",
        "runtime_implementation_approved",
        "v1_product_ready",
    ):
        assert boundary[key] is False


def test_v1_g1_document_states_request_scope_and_next_step() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "This document requests the next Sparkbot_shell proof packet for V1 readiness gap `V1-G1`." in text
    assert "`sparkbot-shell-thinking-state-proof-packet`" in text
    assert "Static/docs-only `thinking` labels are not enough" in text
    assert "haptics remain shell-owned" in text
    assert "no LIMA runtime behavior" in text
    assert "LIMA will intake the future Sparkbot_shell packet as evidence only." in text
