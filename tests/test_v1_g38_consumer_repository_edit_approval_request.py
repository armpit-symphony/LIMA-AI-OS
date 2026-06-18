"""Static checks for the V1-G38 consumer repository edit request."""

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
    / "v1_g38_consumer_repository_edit_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g38_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g38_consumer_repository_edit_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-g38-consumer-repository-edit-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g38_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["consumer_repository_edit_approved"] is False
    assert fixture["consumer_repository_edit_added"] is False
    assert fixture["consumer_integration_approved"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g38_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G38",
        "Revise-V1-G38",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G38 implementation"
    )
    assert fixture["proposed_implementation_branch"] == "v1-g38-consumer-repository-edit"


def test_v1_g38_edit_scope_is_exact_and_limited() -> None:
    scope = _load_fixture()["edit_scope_if_operator_says_yes"]

    assert scope["lima_docs_tests_fixtures_only"] is True
    assert scope["exact_consumer_test_fixture_edits_allowed"] is True
    assert scope["consumer_repo_edits_limited_to_exact_paths"] is True
    assert scope["consumer_runtime_source_edits_allowed"] is False
    assert scope["raw_patch_body_persistence_allowed"] is False
    assert scope["adapter_symbol_calls_allowed"] is False
    assert scope["consumer_runtime_module_import_allowed"] is False
    assert scope["consumer_integration_implementation_allowed"] is False
    assert scope["shell_runtime_wiring_implementation_allowed"] is False
    assert scope["provider_model_calls_allowed"] is False
    assert scope["secret_required"] is False
    assert scope["network_required"] is False
    assert scope["physical_world_behavior_allowed"] is False
    assert scope["product_readiness_claim_allowed"] is False


def test_v1_g38_approved_lima_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_if_operator_says_yes"] == [
        "docs/V1_G38_CONSUMER_REPOSITORY_EDIT.md",
        "docs/V1_G38_CONSUMER_REPOSITORY_EDIT_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g38_consumer_repository_edit.json",
        "tests/test_v1_g38_consumer_repository_edit.py",
    ]
    assert all(
        not path.startswith("lima/")
        for path in fixture["approved_lima_files_if_operator_says_yes"]
    )


def test_v1_g38_approved_consumer_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_consumer_files_if_operator_says_yes"] == {
        "sparkbot": [
            "tests/fixtures/sparkbot_lima_v1_g38_consumer_integration_candidate.json",
            "tests/test_sparkbot_lima_v1_g38_consumer_integration_candidate.py",
        ],
        "arc_bot": [
            "tests/fixtures/arc_bot_shell_lima_v1_g38_consumer_integration_candidate.json",
            "tests/test_arc_bot_shell_lima_v1_g38_consumer_integration_candidate.py",
        ],
    }


def test_v1_g38_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g38_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "lima_runtime_files_changed",
        "consumer_repo_mutation_added_by_request",
        "sparkbot_files_changed_by_request",
        "arc_bot_shell_files_changed_by_request",
        "consumer_runtime_source_files_changed_by_request",
        "raw_patch_bodies_persisted",
        "patches_applied",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "consumer_integration_added",
        "shell_runtime_wiring_implementation_added",
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


def test_v1_g38_docs_contain_edit_boundary_language() -> None:
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

    assert "consumer repository edit" in approval_text
    assert "No `lima/` runtime files" in approval_text
    assert "Consumer repository edit approved: no" in approval_text
    assert "Consumer integration approved: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G38" in decision_text
    assert "Implementation must not start until `Approve-V1-G38`" in preflight_text
