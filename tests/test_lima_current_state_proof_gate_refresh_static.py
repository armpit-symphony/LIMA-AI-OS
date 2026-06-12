from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "current_state_proof_gate_refresh"
    / "current_state_proof_gate_refresh.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _readme_text() -> str:
    return _text("readme_path")


def _current_state_text() -> str:
    return _text("current_state_path")


def _manifest_text() -> str:
    return _text("public_api_manifest_path")


def _refresh_audit_text() -> str:
    return _text("refresh_audit_path")


def _independent_audit_text() -> str:
    return _text("independent_audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_current_state_refresh_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_current_state_proof_gate_refresh_only"
    assert fixture["audit_status"] == "PASS"
    assert fixture["base_commit"] == "905445d684e7338c741cbfd46add6e4a3b4208e1"


def test_current_state_refresh_source_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "readme_path",
        "current_state_path",
        "public_api_manifest_path",
        "refresh_audit_path",
        "independent_audit_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_readme_no_longer_claims_docs_only_no_runtime_status() -> None:
    readme = _readme_text()

    assert "## Current Proof-Stage Runtime Status" in readme
    assert "**Phase 0 only. No runtime implementation yet.**" not in readme
    assert "LIMA-AI-OS is still not product-ready, but it is no longer docs-only." in readme


def test_readme_pins_current_proof_stage_capabilities() -> None:
    fixture = _load_fixture()
    readme = _readme_text()

    for capability in fixture["proof_stage_capabilities"]:
        assert capability in readme

    assert "`lima-runtime` is a `0.0.1` proof-only runtime candidate." in readme
    assert "`from lima.kernel import LimaKernel`" in readme


def test_readme_preserves_blocked_runtime_and_product_surfaces() -> None:
    fixture = _load_fixture()
    readme = _readme_text()

    for surface in fixture["blocked_surfaces"]:
        assert surface in readme

    assert "compatibility freeze and product readiness remain blocked" in readme


def test_current_state_pins_proof_gate_snapshot() -> None:
    fixture = _load_fixture()
    current_state = _current_state_text()

    assert "## Current Proof-Gate Snapshot - 2026-06-12" in current_state
    assert "The active LIMA-to-Sparkbot/Arc readiness track is proof-stage only." in current_state

    for capability in fixture["current_state_capabilities"]:
        assert capability in current_state


def test_current_state_preserves_missing_external_evidence() -> None:
    fixture = _load_fixture()
    current_state = _current_state_text()

    for state in fixture["external_evidence_state"]:
        assert state in current_state


def test_current_state_preserves_input_dependent_next_branches() -> None:
    fixture = _load_fixture()
    current_state = _current_state_text()
    readme = _readme_text()

    manual_branch = fixture["next_branches"]["manual_delivery_confirmed_without_packets"]
    proof_branch = fixture["next_branches"]["proof_packets_supplied"]

    assert manual_branch in current_state
    assert proof_branch in current_state
    assert manual_branch in readme
    assert proof_branch in readme
    assert (
        "If no proof packets are supplied, remain in `WAITING_ON_CONSUMER_PROOF_PACKET_RESPONSES`"
        in current_state
    )
    assert "If neither input exists, remain in waiting state and do not claim Sparkbot/Arc readiness." in readme


def test_current_state_forbids_readiness_inferences() -> None:
    fixture = _load_fixture()
    current_state = _current_state_text()

    for inference in fixture["forbidden_inferences"]:
        assert inference in current_state

    assert "Do not infer" in current_state


def test_public_api_manifest_still_keeps_top_level_exports_unapproved() -> None:
    manifest = _manifest_text()

    assert "top-level runtime exports are not approved." in manifest
    assert "`from lima import LimaKernel` is not a supported proof-stage import." in manifest
    assert "Consumer proof branches should import runtime proof APIs from `lima.kernel`." in manifest


def test_proof_public_imports_remain_manifested_for_consumer_dry_run_only() -> None:
    fixture = _load_fixture()
    manifest = _manifest_text()

    assert "Proof-public imports are allowed for Sparkbot and Arc Bot repo-owned dry-run proof branches only." in manifest
    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in manifest


def test_refresh_audits_preserve_docs_only_scope() -> None:
    refresh_audit = _refresh_audit_text()
    independent_audit = _independent_audit_text()

    assert "PASS for documentation-only current-state refresh." in refresh_audit
    assert "PASS for independent audit of the current-state proof-gate documentation refresh." in independent_audit
    assert "The branch is documentation-only." in independent_audit


def test_static_tests_allowed_files_are_exact() -> None:
    fixture = _load_fixture()
    static_audit = _static_tests_audit_text()

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in static_audit

    assert "No `lima/`, package metadata, public export, consumer repo, or runtime behavior changes are made." in static_audit


def test_static_tests_recommend_independent_audit() -> None:
    fixture = _load_fixture()
    static_audit = _static_tests_audit_text()

    assert fixture["recommended_next_branch"] == "audit-lima-current-state-proof-gate-refresh-static-tests"
    assert f"`{fixture['recommended_next_branch']}`" in static_audit
