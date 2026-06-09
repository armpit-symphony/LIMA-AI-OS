from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_packet_audit_result_gate"
    / "consumer_proof_packet_audit_result_gate.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _gate_text() -> str:
    return _text("result_gate_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_result_gate_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_packet_audit_result_gate_only"
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
    assert fixture["automated_intake_added"] is False
    assert fixture["response_sending_added"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_result_gate_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "result_gate_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_result_gate_current_state_remains_missing_and_not_ready() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    review = _review_text()
    audit = _audit_text()
    state = fixture["current_state"]

    assert f"| Sparkbot proof packet | `{state['sparkbot_proof_packet']}` |" in gate
    assert f"| Arc Bot proof packet | `{state['arc_bot_proof_packet']}` |" in gate
    assert f"| Sparkbot proof audit | `{state['sparkbot_proof_audit']}` |" in gate
    assert f"| Arc Bot proof audit | `{state['arc_bot_proof_audit']}` |" in gate
    assert f"| Combined result gate | `{state['combined_result_gate']}` |" in gate
    assert f"| Public API compatibility freeze | `{state['public_api_compatibility_freeze']}` |" in gate
    assert f"| Product readiness | `{state['product_readiness']}` |" in gate

    assert "does not change those states" in gate
    assert "both packets and both audits" in review
    assert "missing" in review
    assert "It preserves missing Sparkbot and Arc packet/audit state." in audit


def test_result_gate_source_artifacts_exist_and_are_referenced() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in gate

    assert "the stricter artifact controls" in gate


def test_result_gate_required_inputs_are_redacted_completed_audit_reports() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert "completed, redacted, LIMA-side audit reports" in gate
    assert "`docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`" in gate
    assert f"`{fixture['required_input_branches']['sparkbot']}`" in gate
    assert f"`{fixture['required_input_branches']['arc_bot']}`" in gate

    for field in fixture["required_input_fields"]:
        assert field in gate

    assert "`not_ready_for_result_gate`" in gate


def test_result_gate_blocks_forbidden_inputs_and_unredacted_archive() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()

    for forbidden_input in fixture["forbidden_inputs"]:
        assert forbidden_input in gate

    assert "`needs_redaction_before_result_gate`" in gate
    assert "Unredacted evidence must not be archived." in gate
    assert "Unredacted evidence must not be archived." in audit


def test_result_gate_allowed_input_statuses_are_bounded() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for status in fixture["allowed_input_audit_statuses"]:
        assert f"`{status}`" in gate

    assert "The only passing per-consumer audit status is:" in gate
    assert "`pass_for_dry_run_dependency_proof`" in gate
    assert "That status does not mean production readiness." in gate


def test_result_gate_allowed_and_forbidden_combined_states_are_bounded() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()
    combined = "\n".join((gate, audit))

    for status in fixture["allowed_combined_result_states"]:
        assert f"`{status}`" in combined

    for status in fixture["forbidden_combined_result_states"]:
        assert f"`{status}`" in combined

    assert "`compatibility_frozen`" in gate


def test_result_gate_result_mapping_is_fail_closed() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    mapping = fixture["result_mapping_expectations"]

    assert f"| missing | missing | `{mapping['missing_missing']}` |" in gate
    assert f"| pass | missing | `{mapping['pass_missing']}` |" in gate
    assert f"| redaction blocker | any | `{mapping['redaction_any']}` |" in gate
    assert f"| missing evidence | any non-redaction | `{mapping['missing_evidence_any']}` |" in gate
    assert f"| runtime boundary block | any non-redaction | `{mapping['runtime_boundary_any']}` |" in gate
    assert f"| consumer repo boundary block | any non-redaction/runtime | `{mapping['consumer_repo_boundary_any']}` |" in gate
    assert f"| claim boundary block | any non-redaction/runtime/repo | `{mapping['claim_boundary_any']}` |" in gate
    assert f"| design follow-up | any non-blocking | `{mapping['design_followup_any']}` |" in gate
    assert f"| audit follow-up | any non-blocking | `{mapping['audit_followup_any']}` |" in gate
    assert f"| pass | pass | `{mapping['pass_pass']}` |" in gate
    assert "Redaction blockers outrank all other statuses." in gate
    assert "Runtime boundary blockers outrank consumer repo, claim, design, and audit" in gate


def test_result_gate_pass_criteria_do_not_approve_product_use() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for criterion in fixture["pass_criteria"]:
        assert criterion in gate

    assert "`pass_for_dry_run_dual_consumer_proof`" in gate
    assert "This pass state means only that LIMA may design a dry-run public API compatibility freeze next." in gate
    assert "It does not approve:" in gate
    assert "Sparkbot product integration" in gate
    assert "Arc Bot product integration" in gate
    assert "production use" in gate
    assert "physical-world behavior" in gate


def test_result_gate_fail_closed_rules_cover_runtime_and_consumer_boundary() -> None:
    gate = _gate_text()

    assert "The result gate must fail closed when:" in gate
    assert "either consumer audit is missing" in gate
    assert "either packet is unredacted" in gate
    assert "either packet uses forbidden imports" in gate
    assert "either packet omits required non-execution invariant evidence" in gate
    assert "either packet contradicts non-execution invariant evidence" in gate
    assert "either packet sends raw chat or office-task text to LIMA" in gate
    assert "either packet wires production routes" in gate
    assert "Robo-OS access, device" in gate
    assert "product readiness, production readiness, live integration readiness" in gate


def test_result_gate_compatibility_freeze_boundary_remains_design_only() -> None:
    gate = _gate_text()
    review = _review_text()
    audit = _audit_text()
    combined = "\n".join((gate, review, audit))

    assert "The result gate does not start a compatibility freeze." in gate
    assert "`design-lima-dry-run-consumer-compatibility-freeze`" in gate
    assert "`not_ready_for_freeze`" in gate
    assert "It does not start a freeze and does not approve product or" in review
    assert "production use." in review
    assert "The design does not start a compatibility freeze." in audit
    assert "`not_ready_for_freeze`" in combined


def test_result_gate_forbidden_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()
    combined = "\n".join((gate, audit))

    for action in fixture["forbidden_actions"]:
        assert action in combined

    assert "This gate must not trigger:" in gate
    assert "No runtime behavior is introduced." in audit


def test_static_test_fixture_paths_do_not_reference_live_or_external_surfaces() -> None:
    fixture = _load_fixture()
    serialized = json.dumps(fixture, sort_keys=True)

    forbidden_path_fragments = (
        "http://",
        "https://",
        "app://",
        "file://",
        "socket://",
        "sparkbot-lima-dry-run-boundary-proof/",
        "arc-lima-dry-run-boundary-proof/",
        "public/Sparkbot",
    )

    for fragment in forbidden_path_fragments:
        assert fragment not in serialized


def test_static_tests_allowed_files_and_forbidden_surfaces_are_bounded() -> None:
    fixture = _load_fixture()
    static_tests_audit = _static_tests_audit_text()

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in static_tests_audit

    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in static_tests_audit


def test_static_tests_implementation_recommends_independent_audit() -> None:
    fixture = _load_fixture()
    static_tests_audit = _static_tests_audit_text()

    assert (
        fixture["recommended_next_branch"]
        == "audit-lima-consumer-proof-packet-audit-result-gate-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
