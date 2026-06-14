"""Static checks for the V1-G11 operator decision packet."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g11_operator_decision_packet.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_operator_decision_packet_records_exact_approval() -> None:
    fixture = _load_fixture()
    assert DOC_PATH.exists()
    assert fixture["gap_id"] == "V1-G11"
    assert fixture["packet_type"] == "operator_decision_packet"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert (
        fixture["source_commit_before_packet"]
        == "d8e0d3bfce77535a0e9cb20e465a015b896e2db1"
    )
    assert (
        fixture["decision_packet_status"]
        == "approve_v1_g11_recorded"
    )
    assert fixture["decision_record_slot_added"] is True
    assert fixture["operator_approval_recorded"] is True
    assert fixture["runtime_implementation_approved"] is True
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_g11_operator_decision_packet_has_approve_decision_record() -> None:
    fixture = _load_fixture()
    decision_record = fixture["decision_record"]
    assert decision_record["recorded_choice"] == "Approve-V1-G11"
    assert decision_record["recorded_approval_wording"] == fixture["required_approval_wording"]
    assert decision_record["recorded_revision_request"] is None
    assert decision_record["recorded_pause_reason"] is None
    assert decision_record["approved_implementation_branch"] == fixture["if_approved_next_branch"]
    assert decision_record["runtime_implementation_approved"] is True


def test_v1_g11_operator_decision_packet_keeps_all_runtime_boundaries_false() -> None:
    fixture = _load_fixture()
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_import_added",
        "sparkbot_shell_import_added",
        "arc_bot_shell_import_added",
        "sparkbot_code_copied",
        "provider_model_routing_added",
        "shell_wiring_added",
        "persistence_added",
        "haptic_device_behavior_added",
        "browser_file_network_device_robotics_physical_world_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False


def test_v1_g11_operator_decision_packet_names_only_valid_choices() -> None:
    fixture = _load_fixture()
    assert set(fixture["valid_operator_choices"]) == {
        "Approve-V1-G11",
        "Revise-V1-G11",
        "Pause",
    }
    assert "I explicitly approve V1-G11 implementation" in fixture["required_approval_wording"]
    assert (
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md"
        in fixture["required_approval_wording"]
    )
    assert fixture["if_approved_next_branch"] == "v1-g11-runtime-request-decision-gate"
    assert (
        fixture["if_approved_scope"]
        == "typed_request_guardian_decision_preflight_runtime_slice"
    )


def test_v1_g11_operator_decision_record_validation_rules_are_fail_closed() -> None:
    fixture = _load_fixture()
    rules = fixture["decision_record_validation_rules"]
    assert set(rules) == {"none", "Approve-V1-G11", "Revise-V1-G11", "Pause"}

    none_rule = rules["none"]
    assert none_rule["recorded_choice"] is None
    assert none_rule["recorded_approval_wording_required"] is False
    assert none_rule["recorded_revision_request_required"] is False
    assert none_rule["recorded_pause_reason_required"] is False
    assert none_rule["approved_implementation_branch_required"] is False
    assert none_rule["runtime_implementation_approved"] is False

    approve_rule = rules["Approve-V1-G11"]
    assert approve_rule["recorded_choice"] == "Approve-V1-G11"
    assert approve_rule["recorded_approval_wording_required"] is True
    assert approve_rule["recorded_approval_wording_must_equal_required_wording"] is True
    assert approve_rule["approved_implementation_branch_required"] is True
    assert approve_rule["approved_implementation_branch_must_equal_if_approved_next_branch"] is True
    assert approve_rule["recorded_revision_request_required"] is False
    assert approve_rule["recorded_pause_reason_required"] is False
    assert approve_rule["runtime_implementation_approved"] is True

    revise_rule = rules["Revise-V1-G11"]
    assert revise_rule["recorded_choice"] == "Revise-V1-G11"
    assert revise_rule["recorded_revision_request_required"] is True
    assert revise_rule["recorded_approval_wording_required"] is False
    assert revise_rule["recorded_pause_reason_required"] is False
    assert revise_rule["approved_implementation_branch_required"] is False
    assert revise_rule["runtime_implementation_approved"] is False

    pause_rule = rules["Pause"]
    assert pause_rule["recorded_choice"] == "Pause"
    assert pause_rule["recorded_pause_reason_required"] is True
    assert pause_rule["recorded_approval_wording_required"] is False
    assert pause_rule["recorded_revision_request_required"] is False
    assert pause_rule["approved_implementation_branch_required"] is False
    assert pause_rule["runtime_implementation_approved"] is False

    invalid_results = set(fixture["invalid_decision_record_results"])
    assert "mixed_state_treated_as_no_approval" in invalid_results
    assert "missing_choice_treated_as_no_approval" in invalid_results
    assert "misspelled_choice_treated_as_no_approval" in invalid_results
    assert "extra_choice_value_treated_as_no_approval" in invalid_results


def test_v1_g11_operator_decision_record_templates_are_exact() -> None:
    fixture = _load_fixture()
    templates = fixture["decision_record_templates"]
    assert set(templates) == {"none", "Approve-V1-G11", "Revise-V1-G11", "Pause"}

    none_template = templates["none"]
    assert none_template == {
        "recorded_choice": "none",
        "recorded_approval_wording": "none",
        "recorded_revision_request": "none",
        "recorded_pause_reason": "none",
        "approved_implementation_branch": "none",
        "runtime_implementation_approved": "no",
    }

    approve_template = templates["Approve-V1-G11"]
    assert approve_template["recorded_choice"] == "Approve-V1-G11"
    assert approve_template["recorded_approval_wording"] == fixture["required_approval_wording"]
    assert approve_template["recorded_revision_request"] == "none"
    assert approve_template["recorded_pause_reason"] == "none"
    assert approve_template["approved_implementation_branch"] == fixture["if_approved_next_branch"]
    assert approve_template["runtime_implementation_approved"] == "yes"

    revise_template = templates["Revise-V1-G11"]
    assert revise_template["recorded_choice"] == "Revise-V1-G11"
    assert revise_template["recorded_approval_wording"] == "none"
    assert revise_template["recorded_revision_request"] == "<required revision request>"
    assert revise_template["recorded_pause_reason"] == "none"
    assert revise_template["approved_implementation_branch"] == "none"
    assert revise_template["runtime_implementation_approved"] == "no"

    pause_template = templates["Pause"]
    assert pause_template["recorded_choice"] == "Pause"
    assert pause_template["recorded_approval_wording"] == "none"
    assert pause_template["recorded_revision_request"] == "none"
    assert pause_template["recorded_pause_reason"] == "<required pause reason>"
    assert pause_template["approved_implementation_branch"] == "none"
    assert pause_template["runtime_implementation_approved"] == "no"


def test_v1_g11_operator_decision_packet_rejects_implicit_approval_inputs() -> None:
    non_approval_inputs = set(_load_fixture()["non_approval_inputs"])
    assert "general_v1_product_direction" in non_approval_inputs
    assert "active_product_goal" in non_approval_inputs
    assert "prior_static_gates" in non_approval_inputs
    assert "operator_decision_packet" in non_approval_inputs
    assert (
        "broad_acceptability_of_haptics_approval_guardiandecision_provider_model_routing"
        in non_approval_inputs
    )


def test_v1_g11_operator_decision_packet_limits_approved_files_if_approved() -> None:
    eligible_files = set(_load_fixture()["eligible_files_if_approved"])
    assert eligible_files == {
        "lima/kernel/v1_runtime_request.py",
        "lima/kernel/__init__.py",
        "lima/guardian/v1_decision_gate.py",
        "lima/guardian/__init__.py",
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md",
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json",
        "tests/test_v1_g11_runtime_request_decision_gate.py",
    }


def test_v1_g11_operator_decision_packet_stop_conditions_cover_forbidden_scope() -> None:
    stop_conditions = set(_load_fixture()["stop_conditions"])
    assert "file_scope_exceeds_v1_g11_request" in stop_conditions
    assert "raw_natural_language_parsing_introduced" in stop_conditions
    assert "request_metadata_executes_directly" in stop_conditions
    assert "approval_metadata_becomes_execution_authority" in stop_conditions
    assert "destructive_edit_delete_approved_without_operator_approval_evidence" in stop_conditions
    assert "caller_metadata_can_forge_guardian_decision_authority" in stop_conditions
    assert "provider_model_calls_made" in stop_conditions
    assert "tool_file_browser_network_device_robotics_physical_world_invoked" in stop_conditions
    assert "persistent_storage_or_database_writes_added" in stop_conditions
    assert "shell_runtime_wiring_added" in stop_conditions
    assert "sparkbot_sparkbot_shell_arc_bot_shell_code_imported_or_copied" in stop_conditions
    assert "runtime_exports_cleaned_up_or_frozen" in stop_conditions
    assert "validation_fails" in stop_conditions


def test_v1_g11_operator_decision_packet_doc_matches_fixture() -> None:
    fixture = _load_fixture()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Decision packet status: `approve_v1_g11_recorded`" in text
    assert "This packet records the operator decision" in text
    assert "## Decision Record" in text
    assert "One operator choice is recorded." in text
    assert "Recorded choice: `Approve-V1-G11`" in text
    assert f"Recorded approval wording: `{fixture['required_approval_wording']}`" in text
    assert "Recorded revision request: `none`" in text
    assert "Recorded pause reason: `none`" in text
    assert "Any other text is commentary, not a decision." in text
    assert "## Decision Record Validation Rules" in text
    assert "`Approve-V1-G11`: valid only with the exact required approval wording" in text
    assert "`Revise-V1-G11`: valid only with a non-empty revision request" in text
    assert "`Pause`: valid only with a non-empty pause reason" in text
    assert "Any mixed state is invalid and must be treated as no approval." in text
    assert "Runtime implementation may start only from the valid `Approve-V1-G11` state." in text
    assert "## Decision Record Templates" in text
    assert "Template for no recorded choice:" in text
    assert "Template for `Approve-V1-G11`:" in text
    assert "Template for `Revise-V1-G11`:" in text
    assert "Template for `Pause`:" in text
    assert "Recorded choice: Approve-V1-G11" in text
    assert "Approved implementation branch: v1-g11-runtime-request-decision-gate" in text
    assert "Runtime implementation approved: yes" in text
    assert "Runtime implementation approved: yes" in text
    assert "General V1 product direction" in text
    assert "do not count as implementation approval" in text
    assert "### `Approve-V1-G11`" in text
    assert "### `Revise-V1-G11`" in text
    assert "### `Pause`" in text
    assert fixture["required_approval_wording"] in text
    assert fixture["if_approved_next_branch"] in text
    assert fixture["if_approved_scope"] in text
    assert "create the approved implementation branch" in text
    assert fixture["recommended_next_step"] == "create_approved_v1_g11_implementation_branch"
