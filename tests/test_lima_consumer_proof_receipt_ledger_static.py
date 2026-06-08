from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_receipt_ledger"
    / "consumer_proof_receipt_ledger.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _ledger_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["ledger_path"]).read_text(encoding="utf-8")


def _audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def test_receipt_ledger_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_receipt_ledger_only"
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_proof_packet_audited"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_receipt_ledger_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in ("ledger_path", "readiness_review_path", "audit_path"):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_receipt_ledger_current_packet_state_stays_missing_and_blocked() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()
    audit = _audit_text()

    assert fixture["current_ledger_verdict"] == "no_consumer_packets_received"
    assert "`no_consumer_packets_received`" in ledger

    for label, state in fixture["current_packet_states"].items():
        assert state in {"not_received", "not_started", "blocked"}, label
        assert f"`{state}`" in ledger

    assert "The design does not claim that consumer proof packets have been received" in audit
    assert "Compatibility freeze: `blocked`" in audit


def test_receipt_ledger_declares_required_entry_fields() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()

    for field in fixture["required_entry_fields"]:
        assert f"`{field}`" in ledger


def test_receipt_ledger_declares_allowed_status_vocabularies() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()

    for status in fixture["allowed_redaction_statuses"]:
        assert f"`{status}`" in ledger
    for status in fixture["allowed_intake_statuses"]:
        assert f"`{status}`" in ledger
    for status in fixture["allowed_audit_statuses"]:
        assert f"`{status}`" in ledger

    assert fixture["required_production_readiness"] == "not_production_ready"
    assert "`not_production_ready`" in ledger


def test_receipt_ledger_declares_forbidden_statuses() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()
    audit = _audit_text()

    for status in fixture["forbidden_statuses"]:
        assert f"`{status}`" in ledger
    assert "forbids status values that would imply production readiness" in audit


def test_receipt_ledger_initial_entries_stay_pending() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()

    for receipt_id in fixture["pending_receipt_ids"]:
        assert f"receipt_id: {receipt_id}" in ledger
    for branch in fixture["consumer_branches"].values():
        assert f"consumer_branch: {branch}" in ledger
    for evidence in fixture["required_missing_evidence"]:
        assert evidence in ledger

    assert "reviewer_notes: LIMA has not received the Sparkbot proof packet." in ledger
    assert "reviewer_notes: LIMA has not received the Arc Bot proof packet." in ledger


def test_receipt_ledger_requires_redaction_blockers() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in ledger
    assert "`needs_redaction_before_review`" in ledger


def test_receipt_ledger_keeps_compatibility_freeze_blocked_until_all_inputs_pass() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()

    for requirement in fixture["freeze_requirements"]:
        assert requirement in ledger
    assert "Current freeze status:" in ledger
    assert "`blocked`" in ledger


def test_receipt_ledger_forbids_automation_storage_and_live_surfaces() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()

    for behavior in fixture["forbidden_ledger_behaviors"]:
        assert behavior in ledger


def test_receipt_ledger_forbids_consumer_repo_and_runtime_reviewer_actions() -> None:
    fixture = _load_fixture()
    ledger = _ledger_text()

    for action in fixture["forbidden_reviewer_actions"]:
        assert action in ledger


def test_receipt_ledger_static_test_audit_bounds_later_files_and_surfaces() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    for path in fixture["allowed_later_static_files"]:
        assert f"`{path}`" in audit
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in audit


def test_receipt_ledger_recommends_independent_static_test_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == "audit-lima-consumer-proof-receipt-ledger-static-tests"
