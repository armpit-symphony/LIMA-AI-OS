from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_archive_template"
    / "consumer_proof_archive_template.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _template_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["template_path"]).read_text(encoding="utf-8")


def test_archive_template_fixture_is_static_lima_local_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_archive_template_only"
    assert fixture["lima_runtime_behavior_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_integration_implemented"] is False
    assert fixture["production_readiness_claimed"] is False


def test_archive_template_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in ("template_path", "design_path", "audit_path"):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_archive_template_names_consumer_owned_branches() -> None:
    fixture = _load_fixture()
    text = _template_text()

    assert fixture["consumer_branches"]["sparkbot"] == "sparkbot-lima-dry-run-boundary-proof"
    assert fixture["consumer_branches"]["arc"] == "arc-lima-dry-run-boundary-proof"
    assert "`sparkbot-lima-dry-run-boundary-proof`" in text
    assert "`arc-lima-dry-run-boundary-proof`" in text


def test_archive_template_contains_all_required_sections() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for section in fixture["required_archive_sections"]:
        assert section in text


def test_archive_template_limits_public_imports() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for import_line in fixture["allowed_public_imports"]:
        assert f"`{import_line}`" in text
    assert "No LIMA internals should be imported." in text


def test_archive_template_declares_allowed_result_states_and_verdicts() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for result_state in fixture["allowed_result_states"]:
        assert f"`{result_state}`" in text
    for verdict in fixture["allowed_final_verdicts"]:
        assert f"`{verdict}`" in text
    for verdict in fixture["forbidden_final_verdicts"]:
        assert f"`{verdict}`" in text


def test_archive_template_requires_dry_run_scope_fields() -> None:
    fixture = _load_fixture()
    text = _template_text().lower().replace("-", " ").replace("intentenvelope", "intent envelope")

    for field in fixture["required_true_fields"]:
        label = field.replace("_", " ")
        assert label in text
    for field in fixture["required_false_fields"]:
        label = field.replace("_", " ")
        assert label in text


def test_archive_template_requires_default_deny_capabilities() -> None:
    fixture = _load_fixture()
    text = _template_text()

    assert fixture["default_deny_capabilities"]
    assert all(value is False for value in fixture["default_deny_capabilities"].values())
    for capability in fixture["default_deny_capabilities"]:
        assert f"`{capability}: false`" in text


def test_archive_template_requires_non_execution_invariants() -> None:
    fixture = _load_fixture()
    text = _template_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")
    for invariant_name, value in invariants.items():
        expected = "true" if value is True else "false"
        assert f"`{invariant_name}: {expected}`" in text


def test_archive_template_forbids_sensitive_inputs() -> None:
    fixture = _load_fixture()
    text = _template_text()

    for forbidden_input in fixture["forbidden_inputs"]:
        assert forbidden_input in text


def test_archive_template_forbids_runtime_and_physical_surfaces() -> None:
    fixture = _load_fixture()
    text = _template_text().replace("`", "")

    for surface in fixture["forbidden_surfaces"]:
        assert surface in text


def test_archive_template_has_distinct_sparkbot_and_arc_evidence() -> None:
    fixture = _load_fixture()
    text = _template_text().lower()

    for evidence in fixture["sparkbot_specific_evidence"]:
        assert evidence.lower() in text
    for evidence in fixture["arc_specific_evidence"]:
        assert evidence.lower() in text
    assert set(fixture["sparkbot_specific_evidence"]) != set(fixture["arc_specific_evidence"])


def test_archive_template_carries_remaining_product_blockers() -> None:
    fixture = _load_fixture()
    text = _template_text().replace("`", "")

    for blocker in fixture["remaining_blockers"]:
        assert blocker in text
