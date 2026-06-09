from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_intake_response_ledger_update_gate"
    / "consumer_proof_intake_response_ledger_update_gate.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _gate_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["gate_path"]).read_text(encoding="utf-8")


def _gate_audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def _static_tests_design_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["static_tests_design_path"]).read_text(encoding="utf-8")


def _static_tests_design_audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["static_tests_design_audit_path"]).read_text(
        encoding="utf-8"
    )


def _static_tests_audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["static_tests_audit_path"]).read_text(encoding="utf-8")


def test_gate_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == (
        "static_consumer_proof_intake_response_ledger_update_gate_only"
    )
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_exports_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_proof_packet_received"] is False
    assert fixture["consumer_proof_packet_archived"] is False
    assert fixture["consumer_proof_packet_audited"] is False
    assert fixture["response_sending_added"] is False
    assert fixture["ledger_persistence_added"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_gate_static_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "gate_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_design_path",
        "static_tests_design_audit_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_static_tests_reference_source_artifacts_and_stricter_controls() -> None:
    fixture = _load_fixture()
    design = _static_tests_design_text()

    for path in fixture["required_source_artifacts"]:
        assert f"`{path}`" in design
        assert (REPO_ROOT / path).exists(), path

    assert "the stricter source artifact must control" in design


def test_gate_current_proof_state_stays_missing_and_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _gate_audit_text()
    state = fixture["current_proof_state"]

    assert f"Sparkbot proof packet: `{state['sparkbot_proof_packet']}`" in gate
    assert f"Arc Bot proof packet: `{state['arc_bot_proof_packet']}`" in gate
    assert f"Sparkbot redaction review: `{state['sparkbot_redaction_review']}`" in gate
    assert f"Arc Bot redaction review: `{state['arc_bot_redaction_review']}`" in gate
    assert f"Sparkbot proof audit: `{state['sparkbot_proof_audit']}`" in gate
    assert f"Arc Bot proof audit: `{state['arc_bot_proof_audit']}`" in gate
    assert f"compatibility freeze: `{state['compatibility_freeze']}`" in gate
    assert f"product readiness: `{state['product_readiness']}`" in gate
    assert "does not change that state" in gate
    assert "Sparkbot proof packet remains `not_received`" in audit
    assert "Arc Bot proof packet remains `not_received`" in audit


def test_gate_inputs_are_human_supplied_and_forbidden_inputs_are_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert "Allowed gate inputs are human-supplied and redacted" in gate
    for allowed_input in fixture["allowed_gate_inputs"]:
        assert allowed_input in gate

    assert "Forbidden gate inputs:" in gate
    for forbidden_input in fixture["forbidden_gate_inputs"]:
        assert forbidden_input in gate


def test_pre_update_conditions_remain_fail_closed() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert "Do not write an intake response or ledger update unless" in gate
    for condition in fixture["pre_update_entry_conditions"]:
        assert condition in gate

    assert "`needs_missing_evidence`" in gate
    assert "`blocked_by_consumer_repo_boundary`" in gate


def test_response_to_ledger_mapping_includes_all_allowed_statuses() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for row in fixture["response_to_ledger_mapping"]:
        assert f"| `{row['response_status']}` |" in gate
        assert f"| `{row['intake_status']}` |" in gate
        assert f"| `{row['audit_status']}` |" in gate
        for status in row["redaction_status"].split(" or "):
            assert f"`{status}`" in gate


def test_mapping_does_not_approve_live_or_physical_surfaces() -> None:
    gate = _gate_text()

    for phrase in (
        "No response status may map to production readiness",
        "live integration",
        "model-call approval",
        "tool-execution approval",
        "connector approval",
        "storage approval",
        "live-discovery approval",
        "Robo-OS approval",
        "device-control approval",
        "robotics approval",
        "drone approval",
        "physical-world approval",
        "compatibility freeze",
    ):
        assert phrase in gate


def test_manual_ledger_and_response_fields_remain_documented() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for field in fixture["manual_ledger_fields"]:
        assert f"`{field}`" in gate
    for field in fixture["manual_response_fields"]:
        assert f"`{field}`" in gate

    assert fixture["required_production_readiness"] == "not_production_ready"
    assert "`not_production_ready`" in gate
    assert "human-maintained document record only" in gate
    assert "This gate does not send responses automatically" in gate


def test_redaction_gate_blocks_sensitive_evidence_and_raw_storage() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in gate

    assert "`needs_redaction_before_review`" in gate
    assert "must not store the raw sensitive evidence" in gate


def test_non_execution_invariants_remain_required() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in gate

    assert "If evidence is missing, use `needs_missing_evidence`." in gate
    assert "use `blocked_by_runtime_boundary`" in gate


def test_consumer_specific_gates_keep_sparkbot_and_arc_evidence_required() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert "Sparkbot intake cannot move to `accepted_for_archive` unless" in gate
    for requirement in fixture["sparkbot_specific_evidence"]:
        assert requirement in gate

    assert "Arc Bot / LIMA AI Office intake cannot move to `accepted_for_archive` unless" in gate
    for requirement in fixture["arc_specific_evidence"]:
        assert requirement in gate

    assert "Missing consumer-specific evidence maps to `needs_missing_evidence`" in gate


def test_branch_recommendations_remain_safe_and_no_freeze_recommended() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for branch in fixture["branch_recommendations"].values():
        assert f"`{branch}`" in gate

    assert "Do not recommend compatibility freeze until both Sparkbot and Arc Bot proof audits pass" in gate
    assert "`pass_for_dry_run_dependency_proof`" in gate


def test_compatibility_freeze_remains_blocked_until_all_inputs_pass() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _gate_audit_text()

    assert "Compatibility freeze remains:" in gate
    assert "`blocked`" in gate
    for condition in fixture["compatibility_freeze_conditions"]:
        assert condition in gate
    assert "An intake response or ledger update alone must never unfreeze compatibility." in gate
    assert "intake response or ledger update alone must never unfreeze compatibility" in audit


def test_forbidden_status_values_remain_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert "The response and ledger update must not use:" in gate
    for status in fixture["forbidden_status_values"]:
        assert f"`{status}`" in gate


def test_forbidden_gate_behaviors_and_reviewer_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert "This gate must not become:" in gate
    for behavior in fixture["forbidden_gate_behaviors"]:
        assert behavior in gate

    assert "Reviewers must not:" in gate
    for action in fixture["reviewer_forbidden_actions"]:
        assert action in gate


def test_static_test_design_and_audit_bound_later_files_and_surfaces() -> None:
    fixture = _load_fixture()
    design = _static_tests_design_text()
    audit = _static_tests_design_audit_text()
    implementation_audit = _static_tests_audit_text()

    for path in fixture["allowed_static_files"]:
        assert f"`{path}`" in design
        assert f"`{path}`" in audit
        assert f"`{path}`" in implementation_audit

    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in design
        assert surface in audit
        assert surface in implementation_audit


def test_static_tests_implementation_audit_recommends_independent_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == (
        "audit-lima-consumer-proof-intake-response-ledger-update-gate-static-tests-implementation"
    )
