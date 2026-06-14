"""Static checks for the V1-G13 readiness-gap refresh gate."""

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
    / "v1_g13_readiness_gap_refresh_next_lane_decision_gate.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g13_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g13_readiness_gap_refresh_next_lane_decision_gate"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g13-readiness-gap-refresh-next-lane-decision-gate"
    assert fixture["source_branch"] == "audit-v1-g12-durable-audit-evidence-persistence"
    assert fixture["source_commit"] == "ba9f1483e49d8a4e11106f3074d2ced2becd155b"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g13_adds_no_runtime_or_release_approval() -> None:
    fixture = _load_fixture()

    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_behavior_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["operator_approval_recorded_for_next_runtime"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["next_runtime_implementation_approved"] is False


def test_v1_g13_accepts_v1_g11_and_v1_g12_evidence() -> None:
    accepted = _load_fixture()["accepted_evidence"]

    assert accepted["v1_g11_runtime_slice_implemented"] is True
    assert accepted["v1_g11_audit_verdict"] == "PASS"
    assert accepted["v1_g12_runtime_slice_implemented"] is True
    assert accepted["v1_g12_audit_verdict"] == "PASS_WITH_WARNINGS"
    assert accepted["v1_g12_local_jsonl_store_candidate_only"] is True


def test_v1_g13_remaining_blockers_are_explicit() -> None:
    blockers = set(_load_fixture()["remaining_blockers"])

    assert "v1_product_release_boundary_not_passed" in blockers
    assert "live_destructive_edit_delete_approval_enforcement_not_implemented" in blockers
    assert "approval_token_issuance_not_approved" in blockers
    assert "humaninput_bridge_activation_not_implemented" in blockers
    assert "provider_model_runtime_routing_not_implemented" in blockers
    assert "shell_runtime_wiring_not_implemented" in blockers
    assert "external_database_backed_audit_persistence_not_implemented" in blockers
    assert "runtime_export_cleanup_unapproved" in blockers
    assert "final_api_freeze_unapproved" in blockers
    assert "production_behavior_not_approved" in blockers


def test_v1_g13_recommends_v1_g14_approval_request_only() -> None:
    fixture = _load_fixture()
    options = set(fixture["next_lane_options"])

    assert "V1-G14-Approval-Enforcement-Request" in options
    assert "Provider-Model-Routing-Request" in options
    assert "Shell-Wiring-Request" in options
    assert "External-Audit-Store-Request" in options
    assert "Product-Release-Reaudit" in options
    assert fixture["recommended_next_lane"] == "V1-G14-Approval-Enforcement-Request"
    assert (
        fixture["recommended_next_lane_scope"]
        == "docs_tests_fixtures_only_operator_approval_request"
    )


def test_v1_g13_stop_conditions_cover_forbidden_surfaces() -> None:
    stops = set(_load_fixture()["stop_conditions"])

    assert "runtime_approval_enforcement" in stops
    assert "approval_token_issuance" in stops
    assert "provider_model_calls_or_routing" in stops
    assert "shell_runtime_wiring" in stops
    assert "humaninput_bridge_activation" in stops
    assert "connector_behavior" in stops
    assert "browser_file_network_device_robotics_physical_world_behavior" in stops
    assert "external_database_writes_migrations_queues_workers_daemons_subprocesses_threads" in stops
    assert "raw_sensitive_content_persistence" in stops
    assert "runtime_export_cleanup" in stops
    assert "final_api_freeze" in stops
    assert "v1_product_or_production_readiness_claim" in stops


def test_v1_g13_docs_match_fixture() -> None:
    fixture = _load_fixture()
    gate_text = (REPO_ROOT / fixture["documents"]["gate"]).read_text(encoding="utf-8")
    closeout_text = (REPO_ROOT / fixture["documents"]["closeout"]).read_text(
        encoding="utf-8"
    )
    state_text = (REPO_ROOT / fixture["documents"]["current_state"]).read_text(
        encoding="utf-8"
    )

    assert "Recommended next lane: `V1-G14-Approval-Enforcement-Request`" in gate_text
    assert "V1-G13 is complete as a docs/tests/fixtures-only readiness refresh" in gate_text
    assert "Create a separate V1-G14 approval request" in closeout_text
    assert "V1-G13 - Readiness Gap Refresh And Next-Lane Decision Gate" in state_text
