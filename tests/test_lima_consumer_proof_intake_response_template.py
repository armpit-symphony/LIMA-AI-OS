from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_intake_response"
    / "consumer_proof_intake_response.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _template_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["template_path"]).read_text(encoding="utf-8")


def test_intake_response_fixture_is_static_lima_local_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_intake_response_template_only"
    assert fixture["lima_runtime_behavior_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_integration_implemented"] is False
    assert fixture["intake_automation_implemented"] is False
    assert fixture["production_readiness_claimed"] is False


def test_intake_response_template_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in ("template_path", "design_path", "audit_path"):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_intake_response_template_names_consumer_owned_branches() -> None:
    fixture = _load_fixture()
    text = _template_text()

    assert fixture["consumer_branches"]["sparkbot"] == "sparkbot-lima-dry-run-boundary-proof"
    assert fixture["consumer_branches"]["arc"] == "arc-lima-dry-run-boundary-proof"
    assert "`sparkbot-lima-dry-run-boundary-proof`" in text
    assert "`arc-lima-dry-run-boundary-proof`" in text
    assert "The proof branch remains owned by the consumer repo team." in text


def test_intake_response_template_preserves_allowed_and_forbidden_sources() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for source in fixture["allowed_intake_sources"]:
        assert source in text
    for source in fixture["forbidden_intake_sources"]:
        assert source in text


def test_intake_response_template_requires_intake_fields() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for field in fixture["required_intake_fields"]:
        assert f"`{field}`" in text
    assert "`needs_missing_evidence`" in text


def test_intake_response_template_declares_allowed_and_forbidden_verdicts() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for verdict in fixture["allowed_proof_verdicts"]:
        assert f"`{verdict}`" in text
    for verdict in fixture["forbidden_proof_verdicts"]:
        assert f"`{verdict}`" in text
    assert "`blocked_by_claim_boundary`" in text


def test_intake_response_template_declares_allowed_and_forbidden_statuses() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for status in fixture["allowed_response_statuses"]:
        assert f"`{status}`" in text
    for status in fixture["forbidden_response_statuses"]:
        assert f"`{status}`" in text


def test_intake_response_template_requires_response_fields_and_not_ready_claim() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for field in fixture["required_response_fields"]:
        assert f"`{field}`" in text
    assert fixture["required_production_readiness"] == "not_production_ready"
    assert "`production_readiness: not_production_ready`" in text


def test_intake_response_template_requires_redaction_failure_status() -> None:
    fixture = _load_fixture()
    text = _template_text()

    assert fixture["redaction_failure_status"] == "needs_redaction_before_review"
    assert "`needs_redaction_before_review`" in text
    for forbidden_evidence in fixture["redaction_forbidden_evidence"]:
        assert forbidden_evidence in text


def test_intake_response_template_requires_non_execution_invariants() -> None:
    fixture = _load_fixture()
    text = _template_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in text


def test_intake_response_template_declares_boundary_finding_categories() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for category in fixture["boundary_finding_categories"]:
        assert f"`{category}`" in text


def test_intake_response_template_declares_next_branch_rules() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for branch in fixture["next_branch_rules"].values():
        assert f"`{branch}`" in text
    assert "response must be `blocked_by_claim_boundary`" in text


def test_intake_response_template_forbids_runtime_and_consumer_surfaces() -> None:
    fixture = _load_fixture()
    text = _template_text().replace("`", "")

    for surface in fixture["forbidden_surfaces"]:
        assert surface in text


def test_intake_response_template_carries_remaining_product_blockers() -> None:
    fixture = _load_fixture()
    text = _template_text().replace("`", "")

    for blocker in fixture["remaining_blockers"]:
        assert blocker in text
