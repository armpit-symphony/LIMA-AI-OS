"""Static checks for the V1-G35 compatibility review request."""

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
    / "v1_g35_consumer_integration_compatibility_review_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g35_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g35_consumer_integration_compatibility_review_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g35-consumer-integration-compatibility-review-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g35_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["consumer_integration_compatibility_review_approved"] is False
    assert fixture["consumer_integration_compatibility_review_added"] is False
    assert fixture["consumer_integration_approved"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g35_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G35",
        "Revise-V1-G35",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G35 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g35-consumer-integration-compatibility-review"
    )


def test_v1_g35_review_scope_is_metadata_only() -> None:
    scope = _load_fixture()["review_scope_if_operator_says_yes"]

    assert scope["metadata_review_only"] is True
    assert scope["lima_docs_tests_fixtures_only"] is True
    assert scope["consumer_repo_edits_allowed"] is False
    assert scope["adapter_symbol_calls_allowed"] is False
    assert scope["consumer_runtime_module_import_allowed"] is False
    assert scope["shell_runtime_wiring_allowed"] is False
    assert scope["provider_model_calls_allowed"] is False
    assert scope["secret_required"] is False
    assert scope["network_required"] is False
    assert scope["physical_world_behavior_allowed"] is False
    assert scope["product_readiness_claim_allowed"] is False


def test_v1_g35_approved_lima_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_if_operator_says_yes"] == [
        "docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW.md",
        "docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g35_consumer_integration_compatibility_review.json",
        "tests/test_v1_g35_consumer_integration_compatibility_review.py",
    ]
    assert all(
        not path.startswith("lima/")
        for path in fixture["approved_lima_files_if_operator_says_yes"]
    )
    assert fixture["approved_consumer_files_if_operator_says_yes"] == []


def test_v1_g35_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g35_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "lima_runtime_files_changed",
        "consumer_repo_mutation_added_by_request",
        "sparkbot_files_changed_by_request",
        "arc_bot_shell_files_changed_by_request",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "shell_runtime_wiring_added",
        "provider_model_calls_added",
        "model_request_dispatch_added",
        "fallback_execution_added",
        "secret_lookup_added",
        "credential_access_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_sensitive_content_persisted_in_lima_evidence",
        "product_ready",
    ):
        assert fixture[key] is False


def test_v1_g35_docs_contain_review_boundary_language() -> None:
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

    assert "consumer integration compatibility review" in approval_text
    assert "must not edit consumer repositories" in approval_text
    assert "Consumer integration approved: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G35" in decision_text
    assert "Implementation must not start until `Approve-V1-G35`" in preflight_text
