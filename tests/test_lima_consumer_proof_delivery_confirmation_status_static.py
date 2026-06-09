from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_delivery_confirmation_status"
    / "consumer_proof_delivery_confirmation_status.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _design_text() -> str:
    return _text("design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def _one_line(text: str) -> str:
    return " ".join(text.split())


def test_delivery_confirmation_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_delivery_confirmation_status_only"
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_exports_changed"] is False
    assert fixture["actual_delivery_confirmation_recorded"] is False
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
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_branch_created"] is False


def test_delivery_confirmation_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_delivery_confirmation_design_preserves_current_state() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    assert fixture["current_closeout_verdict"] == "lima_local_prerequisites_closed_waiting_on_consumer_proof"
    assert f"`{fixture['current_closeout_verdict']}`" in combined
    assert f"`{fixture['current_freeze_state']}`" in combined
    assert f"`{fixture['current_product_state']}`" in combined

    for state in fixture["current_branch_status"].values():
        assert f"`{state}`" in combined


def test_design_records_no_actual_confirmation_in_this_branch() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    assert fixture["actual_delivery_confirmation_recorded"] is False
    assert "This branch does not record delivery confirmation." in combined
    assert "It does not claim that manual delivery happened in the design branch." in combined
    assert "does not record actual delivery confirmation" in combined


def test_future_confirmation_preconditions_are_explicit_and_human_only() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    for precondition in fixture["future_confirmation_preconditions"]:
        assert precondition in combined

    assert "The confirmation must be human-supplied." in combined
    assert "automated webhook" in combined
    assert "consumer repository scan" in combined
    assert "operator-controlled channel outside LIMA automation" in combined


def test_status_shape_is_reference_only_and_complete() -> None:
    fixture = _load_fixture()
    design = _design_text()
    review = _review_text()

    for field in fixture["status_shape_fields"]:
        assert field in design

    assert "reference-only canonical shape" in design
    assert "redacted summaries and references only" in design
    assert "The canonical status shape is reference-only" in review


def test_allowed_delivery_confirmation_states_are_bounded() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    for state in fixture["allowed_delivery_confirmation_states"]:
        assert f"`{state}`" in combined

    assert "Allowed `delivery_confirmation_state` values" in combined


def test_confirmation_without_packet_required_states_are_pinned() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for field, state in fixture["confirmation_without_packet_required_states"].items():
        assert f"`{field}: {state}`" in design

    assert "If the operator confirms manual delivery and no proof packets are supplied:" in design


def test_forbidden_status_values_do_not_approve_product_or_runtime_readiness() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text()))

    for status_value in fixture["forbidden_status_values"]:
        assert f"`{status_value}`" in combined

    assert "Manual delivery confirmation is only evidence that the request was delivered." in combined
    assert "It is not proof that LIMA is usable by Sparkbot or Arc Bot." in _one_line(combined)


def test_proof_packet_boundary_stays_separate() -> None:
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    assert "If a proof packet is supplied instead of a no-packet confirmation" in combined
    assert "this design is no longer the right next step" in combined
    assert "redaction review and LIMA-side proof audit in a separate approved branch" in combined
    assert "does not receive, archive, audit, evaluate, or run a result gate" in combined


def test_redaction_boundary_blocks_sensitive_content() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    for blocker in fixture["redaction_blockers"]:
        assert blocker in combined

    assert "`rejected_for_redaction_boundary`" in combined
    assert "sensitive material must not be copied into the LIMA repo" in _one_line(combined)


def test_consumer_repo_boundary_remains_closed() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    for action in fixture["consumer_repo_forbidden_actions"]:
        assert action in combined

    assert "`sparkbot-lima-dry-run-boundary-proof`" in combined
    assert "`arc-lima-dry-run-boundary-proof`" in combined
    assert "Consumer proof branches remain owned by their repo teams" in combined


def test_result_gate_freeze_and_product_readiness_remain_blocked() -> None:
    combined = "\n".join((_design_text(), _review_text(), _audit_text()))

    assert "Manual delivery confirmation does not make LIMA ready for the dual-consumer result gate." in combined
    assert "`not_ready_for_result_gate`" in combined
    assert "`not_ready_for_freeze`" in combined
    assert "`not_production_ready`" in combined
    assert (
        "until both Sparkbot and Arc Bot redacted proof packets are supplied and pass LIMA-side audits"
        in _one_line(combined)
    )


def test_forbidden_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text()))

    for action in fixture["forbidden_actions"]:
        assert action in combined

    assert "This confirmation status design must not trigger:" in combined


def test_later_static_implementation_allowed_files_are_exact() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _audit_text(), _static_tests_audit_text()))

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in combined

    assert "A later static implementation branch may add only:" in combined
    assert "This branch adds only the allowed static fixture, static pytest module, and implementation audit." in combined


def test_later_static_implementation_forbidden_surfaces_are_bounded() -> None:
    fixture = _load_fixture()
    static_tests_audit = _static_tests_audit_text()

    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in static_tests_audit

    assert "The implementation remains static and non-executing." in static_tests_audit


def test_static_fixture_paths_do_not_reference_live_or_external_surfaces() -> None:
    fixture = _load_fixture()
    serialized = json.dumps(fixture, sort_keys=True)

    forbidden_path_fragments = (
        "http://",
        "https://",
        "app://",
        "file://",
        "socket://",
        "Sparkbot/",
        "Arc Bot/",
    )

    for fragment in forbidden_path_fragments:
        assert fragment not in serialized


def test_static_tests_recommend_independent_audit() -> None:
    fixture = _load_fixture()
    static_tests_audit = _static_tests_audit_text()

    assert fixture["recommended_next_branch"] == (
        "audit-lima-consumer-proof-delivery-confirmation-status-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
