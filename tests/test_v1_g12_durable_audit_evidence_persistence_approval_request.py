"""Static checks for the V1-G12 durable audit/evidence persistence approval request."""

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
    / "v1_g12_durable_audit_evidence_persistence_approval_request.json"
)
DOCS = {
    "approval_request": (
        REPO_ROOT / "docs" / "V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_APPROVAL_REQUEST.md"
    ),
    "preflight_audit": (
        REPO_ROOT / "docs" / "V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_PREFLIGHT_AUDIT.md"
    ),
    "work_order": (
        REPO_ROOT / "docs" / "V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_WORK_ORDER.md"
    ),
    "operator_decision_packet": (
        REPO_ROOT
        / "docs"
        / "V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_OPERATOR_DECISION_PACKET.md"
    ),
    "current_state": REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md",
    "v1_g11_audit": (
        REPO_ROOT / "docs" / "audits" / "V1_G11_RUNTIME_REQUEST_DECISION_GATE_AUDIT.md"
    ),
}


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g12_approval_request_docs_exist_and_remain_candidate_only() -> None:
    fixture = _load_fixture()
    assert FIXTURE_PATH.exists()
    for path in DOCS.values():
        assert path.exists()

    assert fixture["gap_id"] == "V1-G12"
    assert fixture["packet_type"] == "durable_audit_evidence_persistence_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g12-durable-audit-evidence-persistence-approval-request"
    assert fixture["source_branch"] == "audit-v1-g11-runtime-request-decision-gate"
    assert fixture["base_commit"] == "5ff60a0536485cc3b87792c7ffb93c7e92a59520"
    assert fixture["approval_request_ready"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["decision_packet_status"] == "awaiting_operator_decision"
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_g12_approval_request_adds_no_runtime_behavior() -> None:
    fixture = _load_fixture()
    for key in (
        "runtime_behavior_added",
        "durable_persistence_added",
        "storage_adapter_added",
        "query_api_added",
        "external_database_writes_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_code_copied",
        "sparkbot_import_added",
        "sparkbot_shell_import_added",
        "arc_bot_shell_import_added",
        "provider_model_routing_added",
        "provider_model_calls_added",
        "guardian_authority_expanded",
        "approval_enforcement_added",
        "humaninput_bridge_activated",
        "connector_behavior_added",
        "browser_file_network_device_robotics_physical_world_added",
        "haptic_device_behavior_added",
        "runtime_exports_changed",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False


def test_v1_g12_exact_approval_scope_is_machine_readable() -> None:
    fixture = _load_fixture()
    assert "Do you explicitly approve V1-G12 implementation" in fixture["exact_approval_question"]
    assert fixture["if_approved_next_branch"] == "v1-g12-durable-audit-evidence-persistence"
    assert fixture["if_approved_objective"] == "durable_audit_evidence_persistence_runtime_slice"

    runtime_files = set(fixture["eligible_runtime_files_if_approved"])
    assert runtime_files == {
        "lima/spine/v1_audit_evidence.py",
        "lima/spine/__init__.py",
        "lima/persistence/v1_audit_store.py",
        "lima/persistence/__init__.py",
    }

    non_runtime_files = set(fixture["eligible_non_runtime_files_if_approved"])
    assert "docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE.md" in non_runtime_files
    assert "docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md" in non_runtime_files
    assert (
        "tests/fixtures/runtime_extraction/v1_g12_durable_audit_evidence_persistence.json"
        in non_runtime_files
    )
    assert "tests/test_v1_g12_durable_audit_evidence_persistence.py" in non_runtime_files


def test_v1_g12_allowed_behaviors_preserve_guardian_and_redaction_boundaries() -> None:
    behaviors = set(_load_fixture()["allowed_runtime_behaviors_if_approved"])
    assert "only_reviewed_v1_request_decision_metadata_enters_slice" in behaviors
    assert "audit_records_are_proof_not_authority" in behaviors
    assert "missing_lineage_id_fails_closed" in behaviors
    assert "missing_tenant_ref_fails_closed" in behaviors
    assert "consequential_record_without_decision_id_fails_closed" in behaviors
    assert "destructive_edit_delete_without_approval_evidence_fails_closed" in behaviors
    assert "raw_sensitive_content_fails_closed" in behaviors
    assert "deterministic_record_hashes_over_sanitized_content" in behaviors
    assert "append_only_explicit_local_audit_store" in behaviors
    assert "cross_tenant_or_cross_shell_lookup_fails_closed" in behaviors


def test_v1_g12_forbidden_surfaces_cover_scope_creep() -> None:
    forbidden = set(_load_fixture()["forbidden_surfaces"])
    assert "provider_model_calls_or_routing" in forbidden
    assert "tool_execution" in forbidden
    assert "arbitrary_file_mutation_outside_explicit_audit_store_path" in forbidden
    assert "browser_network_behavior" in forbidden
    assert "connector_behavior" in forbidden
    assert "shell_runtime_wiring" in forbidden
    assert "sparkbot_sparkbot_shell_arc_bot_shell_imports_or_code_copy" in forbidden
    assert "external_database_writes" in forbidden
    assert "queues_workers_daemons_subprocesses_threads" in forbidden
    assert "live_auth_trust_lookup_or_humaninput_bridge_activation" in forbidden
    assert "audit_records_as_execution_authority" in forbidden
    assert "raw_sensitive_content_persistence" in forbidden
    assert "device_robotics_iot_drone_robot_humanoid_physical_world_behavior" in forbidden
    assert "runtime_export_cleanup" in forbidden
    assert "final_api_freeze" in forbidden


def test_v1_g12_acceptance_tests_require_persistence_and_negative_cases() -> None:
    tests = set(_load_fixture()["required_acceptance_tests_if_approved"])
    assert "safe_v1_request_decision_metadata_creates_redacted_audit_event" in tests
    assert (
        "audit_event_requires_lineage_event_tenant_actor_shell_and_decision_for_consequential_action"
        in tests
    )
    assert "destructive_edit_delete_requires_approval_id_and_approval_evidence_ref" in tests
    assert "raw_secret_values_are_rejected" in tests
    assert "raw_approval_pins_and_tokens_are_rejected" in tests
    assert "raw_prompts_and_raw_file_contents_are_rejected" in tests
    assert "unknown_privacy_class_fails_closed" in tests
    assert "record_hashes_are_deterministic_for_sanitized_records" in tests
    assert "append_only_store_writes_and_reads_redacted_records_from_explicit_local_path" in tests
    assert "cross_tenant_or_cross_shell_lookup_fails_closed" in tests
    assert "records_do_not_authorize_execution_or_emit_approval_tokens" in tests


def test_v1_g12_decision_packet_records_no_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]
    assert decision["recorded_choice"] is None
    assert decision["recorded_approval_wording"] is None
    assert decision["recorded_revision_request"] is None
    assert decision["recorded_pause_reason"] is None
    assert decision["approved_implementation_branch"] is None
    assert decision["runtime_implementation_approved"] is False
    assert set(fixture["valid_operator_choices"]) == {
        "Approve-V1-G12",
        "Revise-V1-G12",
        "Pause",
    }


def test_v1_g12_rollback_and_stop_conditions_are_explicit() -> None:
    fixture = _load_fixture()
    rollback = set(fixture["rollback_files_if_approved"])
    assert "lima/spine/v1_audit_evidence.py" in rollback
    assert "lima/persistence/v1_audit_store.py" in rollback
    assert "candidate_exports_added_to_lima/spine/__init__.py" in rollback
    assert "candidate_exports_added_to_lima/persistence/__init__.py" in rollback

    stops = set(fixture["stop_conditions"])
    assert "file_scope_exceeds_approved_v1_g12_files" in stops
    assert "persistence_writes_outside_explicit_audit_store_path" in stops
    assert "raw_sensitive_content_can_persist" in stops
    assert "audit_metadata_becomes_execution_authority" in stops
    assert "destructive_edit_delete_records_persist_without_approval_evidence" in stops
    assert "consequential_records_persist_without_decision_id" in stops
    assert "cross_tenant_or_cross_shell_query_leakage" in stops
    assert "provider_model_calls_or_routing_added" in stops
    assert "shell_runtime_wiring_added" in stops
    assert "sparkbot_code_imported_or_copied" in stops
    assert "runtime_exports_cleaned_up_or_frozen" in stops
    assert "validation_fails" in stops


def test_v1_g12_docs_match_preflight_and_no_approval_verdict() -> None:
    fixture = _load_fixture()
    assert fixture["preflight_audit_result"] == "approval_request_ready_runtime_not_approved"
    assert (
        fixture["recommended_next_step"]
        == "operator_decision_on_exact_v1_g12_approval_question"
    )

    approval_text = DOCS["approval_request"].read_text(encoding="utf-8")
    audit_text = DOCS["preflight_audit"].read_text(encoding="utf-8")
    work_order_text = DOCS["work_order"].read_text(encoding="utf-8")
    decision_text = DOCS["operator_decision_packet"].read_text(encoding="utf-8")
    current_state_text = DOCS["current_state"].read_text(encoding="utf-8")

    assert "Request verdict: `ready_for_operator_decision_not_approved`" in approval_text
    assert "Approval must be explicit before implementation begins." in approval_text
    assert "Preflight verdict: `approval_request_ready_runtime_not_approved`" in audit_text
    assert "Work order verdict: `ready_if_operator_approves_runtime`" in work_order_text
    assert "Decision packet status: `awaiting_operator_decision`" in decision_text
    assert "Recorded choice: `none`" in decision_text
    assert "Runtime implementation approved: no" in decision_text
    assert "## V1-G12 - Durable Audit/Evidence Persistence Approval Request" in current_state_text
