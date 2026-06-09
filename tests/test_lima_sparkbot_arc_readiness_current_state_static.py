from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "sparkbot_arc_readiness_current_state"
    / "sparkbot_arc_readiness_current_state.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _audit_text() -> str:
    return _text("audit_path")


def _manifest_text() -> str:
    return _text("public_api_manifest_path")


def _package_text() -> str:
    return _text("package_metadata_path")


def _top_level_init_text() -> str:
    return _text("top_level_init_path")


def _kernel_init_text() -> str:
    return _text("kernel_init_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_current_state_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_sparkbot_arc_readiness_current_state_only"
    assert fixture["audit_status"] == "PASS"
    assert fixture["top_level_runtime_exports_approved"] is False


def test_current_state_source_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "audit_path",
        "public_api_manifest_path",
        "minimal_kernel_audit_path",
        "delivery_confirmation_static_tests_audit_path",
        "package_metadata_path",
        "top_level_init_path",
        "kernel_init_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_package_metadata_remains_proof_only_candidate() -> None:
    fixture = _load_fixture()
    package_text = _package_text()
    manifest_text = _manifest_text()
    audit_text = _audit_text()

    assert f'name = "{fixture["package_name"]}"' in package_text
    assert f'version = "{fixture["package_version"]}"' in package_text
    assert f"package name: `{fixture['package_name']}`" in manifest_text
    assert f"current version: `{fixture['package_version']}`" in manifest_text
    assert f"version stage: `{fixture['version_stage']}`" in manifest_text
    assert fixture["package_name"] in audit_text
    assert fixture["package_version"] in audit_text


def test_top_level_lima_exports_do_not_expose_runtime() -> None:
    top_level = _top_level_init_text()
    manifest = _manifest_text()
    audit = _audit_text()

    assert '__all__ = ["contracts"]' in top_level
    assert "top-level runtime exports remain unapproved" in audit
    assert "`from lima import LimaKernel` is not a supported proof-stage import." in manifest
    assert "from lima import LimaKernel" not in top_level


def test_proof_public_imports_are_documented_and_exported_from_kernel() -> None:
    fixture = _load_fixture()
    manifest = _manifest_text()
    audit = _audit_text()
    kernel_init = _kernel_init_text()

    for import_line in fixture["proof_public_imports"]:
        symbol = import_line.rsplit(" ", 1)[-1]
        assert f"`{import_line}`" in manifest
        assert f"`{import_line}`" in audit
        assert f'"{symbol}"' in kernel_init


def test_current_allowed_capabilities_are_pinned_to_dry_run_only() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    for capability in fixture["allowed_current_capabilities"]:
        assert capability in audit

    assert "already-normalized metadata dry-run evaluation" in audit
    assert "explicit synthetic simulated discovery surfaces" in audit
    assert "proof-stage ready for consumer-owned dry-run dependency proof" in audit


def test_consumer_evidence_state_remains_missing_and_blocked() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    for state in fixture["current_consumer_evidence_state"].values():
        assert f"`{state}`" in audit

    assert "Sparkbot proof packet: `not_received`" in audit
    assert "Arc Bot proof packet: `not_received`" in audit
    assert "dual-consumer result gate: `not_ready_for_result_gate`" in audit


def test_sparkbot_readiness_remains_not_ready_for_product_integration() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    assert "## Sparkbot Readiness" in audit
    assert "NOT READY for product integration." in audit
    for blocker in fixture["sparkbot_blockers"]:
        assert blocker in audit


def test_arc_bot_readiness_remains_not_ready_for_product_integration() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    assert "## Arc Bot Readiness" in audit
    assert "NOT READY for product integration." in audit
    for blocker in fixture["arc_bot_blockers"]:
        assert blocker in audit


def test_product_readiness_decision_remains_blocked() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    for claim in fixture["not_ready_claims"]:
        assert claim in audit

    assert "`not_ready_for_freeze`" in audit
    assert "`not_production_ready`" in audit


def test_forbidden_current_claims_are_not_made_as_approvals() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    for claim in fixture["forbidden_current_claims"]:
        assert claim not in audit

    assert "cannot claim Sparkbot dependency-use readiness" in audit
    assert "cannot claim Arc Bot dependency-use readiness" in audit


def test_forbidden_surfaces_remain_blocked() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    for surface in fixture["forbidden_surfaces"]:
        assert surface in audit

    assert "This audit does not authorize:" in audit


def test_recommended_next_branches_are_input_dependent() -> None:
    fixture = _load_fixture()
    audit = _audit_text()

    assert fixture["next_branches"]["manual_delivery_confirmed_without_packets"] in audit
    assert fixture["next_branches"]["proof_packets_supplied"] in audit
    assert "If neither input is supplied, remain in waiting state" in audit


def test_static_tests_allowed_files_are_exact() -> None:
    fixture = _load_fixture()
    static_audit = _static_tests_audit_text()

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in static_audit

    assert "No `lima/`, package metadata, public export, consumer repo, or runtime behavior changes are made." in static_audit


def test_static_tests_recommend_independent_audit() -> None:
    fixture = _load_fixture()
    static_audit = _static_tests_audit_text()

    assert fixture["recommended_next_branch"] == "audit-lima-sparkbot-arc-readiness-current-state-static-tests"
    assert f"`{fixture['recommended_next_branch']}`" in static_audit
