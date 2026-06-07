from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


FIXTURE_PATH = (
    pathlib.Path(__file__).resolve().parent
    / "fixtures"
    / "consumer_readiness_checklist"
    / "consumer_readiness_checklist.json"
)
REQUIRED_SHARED_EVIDENCE = {
    "branch_name",
    "lima_package_or_import_method",
    "lima_commit_or_version",
    "normalized_request_fixture_or_builder",
    "dry_run_execution_result_sample",
    "non_execution_invariant_checklist",
    "proof_no_raw_prompt_or_task_text_sent_to_lima",
    "proof_no_production_route_wired",
    "proof_no_model_tool_connector_storage_action",
    "proof_no_scheduler_or_background_worker_triggered",
    "proof_no_external_send",
    "proof_no_device_robot_drone_physical_world_action",
    "rollback_or_disable_plan",
}
REQUIRED_ALLOWED_INPUTS = {
    "redacted_shell_identity",
    "redacted_actor_identity",
    "redacted_session_identity",
    "already_normalized_intent_or_office_task_metadata",
    "default_deny_capability_profile",
    "source_surface_metadata",
    "context_refs_only",
    "synthetic_or_simulated_discovery_metadata",
    "redacted_approval_boundary_hints",
}
REQUIRED_FORBIDDEN_INPUTS = {
    "raw_chat_text",
    "raw_office_task_text",
    "raw_prompt_text",
    "raw_attachments",
    "raw_connector_records",
    "raw_provider_payloads",
    "raw_tool_arguments",
    "credentials",
    "headers",
    "cookies",
    "tokens",
    "unsafe_command_bodies",
    "live_scan_dumps",
    "customer_record_payloads",
    "regulated_data_payloads",
    "device_serials",
    "physical_location",
    "robot_drone_command_payloads",
}
EXPECTED_CONSUMERS = {"sparkbot", "arc"}
EXPECTED_FALSE_INVARIANTS = {
    "executable",
    "execution_allowed",
    "side_effects_allowed",
    "dispatch_allowed",
    "persistence_allowed",
    "model_calls_allowed",
    "model_calls_executed",
    "live_discovery_executed",
    "connection_attempted",
    "pairing_attempted",
    "credentials_used",
    "session_opened",
    "device_control_executed",
    "physical_world_allowed",
    "physical_world_executed",
    "guardian_decision_created",
    "approval_enforced",
    "humaninput_bridge_active",
    "sparkbot_wiring_active",
    "robo_os_wiring_active",
    "adapter_active",
    "tool_execution_allowed",
    "driver_execution_allowed",
    "scheduler_active",
    "external_calls_allowed",
}


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _consumers_by_id() -> dict[str, Mapping[str, Any]]:
    fixture = _load_fixture()
    return {consumer["consumer_id"]: consumer for consumer in fixture["consumers"]}


def test_consumer_readiness_checklist_is_lima_local_fixture_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "synthetic_consumer_readiness_checklist_fixture_only"
    assert fixture["lima_runtime_behavior_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_integration_implemented"] is False
    assert fixture["production_readiness_claimed"] is False


def test_shared_consumer_proof_evidence_is_complete() -> None:
    fixture = _load_fixture()

    assert set(fixture["shared_required_evidence"]) == REQUIRED_SHARED_EVIDENCE
    assert set(fixture["shared_allowed_inputs"]) == REQUIRED_ALLOWED_INPUTS
    assert set(fixture["shared_forbidden_inputs"]) == REQUIRED_FORBIDDEN_INPUTS


def test_required_non_execution_invariants_are_declared() -> None:
    invariants = _load_fixture()["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    for invariant_name in EXPECTED_FALSE_INVARIANTS:
        assert invariants[invariant_name] is False


def test_forbidden_surfaces_are_all_explicitly_blocked() -> None:
    forbidden = _load_fixture()["forbidden_surfaces"]

    assert forbidden
    assert all(forbidden.values())
    assert forbidden["sparkbot_repo_changes"] is True
    assert forbidden["arc_bot_repo_changes"] is True
    assert forbidden["lima_runtime_behavior_changes"] is True
    assert forbidden["provider_model_calls"] is True
    assert forbidden["tool_execution"] is True
    assert forbidden["scheduler_background_work"] is True
    assert forbidden["robot_drone_physical_world_behavior"] is True


def test_consumer_entries_cover_sparkbot_and_arc_with_owned_proof_branches() -> None:
    consumers = _consumers_by_id()

    assert set(consumers) == EXPECTED_CONSUMERS
    assert consumers["sparkbot"]["proof_branch"] == "sparkbot-lima-dry-run-boundary-proof"
    assert consumers["arc"]["proof_branch"] == "arc-lima-dry-run-boundary-proof"
    assert consumers["sparkbot"]["owner_repo_team"] == "sparkbot"
    assert consumers["arc"]["owner_repo_team"] == "arc"


def test_consumer_entries_point_to_existing_lima_evidence() -> None:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    for consumer in _consumers_by_id().values():
        for field_name in (
            "owned_boundary_design",
            "owned_boundary_audit",
            "handoff_fixture_audit",
        ):
            evidence_path = repo_root / consumer[field_name]
            assert evidence_path.exists(), f"missing evidence path: {evidence_path}"


def test_sparkbot_and_arc_have_distinct_required_evidence() -> None:
    consumers = _consumers_by_id()
    sparkbot_evidence = set(consumers["sparkbot"]["consumer_specific_required_evidence"])
    arc_evidence = set(consumers["arc"]["consumer_specific_required_evidence"])

    assert "proof_no_raw_chat_sent_to_lima" in sparkbot_evidence
    assert "proof_no_public_sparkbot_production_route_wired" in sparkbot_evidence
    assert "proof_no_raw_office_task_text_sent_to_lima" in arc_evidence
    assert "proof_no_customer_record_payload_sent_to_lima" in arc_evidence
    assert "proof_no_arc_scheduler_or_background_worker_triggered" in arc_evidence
    assert sparkbot_evidence != arc_evidence


def test_consumer_entries_are_not_production_ready() -> None:
    for consumer in _consumers_by_id().values():
        assert consumer["dry_run_proof_conditionally_ready"] is True
        assert consumer["production_ready"] is False


def test_remaining_lima_blockers_prevent_production_claims() -> None:
    blockers = set(_load_fixture()["remaining_lima_blockers_before_production_use"])

    assert "real_guardian_request_decision_lifecycle" in blockers
    assert "approval_enforcement_implementation" in blockers
    assert "humaninput_bridge_contract_and_implementation" in blockers
    assert "provider_model_boundary_design_and_implementation" in blockers
    assert "tool_execution_boundary_design" in blockers
    assert "connector_boundary_design" in blockers
    assert "event_spine_persistence_design" in blockers
    assert "storage_interface_implementation" in blockers
    assert "consumer_owned_proof_branch_design_and_audit_in_each_repo" in blockers
