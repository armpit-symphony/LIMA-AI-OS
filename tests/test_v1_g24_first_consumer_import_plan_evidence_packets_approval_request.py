"""Static checks for the V1-G24 first consumer import-plan packet request."""

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
    / "v1_g24_first_consumer_import_plan_evidence_packets_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g24_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g24_first_consumer_import_plan_evidence_packets_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g24-first-consumer-import-plan-evidence-packets-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g24_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["first_consumer_import_plan_evidence_packets_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_repo_mutation_added"] is False
    assert fixture["arc_bot_shell_repo_mutation_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g24_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G24",
        "Revise-V1-G24",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G24 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g24-first-consumer-import-plan-evidence-packets"
    )


def test_v1_g24_target_consumers_are_locked() -> None:
    assert _load_fixture()["target_consumers"] == ["sparkbot", "arc_bot"]


def test_v1_g24_approved_file_scope_is_docs_tests_fixtures_only() -> None:
    approved_files = set(_load_fixture()["approved_files_if_operator_says_yes"])

    assert approved_files == {
        "docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS.md",
        "docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g24_first_consumer_import_plan_evidence_packets.json",
        "tests/test_v1_g24_first_consumer_import_plan_evidence_packets.py",
    }
    assert all(not path.startswith("lima/") for path in approved_files)


def test_v1_g24_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_repo_mutation_added"] is False
    assert fixture["arc_bot_shell_repo_mutation_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["product_ready"] is False


def test_v1_g24_docs_contain_consumer_packet_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "Sparkbot" in approval_text
    assert "Arc-Bot-shell" in approval_text
    assert "consumer repo edits" in approval_text
    assert "live import/call" in approval_text
    assert "Do not edit consumer repos" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G24" in decision_text
