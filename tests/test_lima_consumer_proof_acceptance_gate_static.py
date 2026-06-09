from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_acceptance_gate"
    / "consumer_proof_acceptance_gate.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _gate_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["gate_path"]).read_text(encoding="utf-8")


def _audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def _public_api_fixture() -> Mapping[str, Any]:
    fixture = _load_fixture()
    return json.loads(
        (REPO_ROOT / fixture["public_api_manifest_fixture_path"]).read_text(encoding="utf-8")
    )


def test_acceptance_gate_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_acceptance_gate_only"
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


def test_acceptance_gate_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "gate_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_acceptance_gate_references_authoritative_artifacts() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for path in fixture["required_source_artifacts"]:
        assert f"`{path}`" in gate
        assert (REPO_ROOT / path).exists(), path

    assert "If this gate conflicts with a source artifact, the stricter source artifact controls." in gate


def test_acceptance_gate_declares_entry_conditions_and_missing_evidence_response() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert fixture["consumer_branches"]["sparkbot"] == "sparkbot-lima-dry-run-boundary-proof"
    assert fixture["consumer_branches"]["arc"] == "arc-lima-dry-run-boundary-proof"
    assert "`sparkbot-lima-dry-run-boundary-proof`" in gate
    assert "`arc-lima-dry-run-boundary-proof`" in gate

    for phrase in fixture["entry_condition_phrases"]:
        assert phrase in gate

    assert "`not_ready_for_acceptance_review`" in gate
    assert "`needs_missing_evidence`" in gate


def test_acceptance_gate_public_api_matches_proof_public_manifest_entries() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    public_api = _public_api_fixture()

    manifest_proof_imports = {
        entry["import"]
        for entry in public_api["public_imports"]
        if entry["classification"] == "proof_public"
    }
    assert set(fixture["allowed_proof_imports"]) == manifest_proof_imports

    for import_line in fixture["allowed_proof_imports"]:
        assert f"`{import_line}`" in gate

    method_entries = [
        entry
        for entry in public_api["public_imports"]
        if entry["classification"] == "method_level_dry_run_candidate"
    ]
    method_members = [entry["member"] for entry in method_entries]
    assert "LimaKernel.preview_guardian_lifecycle" in method_members
    assert all(entry["execution_authority"] is False for entry in method_entries)

    for candidate in fixture["method_level_candidates"]:
        assert candidate.removesuffix("(...)") in method_members
        assert f"`{candidate}`" in gate
    assert "Consumer proof branches must not import lifecycle preview result dataclasses as public API." in gate


def test_acceptance_gate_blocks_internal_and_forbidden_consumer_imports() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    public_api = _public_api_fixture()

    manifest_blocked = set(public_api["forbidden_consumer_imports"])
    manifest_blocked.update(public_api["experimental_internal_modules"])
    assert set(fixture["forbidden_consumer_imports"]) == manifest_blocked

    for import_pattern in fixture["forbidden_consumer_imports"]:
        assert f"`{import_pattern}`" in gate

    assert "`rejected_forbidden_imports`" in gate
    assert "`blocked_by_consumer_repo_boundary`" in gate
    assert "`requires_api_followup`" in gate
    assert "`requires_lima_design_followup`" in gate


def test_acceptance_gate_redaction_blockers_remain_fail_closed() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in gate

    assert "`rejected_redaction_blocker`" in gate
    assert "`needs_redaction_before_review`" in gate
    assert "Do not archive unredacted evidence." in gate


def test_acceptance_gate_requires_normalized_metadata_not_raw_input() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for requirement in fixture["normalized_metadata_requirements"]:
        assert requirement in gate

    assert "`rejected_missing_normalized_metadata`" in gate
    assert "`rejected_raw_input_boundary`" in gate
    assert "`blocked_by_runtime_boundary`" in gate


def test_acceptance_gate_requires_kernel_dry_run_boundaries() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for requirement in fixture["kernel_dry_run_requirements"]:
        assert requirement in gate

    assert "If the result claims execution, dispatch, persistence" in gate
    assert "`rejected_runtime_boundary`" in gate


def test_acceptance_gate_bounds_optional_simulated_discovery() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for requirement in fixture["simulated_discovery_requirements"]:
        assert requirement in gate

    assert "`rejected_simulated_discovery_boundary`" in gate
    assert "live discovery, scanning, connection, pairing, credential use" in gate


def test_acceptance_gate_bounds_optional_guardian_lifecycle_preview() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for requirement in fixture["guardian_lifecycle_preview_requirements"]:
        assert requirement in gate

    assert "`rejected_guardian_authority_boundary`" in gate
    assert "lifecycle preview output is treated as real Guardian authority" in gate


def test_acceptance_gate_requires_current_non_execution_invariants() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    public_api = _public_api_fixture()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants == public_api["required_non_execution_invariants"]
    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in gate

    assert "`rejected_missing_invariants`" in gate


def test_acceptance_gate_requires_sparkbot_and_arc_specific_evidence() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for evidence in fixture["sparkbot_specific_evidence"]:
        assert evidence in gate
    assert "`rejected_missing_sparkbot_evidence`" in gate

    for evidence in fixture["arc_specific_evidence"]:
        assert evidence in gate
    assert "`rejected_missing_arc_evidence`" in gate
    assert "`rejected_consumer_repo_boundary`" in gate


def test_acceptance_gate_declares_allowed_and_forbidden_statuses() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for status in fixture["allowed_acceptance_statuses"]:
        assert f"`{status}`" in gate
    for status in fixture["forbidden_acceptance_statuses"]:
        assert f"`{status}`" in gate

    assert "It does not mean the packet passed." in gate
    assert "It does not approve production integration." in gate


def test_acceptance_gate_keeps_compatibility_freeze_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()

    for condition in fixture["compatibility_freeze_conditions"]:
        assert condition in gate

    assert "Until then, freeze status remains:" in gate
    assert "`blocked`" in gate
    assert "Compatibility freeze remains blocked" in audit


def test_acceptance_gate_forbids_reviewer_runtime_and_consumer_repo_actions() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for action in fixture["reviewer_forbidden_actions"]:
        assert action in gate

    assert "Reviewers must not:" in gate


def test_acceptance_gate_audit_confirms_no_runtime_or_product_approval() -> None:
    audit = _audit_text()

    assert "No runtime behavior, public API behavior, shell behavior" in audit
    assert "No Sparkbot or Arc packet has been supplied." in audit
    assert "not \"ready for product integration.\"" in audit


def test_acceptance_gate_static_tests_audit_bounds_files_and_surfaces() -> None:
    fixture = _load_fixture()
    audit = (REPO_ROOT / fixture["static_tests_audit_path"]).read_text(encoding="utf-8")

    for path in fixture["allowed_later_static_files"]:
        assert f"`{path}`" in audit
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in audit


def test_acceptance_gate_static_tests_recommend_independent_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == "audit-lima-consumer-proof-acceptance-gate-static-tests"
