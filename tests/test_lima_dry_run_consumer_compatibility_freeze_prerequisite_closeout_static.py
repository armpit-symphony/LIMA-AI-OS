from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "dry_run_consumer_compatibility_freeze_prerequisite_closeout"
    / "freeze_prerequisite_closeout.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _closeout_text() -> str:
    return _text("closeout_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_closeout_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert (
        fixture["fixture_scope"]
        == "static_dry_run_consumer_compatibility_freeze_prerequisite_closeout_only"
    )
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


def test_closeout_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "closeout_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_closeout_verdict_remains_waiting_on_consumer_proof() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    review = _review_text()
    audit = _audit_text()
    combined = "\n".join((closeout, review, audit))

    assert (
        fixture["current_closeout_verdict"]
        == "lima_local_prerequisites_closed_waiting_on_consumer_proof"
    )
    assert f"`{fixture['current_closeout_verdict']}`" in combined
    assert f"`{fixture['current_freeze_state']}`" in combined
    assert f"`{fixture['current_product_state']}`" in combined
    assert "NOT READY for compatibility freeze" in combined
    assert "NOT READY for Sparkbot or Arc dependency-use claims" in closeout


def test_closeout_tracks_missing_external_inputs() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    review = _review_text()
    audit = _audit_text()
    combined = "\n".join((closeout, review, audit))

    for state in fixture["current_external_inputs"].values():
        assert f"`{state}`" in combined

    assert "Sparkbot dry-run proof packet | Sparkbot repo team | `not_received`" in closeout
    assert "Arc Bot dry-run proof packet | Arc Bot / LIMA Office repo team | `not_received`" in closeout
    assert "Sparkbot proof packet: `not_received`" in review
    assert "Arc Bot proof packet: `not_received`" in review
    assert "The LIMA repo remains waiting for consumer-owned proof packets." in audit


def test_closeout_references_source_artifacts_and_local_prerequisites() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _audit_text()
    combined = "\n".join((closeout, audit))

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in closeout or f"`{path}`" in audit

    for prerequisite in fixture["lima_local_prerequisites"]:
        assert prerequisite in combined

    assert "the stricter artifact controls" in closeout


def test_closeout_freeze_entry_conditions_remain_blocked() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _audit_text()
    combined = "\n".join((closeout, audit))

    for requirement in fixture["freeze_entry_requirements"]:
        assert requirement in combined

    assert "A future `design-lima-dry-run-consumer-compatibility-freeze` branch may start only after" in closeout
    assert "Until then, freeze status remains:" in closeout
    assert "`not_ready_for_freeze`" in closeout


def test_closeout_public_api_boundary_matches_proof_public_imports() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _audit_text()
    combined = "\n".join((closeout, audit))

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in combined

    for forbidden in fixture["forbidden_public_import_claims"]:
        assert forbidden in combined


def test_closeout_requires_full_non_execution_invariants() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in closeout

    assert "Missing or contradictory invariant evidence blocks freeze design." in closeout


def test_closeout_blocks_unredacted_sensitive_evidence() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _audit_text()
    combined = "\n".join((closeout, audit))

    for blocker in fixture["redaction_blockers"]:
        assert blocker in combined

    assert "Unredacted evidence must not be archived." in combined


def test_closeout_preserves_consumer_repo_ownership() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _audit_text()
    combined = "\n".join((closeout, audit))

    for branch in fixture["consumer_owned_branches"].values():
        assert f"`{branch}`" in combined

    assert "The LIMA repo team must not create, edit, push, fetch, clone, scan, inspect, or validate" in closeout
    assert "unless explicit approved proof artifacts or explicit read-only reference review approval are supplied" in audit


def test_closeout_forbidden_claims_and_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _audit_text()
    combined = "\n".join((closeout, audit))

    for claim in fixture["forbidden_claims"]:
        assert claim in combined
    for action in fixture["forbidden_actions"]:
        assert action in combined

    assert "This closeout must not be described as:" in closeout
    assert "This closeout must not trigger:" in closeout


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
        == "audit-lima-dry-run-consumer-compatibility-freeze-prerequisite-closeout-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
