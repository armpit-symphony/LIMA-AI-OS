"""Static checks for the V1-G33 consumer fake-runtime smoke request."""

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
    / "v1_g33_consumer_fake_runtime_import_call_smoke_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g33_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g33_consumer_fake_runtime_import_call_smoke_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g33-consumer-fake-runtime-import-call-smoke-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g33_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["consumer_fake_runtime_import_call_smoke_approved"] is False
    assert fixture["consumer_fake_runtime_import_call_smoke_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g33_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G33",
        "Revise-V1-G33",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G33 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g33-consumer-fake-runtime-import-call-smoke"
    )


def test_v1_g33_candidate_adapter_symbols_are_exact() -> None:
    fixture = _load_fixture()

    assert fixture["candidate_adapter_symbols_if_operator_says_yes"] == [
        "lima.adapters.validate_v1_consumer_integration_compatibility_freeze",
        "lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run",
    ]
    assert fixture["planned_adapter_symbols_called"] is False


def test_v1_g33_smoke_scope_is_metadata_only() -> None:
    scope = _load_fixture()["smoke_scope_if_operator_says_yes"]

    assert scope["metadata_only"] is True
    assert scope["fake_runtime_only"] is True
    assert scope["consumer_test_results_may_be_referenced"] is True
    assert scope["fake_call_shape_smoke_metadata_allowed"] is True
    assert scope["adapter_symbol_calls_allowed"] is False
    assert scope["fake_call_envelope_execution_allowed"] is False
    assert scope["consumer_repo_edits_allowed"] is False
    assert scope["consumer_runtime_source_file_edits_allowed"] is False
    assert scope["lima_runtime_file_edits_allowed"] is False
    assert scope["live_runtime_calls_allowed"] is False
    assert scope["no_network_required"] is True
    assert scope["no_secret_required"] is True
    assert scope["provider_model_calls_allowed"] is False
    assert scope["raw_patch_persistence_in_lima_evidence_allowed"] is False


def test_v1_g33_approved_lima_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_if_operator_says_yes"] == [
        "docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE.md",
        "docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g33_consumer_fake_runtime_import_call_smoke.json",
        "tests/test_v1_g33_consumer_fake_runtime_import_call_smoke.py",
    ]
    assert all(
        not path.startswith("lima/")
        for path in fixture["approved_lima_files_if_operator_says_yes"]
    )
    assert fixture["approved_consumer_files_if_operator_says_yes"] == []


def test_v1_g33_consumer_test_refs_are_existing_g32_files() -> None:
    fixture = _load_fixture()

    assert fixture["target_consumers"] == ["sparkbot", "arc_bot"]
    assert fixture["required_consumer_test_refs_if_operator_says_yes"] == {
        "sparkbot": [
            "tests/fixtures/sparkbot_lima_v1_g31_fake_runtime_consumer_call_preview.json",
            "tests/test_sparkbot_lima_v1_g31_fake_runtime_consumer_call_preview.py",
        ],
        "arc_bot": [
            "tests/fixtures/arc_bot_shell_lima_v1_g31_fake_runtime_consumer_call_preview.json",
            "tests/test_arc_bot_shell_lima_v1_g31_fake_runtime_consumer_call_preview.py",
        ],
    }
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False


def test_v1_g33_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g33_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_runtime_source_files_changed"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["live_consumer_import_calls_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture["fake_call_envelopes_executed"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["raw_diff_or_patch_persisted_in_lima_evidence"] is False
    assert fixture["raw_file_content_persisted_in_lima_evidence"] is False
    assert fixture["product_ready"] is False


def test_v1_g33_docs_contain_smoke_boundary_language() -> None:
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

    assert "consumer fake-runtime import/call smoke" in approval_text
    assert "must not call those symbols" in approval_text
    assert "No Sparkbot or Arc-Bot-shell files" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G33" in decision_text
    assert "Implementation must not start until `Approve-V1-G33`" in preflight_text
