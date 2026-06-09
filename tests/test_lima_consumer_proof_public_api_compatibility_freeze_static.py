from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_public_api_compatibility_freeze"
    / "consumer_proof_public_api_compatibility_freeze.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _freeze_text() -> str:
    return _text("freeze_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def _public_api_fixture() -> Mapping[str, Any]:
    fixture = _load_fixture()
    return json.loads(
        (REPO_ROOT / fixture["public_api_manifest_fixture_path"]).read_text(encoding="utf-8")
    )


def test_public_api_freeze_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_public_api_compatibility_freeze_only"
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
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_public_api_freeze_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "freeze_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_public_api_freeze_current_verdict_remains_not_ready() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()
    review = _review_text()
    audit = _audit_text()

    assert fixture["current_freeze_verdict"] == "not_ready_for_freeze"
    assert "`not_ready_for_freeze`" in freeze
    assert "NOT READY for an actual compatibility freeze" in review
    assert "NOT READY for an actual compatibility freeze" in audit

    for reason in fixture["blocked_reasons"]:
        assert reason in freeze


def test_public_api_freeze_references_authoritative_artifacts() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()

    for path in fixture["required_source_artifacts"]:
        assert f"`{path}`" in freeze
        assert (REPO_ROOT / path).exists(), path

    assert "the stricter artifact controls" in freeze


def test_public_api_freeze_requires_all_entry_conditions() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()

    for requirement in fixture["freeze_entry_requirements"]:
        assert requirement in freeze

    assert "If any requirement is missing, stale, contradictory, or unredacted" in freeze
    assert "`pass_for_dry_run_dependency_proof`" in freeze


def test_public_api_freeze_imports_match_proof_public_manifest_entries() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()
    review = _review_text()
    audit = _audit_text()
    public_api = _public_api_fixture()
    combined = "\n".join((freeze, review, audit))

    manifest_proof_imports = {
        entry["import"]
        for entry in public_api["public_imports"]
        if entry["classification"] == "proof_public"
    }
    assert set(fixture["proof_public_imports"]) == manifest_proof_imports

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in freeze

    for forbidden in fixture["forbidden_public_import_claims"]:
        assert forbidden in combined


def test_public_api_freeze_method_level_candidates_match_manifest() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()
    public_api = _public_api_fixture()

    manifest_method_candidates = {
        f"{entry['member']}(...)"
        for entry in public_api["public_imports"]
        if entry["classification"] == "method_level_dry_run_candidate"
    }
    assert set(fixture["method_level_candidates"]) == manifest_method_candidates

    for candidate in fixture["method_level_candidates"]:
        assert f"`{candidate}`" in freeze

    assert "optional non-authoritative metadata surfaces" in freeze
    assert "Result dataclasses remain internal" in freeze


def test_public_api_freeze_requires_current_non_execution_invariants() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()
    public_api = _public_api_fixture()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants == public_api["required_non_execution_invariants"]
    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in freeze

    assert "Missing or contradictory invariant evidence blocks the freeze." in freeze


def test_public_api_freeze_requires_sparkbot_and_arc_proof_boundaries() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()
    normalized = " ".join(freeze.split())

    for requirement in fixture["sparkbot_proof_requirements"]:
        assert requirement in normalized
    for requirement in fixture["arc_proof_requirements"]:
        assert requirement in normalized


def test_public_api_freeze_blocks_redaction_sensitive_evidence() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in freeze

    assert "Unredacted evidence must not be archived as freeze evidence." in freeze


def test_public_api_freeze_change_control_triggers_are_documented() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()

    for trigger in fixture["change_control_triggers"]:
        assert trigger in freeze

    assert "After a future freeze exists, a new compatibility review is required before:" in freeze


def test_public_api_freeze_forbidden_claims_are_blocked() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()

    for claim in fixture["forbidden_claims"]:
        assert claim in freeze


def test_public_api_freeze_future_static_boundary_is_limited() -> None:
    fixture = _load_fixture()
    freeze = _freeze_text()
    review = _review_text()
    audit = _audit_text()
    static_tests_audit = _static_tests_audit_text()

    for path in fixture["allowed_later_static_files"]:
        assert f"`{path}`" in freeze or f"`{path}`" in audit or f"`{path}`" in static_tests_audit

    combined = "\n".join((freeze, review, audit, static_tests_audit))
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in combined

    assert "static fixture metadata for the freeze contract" in freeze
    assert "static tests that check required references" in freeze


def test_public_api_freeze_recommended_next_branch_is_independent_audit() -> None:
    fixture = _load_fixture()

    assert (
        fixture["recommended_next_branch"]
        == "audit-lima-consumer-proof-public-api-compatibility-freeze-static-tests"
    )
