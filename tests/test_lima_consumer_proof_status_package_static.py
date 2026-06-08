from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_status_package"
    / "consumer_proof_status_package.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _package_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["package_path"]).read_text(encoding="utf-8")


def _audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def _static_tests_audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["static_tests_audit_path"]).read_text(encoding="utf-8")


def test_consumer_proof_status_package_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_status_package_only"
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
    assert fixture["consumer_branch_pushed"] is False
    assert fixture["consumer_proof_packet_received"] is False
    assert fixture["consumer_proof_packet_audited"] is False
    assert fixture["receipt_ledger_updated"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_consumer_proof_status_package_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "package_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_consumer_proof_status_package_verdict_stays_waiting() -> None:
    fixture = _load_fixture()
    package = _package_text()
    audit = _audit_text()

    assert fixture["current_package_verdict"] == "waiting_for_consumer_proof_packets"
    assert "`waiting_for_consumer_proof_packets`" in package
    assert "not proven consumers yet" in package
    assert "waiting_for_consumer_proof_packets" in audit

    for blocker in fixture["current_blockers"]:
        assert blocker in package


def test_consumer_proof_status_package_references_source_artifacts_without_overriding() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for path in fixture["source_artifacts"]:
        assert f"`{path}`" in package
        assert (REPO_ROOT / path).exists(), path

    assert "If this package conflicts with a source artifact, the source artifact controls." in package


def test_consumer_proof_status_package_requires_sparkbot_packet_evidence() -> None:
    fixture = _load_fixture()
    package = _package_text()

    assert "`sparkbot-lima-dry-run-boundary-proof`" in package
    for field in fixture["required_sparkbot_packet_fields"]:
        assert field in package
    for evidence in fixture["sparkbot_specific_evidence"]:
        assert evidence in package


def test_consumer_proof_status_package_requires_arc_packet_evidence() -> None:
    fixture = _load_fixture()
    package = _package_text()

    assert "`arc-lima-dry-run-boundary-proof`" in package
    for field in fixture["required_arc_packet_fields"]:
        assert field in package
    for evidence in fixture["arc_specific_evidence"]:
        assert evidence in package


def test_consumer_proof_status_package_limits_public_imports() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for import_line in fixture["allowed_proof_public_imports"]:
        assert f"`{import_line}`" in package
    for import_line in fixture["forbidden_consumer_imports"]:
        assert f"`{import_line}`" in package

    assert "dry_run_candidate" in package
    assert "without explicit LIMA-side follow-up review" in package


def test_consumer_proof_status_package_preserves_proof_shape_and_repo_boundary() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for line in fixture["required_proof_shape_lines"]:
        assert line in package

    assert "LIMA must not create the consumer branch." in package
    assert "LIMA must not push consumer proof code." in package
    assert "LIMA must not fetch, clone, scan, or inspect consumer repositories without explicit approval." in package


def test_consumer_proof_status_package_requires_non_execution_invariants() -> None:
    fixture = _load_fixture()
    package = _package_text()
    audit = _audit_text()

    for invariant in fixture["required_non_execution_invariants"]:
        assert f"`{invariant}`" in package

    assert "Missing invariant evidence means the packet is not ready for proof acceptance." in package
    assert "Contradictory invariant evidence must be treated as a runtime boundary blocker." in package
    assert "no physical-world execution" in audit


def test_consumer_proof_status_package_requires_redaction_gate() -> None:
    fixture = _load_fixture()
    package = _package_text()
    audit = _audit_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in package

    assert "`needs_redaction_before_review`" in package
    assert "redaction before LIMA-side archive or audit" in audit


def test_consumer_proof_status_package_declares_safe_and_forbidden_statuses() -> None:
    fixture = _load_fixture()
    package = _package_text()
    audit = _audit_text()

    for status in fixture["allowed_response_statuses"]:
        assert f"`{status}`" in package
    for status in fixture["allowed_audit_statuses"]:
        assert f"`{status}`" in package
    for status in fixture["forbidden_statuses"]:
        assert f"`{status}`" in package

    assert "That status does not mean production readiness." in package
    assert "pass_for_dry_run_dependency_proof" in audit


def test_consumer_proof_status_package_forbids_product_runtime_and_physical_world_claims() -> None:
    fixture = _load_fixture()
    package = _package_text()
    audit = _audit_text()

    for interpretation in fixture["forbidden_package_interpretations"]:
        assert interpretation in package

    assert "No forbidden surface is approved by the package." in audit


def test_consumer_proof_status_package_keeps_product_blockers_visible() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for blocker in fixture["current_product_blockers"]:
        assert blocker in package

    assert "Sparkbot and Arc Bot remain blocked from product use" in package


def test_consumer_proof_status_package_static_tests_audit_bounds_later_files_and_surfaces() -> None:
    fixture = _load_fixture()
    static_tests_audit = _static_tests_audit_text()

    for path in fixture["allowed_later_static_files"]:
        assert f"`{path}`" in static_tests_audit
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in static_tests_audit


def test_consumer_proof_status_package_static_tests_recommend_independent_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == "audit-lima-consumer-proof-status-package-static-tests"
