from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_ledger_update_closeout"
    / "consumer_proof_ledger_update_closeout.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _closeout_text() -> str:
    return _text("closeout_path")


def _closeout_audit_text() -> str:
    return _text("audit_path")


def _static_tests_design_text() -> str:
    return _text("static_tests_design_path")


def _static_tests_design_audit_text() -> str:
    return _text("static_tests_design_audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_closeout_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_ledger_update_closeout_only"
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


def test_closeout_static_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "closeout_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_design_path",
        "static_tests_design_audit_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_static_tests_reference_source_artifacts_and_stricter_controls() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    design = _static_tests_design_text()

    for path in fixture["required_source_artifacts"]:
        assert f"`{path}`" in design
        assert (REPO_ROOT / path).exists(), path

    assert "the stricter source artifact must control" in design
    assert "the stricter source artifact controls" in closeout


def test_closeout_verdict_remains_waiting_for_consumer_packets() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _closeout_audit_text()
    design = _static_tests_design_text()

    verdict = fixture["closeout_verdict"]
    assert f"`{verdict}`" in closeout
    assert f"`{verdict}`" in audit
    assert f"closeout verdict remains `{verdict}`" in design
    assert "LIMA is not ready to claim Sparkbot or Arc Bot dependency use" in closeout
    assert "Compatibility freeze remains blocked" in closeout
    assert "Product readiness remains blocked" in closeout


def test_current_closeout_state_stays_missing_and_blocked() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    design = _static_tests_design_text()
    state = fixture["current_proof_state"]

    assert f"| Sparkbot proof packet | `{state['sparkbot_proof_packet']}` |" in closeout
    assert f"| Arc Bot proof packet | `{state['arc_bot_proof_packet']}` |" in closeout
    sparkbot_redaction_values = state["sparkbot_redaction_review"].split(" / ")
    arc_redaction_values = state["arc_bot_redaction_review"].split(" / ")
    assert (
        f"| Sparkbot redaction review | `{sparkbot_redaction_values[0]}` / "
        f"`{sparkbot_redaction_values[1]}` |"
    ) in closeout
    assert (
        f"| Arc Bot redaction review | `{arc_redaction_values[0]}` / "
        f"`{arc_redaction_values[1]}` |"
    ) in closeout
    assert f"| Sparkbot proof audit | `{state['sparkbot_proof_audit']}` |" in closeout
    assert f"| Arc Bot proof audit | `{state['arc_bot_proof_audit']}` |" in closeout
    assert f"| Compatibility freeze | `{state['compatibility_freeze']}` |" in closeout
    assert f"| Product readiness | `{state['product_readiness']}` |" in closeout
    assert "Sparkbot packet remains `not_received`" in design
    assert "Arc Bot packet remains `not_received`" in design


def test_ready_materials_are_preparation_only_not_dependency_proof() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    design = _static_tests_design_text()

    for material in fixture["ready_lima_local_materials"]:
        assert material in closeout
        assert material in design

    assert "These materials are guardrails for future human review" in closeout
    assert "not proof that Sparkbot or Arc Bot can use LIMA" in closeout
    assert "not proof that Sparkbot or Arc Bot can use LIMA" in design


def test_manual_update_flow_remains_human_reviewed_and_non_automated() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    design = _static_tests_design_text()

    for step in fixture["manual_update_flow"]:
        assert step in closeout

    assert "This closeout does not automate that flow." in closeout
    assert "The later static tests must not automate this flow." in design


def test_response_to_ledger_mapping_includes_every_allowed_status() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    design = _static_tests_design_text()

    for row in fixture["response_to_ledger_mapping"]:
        assert f"| `{row['response_status']}` |" in closeout
        assert f"| `{row['intake_status']}` |" in closeout
        assert f"| `{row['audit_status']}` |" in closeout
        assert row["response_status"] in design
        for status in row["redaction_status"].split(" or "):
            assert f"`{status}`" in closeout


def test_mapping_does_not_approve_live_runtime_or_physical_surfaces() -> None:
    closeout = _closeout_text()
    design = _static_tests_design_text()

    for phrase in (
        "No mapping approves production readiness",
        "live integration",
        "model calls",
        "tool execution",
        "connector access",
        "storage",
        "live discovery",
        "Robo-OS",
        "device control",
        "robotics",
        "drones",
        "physical-world behavior",
        "compatibility freeze",
    ):
        assert phrase in closeout

    assert "response-to-ledger mapping does not allow production/live" in design


def test_manual_ledger_and_response_fields_remain_documented() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    for field in fixture["manual_ledger_fields"]:
        assert f"`{field}`" in closeout
    for field in fixture["manual_response_fields"]:
        assert f"`{field}`" in closeout

    assert fixture["required_production_readiness"] == "not_production_ready"
    assert "`not_production_ready`" in closeout
    assert "human-maintained document record only" in closeout
    assert "This closeout does not send responses automatically" in closeout


def test_redaction_blockers_and_raw_sensitive_storage_remain_blocked() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    design = _static_tests_design_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in closeout
        assert blocker in design

    assert "`needs_redaction_before_review`" in closeout
    assert "must not store raw sensitive evidence" in closeout
    assert "raw sensitive evidence must not be stored in ledger records" in design


def test_non_execution_invariants_remain_required() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    design = _static_tests_design_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in closeout

    assert "If evidence is missing, use `needs_missing_evidence`." in closeout
    assert "use `blocked_by_runtime_boundary`" in closeout
    assert "non-execution invariants remain listed" in design


def test_sparkbot_and_arc_missing_evidence_remains_required() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    assert "Sparkbot proof remains missing until the Sparkbot repo team supplies" in closeout
    for requirement in fixture["sparkbot_missing_evidence"]:
        assert requirement in closeout

    assert "Arc Bot / LIMA AI Office proof remains missing until the Arc Bot / LIMA Office repo team supplies" in closeout
    for requirement in fixture["arc_missing_evidence"]:
        assert requirement in closeout


def test_compatibility_freeze_remains_blocked_until_both_proof_audits_pass() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    design = _static_tests_design_text()

    assert "Current freeze status:" in closeout
    assert "`blocked`" in closeout
    for condition in fixture["compatibility_freeze_conditions"]:
        assert condition in closeout
        assert condition in design

    assert "An intake response, ledger update, closeout, static test, or audit alone must never unfreeze compatibility." in closeout
    assert "closeout/static test/audit alone never unfreezes compatibility" in design


def test_forbidden_closeout_claims_remain_blocked() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    assert "This closeout must not be used to claim:" in closeout
    for claim in fixture["forbidden_closeout_claims"]:
        assert claim in closeout


def test_forbidden_closeout_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    assert "This closeout must not trigger:" in closeout
    for action in fixture["forbidden_closeout_actions"]:
        assert action in closeout


def test_static_test_design_and_audit_bound_later_files_and_surfaces() -> None:
    fixture = _load_fixture()
    design = _static_tests_design_text()
    design_audit = _static_tests_design_audit_text()
    implementation_audit = _static_tests_audit_text()

    for path in fixture["allowed_static_files"]:
        assert f"`{path}`" in design
        assert f"`{path}`" in design_audit
        assert f"`{path}`" in implementation_audit

    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in design
        assert surface in design_audit
        assert surface in implementation_audit


def test_static_tests_implementation_recommends_independent_audit() -> None:
    fixture = _load_fixture()
    implementation_audit = _static_tests_audit_text()

    assert fixture["recommended_next_branch"] == (
        "audit-lima-consumer-proof-ledger-update-closeout-static-tests-implementation"
    )
    assert f"`{fixture['recommended_next_branch']}`" in implementation_audit
    assert fixture["independent_audit_path"].endswith(
        "LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md"
    )
