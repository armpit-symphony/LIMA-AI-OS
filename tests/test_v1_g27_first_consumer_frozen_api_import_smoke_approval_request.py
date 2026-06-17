"""Static checks for the V1-G27 consumer frozen API import-smoke request."""

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
    / "v1_g27_first_consumer_frozen_api_import_smoke_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g27_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g27_first_consumer_frozen_api_import_smoke_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g27-first-consumer-frozen-api-import-smoke-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g27_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["consumer_frozen_api_import_smoke_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_runtime_source_mutation_added"] is False
    assert fixture["arc_bot_shell_runtime_source_mutation_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g27_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G27",
        "Revise-V1-G27",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G27 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g27-first-consumer-frozen-api-import-smoke"
    )


def test_v1_g27_approved_import_symbols_are_frozen_g22_surface() -> None:
    fixture = _load_fixture()

    assert fixture["approved_import_smoke_symbols_if_operator_says_yes"] == [
        "lima.adapters.validate_v1_consumer_integration_compatibility_freeze",
        "lima.adapters.V1ConsumerIntegrationCompatibilityError",
    ]


def test_v1_g27_approved_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert set(fixture["approved_lima_files_if_operator_says_yes"]) == {
        "docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE.md",
        "docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g27_first_consumer_frozen_api_import_smoke.json",
        "tests/test_v1_g27_first_consumer_frozen_api_import_smoke.py",
    }
    assert set(fixture["approved_sparkbot_files_if_operator_says_yes"]) == {
        "tests/fixtures/sparkbot_lima_v1_g27_frozen_api_import_smoke.json",
        "tests/test_sparkbot_lima_v1_g27_frozen_api_import_smoke.py",
    }
    assert set(fixture["approved_arc_bot_shell_files_if_operator_says_yes"]) == {
        "tests/fixtures/arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.json",
        "tests/test_arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.py",
    }
    assert all(
        not path.startswith("lima/")
        for path in fixture["approved_lima_files_if_operator_says_yes"]
    )


def test_v1_g27_import_smoke_scope_is_test_only() -> None:
    scope = _load_fixture()["import_smoke_scope_if_approved"]

    assert scope["test_only_import_allowed"] is True
    assert scope["call_imported_symbols_allowed"] is False
    assert scope["consumer_runtime_calls_allowed"] is False
    assert scope["runtime_source_files_allowed"] is False
    assert scope["live_provider_model_calls_allowed"] is False


def test_v1_g27_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["target_consumers"] == ["sparkbot", "arc_bot"]
    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g27_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["raw_diff_or_patch_persisted"] is False
    assert fixture["raw_file_content_persisted"] is False
    assert fixture["product_ready"] is False


def test_v1_g27_docs_contain_import_smoke_boundary_language() -> None:
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

    assert "Approved import-smoke surface" in approval_text
    assert "calls to `validate_v1_consumer_integration_compatibility_freeze`" in approval_text
    assert "No Sparkbot or Arc-Bot-shell runtime/source files" in approval_text
    assert "Do not add runtime calls" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G27" in decision_text
    assert "Implementation must not start until `Approve-V1-G27`" in preflight_text
