"""Static checks for the LIMA-AI-OS V1 product readiness target."""

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
    / "v1_product_readiness_target.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_target_documents_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["target_version"] == "1.0"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-product-readiness-through-g55"
    assert fixture["source_commit_before_refresh"] == (
        "ddd93607504fa9b432948e819e65b68dfefc9a9f"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_first_shell_consumers_and_sparkbot_reference_are_explicit() -> None:
    fixture = _load_fixture()
    assert set(fixture["first_shell_consumers"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }

    reference = fixture["shell_behavior_reference"]
    assert reference["reference_repo"] == "Sparkbot"
    assert reference["reference_role"] == "r_and_d_shell_behavior_source"
    assert reference["copy_sparkbot_code"] is False
    assert reference["import_sparkbot_runtime"] is False
    assert reference["wire_sparkbot_routes"] is False
    assert reference["mutate_consumer_repo_for_g55"] is False


def test_v1_accepts_future_capabilities_without_approving_them_here() -> None:
    fixture = _load_fixture()
    accepted = set(fixture["accepted_future_v1_runtime_capabilities"])

    assert "live_actual_approval_flow" in accepted
    assert "real_guardian_decision_runtime_path" in accepted
    assert "provider_model_routing" in accepted
    assert "shell_haptic_intent_support" in accepted
    assert "first_shell_response_state_parity" in accepted
    assert "bounded_real_provider_sdk_network_egress_authority" in accepted
    assert fixture["product_direction_only"] is True
    assert fixture["runtime_implementation_approved_by_this_fixture"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_destructive_edits_and_deletes_require_operator_approval() -> None:
    policy = _load_fixture()["operator_approval_policy"]

    assert policy["delete_requires_operator_approval"] is True
    assert policy["edit_requires_operator_approval"] is True
    assert policy["overwrite_requires_operator_approval"] is True
    assert policy["destructive_admin_or_connector_action_requires_operator_approval"] is True
    assert policy["applies_to_lima_ai_os"] is True
    assert policy["applies_to_shells"] is True


def test_v1_haptics_remain_shell_owned() -> None:
    haptics = _load_fixture()["haptics_ownership"]

    assert haptics["haptics_acceptable_as_v1_shell_experience_requirement"] is True
    assert haptics["shells_own_haptic_rendering"] is True
    assert haptics["lima_owns_haptic_device_implementation"] is False
    assert haptics["lima_may_define_future_haptic_intent_metadata"] is True
    assert haptics["haptic_implementation_added_here"] is False


def test_v1_current_status_tracks_g55_gate() -> None:
    current = _load_fixture()["current_status"]

    assert current["latest_completed_gate"] == "V1-G54"
    assert current["latest_authority_chain_audit"] == "V1-G54"
    assert current["latest_readiness_rollup"] == "V1-G54"
    assert current["current_gate"] == "V1-G55"
    assert current["v1_g55_approval_request_ready"] is True
    assert current["v1_g55_work_order_ready"] is True
    assert current["v1_g55_preflight_audit_ready"] is True
    assert current["v1_g55_operator_decision_packet_ready"] is True
    assert current["v1_g55_implementation_blocker_audit_active"] is True
    assert current["v1_g55_operator_decision_recorded_choice"] is None
    assert current["v1_g55_operator_approval_recorded"] is False
    assert current["v1_g55_runtime_implementation_approved"] is False
    assert current["v1_g55_wrapper_added"] is False
    assert current["v1_g55_public_api_exports_changed"] is False


def test_v1_current_status_adds_no_runtime_sdk_network_or_secret_behavior() -> None:
    current = _load_fixture()["current_status"]

    for key in (
        "runtime_behavior_added_by_refresh",
        "lima_runtime_files_changed_by_refresh",
        "tests_support_changed",
        "shell_repos_changed_by_refresh",
        "provider_sdk_network_egress_invocation_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_sdk_import_added",
        "provider_endpoint_resolution_by_lima_added",
        "network_call_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
    ):
        assert current[key] is False


def test_v1_remaining_blockers_and_next_step_are_g55() -> None:
    fixture = _load_fixture()
    blockers = set(fixture["remaining_blockers"])

    assert "approve_v1_g55_not_recorded" in blockers
    assert "bounded_real_provider_sdk_network_egress_wrapper_not_implemented" in blockers
    assert "provider_secrets_and_credential_values_inaccessible_to_lima" in blockers
    assert "consumer_production_runtime_integration_unapproved" in blockers
    assert "release_boundary_not_passed" in blockers
    assert "v1_product_readiness_not_approved" in blockers
    assert "production_behavior_not_approved" in blockers
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G55",
        "Revise-V1-G55",
        "Pause",
    ]
    assert (
        fixture["recommended_next_step"]
        == "record_one_valid_operator_choice_in_v1_g55_decision_record"
    )
    assert fixture["recommended_next_gap_id"] == "V1-G55"
    assert (
        fixture["recommended_next_gap_to_close"]
        == "bounded_real_provider_sdk_network_egress_authority_wrapper"
    )


def test_v1_product_readiness_doc_matches_g55_gate() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["target"]).read_text(encoding="utf-8")

    assert "LIMA remains `CANDIDATE_ONLY`." in text
    assert "first shell consumers" in text
    assert "public `Sparkbot`" in text
    assert "audited through `V1-G54`" in text
    assert "`V1-G55` is an approval request" in text
    assert "Runtime implementation may start only after the exact `Approve-V1-G55` state" in text
    assert "Current status remains not V1 product-ready." in text
    assert "provider SDK/network egress invocation" in text
    assert "built-in provider SDK clients" in text
    assert "secret lookup, credential value access" in text
    assert "Sparkbot or Arc-Bot-shell edits for G55" in text
    assert "V1 product readiness or production readiness claims" in text
