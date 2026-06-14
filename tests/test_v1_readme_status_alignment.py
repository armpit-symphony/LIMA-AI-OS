"""Static checks for the root README V1 status alignment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_readme_status_alignment.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_readme_status_fixture_preserves_candidate_only_boundary() -> None:
    fixture = _load_fixture()
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert (
        fixture["source_commit_before_alignment"]
        == "b095478efdb90bf92b7a11b6e820e5d97806e433"
    )
    assert fixture["document"] == "README.md"
    assert fixture["readme_section"] == "Current V1 Status"
    assert fixture["v1_g10_gate_complete"] is True
    assert fixture["v1_g11_approval_request_ready"] is True
    assert fixture["v1_g11_preflight_audit_ready"] is True
    assert fixture["v1_g11_work_order_ready"] is True
    assert fixture["v1_g11_operator_decision_packet_ready"] is True
    assert fixture["v1_g11_operator_decision_record_slot_added"] is True
    assert fixture["v1_g11_operator_decision_recorded_choice"] is None
    assert fixture["v1_g11_operator_decision_packet_records_approval"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_readme_status_fixture_names_first_shells() -> None:
    assert set(_load_fixture()["v1_target_shells"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_readme_status_fixture_adds_no_runtime_or_integration_behavior() -> None:
    fixture = _load_fixture()
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "provider_model_routing_added",
        "shell_wiring_added",
        "persistence_added",
        "haptic_device_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False


def test_v1_readme_status_fixture_points_to_exact_next_step() -> None:
    fixture = _load_fixture()
    assert (
        fixture["if_approved_scope"]
        == "typed_request_guardian_decision_preflight_runtime_slice"
    )
    assert (
        fixture["next_step"]
        == "record_one_valid_operator_choice_in_v1_g11_decision_record"
    )


def test_readme_contains_current_v1_status_and_boundaries() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    assert "## Current V1 Status" in text
    assert "LIMA remains `CANDIDATE_ONLY`." in text
    assert "`Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`" in text
    assert "`V1-G10` is complete" in text
    assert "The `V1-G11` approval request" in text
    assert "ready for operator decision" in text
    assert "does not approve runtime implementation" in text
    assert "No `lima/` runtime change" in text
    assert "provider/model routing" in text
    assert "shell wiring" in text
    assert "persistence" in text
    assert "haptic device behavior" in text
    assert "runtime export cleanup" in text
    assert "final API freeze" in text
    assert "production readiness" in text
    assert "empty Decision Record section" in text
    assert "record one valid operator choice in the packet's Decision Record section" in text
