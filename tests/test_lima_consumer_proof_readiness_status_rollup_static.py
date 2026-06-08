from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_readiness_status_rollup"
    / "consumer_proof_readiness_status_rollup.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _rollup_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["rollup_path"]).read_text(encoding="utf-8")


def _audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def _static_tests_audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["static_tests_audit_path"]).read_text(encoding="utf-8")


def test_readiness_status_rollup_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_readiness_status_rollup_only"
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_proof_packet_received"] is False
    assert fixture["consumer_proof_packet_audited"] is False
    assert fixture["receipt_ledger_updated"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_readiness_status_rollup_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "rollup_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_readiness_status_rollup_current_verdict_stays_not_ready() -> None:
    fixture = _load_fixture()
    rollup = _rollup_text()
    audit = _audit_text()

    assert fixture["current_rollup_verdict"] == "not_ready_for_sparkbot_arc_dependency_use"
    assert "`not_ready_for_sparkbot_arc_dependency_use`" in rollup
    assert "not yet have consumer-owned proof packets" in audit

    for reason in fixture["required_missing_reasons"]:
        assert reason in rollup


def test_readiness_status_rollup_current_consumer_states_stay_blocked() -> None:
    fixture = _load_fixture()
    rollup = _rollup_text()

    for state in fixture["current_consumer_proof_states"].values():
        assert state in {"not_received", "not_started", "blocked", "not_production_ready"}
        assert f"`{state}`" in rollup

    assert "Sparkbot proof packet | `not_received`" in rollup
    assert "Arc Bot proof packet | `not_received`" in rollup
    assert "Compatibility freeze | `blocked`" in rollup
    assert "Product readiness | `not_production_ready`" in rollup


def test_readiness_status_rollup_references_source_artifacts_without_overriding() -> None:
    fixture = _load_fixture()
    rollup = _rollup_text()

    for path in fixture["source_artifacts"]:
        assert f"`{path}`" in rollup
        assert (REPO_ROOT / path).exists(), path

    assert "If this rollup conflicts with a source artifact, the source artifact controls." in rollup


def test_readiness_status_rollup_prepared_materials_are_not_readiness_claims() -> None:
    fixture = _load_fixture()
    rollup = _rollup_text()

    for material in fixture["prepared_materials_only"]:
        assert material in rollup

    assert "These are readiness materials only." in rollup
    assert "They do not prove that Sparkbot or Arc Bot can use LIMA yet." in rollup


def test_readiness_status_rollup_lists_all_not_ready_requirements() -> None:
    fixture = _load_fixture()
    rollup = _rollup_text()
    audit = _audit_text()

    for requirement in fixture["not_ready_requirements"]:
        assert requirement in rollup

    assert "packet receipt, redaction, proof audit, then freeze design" in audit
    assert "both proof audits to pass" in audit


def test_readiness_status_rollup_future_flow_stays_manual_and_reviewed() -> None:
    fixture = _load_fixture()
    rollup = _rollup_text()

    for step in fixture["required_future_flow"]:
        assert step in rollup

    assert "This rollup does not automate that flow." in rollup


def test_readiness_status_rollup_blocks_runtime_consumer_repo_and_live_surfaces() -> None:
    fixture = _load_fixture()
    rollup = _rollup_text()
    audit = _audit_text()

    for action in fixture["blocked_actions"]:
        assert action in rollup

    assert "No blocked action is approved by the rollup." in audit


def test_readiness_status_rollup_declares_allowed_and_forbidden_statuses() -> None:
    fixture = _load_fixture()
    rollup = _rollup_text()
    audit = _audit_text()

    for status in fixture["allowed_rollup_statuses"]:
        assert f"`{status}`" in rollup
    for status in fixture["forbidden_rollup_statuses"]:
        assert f"`{status}`" in rollup

    assert "Forbidden statuses correctly prevent readiness inflation" in audit


def test_readiness_status_rollup_static_tests_audit_bounds_later_files_and_surfaces() -> None:
    fixture = _load_fixture()
    static_tests_audit = _static_tests_audit_text()

    for path in fixture["allowed_later_static_files"]:
        assert f"`{path}`" in static_tests_audit
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in static_tests_audit


def test_readiness_status_rollup_static_tests_recommend_independent_audit() -> None:
    fixture = _load_fixture()

    assert (
        fixture["recommended_next_branch"]
        == "audit-lima-consumer-proof-readiness-status-rollup-static-tests"
    )
