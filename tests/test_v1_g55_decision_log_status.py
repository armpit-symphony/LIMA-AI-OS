"""Static checks for the V1-G55 decision-log status refresh."""

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
    / "v1_g55_decision_log_status.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g55_decision_log_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["decision_log_status_id"] == "v1_g55_decision_log_status"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-g55-decision-log-status"
    assert fixture["source_commit_before_refresh"] == (
        "4bdd35ff6918d3c49464838d4db5f64b45621849"
    )
    assert fixture["decision_log_adr"] == "ADR-0338"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g55_decision_log_records_current_gate_without_approval() -> None:
    fixture = _load_fixture()

    assert fixture["current_gate"] == "V1-G55"
    assert fixture["latest_completed_gate"] == "V1-G54"
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G55",
        "Revise-V1-G55",
        "Pause",
    ]
    assert fixture["proposed_implementation_branch"] == (
        "v1-g55-real-provider-sdk-network-egress"
    )
    assert fixture["next_smallest_safe_step"] == (
        "record_one_valid_operator_choice_in_v1_g55_operator_decision_packet"
    )


def test_v1_g55_decision_log_only_allows_non_runtime_followup_work() -> None:
    assert set(_load_fixture()["can_continue_without_approval"]) == {
        "docs_tests_fixtures_review",
        "guard_docs",
        "audit_docs",
        "request_revision_work",
        "decision_recording_work",
    }


def test_v1_g55_decision_log_refresh_adds_no_forbidden_behavior() -> None:
    forbidden = _load_fixture()["forbidden_by_decision_log_refresh"]

    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "public_api_exports_changed",
        "sparkbot_touched",
        "public_sparkbot_touched",
        "sparkbot_shell_touched",
        "arc_bot_shell_touched",
        "consumer_repos_touched",
        "provider_sdk_network_egress_invocation_added",
        "caller_injected_provider_sdk_network_executor_invoked",
        "built_in_provider_sdk_client_added",
        "real_provider_sdk_client_added_by_lima",
        "sdk_dependency_added",
        "vendor_provider_sdk_import_added",
        "direct_provider_sdk_added",
        "provider_endpoint_resolution_added",
        "dns_lookup_added",
        "http_client_added",
        "socket_client_added",
        "network_call_performed_by_lima",
        "direct_provider_egress_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_behavior_added",
        "browser_file_network_device_robotics_physical_world_behavior_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "raw_provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "product_readiness_claim_added",
        "production_readiness_claim_added",
    ):
        assert forbidden[key] is False


def test_v1_g55_decision_log_text_matches_active_gate() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["decision_log"]).read_text(
        encoding="utf-8"
    )
    operator_packet = (
        REPO_ROOT / fixture["documents"]["operator_decision_packet"]
    ).read_text(encoding="utf-8")
    blocker_audit = (
        REPO_ROOT / fixture["documents"]["implementation_blocker_audit"]
    ).read_text(encoding="utf-8")

    assert "## ADR-0338: V1-G55 Is The Active Provider SDK Network Egress Decision Gate" in text
    assert "V1-G55 as the active operator decision gate" in text
    assert "implementation remains blocked pending explicit `Approve-V1-G55`" in text
    assert "`Approve-V1-G55`, `Revise-V1-G55`, or `Pause`" in text
    assert "Runtime implementation remains unapproved." in text
    assert "`v1-g55-real-provider-sdk-network-egress`" in text
    assert "No runtime behavior is added by this decision-log refresh." in text
    assert "No public API exports are changed by this decision-log refresh." in text
    assert "No Sparkbot, public Sparkbot, Sparkbot_shell, or Arc-Bot-shell files" in text
    assert "No provider SDK/network egress invocation" in text
    assert "product-readiness claim" in text
    assert "production-readiness claim" in text
    operator_packet_is_pre_approval = (
        "Recorded choice: `none`" in operator_packet
        and "Implementation approved: no" in operator_packet
    )
    operator_packet_is_approved = (
        "Recorded choice: `Approve-V1-G55`" in operator_packet
        and "Implementation approved: yes" in operator_packet
        and (
            "I explicitly approve V1-G55 implementation of the LIMA-side "
            "bounded real provider SDK/network egress authority slice"
        )
        in operator_packet
    )
    assert operator_packet_is_pre_approval or operator_packet_is_approved
    assert "Recorded choice: `none`" in blocker_audit
    assert (
        "V1-G55 runtime implementation is blocked pending an explicit "
        "operator decision."
    ) in blocker_audit
