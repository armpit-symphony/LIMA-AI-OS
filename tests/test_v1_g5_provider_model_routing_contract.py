"""Static checks for the V1-G5 provider/model routing contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
SUMMARY_PATH = FIXTURE_DIR / "v1_g5_provider_model_routing_contract.json"
DOCS = {
    "contract": REPO_ROOT / "docs" / "V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md",
    "audit": REPO_ROOT / "docs" / "V1_G5_PROVIDER_MODEL_ROUTING_AUDIT.md",
    "closeout": REPO_ROOT / "docs" / "V1_G5_PROVIDER_MODEL_ROUTING_CLOSEOUT.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g5_summary_and_docs_exist_and_accept_static_contract_only() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert SUMMARY_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()
    assert summary["gap_id"] == "V1-G5"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["contract_completed"] is True
    assert summary["contract_accepted_as_static_evidence"] is True
    assert summary["contract_accepted_as_runtime_routing"] is False
    assert summary["v1_product_ready"] is False


def test_v1_g5_summary_tracks_expected_case_fixtures() -> None:
    summary = _load_json(SUMMARY_PATH)
    expected = {
        "tests/fixtures/runtime_extraction/v1_g5_safe_openai_route_shape.json",
        "tests/fixtures/runtime_extraction/v1_g5_private_data_requires_guardian_review.json",
        "tests/fixtures/runtime_extraction/v1_g5_expensive_model_requires_budget_review.json",
        "tests/fixtures/runtime_extraction/v1_g5_unknown_provider_denied.json",
        "tests/fixtures/runtime_extraction/v1_g5_missing_secret_ref_blocks_route.json",
        (
            "tests/fixtures/runtime_extraction/"
            "v1_g5_tool_capable_model_without_tool_scope_blocked.json"
        ),
        "tests/fixtures/runtime_extraction/v1_g5_shell_disallowed_provider_denied.json",
        "tests/fixtures/runtime_extraction/v1_g5_forged_route_decision_fail_closed.json",
    }
    assert set(summary["case_fixture_files"]) == expected
    for relative_path in expected:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g5_route_families_cover_sparkbot_reference_patterns() -> None:
    route_families = set(_load_json(SUMMARY_PATH)["route_families"])
    assert {
        "primary_model_route",
        "backup_fallback_route",
        "heavy_hitter_route",
        "agent_override_route",
        "workstation_model_seat_route",
        "local_endpoint_route",
        "codex_subscription_route",
        "provider_readiness_self_inspection_route",
    }.issubset(route_families)


def test_v1_g5_required_route_metadata_and_gates_are_defined() -> None:
    summary = _load_json(SUMMARY_PATH)
    metadata = set(summary["required_route_metadata"])
    assert {
        "route_id",
        "source_shell",
        "actor_id",
        "session_id",
        "intent_id",
        "decision_id",
        "provider_id",
        "model_id",
        "model_role",
        "route_family",
        "data_sensitivity",
        "prompt_context_class",
        "requested_tool_packs",
        "allowed_tool_packs",
        "secret_ref",
        "budget_class",
        "estimated_cost_class",
        "latency_tier",
        "fallback_chain",
        "audit_evidence_ref",
        "policy_version",
    }.issubset(metadata)
    gates = set(summary["required_routing_gates"])
    assert "shell_allows_model_pack" in gates
    assert "actor_session_policy_allows_model_use" in gates
    assert "guardian_decision_allows_model_routing" in gates
    assert "provider_model_configured_for_shell_room_or_agent" in gates
    assert "secret_ref_exists_or_provider_is_no_key_local" in gates
    assert "data_sensitivity_allowed_for_provider_class" in gates
    assert "budget_cost_policy_allows_model" in gates
    assert "requested_tool_packs_allowed_by_decision_and_shell_scope" in gates
    assert "fallback_candidates_satisfy_same_gates" in gates
    assert "audit_evidence_redacted_and_reference_only" in gates


def test_v1_g5_secret_and_fallback_constraints_are_fail_closed() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert summary["fallback_inheritance_required"] is True
    assert summary["raw_secrets_allowed_in_route_metadata"] is False
    assert summary["raw_private_context_allowed_in_audit"] is False


def test_v1_g5_summary_boundary_results_add_no_runtime_routing() -> None:
    summary = _load_json(SUMMARY_PATH)
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
        "shell_repos_changed",
        "sparkbot_shell_wiring_added",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "arc_bot_shell_wiring_added",
        "provider_model_routing_added",
        "provider_model_calls_added",
        "provider_readiness_checks_added",
        "token_guardian_live_routing_added",
        "secret_access_added",
        "guardian_decision_runtime_added",
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "haptic_device_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert summary[key] is False


def test_v1_g5_docs_state_static_only_verdict_and_next_gap() -> None:
    contract_text = DOCS["contract"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    assert "`V1-G5` is complete as a static provider/model routing contract" in contract_text
    assert "Fallback does not relax policy." in contract_text
    assert "Verdict: `accept_static_provider_model_routing_contract_only`." in audit_text
    assert "Recommended: `V1-G6`." in closeout_text
