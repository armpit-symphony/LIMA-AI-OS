from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_results_audit"
    / "consumer_proof_results_audit.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _template_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["template_path"]).read_text(encoding="utf-8")


def test_proof_results_audit_fixture_is_static_lima_local_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_results_audit_template_only"
    assert fixture["lima_runtime_behavior_changed"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_integration_implemented"] is False
    assert fixture["proof_packet_audited"] is False
    assert fixture["production_readiness_claimed"] is False


def test_proof_results_audit_template_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in ("template_path", "design_path", "audit_path"):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_proof_results_audit_template_references_required_artifacts() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for path in fixture["reference_artifacts"]:
        assert f"`{path}`" in text
        assert (REPO_ROOT / path).exists(), path


def test_proof_results_audit_template_names_consumer_owned_branches() -> None:
    fixture = _load_fixture()
    text = _template_text()

    assert fixture["consumer_branches"]["sparkbot"] == "sparkbot-lima-dry-run-boundary-proof"
    assert fixture["consumer_branches"]["arc"] == "arc-lima-dry-run-boundary-proof"
    assert "`sparkbot-lima-dry-run-boundary-proof`" in text
    assert "`arc-lima-dry-run-boundary-proof`" in text
    assert "must not create, edit, or push those branches" in text


def test_proof_results_audit_template_requires_proof_evidence() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for field in fixture["required_proof_evidence"]:
        assert f"`{field}`" in text
    assert "`needs_missing_evidence`" in text


def test_proof_results_audit_template_limits_public_imports() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for import_line in fixture["allowed_proof_imports"]:
        assert f"`{import_line}`" in text
    for import_line in fixture["forbidden_consumer_imports"]:
        assert f"`{import_line}`" in text
    assert "`blocked_by_consumer_repo_boundary`" in text


def test_proof_results_audit_template_declares_result_and_simulated_discovery_rules() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for state in fixture["allowed_result_states"]:
        assert f"`{state}`" in text
    for requirement in fixture["simulated_discovery_requirements"]:
        assert requirement in text
    assert "`blocked_by_runtime_boundary`" in text


def test_proof_results_audit_template_requires_non_execution_invariants() -> None:
    fixture = _load_fixture()
    text = _template_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in text


def test_proof_results_audit_template_requires_redaction_review() -> None:
    fixture = _load_fixture()
    text = _template_text()

    assert "`needs_redaction_before_review`" in text
    for evidence in fixture["redaction_forbidden_evidence"]:
        assert evidence in text


def test_proof_results_audit_template_requires_consumer_specific_evidence() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for evidence in fixture["sparkbot_specific_evidence"]:
        assert evidence in text
    for evidence in fixture["arc_specific_evidence"]:
        assert evidence in text


def test_proof_results_audit_template_declares_statuses_and_pass_scope() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for status in fixture["allowed_audit_statuses"]:
        assert f"`{status}`" in text
    for status in fixture["forbidden_audit_statuses"]:
        assert f"`{status}`" in text
    assert fixture["passing_status"] == "pass_for_dry_run_dependency_proof"
    assert "does not mean production readiness" in text


def test_proof_results_audit_template_requires_output_fields() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for field in fixture["required_output_fields"]:
        assert field in text


def test_proof_results_audit_template_declares_next_branch_rules() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for branch in fixture["next_branch_rules"].values():
        assert f"`{branch}`" in text
    assert "response must be `blocked_by_claim_boundary`" in text


def test_proof_results_audit_template_forbids_runtime_and_consumer_surfaces() -> None:
    fixture = _load_fixture()
    text = _template_text().replace("`", "")

    for surface in fixture["forbidden_surfaces"]:
        assert surface in text


def test_proof_results_audit_template_does_not_claim_production_ready() -> None:
    fixture = _load_fixture()
    text = _template_text()

    assert fixture["required_production_readiness"] == "not_production_ready"
    assert "`not_production_ready`" in text
    assert "It does not approve production integration." in text
