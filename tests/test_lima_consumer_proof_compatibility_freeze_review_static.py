from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_compatibility_freeze_review"
    / "consumer_proof_compatibility_freeze_review.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _review_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["review_path"]).read_text(encoding="utf-8")


def _audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def _static_tests_audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["static_tests_audit_path"]).read_text(encoding="utf-8")


def _public_api_fixture() -> Mapping[str, Any]:
    fixture = _load_fixture()
    return json.loads(
        (REPO_ROOT / fixture["public_api_manifest_fixture_path"]).read_text(encoding="utf-8")
    )


def test_freeze_review_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_compatibility_freeze_review_only"
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
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_freeze_review_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "review_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_freeze_review_references_authoritative_artifacts() -> None:
    fixture = _load_fixture()
    review = _review_text()

    for path in fixture["required_source_artifacts"]:
        assert f"`{path}`" in review
        assert (REPO_ROOT / path).exists(), path

    assert "If this review conflicts with any source artifact, the stricter artifact controls." in review


def test_freeze_review_current_verdict_remains_blocked() -> None:
    fixture = _load_fixture()
    review = _review_text()
    audit = _audit_text()

    assert fixture["current_review_verdict"] == "freeze_review_blocked"
    assert "`freeze_review_blocked`" in review
    assert "The current review status remains blocked." in audit

    for reason in fixture["blocked_reasons"]:
        assert reason in review


def test_freeze_review_requires_all_inputs_before_pass() -> None:
    fixture = _load_fixture()
    review = _review_text()

    for input_id in fixture["required_review_inputs"]:
        assert f"`{input_id}`" in review

    assert "If any input is missing, contradictory, stale, or unredacted" in review
    assert "`accepted_for_dry_run_proof_audit`" in review
    assert "`pass_for_dry_run_dependency_proof`" in review
    assert "`passed_redaction_review`" in review


def test_freeze_review_status_language_is_narrow_and_non_product() -> None:
    fixture = _load_fixture()
    review = _review_text()

    for status in fixture["allowed_review_statuses"]:
        assert f"`{status}`" in review
    for status in fixture["forbidden_review_statuses"]:
        assert f"`{status}`" in review

    assert "does not mean a freeze exists" in review
    assert "can use LIMA in product" in review


def test_freeze_review_public_api_matches_proof_public_manifest_entries() -> None:
    fixture = _load_fixture()
    review = _review_text()
    public_api = _public_api_fixture()

    manifest_proof_imports = {
        entry["import"]
        for entry in public_api["public_imports"]
        if entry["classification"] == "proof_public"
    }
    assert set(fixture["proof_public_imports"]) == manifest_proof_imports

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in review

    assert "must not promote `dry_run_candidate` imports" in review
    assert "top-level runtime re-exports" in review


def test_freeze_review_blocks_internal_and_forbidden_consumer_imports() -> None:
    fixture = _load_fixture()
    review = _review_text()
    public_api = _public_api_fixture()

    manifest_blocked = set(public_api["forbidden_consumer_imports"])
    manifest_blocked.update(public_api["experimental_internal_modules"])
    assert set(fixture["forbidden_consumer_imports"]) == manifest_blocked

    for import_pattern in fixture["forbidden_consumer_imports"]:
        assert f"`{import_pattern}`" in review


def test_freeze_review_allows_lifecycle_preview_only_as_method_candidate() -> None:
    fixture = _load_fixture()
    review = _review_text()

    for candidate in fixture["method_level_candidates"]:
        assert f"`{candidate}`" in review

    assert "method-level dry-run candidate" in review
    assert "lifecycle preview result dataclasses" in review


def test_freeze_review_requires_current_non_execution_invariants() -> None:
    fixture = _load_fixture()
    review = _review_text()
    public_api = _public_api_fixture()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants == public_api["required_non_execution_invariants"]
    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in review

    assert "`blocked_by_runtime_boundary`" in review


def test_freeze_review_blocks_redaction_sensitive_evidence() -> None:
    fixture = _load_fixture()
    review = _review_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in review

    assert "Unredacted evidence must not be archived or used as freeze evidence." in review


def test_freeze_review_requires_sparkbot_and_arc_boundary_evidence() -> None:
    fixture = _load_fixture()
    review = _review_text()

    for requirement in fixture["sparkbot_freeze_review_requirements"]:
        assert requirement in review
    for requirement in fixture["arc_freeze_review_requirements"]:
        assert requirement in review


def test_freeze_review_decision_table_is_fail_closed() -> None:
    fixture = _load_fixture()
    review = _review_text()

    for status in fixture["decision_statuses"]:
        assert f"`{status}`" in review

    assert "Either packet is missing" in review
    assert "Either proof audit reports runtime behavior" in review
    assert "Public API manifest changed after proof audits" in review
    assert "Both proof audits pass and all blockers are clear" in review


def test_freeze_review_future_design_boundary_stays_static() -> None:
    review = _review_text()

    assert "may only design a static compatibility freeze" in review
    assert "frozen proof-public import list" in review
    assert "frozen non-execution invariants" in review
    assert "must not implement runtime behavior or approve product use" in review


def test_freeze_review_forbids_reviewer_runtime_and_consumer_repo_actions() -> None:
    fixture = _load_fixture()
    review = _review_text()

    for action in fixture["reviewer_forbidden_actions"]:
        assert action in review


def test_freeze_review_audit_confirms_no_freeze_or_readiness_claim() -> None:
    audit = _audit_text()

    assert "does not start a freeze" in audit
    assert "does not approve" in audit
    assert "Not ready for:" in audit
    assert "product use" in audit


def test_freeze_review_static_tests_audit_bounds_files_and_surfaces() -> None:
    fixture = _load_fixture()
    audit = _static_tests_audit_text()

    for path in fixture["allowed_later_static_files"]:
        assert f"`{path}`" in audit
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in audit


def test_freeze_review_static_tests_recommend_independent_audit() -> None:
    fixture = _load_fixture()

    assert (
        fixture["recommended_next_branch"]
        == "audit-lima-consumer-proof-compatibility-freeze-review-static-tests"
    )
