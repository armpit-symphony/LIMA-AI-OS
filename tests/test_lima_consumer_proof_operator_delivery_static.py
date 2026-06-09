from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_operator_delivery"
    / "consumer_proof_operator_delivery.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _operator_delivery_text() -> str:
    return _text("operator_delivery_design_path")


def _operator_delivery_audit_text() -> str:
    return _text("operator_delivery_audit_path")


def _static_tests_design_text() -> str:
    return _text("static_tests_design_path")


def _static_tests_design_audit_text() -> str:
    return _text("static_tests_design_audit_path")


def _implementation_audit_text() -> str:
    return _text("static_tests_audit_path")


def _normal(text: str) -> str:
    normalized = " ".join(text.split())
    return normalized.replace("/ ", "/").replace(" /", "/")


def _assert_contains_normalized(text: str, expected: str) -> None:
    assert _normal(expected) in _normal(text)


def test_operator_delivery_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_operator_delivery_only"
    assert fixture["automated_delivery_added"] is False
    assert fixture["external_send_added"] is False
    assert fixture["proof_packet_created"] is False
    assert fixture["proof_packet_received"] is False
    assert fixture["proof_packet_archived"] is False
    assert fixture["proof_packet_audited"] is False
    assert fixture["response_sending_added"] is False
    assert fixture["ledger_persistence_added"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_repo_modified"] is False
    assert fixture["consumer_branch_created_by_lima"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_exports_changed"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_operator_delivery_static_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "operator_delivery_design_path",
        "operator_delivery_readiness_review_path",
        "operator_delivery_audit_path",
        "static_tests_design_path",
        "static_tests_readiness_review_path",
        "static_tests_design_audit_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_operator_delivery_source_artifacts_exist_and_remain_strict() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()
    design_audit = _static_tests_design_audit_text()

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in design

    assert "the stricter source artifact controls" in operator_delivery
    assert "the stricter source artifact must control" in design
    assert "The stricter-source rule remains in force" in design_audit


def test_operator_delivery_verdict_and_current_state_remain_waiting() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()
    state = fixture["current_state"]

    assert fixture["operator_delivery_verdict"] == "ready_for_manual_operator_delivery_request_only"
    assert f"`{fixture['operator_delivery_verdict']}`" in operator_delivery
    assert f"operator-delivery verdict: `{fixture['operator_delivery_verdict']}`" in design
    assert state["delivery_status"] == "manual_operator_delivery_request_only"
    assert state["sparkbot_proof_packet"] == "not_received"
    assert state["arc_bot_proof_packet"] == "not_received"
    assert state["proof_archive_status"] == "not_started"
    assert state["proof_audit_status"] == "not_started"
    assert state["compatibility_freeze"] == "blocked"
    assert state["product_readiness"] == "not_production_ready"
    assert "Sparkbot and Arc proof packets remain missing until supplied by their repo teams" in design


def test_manual_delivery_artifacts_remain_lima_local_docs_only() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()

    for artifact in fixture["manual_delivery_artifacts"]:
        assert artifact in operator_delivery

    assert "manual delivery artifacts remain LIMA-local documentation and templates only" in design
    assert "The operator must not deliver:" in operator_delivery
    assert "raw proof packet contents" in operator_delivery
    assert "credentials" in operator_delivery
    assert "physical-world actuator payloads" in operator_delivery


def test_manual_delivery_warning_remains_proof_only_and_dry_run_only() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()

    for warning_line in fixture["manual_delivery_warning"]:
        _assert_contains_normalized(operator_delivery, warning_line)

    assert "Do not wire production routes." in operator_delivery
    assert "The first proof is normalized metadata in and dry-run ExecutionResult out." in operator_delivery


def test_sparkbot_operator_request_remains_dry_run_only() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    request = fixture["sparkbot_operator_request"]

    assert f"`{request['branch']}`" in operator_delivery
    for phrase in request["required_boundary_phrases"]:
        assert phrase in operator_delivery
    for forbidden_surface in request["forbidden_surfaces"]:
        _assert_contains_normalized(operator_delivery, forbidden_surface)


def test_arc_bot_operator_request_remains_dry_run_only() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    request = fixture["arc_bot_operator_request"]

    assert f"`{request['branch']}`" in operator_delivery
    for phrase in request["required_boundary_phrases"]:
        assert phrase in operator_delivery
    for forbidden_surface in request["forbidden_surfaces"]:
        _assert_contains_normalized(operator_delivery, forbidden_surface)


def test_required_returned_evidence_and_verdict_remain_non_production() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()

    for evidence in fixture["required_returned_evidence"]:
        assert evidence in operator_delivery

    assert fixture["allowed_proof_verdict"] == "pass_for_dry_run_dependency_proof"
    assert f"`{fixture['allowed_proof_verdict']}`" in operator_delivery
    assert "That verdict does not mean production readiness." in operator_delivery
    assert "`pass_for_dry_run_dependency_proof` remains non-production" in design


def test_non_execution_invariants_remain_required() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()
    invariants = fixture["non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in operator_delivery

    assert "Missing evidence remains `needs_missing_evidence`." in operator_delivery
    assert "Contradictory execution evidence remains `blocked_by_runtime_boundary`." in operator_delivery
    assert "non-execution invariants remain listed" in design


def test_redaction_blockers_remain_required() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in design

    assert "raw proof packet contents" in operator_delivery
    assert "The operator must not deliver:" in operator_delivery
    assert "Unsafe returned packets must remain classified as:" in design
    assert "`needs_redaction_before_review`" in design


def test_delivery_controls_keep_archive_audit_and_freeze_later_only() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()

    for control in fixture["delivery_controls"]:
        assert control in operator_delivery

    assert "proof archive and audit happen only in later approved branches" in design
    assert "Sparkbot and Arc packets are audited separately" in design
    assert "compatibility freeze remains blocked until both proof audits pass" in design
    assert "production readiness remains blocked" in design


def test_forbidden_claims_remain_blocked() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()
    design_audit = _static_tests_design_audit_text()

    assert "This operator delivery design must not be described as:" in operator_delivery
    for claim in fixture["forbidden_claims"]:
        assert claim in operator_delivery
        assert claim in design

    assert "forbidden claims" in design_audit
    assert "product use" in design_audit
    assert "production use" in design_audit


def test_forbidden_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    operator_delivery = _operator_delivery_text()
    design = _static_tests_design_text()
    design_audit = _static_tests_design_audit_text()

    assert "This operator delivery design must not trigger:" in operator_delivery
    for action in fixture["forbidden_actions"]:
        assert action in operator_delivery
        assert action in design

    assert "Forbidden Surface Review" in design_audit
    assert "runtime behavior" in design_audit
    assert "model/tool/connector execution" in design_audit


def test_later_implementation_files_and_surfaces_remain_bounded() -> None:
    fixture = _load_fixture()
    design = _static_tests_design_text()
    design_audit = _static_tests_design_audit_text()
    implementation_audit = _implementation_audit_text()

    for path in fixture["allowed_later_files"]:
        assert f"`{path}`" in design
        assert f"`{path}`" in design_audit
        assert f"`{path}`" in implementation_audit

    for design_surface in (
        "lima/",
        "tests/support/",
        "pyproject.toml",
        "Sparkbot",
        "Arc Bot",
        "provider/model",
        "adapters",
        "connectors",
        "live discovery",
        "physical-world behavior",
    ):
        assert design_surface in design

    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in design_audit
        assert surface in implementation_audit


def test_fixture_paths_do_not_reference_live_or_external_surfaces() -> None:
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


def test_static_tests_implementation_recommends_independent_audit() -> None:
    fixture = _load_fixture()
    implementation_audit = _implementation_audit_text()

    assert fixture["recommended_next_branch"] == (
        "audit-lima-consumer-proof-operator-delivery-static-tests-implementation"
    )
    assert f"`{fixture['recommended_next_branch']}`" in implementation_audit
    assert fixture["independent_audit_path"].endswith(
        "LIMA_CONSUMER_PROOF_OPERATOR_DELIVERY_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md"
    )
