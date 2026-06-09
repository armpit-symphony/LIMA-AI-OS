from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_packet_request"
    / "consumer_proof_packet_request.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _design_text() -> str:
    return _text("request_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_request_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_packet_request_only"
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_exports_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_branch_created"] is False
    assert fixture["request_sent"] is False
    assert fixture["external_send_added"] is False
    assert fixture["webhook_added"] is False
    assert fixture["email_or_chat_send_added"] is False
    assert fixture["issue_or_pr_creation_added"] is False
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


def test_request_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "request_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_request_preserves_current_missing_state() -> None:
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


def test_request_references_source_artifacts() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text()))

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in combined

    assert "the stricter artifact controls" in _design_text()


def test_request_delivery_boundary_is_manual_only() -> None:
    fixture = _load_fixture()
    design = _design_text()

    assert "Delivery must remain manual and operator-controlled." in design
    for item in fixture["request_delivery_allowed_items"]:
        assert item in design
    for item in fixture["request_delivery_forbidden_items"]:
        assert item in design


def test_request_packet_shape_is_reference_only_and_not_ready() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for field in fixture["request_packet_fields"]:
        assert field in design
    for field, value in fixture["request_packet_required_values"].items():
        assert f"{field}: {value}" in design

    assert "The request packet must contain instructions and references only." in design
    assert "It must not contain raw proof evidence" in design


def test_request_targets_consumer_owned_branches() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    for consumer in fixture["target_consumers"]:
        assert consumer in combined
    for branch in fixture["consumer_branch_requests"].values():
        assert f"`{branch}`" in combined

    assert "LIMA does not create, modify, fetch, clone, scan, or inspect those branches." in combined


def test_request_included_artifacts_are_local_docs() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for path in fixture["included_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in design

    assert "The operator must not include raw proof packet contents" in design


def test_manual_delivery_warning_preserves_boundary() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for fragment in fixture["manual_delivery_warning_fragments"]:
        assert fragment in design

    assert "Do not wire production routes." in design
    assert "dry-run ExecutionResult out" in design


def test_sparkbot_and_arc_manual_request_texts_are_bounded() -> None:
    design = _design_text()

    assert "Please create `sparkbot-lima-dry-run-boundary-proof` in the Sparkbot repo." in design
    assert "Please create `arc-lima-dry-run-boundary-proof` in the Arc Bot / LIMA Office repo." in design
    assert "Use only proof-public LIMA imports." in design
    assert "Call `LimaKernel.evaluate(...)` with a default-deny capability profile." in design
    assert "Optionally use `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata." in design
    assert "Return a redacted proof packet using `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`." in design
    assert "Do not wire public routes" in design
    assert "Do not wire production office routes" in design


def test_public_api_boundary_preserves_proof_public_imports() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text()))

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in combined
    for forbidden in fixture["forbidden_public_import_claims"]:
        assert forbidden in combined

    assert "No public exports are changed." in combined


def test_returned_proof_packet_requirements_are_complete() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for requirement in fixture["returned_proof_packet_requirements"]:
        assert requirement in design

    assert f"`{fixture['allowed_repo_team_proof_verdict']}`" in design
    assert "does not mean product readiness" in design
    assert "dependency-use approval" in design


def test_non_execution_invariant_requirements_are_complete() -> None:
    fixture = _load_fixture()
    design = _design_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in design

    assert "Missing evidence remains `needs_missing_evidence`." in design
    assert "Contradictory execution evidence remains `blocked_by_runtime_boundary`." in design


def test_redaction_rules_block_sensitive_content() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    for blocker in fixture["redaction_blockers"]:
        assert blocker in combined

    assert "the packet must be redacted before LIMA-side review" in combined


def test_consumer_specific_requirements_preserve_sparkbot_and_arc_boundaries() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for requirement in fixture["sparkbot_evidence_requirements"]:
        assert requirement in design
    for requirement in fixture["arc_bot_evidence_requirements"]:
        assert requirement in design


def test_after_manual_delivery_keeps_waiting_state_without_packet() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for state in fixture["after_manual_delivery_without_packet_states"].values():
        assert f"`{state}`" in design

    assert "If the operator manually delivers the request and no packet is supplied:" in design


def test_after_packet_supplied_remains_future_review_only() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for step in fixture["after_packet_supplied_steps"]:
        assert step in design

    assert "If a proof packet is supplied:" in design


def test_forbidden_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text()))

    for action in fixture["forbidden_actions"]:
        assert action in combined

    assert "This request contract must not trigger:" in combined


def test_static_fixture_paths_do_not_reference_live_or_external_surfaces() -> None:
    fixture = _load_fixture()
    serialized = json.dumps(fixture, sort_keys=True)

    forbidden_path_fragments = (
        "http://",
        "https://",
        "app://",
        "file://",
        "socket://",
        "public/Sparkbot",
        "public/Sparkbot/",
        "Sparkbot/",
        "Arc Bot/",
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

    assert fixture["recommended_next_branch"] == "audit-lima-consumer-proof-packet-request-static-tests"
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
