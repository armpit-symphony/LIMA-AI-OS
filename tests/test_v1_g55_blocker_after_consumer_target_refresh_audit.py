"""Static checks for the V1-G55 blocker refresh after consumer target state."""

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
    / "v1_g55_blocker_after_consumer_target_refresh_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g55_blocker_refresh_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g55_blocker_after_consumer_target_refresh_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["audit_branch"] == "audit-v1-g55-blocker-after-consumer-target-refresh"
    assert fixture["source_commit_before_audit"] == (
        "26896c4b866dd54e51e22572b6cd70bd41818ec0"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g55_blocker_refresh_preserves_missing_operator_decision() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["audit_verdict"] == "BLOCKED_PENDING_OPERATOR_DECISION"
    assert fixture["blocker"] == "missing_valid_approve_v1_g55_decision_record"
    assert fixture["required_unblock_choice"] == "Approve-V1-G55"
    assert fixture["required_approved_branch"] == (
        "v1-g55-real-provider-sdk-network-egress"
    )
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G55",
        "Revise-V1-G55",
        "Pause",
    ]
    assert decision == {
        "recorded_choice": "none",
        "recorded_approval_wording": "none",
        "recorded_revision_request": "none",
        "recorded_pause_reason": "none",
        "approved_implementation_branch": "none",
        "implementation_approved": False,
    }


def test_v1_g55_blocker_refresh_rejects_latest_non_approval_inputs() -> None:
    not_approval = set(_load_fixture()["inputs_that_are_not_approval"])

    assert "persistent_broad_goal" in not_approval
    assert "v1_consumer_target_state_after_arc_readiness_integration" in not_approval
    assert "arc_runtime_gating_readiness_integration_audit" in not_approval
    assert "public_sparkbot_local_preview_branch" in not_approval
    assert "public_sparkbot_github_403_publication_blocker" in not_approval
    assert "v1_g54_audit" in not_approval
    assert "v1_runtime_authority_chain_through_g54_audit" in not_approval
    assert "v1_g55_approval_request" in not_approval
    assert "v1_g55_implementation_blocker_audit" in not_approval
    assert "successful_validation_runs" in not_approval
    assert "clean_consumer_repository_status" in not_approval


def test_v1_g55_blocker_refresh_only_docs_work_can_continue() -> None:
    fixture = _load_fixture()
    can_continue = set(fixture["can_continue_without_approval"])
    cannot_continue = set(fixture["cannot_continue_without_approval"])

    assert can_continue == {
        "docs_tests_fixtures_review",
        "guard_docs",
        "audit_docs",
        "request_revision_work",
        "decision_recording_work",
    }
    for blocked in (
        "v1_g55_runtime_implementation",
        "lima_runtime_file_changes_for_v1_g55",
        "public_api_export_changes_for_v1_g55",
        "bounded_real_provider_sdk_network_egress_wrapper",
        "provider_sdk_network_egress_invocation",
        "built_in_provider_sdk_clients",
        "sdk_dependencies",
        "vendor_sdk_imports",
        "endpoint_resolution_by_lima",
        "dns_http_socket_network_calls_by_lima",
        "direct_provider_egress_by_lima",
        "secret_lookup_or_credential_value_access",
        "provider_token_or_api_key_access",
        "provider_configuration_changes",
        "fallback_execution",
        "consumer_production_runtime_integration",
        "sparkbot_sparkbot_shell_public_sparkbot_or_arc_bot_shell_file_changes_for_g55",
        "connector_browser_network_file_device_robotics_physical_world_behavior",
        "product_readiness",
        "production_readiness",
    ):
        assert blocked in cannot_continue


def test_v1_g55_blocker_refresh_records_public_sparkbot_permission_blocker() -> None:
    blocker = _load_fixture()["public_sparkbot_publication_blocker"]

    assert blocker == {
        "blocked": True,
        "reason": "github_403_permission_denied_to_armpit_symphony",
        "is_g55_implementation_approval": False,
        "is_lima_runtime_blocker": False,
    }


def test_v1_g55_blocker_refresh_boundaries_are_false() -> None:
    for key, value in _load_fixture()["boundaries"].items():
        assert value is False, key


def test_v1_g55_blocker_refresh_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["blocker_refresh_audit"]).read_text(
        encoding="utf-8"
    )
    state_text = (
        REPO_ROOT / fixture["documents"]["current_project_state"]
    ).read_text(encoding="utf-8")

    assert "# V1-G55 Blocker After Consumer Target Refresh Audit" in text
    assert "`audit-v1-g55-blocker-after-consumer-target-refresh`" in text
    assert "26896c4b866dd54e51e22572b6cd70bd41818ec0" in text
    assert "V1-G55 runtime implementation remains blocked" in text
    assert "The V1 consumer target state refresh is accepted" in text
    assert "Public Sparkbot publication remains blocked by a GitHub 403" in text
    assert "not a G55 implementation approval" in text
    assert "V1-G55 runtime implementation." in text
    assert "Product readiness claimed: no." in text
    assert "Record exactly one valid operator choice" in text
    assert "V1-G55 blocker after consumer target refresh audit: complete." in state_text
