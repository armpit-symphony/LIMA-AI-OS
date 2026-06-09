from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_audit_execution_packet"
    / "audit_execution_packet.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _design_text() -> str:
    return _text("audit_execution_packet_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_audit_execution_packet_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_audit_execution_packet_only"
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
    assert fixture["automated_evaluation_added"] is False
    assert fixture["response_sending_added"] is False
    assert fixture["result_gate_execution_added"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_audit_execution_packet_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "audit_execution_packet_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_audit_execution_packet_preserves_current_missing_state() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    assert (
        fixture["current_closeout_verdict"]
        == "lima_local_prerequisites_closed_waiting_on_consumer_proof"
    )
    assert f"`{fixture['current_closeout_verdict']}`" in combined
    assert f"`{fixture['current_freeze_state']}`" in combined
    assert f"`{fixture['current_product_state']}`" in combined

    for state in fixture["current_missing_inputs"].values():
        assert f"`{state}`" in combined


def test_audit_execution_packet_references_source_artifacts() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text()))

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in combined

    assert "the stricter artifact controls" in _design_text()


def test_audit_execution_packet_preconditions_are_human_reviewed() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for precondition in fixture["packet_preconditions"]:
        assert precondition in design

    assert "If any precondition is missing" in design
    assert "must not feed the result" in design
    assert "gate as a passing input" in design


def test_audit_execution_packet_identity_and_review_area_shapes_are_reference_only() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for field in fixture["packet_identity_fields"]:
        assert field in design
    for field in fixture["review_area_fields"]:
        assert field in design

    assert "The `proof_packet_reference` must be a redacted reference only." in design
    assert "Every review area must contain redacted summaries and references only." in design


def test_required_review_areas_and_review_statuses_are_bounded() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for area in fixture["required_review_areas"]:
        assert f"`{area}`" in design
    for status in fixture["allowed_review_area_statuses"]:
        assert f"`{status}`" in design
    for status in fixture["forbidden_review_area_statuses"]:
        assert f"`{status}`" in design

    assert "Forbidden review-area statuses" in design


def test_public_api_boundary_preserves_proof_public_imports() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text()))

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in combined
    for forbidden in fixture["forbidden_public_import_claims"]:
        assert forbidden in combined

    assert "No public exports are changed." in combined
    assert "Forbidden import evidence maps" in combined


def test_runtime_review_remains_explicit_dry_run_only() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for requirement in fixture["runtime_review_requirements"]:
        assert requirement in design
    for state in fixture["allowed_result_states"]:
        assert f"`{state}`" in design

    assert "Any execution, dispatch, persistence, model call" in design
    assert "maps the packet to `blocked_by_runtime_boundary`" in design


def test_simulated_discovery_review_blocks_live_behavior() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for requirement in fixture["simulated_discovery_requirements"]:
        assert requirement in design

    blocked_terms = (
        "Live discovery",
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
        assert term in design


def test_non_execution_invariant_requirements_are_complete() -> None:
    fixture = _load_fixture()
    design = _design_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in design

    assert "Missing invariant evidence maps the packet to `needs_missing_evidence`." in design
    assert "Contradictory invariant evidence maps the packet to `blocked_by_runtime_boundary`." in design


def test_redaction_rules_block_sensitive_content() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    for blocker in fixture["redaction_blockers"]:
        assert blocker in combined

    assert "sensitive content must not be copied" in combined
    assert "into the LIMA repo" in combined


def test_consumer_specific_requirements_preserve_sparkbot_and_arc_boundaries() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for requirement in fixture["sparkbot_evidence_requirements"]:
        assert requirement in design
    for requirement in fixture["arc_bot_evidence_requirements"]:
        assert requirement in design

    assert "Missing consumer-specific evidence maps the packet to `needs_missing_evidence`." in design
    assert "Contradictory consumer-specific evidence maps the packet to `blocked_by_consumer_repo_boundary`" in design


def test_overall_statuses_and_precedence_are_fail_closed() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for status in fixture["allowed_overall_statuses"]:
        assert f"`{status}`" in design
    for status in fixture["forbidden_overall_statuses"]:
        assert f"`{status}`" in design

    precedence = fixture["status_precedence"]
    assert precedence[-1] == "pass_for_dry_run_dependency_proof"
    for index, status in enumerate(precedence, start=1):
        assert f"{index}. `{status}`" in design

    assert "does not mean production readiness" in design


def test_result_gate_boundary_does_not_run_gate_or_freeze() -> None:
    fixture = _load_fixture()
    design = _design_text()

    assert "This packet does not run the dual-consumer result gate." in design
    for requirement in fixture["result_gate_requirements"]:
        assert requirement in design

    assert "If either packet is missing or not passing" in design
    assert "the combined result remains fail-closed" in design


def test_output_shape_is_redacted_and_not_ready() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for field in fixture["output_fields"]:
        assert field in design

    for field, value in fixture["output_required_values"].items():
        assert f"{field}: {value}" in design

    assert "The packet must contain redacted summaries and evidence references only." in design


def test_recommended_branch_rules_preserve_ownership() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for branch_or_instruction in fixture["recommended_branch_rules"].values():
        assert f"`{branch_or_instruction}`" in design or branch_or_instruction in design

    assert "owner: consumer repo team" in design
    assert "owner: LIMA repo team" in design
    assert "still design-only unless separately approved" in design


def test_forbidden_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text()))

    for action in fixture["forbidden_actions"]:
        assert action in combined

    assert "This design must not trigger:" in combined


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
        == "audit-lima-consumer-proof-audit-execution-packet-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
