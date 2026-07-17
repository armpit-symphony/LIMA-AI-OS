"""Static checks for the V1-G43 provider/model dispatch request."""

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
    / "v1_g43_provider_model_dispatch_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g43_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g43_provider_model_dispatch_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-g43-provider-model-dispatch-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g43_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["provider_model_dispatch_approved"] is False
    assert fixture["provider_model_dispatch_added"] is False
    assert fixture["fake_provider_dispatch_evidence_added"] is False
    assert fixture["live_provider_model_calls_approved"] is False
    assert fixture["live_provider_model_calls_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g43_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G43",
        "Revise-V1-G43",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G43 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g43-provider-model-dispatch"
    )


def test_v1_g43_edit_scope_is_lima_only_and_no_secret_no_network() -> None:
    scope = _load_fixture()["edit_scope_if_operator_says_yes"]

    assert scope["lima_docs_tests_fixtures_only"] is True
    assert scope["approved_consumer_files_empty"] is True
    assert scope["provider_model_dispatch_evidence_allowed"] is True
    assert scope["deterministic_fake_provider_evidence_allowed"] is True
    assert scope["no_secret_no_network_evidence_allowed"] is True
    assert scope["live_provider_model_calls_allowed"] is False
    assert scope["actual_model_request_dispatch_execution_allowed"] is False
    assert scope["fallback_execution_allowed"] is False
    assert scope["provider_readiness_network_check_allowed"] is False
    assert scope["token_guardian_live_routing_allowed"] is False
    assert scope["secret_lookup_allowed"] is False
    assert scope["credential_access_allowed"] is False
    assert scope["tool_execution_allowed"] is False
    assert scope["consumer_repo_edits_allowed"] is False
    assert scope["consumer_runtime_source_edits_allowed"] is False
    assert scope["runtime_shell_wiring_execution_allowed"] is False
    assert scope["raw_prompt_or_model_response_persistence_allowed"] is False
    assert scope["raw_secret_or_credential_persistence_allowed"] is False
    assert scope["connector_browser_network_behavior_allowed"] is False
    assert scope["physical_world_behavior_allowed"] is False
    assert scope["product_readiness_claim_allowed"] is False


def test_v1_g43_approved_lima_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_if_operator_says_yes"] == [
        "docs/V1_G43_PROVIDER_MODEL_DISPATCH.md",
        "docs/V1_G43_PROVIDER_MODEL_DISPATCH_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g43_provider_model_dispatch.json",
        "tests/test_v1_g43_provider_model_dispatch.py",
    ]
    assert all(
        not path.startswith("lima/")
        for path in fixture["approved_lima_files_if_operator_says_yes"]
    )


def test_v1_g43_has_no_consumer_file_scope() -> None:
    fixture = _load_fixture()

    assert fixture["target_consumers"] == []
    assert fixture["approved_consumer_files_if_operator_says_yes"] == {}


def test_v1_g43_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g43_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "lima_runtime_files_changed",
        "consumer_repo_mutation_added_by_request",
        "sparkbot_files_changed_by_request",
        "arc_bot_shell_files_changed_by_request",
        "consumer_runtime_source_files_changed_by_request",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "raw_patch_bodies_persisted",
        "patches_applied",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "runtime_shell_wiring_execution_added",
        "model_request_dispatch_added",
        "fallback_execution_added",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "secret_lookup_added",
        "credential_access_added",
        "tool_execution_added",
        "file_mutation_execution_added",
        "external_sends_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_sensitive_content_persisted_in_lima_evidence",
        "product_ready",
    ):
        assert fixture[key] is False


def test_v1_g43_docs_contain_provider_dispatch_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )
    preflight_text = (REPO_ROOT / fixture["documents"]["preflight_audit"]).read_text(
        encoding="utf-8"
    )

    assert "provider/model dispatch" in approval_text
    assert "fake-provider/no-secret" in approval_text
    assert "No `lima/` runtime files" in approval_text
    assert "No Sparkbot or Arc-Bot-shell files" in approval_text
    assert "Live provider/model calls approved: no" in approval_text
    assert "Actual model request dispatch execution approved: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G43" in decision_text
    assert "Implementation must not start until `Approve-V1-G43`" in preflight_text
