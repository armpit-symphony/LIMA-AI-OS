from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_readiness_closeout_package"
    / "consumer_proof_readiness_closeout_package.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _package_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["package_path"]).read_text(encoding="utf-8")


def _package_audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def _static_tests_design_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["static_tests_design_path"]).read_text(encoding="utf-8")


def _static_tests_audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["static_tests_audit_path"]).read_text(encoding="utf-8")


def _public_api_fixture() -> Mapping[str, Any]:
    fixture = _load_fixture()
    return json.loads(
        (REPO_ROOT / fixture["public_api_manifest_fixture_path"]).read_text(encoding="utf-8")
    )


def test_package_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_readiness_closeout_package_only"
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


def test_package_static_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "package_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_design_path",
        "static_tests_design_audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_static_tests_reference_source_artifacts_and_stricter_controls() -> None:
    fixture = _load_fixture()
    design = _static_tests_design_text()

    for path in fixture["required_source_artifacts"]:
        assert f"`{path}`" in design
        assert (REPO_ROOT / path).exists(), path

    assert "the stricter source artifact must control" in design


def test_package_verdict_and_evidence_state_remain_proof_handoff_only() -> None:
    fixture = _load_fixture()
    package = _package_text()
    audit = _package_audit_text()
    state = fixture["current_evidence_state"]

    assert fixture["current_package_verdict"] == (
        "ready_for_consumer_owned_dry_run_proof_handoff_only"
    )
    assert "`ready_for_consumer_owned_dry_run_proof_handoff_only`" in package
    assert "`ready_for_consumer_owned_dry_run_proof_handoff_only`" in audit

    assert f"| Sparkbot proof packet | `{state['sparkbot_proof_packet']}`" in package
    assert f"| Arc Bot proof packet | `{state['arc_bot_proof_packet']}`" in package
    assert f"| Sparkbot redaction review | `{state['sparkbot_redaction_review']}`" in package
    assert f"| Arc Bot redaction review | `{state['arc_bot_redaction_review']}`" in package
    assert f"| Sparkbot proof audit | `{state['sparkbot_proof_audit']}`" in package
    assert f"| Arc Bot proof audit | `{state['arc_bot_proof_audit']}`" in package
    assert f"| Compatibility freeze | `{state['compatibility_freeze']}`" in package
    assert f"| Product readiness | `{state['product_readiness']}`" in package


def test_latest_lima_reference_commit_stays_preparation_only() -> None:
    fixture = _load_fixture()
    package = _package_text()

    assert fixture["latest_lima_local_reference_commit"] in package
    assert "not proof that Sparkbot or Arc Bot can use LIMA" in package
    assert "latest audited LIMA-local preparation checkpoint" in package


def test_required_package_contents_and_audit_references_remain_listed() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for path in fixture["required_package_contents"]:
        assert f"`{path}`" in package
    for path in fixture["required_audit_references"]:
        assert f"`{path}`" in package


def test_consumer_branches_remain_consumer_owned() -> None:
    fixture = _load_fixture()
    package = _package_text()

    assert fixture["consumer_branches"]["sparkbot"] == "sparkbot-lima-dry-run-boundary-proof"
    assert fixture["consumer_branches"]["arc"] == "arc-lima-dry-run-boundary-proof"
    assert "`sparkbot-lima-dry-run-boundary-proof`" in package
    assert "`arc-lima-dry-run-boundary-proof`" in package
    assert "must be created and owned by consumer repo teams" in package
    assert "must not create, edit, push, fetch, clone, scan, or inspect those branches" in package


def test_delivery_warning_remains_proof_only_and_non_executing() -> None:
    package = _package_text()

    assert "This is a proof-only LIMA handoff package." in package
    assert "Do not wire production routes." in package
    assert "Do not send raw prompts" in package
    assert "Do not expect LIMA to call models" in package
    assert "Robo-OS, robots, drones, or physical-world systems" in package
    assert "already-normalized metadata in and dry-run ExecutionResult out" in package


def test_allowed_proof_shape_remains_explicit_dry_run_only() -> None:
    package = _package_text()

    for line in (
        "consumer-owned branch",
        "redacted already-normalized metadata in",
        "default-deny capability profile",
        "explicit LimaKernel.evaluate(...) dry-run call",
        "optional explicit SimulatedDiscoveryAdapter for synthetic preview only",
        "optional LimaKernel.preview_guardian_lifecycle(...) as non-authoritative metadata only",
        "dry-run ExecutionResult out",
        "redacted proof packet",
        "repo-team-owned proof verdict",
        "LIMA-side proof audit later",
    ):
        assert line in package


def test_package_requires_consumer_proof_packet_fields() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for field in fixture["required_packet_fields"]:
        assert field in package


def test_package_public_api_matches_proof_public_manifest_entries() -> None:
    fixture = _load_fixture()
    package = _package_text()
    public_api = _public_api_fixture()

    manifest_proof_imports = {
        entry["import"]
        for entry in public_api["public_imports"]
        if entry["classification"] == "proof_public"
    }
    assert set(fixture["proof_public_imports"]) == manifest_proof_imports

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in package


def test_lifecycle_preview_stays_method_level_only() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for candidate in fixture["method_level_candidates"]:
        assert f"`{candidate}`" in package

    assert "Optional method-level dry-run candidate:" in package
    assert "standalone lifecycle preview result dataclass imports" in package
    assert "unreviewed `dry_run_candidate` imports" in package
    assert "top-level runtime re-exports" in package


def test_package_blocks_internal_and_forbidden_consumer_imports() -> None:
    fixture = _load_fixture()
    package = _package_text()
    public_api = _public_api_fixture()

    manifest_blocked = set(public_api["forbidden_consumer_imports"])
    manifest_blocked.update(public_api["experimental_internal_modules"])
    assert set(fixture["forbidden_consumer_imports"]) == manifest_blocked

    for import_pattern in fixture["forbidden_consumer_imports"]:
        assert f"`{import_pattern}`" in package


def test_package_requires_current_non_execution_invariants() -> None:
    fixture = _load_fixture()
    package = _package_text()
    public_api = _public_api_fixture()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants == public_api["required_non_execution_invariants"]
    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in package


def test_package_blocks_redaction_sensitive_evidence() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in package

    assert "`needs_redaction_before_review`" in package
    assert "Do not archive unredacted evidence." in package


def test_package_requires_sparkbot_evidence_before_readiness() -> None:
    fixture = _load_fixture()
    package = _package_text()

    assert "Sparkbot proof packet must show:" in package
    for requirement in fixture["sparkbot_evidence_requirements"]:
        assert requirement in package


def test_package_requires_arc_bot_evidence_before_readiness() -> None:
    fixture = _load_fixture()
    package = _package_text()

    assert "Arc Bot proof packet must show:" in package
    for requirement in fixture["arc_evidence_requirements"]:
        assert requirement in package


def test_manual_intake_path_remains_manual_and_non_automated() -> None:
    fixture = _load_fixture()
    package = _package_text()

    for step in fixture["manual_intake_flow_steps"]:
        assert step in package

    assert "This package does not automate intake" in package


def test_compatibility_freeze_remains_blocked() -> None:
    fixture = _load_fixture()
    package = _package_text()
    audit = _package_audit_text()

    for condition in fixture["compatibility_freeze_conditions"]:
        assert condition in package

    assert "Current freeze status:" in package
    assert "`blocked`" in package
    assert "compatibility freeze remains `blocked`" in audit


def test_package_forbids_readiness_claims() -> None:
    fixture = _load_fixture()
    package = _package_text()

    assert "This package must not be described as:" in package
    for claim in fixture["forbidden_package_claims"]:
        assert claim in package


def test_package_forbids_runtime_and_consumer_repo_actions() -> None:
    fixture = _load_fixture()
    package = _package_text()

    assert "This package must not trigger:" in package
    for action in fixture["forbidden_package_actions"]:
        assert action in package


def test_static_tests_implementation_audit_bounds_files_and_surfaces() -> None:
    fixture = _load_fixture()
    audit = _static_tests_audit_text()

    for path in fixture["allowed_static_files"]:
        assert f"`{path}`" in audit
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in audit


def test_static_tests_implementation_audit_recommends_independent_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == (
        "audit-lima-consumer-proof-readiness-closeout-package-static-tests-implementation"
    )
