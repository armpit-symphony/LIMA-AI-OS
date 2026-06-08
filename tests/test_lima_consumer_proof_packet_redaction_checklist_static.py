from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_packet_redaction_checklist"
    / "consumer_proof_packet_redaction_checklist.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _checklist_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["checklist_path"]).read_text(encoding="utf-8")


def _audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def test_redaction_checklist_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_packet_redaction_checklist_only"
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_proof_packet_audited"] is False
    assert fixture["redaction_engine_added"] is False
    assert fixture["redaction_scanner_added"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_redaction_checklist_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in ("checklist_path", "readiness_review_path", "audit_path"):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_redaction_checklist_declares_attestation_fields() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for field in fixture["required_redaction_attestation_fields"]:
        assert f"`{field}`" in checklist
    assert "`needs_redaction_before_review`" in checklist


def test_redaction_checklist_declares_allowed_and_forbidden_statuses() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for status in fixture["allowed_redaction_statuses"]:
        assert f"`{status}`" in checklist
    for status in fixture["forbidden_statuses"]:
        assert f"`{status}`" in checklist
    assert fixture["required_production_readiness"] == "not_production_ready"
    assert "`not_production_ready`" in checklist


def test_redaction_checklist_blocks_sensitive_categories_before_archive() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for blocker in fixture["blocker_categories"]:
        assert blocker in checklist
    assert "`blocked_unredacted_sensitive_evidence`" in checklist
    assert "stop before archive or proof audit" in checklist


def test_redaction_checklist_limits_acceptable_evidence_to_redacted_or_inert_refs() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for example in fixture["acceptable_evidence_examples"]:
        assert example in checklist
    assert "summaries, references, hashes, or inert examples" in checklist
    assert "`needs_human_redaction_review`" in checklist


def test_redaction_checklist_blocks_sparkbot_sensitive_evidence() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for blocker in fixture["sparkbot_blockers"]:
        assert blocker in checklist
    assert "absence of Sparkbot route wiring" in checklist
    assert "absence of Sparkbot task/message mutation" in checklist


def test_redaction_checklist_blocks_arc_bot_sensitive_evidence() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for blocker in fixture["arc_bot_blockers"]:
        assert blocker in checklist
    assert "absence of Arc route wiring" in checklist
    assert "absence of task, project, note, form, record, or customer file mutation" in checklist


def test_redaction_checklist_blocks_connection_device_and_physical_world_evidence() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for blocker in fixture["connection_device_physical_world_blockers"]:
        assert blocker in checklist
    for statement in fixture["acceptable_non_execution_statements"]:
        assert statement in checklist


def test_redaction_checklist_decision_flow_is_fail_closed() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for phrase in fixture["decision_flow_required_phrases"]:
        assert phrase in checklist


def test_redaction_checklist_forbids_reviewer_runtime_and_repo_actions() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for action in fixture["forbidden_reviewer_actions"]:
        assert action in checklist


def test_redaction_checklist_preserves_compatibility_freeze_boundary() -> None:
    fixture = _load_fixture()
    checklist = _checklist_text()

    for claim in fixture["compatibility_freeze_non_claims"]:
        assert claim in checklist
    assert "Compatibility freeze remains blocked" in checklist


def test_redaction_checklist_audit_confirms_no_runtime_or_product_approval() -> None:
    audit = _audit_text()

    assert "does not implement redaction, scanning, parsing, proof intake" in audit
    assert "does not approve proof packet audit, compatibility freeze" in audit
    assert "It does not approve proof packet audit" in audit


def test_redaction_checklist_recommends_independent_static_test_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == "audit-lima-consumer-proof-packet-redaction-checklist-static-tests"
