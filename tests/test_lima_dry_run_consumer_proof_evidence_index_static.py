from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "dry_run_consumer_proof_evidence_index"
    / "evidence_index.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _design_text() -> str:
    return _text("evidence_index_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_evidence_index_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_dry_run_consumer_proof_evidence_index_only"
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


def test_evidence_index_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "evidence_index_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_evidence_index_preserves_current_missing_state() -> None:
    fixture = _load_fixture()
    design = _design_text()
    review = _review_text()
    audit = _audit_text()
    combined = "\n".join((design, review, audit))

    assert (
        fixture["current_closeout_verdict"]
        == "lima_local_prerequisites_closed_waiting_on_consumer_proof"
    )
    assert f"`{fixture['current_closeout_verdict']}`" in combined
    assert f"`{fixture['current_freeze_state']}`" in combined
    assert f"`{fixture['current_product_state']}`" in combined

    for state in fixture["current_missing_inputs"].values():
        assert f"`{state}`" in combined

    assert "The index must start empty because no consumer-owned proof packet has been supplied." in design


def test_evidence_index_references_source_artifacts() -> None:
    fixture = _load_fixture()
    design = _design_text()
    audit = _audit_text()
    combined = "\n".join((design, audit))

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in combined

    assert "the stricter artifact controls" in design


def test_evidence_index_entry_shape_is_reference_only() -> None:
    fixture = _load_fixture()
    design = _design_text()
    audit = _audit_text()
    combined = "\n".join((design, audit))

    for field in fixture["index_entry_fields"]:
        assert field in combined

    assert "The index must store references and redacted summaries only." in design
    assert "It must not store raw proof evidence." in design
    assert "not raw proof evidence" in audit


def test_evidence_index_allowed_values_are_bounded() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for value in fixture["allowed_consumer_repos"]:
        assert f"`{value}`" in design
    for state in fixture["allowed_proof_packet_received_states"]:
        assert f"`{state}`" in design
    for state in fixture["allowed_redaction_states"]:
        assert f"`{state}`" in design
    for state in fixture["allowed_lima_side_audit_states"]:
        assert f"`{state}`" in design
    for state in fixture["allowed_result_gate_input_states"]:
        assert f"`{state}`" in design

    assert "Required `compatibility_freeze_state` value until both audits pass" in design
    assert "Required `product_readiness` value" in design


def test_evidence_index_forbidden_values_block_product_claims() -> None:
    fixture = _load_fixture()
    design = _design_text()
    review = _review_text()
    audit = _audit_text()
    combined = "\n".join((design, review, audit))

    for value in fixture["forbidden_index_values"]:
        assert f"`{value}`" in combined

    assert "Forbidden Index Values" in design


def test_evidence_index_public_api_boundary_is_proof_public_only() -> None:
    fixture = _load_fixture()
    design = _design_text()
    review = _review_text()
    audit = _audit_text()
    combined = "\n".join((design, review, audit))

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in combined

    for forbidden in fixture["forbidden_public_import_claims"]:
        assert forbidden in combined

    assert "No public exports are changed." in audit


def test_evidence_index_requires_non_execution_invariants() -> None:
    fixture = _load_fixture()
    design = _design_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in design

    assert "Missing evidence must keep the entry at `needs_missing_evidence` or `not_ready_for_result_gate`." in design
    assert "Contradictory evidence must become `blocked_by_runtime_boundary`." in design


def test_evidence_index_blocks_unredacted_sensitive_content() -> None:
    fixture = _load_fixture()
    design = _design_text()
    review = _review_text()
    audit = _audit_text()
    combined = "\n".join((design, review, audit))

    for blocker in fixture["redaction_blockers"]:
        assert blocker in combined

    assert "must not copy the sensitive content into the LIMA repo" in combined


def test_evidence_index_preserves_consumer_specific_boundaries() -> None:
    fixture = _load_fixture()
    design = _design_text()

    for branch in fixture["consumer_owned_branches"].values():
        assert f"`{branch}`" in design

    for requirement in fixture["sparkbot_evidence_requirements"]:
        assert requirement in design
    for requirement in fixture["arc_bot_evidence_requirements"]:
        assert requirement in design

    assert "If consumer-specific evidence is missing, the index state must remain `needs_missing_evidence`." in design


def test_evidence_index_lifecycle_is_human_reviewed_and_non_persistent() -> None:
    fixture = _load_fixture()
    design = _design_text()
    audit = _audit_text()
    combined = "\n".join((design, audit))

    for state in fixture["lifecycle_states"]:
        assert f"`{state}`" in combined
    for behavior in fixture["forbidden_lifecycle_behaviors"]:
        assert behavior in combined

    assert "human-reviewed" in combined
    assert "durable persistence unless separately designed and approved" in design


def test_empty_index_example_remains_not_received_and_not_ready() -> None:
    fixture = _load_fixture()
    design = _design_text()
    audit = _audit_text()
    combined = "\n".join((design, audit))

    for state in fixture["empty_index_required_states"].values():
        assert state in combined

    assert "This branch may describe an empty index only:" in design
    assert "This is not a received proof packet and not an archive." in design


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
        == "audit-lima-dry-run-consumer-proof-evidence-index-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
