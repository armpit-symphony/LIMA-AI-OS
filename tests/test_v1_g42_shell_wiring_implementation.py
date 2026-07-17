"""Tests for the approved V1-G42 shell wiring implementation slice."""

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
    / "v1_g42_shell_wiring_implementation.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["shell_wiring_records"]
    assert isinstance(records, list)
    return records


def test_v1_g42_fixture_records_approved_scope_and_candidate_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g42_shell_wiring_implementation"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g42-shell-wiring-implementation"
    assert fixture["operator_decision"] == "Approve-V1-G42"
    assert fixture["approved_scope"] == "shell_wiring_implementation_slice"
    assert fixture["shell_wiring_implementation_approved"] is True
    assert fixture["shell_wiring_implementation_added"] is True
    assert fixture["static_shell_wiring_implementation_evidence_added"] is True
    assert fixture["bounded_shell_wiring_implementation_evidence_only"] is True
    assert fixture["runtime_shell_wiring_execution_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g42_lima_file_scope_is_exact_and_runtime_free() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G42_SHELL_WIRING_IMPLEMENTATION.md",
        "docs/V1_G42_SHELL_WIRING_IMPLEMENTATION_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g42_shell_wiring_implementation.json",
        "tests/test_v1_g42_shell_wiring_implementation.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_docs_tests_fixtures_only"] is True


def test_v1_g42_consumer_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_consumer_files_changed"] == {
        "sparkbot": [
            "tests/fixtures/sparkbot_lima_v1_g42_shell_wiring_implementation.json",
            "tests/test_sparkbot_lima_v1_g42_shell_wiring_implementation.py",
        ],
        "arc_bot": [
            "tests/fixtures/arc_bot_shell_lima_v1_g42_shell_wiring_implementation.json",
            "tests/test_arc_bot_shell_lima_v1_g42_shell_wiring_implementation.py",
        ],
    }
    assert fixture["sparkbot_files_changed"] is True
    assert fixture["arc_bot_shell_files_changed"] is True
    assert fixture["sparkbot_files_limited_to_approved_paths"] is True
    assert fixture["arc_bot_shell_files_limited_to_approved_paths"] is True
    assert fixture["consumer_runtime_source_files_changed"] is False

    for record in _records():
        expected = fixture["approved_consumer_files_changed"][record["consumer_packet_family"]]
        assert record["approved_consumer_files_changed"] == expected
        assert record["consumer_runtime_source_files_changed"] is False


def test_v1_g42_contains_exactly_two_shell_wiring_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g42_records_saved_consumer_commits_and_source_refs() -> None:
    expected = {
        "sparkbot": (
            "sparkpit-labs/Sparkbot",
            "25c1e288b3d6b8c94d4bfe1c91113d078480f96e",
            "consumer-integration-implementation:v1-g41:sparkbot:001",
            "shell-wiring-design:v1-g40:sparkbot:001",
            "shell-boundary-map:v1-g40:sparkbot",
        ),
        "arc_bot": (
            "armpit-symphony/Arc-Bot-shell",
            "e76c33e32676386ae35a4b12f934684ad1969038",
            "consumer-integration-implementation:v1-g41:arc-bot-shell:001",
            "shell-wiring-design:v1-g40:arc-bot-shell:001",
            "shell-boundary-map:v1-g40:arc-bot-shell",
        ),
    }

    for record in _records():
        repository, commit_sha, g41_ref, shell_ref, map_ref = expected[
            record["consumer_packet_family"]
        ]

        assert record["shell_wiring_record_id"].startswith(
            "shell-wiring-implementation:v1-g42:"
        )
        assert record["consumer_repository"] == repository
        assert record["consumer_branch"] == "v1-g42-shell-wiring-implementation"
        assert record["consumer_commit_sha"] == commit_sha
        assert len(record["consumer_commit_sha"]) == 40
        assert record["source_consumer_integration_implementation_record_ref"] == g41_ref
        assert record["source_shell_boundary_record_ref"] == shell_ref
        assert record["source_boundary_map_ref"] == map_ref


def test_v1_g42_implementation_result_and_remaining_gaps_are_locked() -> None:
    expected_gaps = [
        "runtime_shell_wiring_execution_not_approved",
        "provider_model_dispatch_not_approved",
        "secret_credential_access_not_approved",
        "connector_browser_network_authority_not_approved",
        "physical_world_authority_not_approved",
        "product_readiness_not_approved",
    ]

    assert _load_fixture()["remaining_gaps"] == expected_gaps
    for record in _records():
        assert record["shell_wiring_implementation_result"] == (
            "static_shell_wiring_implementation_evidence_created"
        )
        assert record["shell_wiring_implementation_approved"] is True
        assert record["shell_wiring_implementation_added"] is True
        assert record["static_wiring_fixture_added"] is True
        assert record["static_wiring_test_added"] is True
        assert record["bounded_shell_wiring_implementation_evidence_only"] is True
        assert record["static_g41_implementation_fixture_reference_validated"] is True
        assert record["static_shell_boundary_reference_validated"] is True
        assert record["docs_tests_fixtures_only"] is True
        assert record["remaining_gaps"] == expected_gaps
        assert record["runtime_shell_wiring_execution_added"] is False
        assert record["proof_not_live_dispatch_authority"] is True
        assert record["proof_not_product_readiness"] is True
        assert record["product_ready"] is False


def test_v1_g42_future_gates_remain_blocked() -> None:
    expected_gates = [
        "provider_model_dispatch_approval_request",
        "connector_browser_network_authority_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    expected_blocked_authorities = {
        "provider_model_dispatch_approved": False,
        "connector_browser_network_authority_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == expected_gates
    assert fixture["blocked_future_authorities"] == expected_blocked_authorities

    for record in _records():
        assert record["future_required_gates"] == expected_gates
        assert record["blocked_future_authorities"] == expected_blocked_authorities


def test_v1_g42_links_required_prior_evidence_documents() -> None:
    fixture = _load_fixture()

    assert fixture["reviewed_evidence_refs"] == [
        "docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION.md",
        "docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION_CLOSEOUT.md",
        "docs/audits/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION_AUDIT.md",
        "docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G41_AUDIT.md",
        "docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G41.md",
        "docs/readiness/V1_POST_G41_NEXT_LANE_DECISION_MATRIX.md",
    ]

    for relative_path in fixture["reviewed_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g42_runtime_patch_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    forbidden_keys = (
        "lima_runtime_files_changed",
        "consumer_runtime_source_files_changed",
        "raw_patch_bodies_persisted",
        "raw_patch_bodies_persisted_in_lima_evidence",
        "unapproved_patches_applied",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "lima_runtime_modules_imported_by_consumer_tests",
        "runtime_shell_wiring_execution_added",
        "provider_model_calls_added",
        "model_request_dispatch_added",
        "fallback_execution_added",
        "secret_lookup_added",
        "credential_access_added",
        "tool_execution_outside_local_tests_added",
        "action_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "human_input_bridge_activated",
        "scheduled_task_execution_added",
        "external_sends_added",
        "external_database_writes_added",
        "raw_sensitive_content_persisted_in_lima_evidence",
    )

    for key in forbidden_keys:
        assert fixture[key] is False

    for record in _records():
        for key in forbidden_keys:
            if key in record:
                assert record[key] is False
        assert record["product_ready"] is False


def test_v1_g42_rollback_metadata_is_exact_and_reversible() -> None:
    fixture = _load_fixture()
    expected_lima_files = fixture["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"].startswith("rollback:v1-g42:")
        assert rollback["rollback_lima_file_refs"] == expected_lima_files
        assert rollback["rollback_consumer_file_refs"] == record[
            "approved_consumer_files_changed"
        ]
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["consumer_runtime_source_repair_required"] is False
        assert rollback["shell_runtime_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g42_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["shell_wiring_implementation_approval_recorded_confirmation"] is True
        assert confirmations["no_lima_runtime_file_change_confirmation"] is True
        assert confirmations["approved_consumer_files_only_confirmation"] is True
        assert (
            confirmations[
                "g41_consumer_integration_implementation_reference_only_confirmation"
            ]
            is True
        )
        assert confirmations["g40_shell_boundary_reference_only_confirmation"] is True
        assert confirmations["no_consumer_runtime_source_change_confirmation"] is True
        assert confirmations["no_raw_patch_body_persistence_confirmation"] is True
        assert confirmations["no_unapproved_patch_application_confirmation"] is True
        assert confirmations["no_adapter_symbol_call_confirmation"] is True
        assert confirmations["no_consumer_runtime_module_import_confirmation"] is True
        assert confirmations["no_lima_runtime_module_import_confirmation"] is True
        assert confirmations["no_runtime_shell_wiring_execution_confirmation"] is True
        assert (
            confirmations[
                "no_provider_model_secret_credential_connector_browser_network_physical_world_confirmation"
            ]
            is True
        )
        assert (
            confirmations["no_raw_sensitive_content_in_lima_evidence_confirmation"]
            is True
        )
        assert confirmations["proof_not_live_dispatch_authority_confirmation"] is True
        assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g42_output_does_not_include_patch_bodies_imports_or_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw customer data value",
        "provider token value",
        "api key value",
        "raw-secret-123",
        "def test_",
        "import lima",
        "from lima",
    ):
        assert forbidden not in output


def test_v1_g42_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G42_SHELL_WIRING_IMPLEMENTATION.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G42_SHELL_WIRING_IMPLEMENTATION_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "approved bounded shell wiring implementation evidence slice" in implementation_text
    assert "No `lima/` runtime file" in implementation_text
    assert "does not approve that request or implementation" in implementation_text
    assert "proof-not-live-dispatch-authority" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
    assert "V1-G42 is complete" in closeout_text
