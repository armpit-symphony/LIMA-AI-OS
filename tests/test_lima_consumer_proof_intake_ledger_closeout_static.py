from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_intake_ledger_closeout"
    / "consumer_proof_intake_ledger_closeout.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _closeout_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["closeout_path"]).read_text(encoding="utf-8")


def _closeout_audit_text() -> str:
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


def test_closeout_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_intake_ledger_closeout_only"
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


def test_closeout_static_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "closeout_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_design_path",
        "static_tests_design_audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_closeout_static_tests_reference_authoritative_artifacts() -> None:
    fixture = _load_fixture()
    design = _static_tests_design_text()

    for path in fixture["required_source_artifacts"]:
        assert f"`{path}`" in design
        assert (REPO_ROOT / path).exists(), path

    assert "the stricter source artifact must control" in design


def test_closeout_verdict_and_ledger_state_remain_waiting() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _closeout_audit_text()
    state = fixture["current_ledger_state"]

    assert fixture["current_closeout_verdict"] == "intake_ledger_ready_waiting_for_consumer_packets"
    assert "`intake_ledger_ready_waiting_for_consumer_packets`" in closeout
    assert "not that Sparkbot or Arc proof has passed" in audit

    assert f"| Sparkbot proof packet | `{state['sparkbot_proof_packet']}`" in closeout
    assert f"| Arc Bot proof packet | `{state['arc_bot_proof_packet']}`" in closeout
    assert f"| Sparkbot proof audit | `{state['sparkbot_proof_audit']}`" in closeout
    assert f"| Arc Bot proof audit | `{state['arc_bot_proof_audit']}`" in closeout
    assert f"| Product readiness | `{state['product_readiness']}`" in closeout
    assert "`blocked`" in closeout
    assert "`freeze_review_blocked`" in closeout


def test_closeout_lima_local_materials_are_preparation_only() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    for material in fixture["lima_local_materials_ready"]:
        assert material in closeout

    assert "Ready as LIMA-local materials only:" in closeout
    assert "They do not prove Sparkbot or Arc Bot can use LIMA." in closeout


def test_closeout_requires_consumer_owned_packets_and_fields() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    assert fixture["consumer_branches"]["sparkbot"] == "sparkbot-lima-dry-run-boundary-proof"
    assert fixture["consumer_branches"]["arc"] == "arc-lima-dry-run-boundary-proof"
    assert "`sparkbot-lima-dry-run-boundary-proof`" in closeout
    assert "`arc-lima-dry-run-boundary-proof`" in closeout

    for field in fixture["required_packet_fields"]:
        assert field in closeout


def test_closeout_public_api_matches_proof_public_manifest_entries() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    public_api = _public_api_fixture()

    manifest_proof_imports = {
        entry["import"]
        for entry in public_api["public_imports"]
        if entry["classification"] == "proof_public"
    }
    assert set(fixture["proof_public_imports"]) == manifest_proof_imports

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in closeout


def test_closeout_lifecycle_preview_stays_method_level_only() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    for candidate in fixture["method_level_candidates"]:
        assert f"`{candidate}`" in closeout

    assert "Method-level dry-run candidate:" in closeout
    assert "lifecycle preview result dataclasses" in closeout
    assert "`dry_run_candidate` imports" in closeout
    assert "top-level runtime re-exports" in closeout


def test_closeout_blocks_internal_and_forbidden_consumer_imports() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    public_api = _public_api_fixture()

    manifest_blocked = set(public_api["forbidden_consumer_imports"])
    manifest_blocked.update(public_api["experimental_internal_modules"])
    assert set(fixture["forbidden_consumer_imports"]) == manifest_blocked

    for import_pattern in fixture["forbidden_consumer_imports"]:
        assert f"`{import_pattern}`" in closeout


def test_closeout_requires_current_non_execution_invariants() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    public_api = _public_api_fixture()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants == public_api["required_non_execution_invariants"]
    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in closeout


def test_closeout_blocks_redaction_sensitive_evidence() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in closeout

    assert "Do not archive or audit packet contents" in closeout


def test_closeout_requires_sparkbot_missing_evidence() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    assert "Sparkbot proof remains missing" in closeout
    for requirement in fixture["sparkbot_specific_missing_evidence"]:
        assert requirement in closeout


def test_closeout_requires_arc_bot_missing_evidence() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    assert "Arc Bot proof remains missing" in closeout
    for requirement in fixture["arc_specific_missing_evidence"]:
        assert requirement in closeout


def test_closeout_manual_intake_flow_stays_manual() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    for step in fixture["manual_intake_flow_steps"]:
        assert step in closeout

    assert "This closeout does not automate that flow." in closeout


def test_closeout_keeps_compatibility_freeze_blocked() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()
    audit = _closeout_audit_text()

    for condition in fixture["compatibility_freeze_conditions"]:
        assert condition in closeout

    assert "Current freeze status:" in closeout
    assert "`blocked`" in closeout
    assert "The closeout does not start a freeze." in audit


def test_closeout_forbids_readiness_and_runtime_claims() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    assert "This closeout must not be used to claim:" in closeout
    for claim in fixture["forbidden_closeout_claims"]:
        assert claim in closeout


def test_closeout_forbids_reviewer_runtime_and_consumer_repo_actions() -> None:
    fixture = _load_fixture()
    closeout = _closeout_text()

    assert "Reviewers must not:" in closeout
    for action in fixture["reviewer_forbidden_actions"]:
        assert action in closeout


def test_static_tests_implementation_audit_bounds_files_and_surfaces() -> None:
    fixture = _load_fixture()
    audit = _static_tests_audit_text()

    for path in fixture["allowed_later_static_files"]:
        assert f"`{path}`" in audit
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in audit


def test_static_tests_implementation_audit_recommends_independent_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == (
        "audit-lima-consumer-proof-intake-ledger-closeout-static-tests"
    )
