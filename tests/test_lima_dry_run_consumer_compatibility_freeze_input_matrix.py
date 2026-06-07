from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "dry_run_consumer_compatibility_freeze_input_matrix"
    / "freeze_input_matrix.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _matrix_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["matrix_path"]).read_text(encoding="utf-8")


def _review_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["readiness_review_path"]).read_text(encoding="utf-8")


def test_freeze_input_matrix_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_dry_run_consumer_compatibility_freeze_input_matrix_only"
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_proof_packet_audited"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_freeze_input_matrix_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in ("matrix_path", "readiness_review_path", "design_audit_path"):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_freeze_input_matrix_current_verdict_stays_not_ready() -> None:
    fixture = _load_fixture()
    text = _matrix_text()
    review = _review_text()

    assert fixture["current_matrix_verdict"] == "not_ready_for_freeze"
    assert "`not_ready_for_freeze`" in text
    assert "NOT READY for an actual dry-run consumer compatibility freeze" in review


def test_freeze_input_matrix_tracks_required_missing_inputs() -> None:
    fixture = _load_fixture()
    text = _matrix_text()
    review = _review_text()

    for input_id in fixture["required_missing_inputs"]:
        assert f"`{input_id}`" in text
    assert "Sparkbot consumer-owned dry-run proof packet is missing" in review
    assert "Arc Bot consumer-owned dry-run proof packet is missing" in review


def test_freeze_input_matrix_references_authoritative_artifacts() -> None:
    fixture = _load_fixture()
    text = _matrix_text()

    for path in fixture["required_reference_artifacts"]:
        assert f"`{path}`" in text
        assert (REPO_ROOT / path).exists(), path


def test_freeze_input_matrix_declares_allowed_and_forbidden_statuses() -> None:
    fixture = _load_fixture()
    text = _matrix_text()

    for status in fixture["allowed_input_statuses"]:
        assert f"`{status}`" in text
    for status in fixture["forbidden_input_statuses"]:
        assert f"`{status}`" in text
    assert "Only `accepted_for_dry_run_freeze_input` may count toward a future freeze design." in text


def test_freeze_input_matrix_limits_public_api_freeze_candidates() -> None:
    fixture = _load_fixture()
    text = _matrix_text()

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in text
    assert "must not promote `dry_run_candidate` imports" in text
    assert "`from lima import LimaKernel`" in text


def test_freeze_input_matrix_requires_non_execution_invariants() -> None:
    fixture = _load_fixture()
    text = _matrix_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in text


def test_freeze_input_matrix_requires_redaction_blockers() -> None:
    fixture = _load_fixture()
    text = _matrix_text()

    for blocker in fixture["redaction_blockers"]:
        assert blocker in text
    assert "status must be `needs_redaction`" in text


def test_freeze_input_matrix_keeps_freeze_blocked_on_missing_or_unsafe_evidence() -> None:
    fixture = _load_fixture()
    text = _matrix_text()

    for blocker in fixture["freeze_blockers"]:
        assert blocker in text


def test_freeze_input_matrix_forbids_automation_and_live_surfaces() -> None:
    fixture = _load_fixture()
    text = _matrix_text()

    for forbidden in fixture["forbidden_automation"]:
        assert forbidden in text


def test_freeze_input_matrix_declares_static_later_implementation_bounds() -> None:
    fixture = _load_fixture()
    text = _matrix_text()

    for path in fixture["allowed_later_static_files"]:
        assert f"`{path}`" in text
    assert "must remain static" in text

    normalized_text = text.replace("`", "")
    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in normalized_text


def test_freeze_input_matrix_recommends_independent_static_test_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == "audit-lima-dry-run-consumer-compatibility-freeze-input-matrix-static-tests"
