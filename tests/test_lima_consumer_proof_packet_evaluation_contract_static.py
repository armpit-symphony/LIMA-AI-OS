from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_packet_evaluation_contract"
    / "evaluation_contract.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _contract_text() -> str:
    return _text("evaluation_contract_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_evaluation_contract_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_packet_evaluation_contract_only"
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


def test_evaluation_contract_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "evaluation_contract_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_evaluation_contract_preserves_current_missing_state() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_contract_text(), _review_text(), _audit_text()))

    assert (
        fixture["current_closeout_verdict"]
        == "lima_local_prerequisites_closed_waiting_on_consumer_proof"
    )
    assert f"`{fixture['current_closeout_verdict']}`" in combined
    assert f"`{fixture['current_freeze_state']}`" in combined
    assert f"`{fixture['current_product_state']}`" in combined

    for state in fixture["current_missing_inputs"].values():
        assert f"`{state}`" in combined

    assert "both consumer proof packets are missing" in combined


def test_evaluation_contract_references_source_artifacts() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_contract_text(), _audit_text()))

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in combined

    assert "the stricter artifact controls" in _contract_text()


def test_evaluation_contract_input_shape_is_reference_only() -> None:
    fixture = _load_fixture()
    contract = _contract_text()

    for field in fixture["required_packet_identity_fields"]:
        assert f"`{field}`" in contract
    for field in fixture["required_evidence_reference_fields"]:
        assert f"`{field}`" in contract

    assert "redacted summaries and references only" in contract
    assert "must not copy raw proof evidence into" in contract


def test_preflight_gate_is_fail_closed() -> None:
    fixture = _load_fixture()
    contract = _contract_text()
    mapping = fixture["preflight_mapping"]

    for state in fixture["allowed_preflight_states"]:
        assert f"`{state}`" in contract

    for state, status in mapping.items():
        assert f"`{state}`" in contract
        assert f"`{status}`" in contract or status in contract

    assert mapping["received_redacted_reference_only"] == "continue evaluation"
    assert "If the preflight state is anything except `received_redacted_reference_only`, evaluation stops." in contract


def test_public_api_evaluation_preserves_proof_public_boundary() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_contract_text(), _audit_text()))

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in combined
    for forbidden in fixture["forbidden_public_import_claims"]:
        assert forbidden in combined

    for outcome in fixture["public_api_outcomes"].values():
        assert f"`{outcome}`" in combined or outcome in combined

    assert "No public exports are changed." in combined


def test_normalized_metadata_and_capability_checks_are_default_deny() -> None:
    fixture = _load_fixture()
    contract = _contract_text()

    for evidence in fixture["allowed_input_evidence"]:
        assert evidence in contract
    for evidence in fixture["forbidden_input_evidence"]:
        assert evidence in contract

    for capability, value in fixture["required_default_deny_capabilities"].items():
        expected = "false" if value is False else "true"
        assert f"`{capability}: {expected}`" in contract

    assert "Missing capability evidence maps to `needs_missing_evidence`." in contract
    assert "maps to `blocked_by_runtime_boundary`" in contract


def test_kernel_call_evaluation_remains_explicit_and_dry_run_only() -> None:
    fixture = _load_fixture()
    contract = _contract_text()

    for requirement in fixture["kernel_call_requirements"]:
        assert requirement in contract
    for state in fixture["allowed_result_states"]:
        assert f"`{state}`" in contract

    assert "Missing kernel-call evidence maps to `needs_missing_evidence`." in contract
    assert "maps to `blocked_by_runtime_boundary`" in contract


def test_simulated_discovery_evaluation_blocks_live_behavior() -> None:
    fixture = _load_fixture()
    contract = _contract_text()

    for requirement in fixture["simulated_discovery_requirements"]:
        assert requirement in contract

    blocked_terms = (
        "live discovery",
        "scanning",
        "connection",
        "pairing",
        "credential use",
        "Robo-OS access",
        "robotics",
        "drones",
        "physical-world behavior",
    )
    for term in blocked_terms:
        assert term in contract


def test_non_execution_invariant_evaluation_is_complete() -> None:
    fixture = _load_fixture()
    contract = _contract_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in contract

    assert "Missing invariant evidence maps to `needs_missing_evidence`." in contract
    assert "Contradictory invariant evidence maps to `blocked_by_runtime_boundary`." in contract


def test_redaction_rules_block_sensitive_content() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_contract_text(), _review_text(), _audit_text()))

    for blocker in fixture["redaction_blockers"]:
        assert blocker in combined

    assert "LIMA must not archive unredacted consumer evidence." in combined


def test_consumer_specific_evaluation_preserves_sparkbot_and_arc_boundaries() -> None:
    fixture = _load_fixture()
    contract = _contract_text()

    for requirement in fixture["sparkbot_evidence_requirements"]:
        assert requirement in contract
    for requirement in fixture["arc_bot_evidence_requirements"]:
        assert requirement in contract

    assert "Missing consumer-specific evidence maps to `needs_missing_evidence`." in contract
    assert "Contradictory consumer-specific evidence maps to `blocked_by_consumer_repo_boundary`" in contract


def test_audit_statuses_and_precedence_are_fail_closed() -> None:
    fixture = _load_fixture()
    contract = _contract_text()

    for status in fixture["allowed_audit_statuses"]:
        assert f"`{status}`" in contract
    for status in fixture["forbidden_audit_statuses"]:
        assert f"`{status}`" in contract

    precedence = fixture["evaluation_precedence"]
    assert precedence[-1] == "pass_for_dry_run_dependency_proof"
    for index, status in enumerate(precedence, start=1):
        assert f"{index}. `{status}`" in contract

    assert "A pass can occur only when every required review area passes" in contract


def test_evaluation_output_shape_is_redacted_and_not_ready() -> None:
    fixture = _load_fixture()
    contract = _contract_text()

    for field in fixture["evaluation_output_fields"]:
        assert field in contract

    for field, value in fixture["evaluation_output_required_values"].items():
        assert f"{field}: {value}" in contract

    assert "The report must contain redacted summaries and references only." in contract


def test_recommended_branch_rules_preserve_ownership_and_design_only_freeze() -> None:
    fixture = _load_fixture()
    contract = _contract_text()

    for branch_or_instruction in fixture["recommended_branch_rules"].values():
        assert f"`{branch_or_instruction}`" in contract or branch_or_instruction in contract

    assert "owner: consumer repo team" in contract
    assert "owner: LIMA repo team" in contract
    assert "still design-only unless separately approved" in contract


def test_forbidden_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_contract_text(), _audit_text()))

    for action in fixture["forbidden_actions"]:
        assert action in combined

    assert "This evaluation contract must not trigger:" in combined


def test_static_fixture_paths_do_not_reference_live_or_external_surfaces() -> None:
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
        == "audit-lima-consumer-proof-packet-evaluation-contract-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
