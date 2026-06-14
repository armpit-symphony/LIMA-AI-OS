"""Static checks for the V1-G12 durable audit/evidence persistence audit."""

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
    / "v1_g12_durable_audit_evidence_persistence_audit.json"
)
STATE_PATH = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g12_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g12_durable_audit_evidence_persistence_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["audit_branch"] == "audit-v1-g12-durable-audit-evidence-persistence"
    assert fixture["implementation_branch"] == "v1-g12-durable-audit-evidence-persistence"
    assert fixture["implementation_commit"] == "457b654a50e100ef7c000de25bb6d2c7493b9fc6"
    assert fixture["verdict"] == "PASS_WITH_WARNINGS"

    assert (REPO_ROOT / fixture["audit_document"]).exists()
    for relative_path in fixture["files_audited"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g12_audit_runtime_files_stay_inside_approved_map() -> None:
    fixture = _load_fixture()
    approved_runtime = set(fixture["approved_runtime_file_map"])
    changed_runtime = {
        path
        for path in fixture["implementation_changed_files"]
        if path.startswith("lima/")
    }

    assert fixture["runtime_files_within_approved_map"] is True
    assert changed_runtime == approved_runtime


def test_v1_g12_audit_records_operator_decision() -> None:
    decision = _load_fixture()["operator_decision"]

    assert decision["recorded_choice"] == "Approve-V1-G12"
    assert (
        decision["approved_implementation_branch"]
        == "v1-g12-durable-audit-evidence-persistence"
    )
    assert decision["runtime_implementation_approved"] is True


def test_v1_g12_audit_locks_runtime_symbols() -> None:
    assert set(_load_fixture()["runtime_symbols"]) == {
        "V1AuditEvidenceError",
        "build_v1_audit_event_record",
        "build_v1_audit_lineage_record",
        "V1AuditStoreError",
        "V1LocalAuditStore",
    }


def test_v1_g12_audit_behavior_results_pass() -> None:
    behavior = _load_fixture()["behavior_results"]

    for key in (
        "reviewed_v1_request_decision_metadata_creates_redacted_event",
        "missing_lineage_event_tenant_actor_shell_decision_fails_closed",
        "destructive_edit_delete_requires_approval_evidence",
        "raw_sensitive_content_fails_closed",
        "unknown_privacy_class_fails_closed",
        "record_hashes_are_deterministic",
        "append_only_store_writes_explicit_local_path",
        "lookup_by_event_lineage_decision_scoped",
        "cross_tenant_or_cross_shell_lookup_fails_closed",
        "audit_records_proof_not_authority",
        "future_policy_claims_remain_non_executing",
    ):
        assert behavior[key] == "pass"


def test_v1_g12_audit_boundary_results_remain_closed() -> None:
    boundary = _load_fixture()["boundary_results"]

    for key in (
        "consumer_repos_touched",
        "sparkbot_touched",
        "sparkbot_shell_touched",
        "arc_bot_shell_touched",
        "lima_robo_os_touched",
        "lima_office_touched",
        "provider_model_routing_added",
        "provider_model_calls_added",
        "tool_execution_added",
        "shell_runtime_wiring_added",
        "humaninput_bridge_activated",
        "connector_behavior_added",
        "browser_file_network_device_robotics_physical_world_added",
        "external_database_writes_added",
        "migrations_added",
        "queues_workers_daemons_subprocesses_threads_added",
        "raw_sensitive_content_persistence_allowed",
        "audit_metadata_execution_authority_added",
        "approval_token_or_pin_emitted",
        "runtime_export_cleanup_approved",
        "final_api_freeze_approved",
        "product_readiness_claimed",
        "production_readiness_claimed",
    ):
        assert boundary[key] is False


def test_v1_g12_audit_warnings_and_next_lane_are_explicit() -> None:
    fixture = _load_fixture()
    warnings = set(fixture["warnings"])

    assert (
        "operator_decision_packet_updated_by_explicit_operator_instruction_outside_implementation_file_map"
        in warnings
    )
    assert "local_jsonl_store_is_not_external_database_or_production_audit_service" in warnings
    assert "approved_decision_status_is_evidence_only_not_execution_authority" in warnings
    assert (
        fixture["recommended_next_lane"]
        == "v1_g13_readiness_gap_refresh_and_next_lane_decision_gate"
    )
    assert fixture["recommended_next_lane_scope"] == "docs_tests_fixtures_only"


def test_v1_g12_audit_doc_and_current_state_match_fixture() -> None:
    fixture = _load_fixture()
    audit_text = (REPO_ROOT / fixture["audit_document"]).read_text(encoding="utf-8")
    state_text = STATE_PATH.read_text(encoding="utf-8")

    assert "Verdict: `PASS WITH WARNINGS`" in audit_text
    assert "Runtime implementation files stayed within the approved V1-G12 runtime map" in audit_text
    assert "operator-directed decision recording" in audit_text
    assert "audit records, for authority" in audit_text
    assert "V1-G12 implementation and audit status" in state_text
    assert "audit status: `PASS WITH WARNINGS`" in state_text
