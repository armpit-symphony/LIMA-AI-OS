"""Static checklist for V1-G11 implementation-start preconditions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_G11_IMPLEMENTATION_START_CHECKLIST.md"
STATE_PATH = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g11_implementation_start_checklist.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_implementation_start_checklist_fixture_and_doc_exist() -> None:
    fixture = _load_fixture()

    assert DOC_PATH.exists()
    assert fixture["checklist_id"] == "v1_g11_implementation_start_checklist"
    assert fixture["gap_id"] == "V1-G11"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert fixture["checklist_status"] == "not_allowed_until_approve_v1_g11_recorded"
    assert fixture["docs_tests_fixtures_only"] is True


def test_v1_g11_implementation_start_is_not_allowed_today() -> None:
    fixture = _load_fixture()

    assert fixture["runtime_implementation_allowed_now"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["current_branch_may_implement"] is False


def test_v1_g11_required_approval_record_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["required_approval_record"] == {
        "recorded_choice": "Approve-V1-G11",
        "recorded_approval_wording": (
            "I explicitly approve V1-G11 implementation of the typed request and "
            "GuardianDecision preflight runtime slice, limited to the file scope, "
            "behavior scope, tests, rollback plan, and stop conditions in "
            "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md."
        ),
        "recorded_revision_request": None,
        "recorded_pause_reason": None,
        "approved_implementation_branch": "v1-g11-runtime-request-decision-gate",
        "runtime_implementation_approved": True,
    }


def test_v1_g11_current_decision_record_is_not_approval() -> None:
    fixture = _load_fixture()

    assert fixture["current_decision_record"] == {
        "recorded_choice": None,
        "recorded_approval_wording": None,
        "recorded_revision_request": None,
        "recorded_pause_reason": None,
        "approved_implementation_branch": None,
        "runtime_implementation_approved": False,
    }
    assert fixture["current_decision_record"] != fixture["required_approval_record"]


def test_v1_g11_allowed_branch_and_scope_are_fixed_if_approved() -> None:
    fixture = _load_fixture()

    assert (
        fixture["allowed_implementation_branch_if_approved"]
        == "v1-g11-runtime-request-decision-gate"
    )
    assert (
        fixture["approved_runtime_scope_if_approved"]
        == "typed_request_guardian_decision_preflight_runtime_slice"
    )


def test_v1_g11_approved_file_scope_if_approved_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_files_if_approved"] == [
        "lima/kernel/v1_runtime_request.py",
        "lima/kernel/__init__.py",
        "lima/guardian/v1_decision_gate.py",
        "lima/guardian/__init__.py",
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md",
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json",
        "tests/test_v1_g11_runtime_request_decision_gate.py",
    ]


def test_v1_g11_required_future_symbols_are_candidate_only() -> None:
    fixture = _load_fixture()

    assert fixture["required_future_symbols_if_approved"] == [
        "V1RuntimeRequestError",
        "build_v1_runtime_request",
        "V1GuardianDecisionGateError",
        "review_v1_runtime_request",
    ]


def test_v1_g11_current_boundary_flags_all_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["current_boundary_flags"]
    assert all(value is False for value in fixture["current_boundary_flags"].values())


def test_v1_g11_still_forbidden_if_approved_contains_major_boundaries() -> None:
    fixture = _load_fixture()
    forbidden = set(fixture["still_forbidden_if_approved"])

    for key in (
        "provider_model_calls_or_runtime_routing",
        "shell_runtime_wiring",
        "sparkbot_sparkbot_shell_arc_bot_shell_imports_or_code_copy",
        "durable_persistence_database_writes_audit_storage",
        "haptic_device_behavior",
        "runtime_export_cleanup",
        "final_api_freeze",
        "v1_product_or_production_readiness_claims",
    ):
        assert key in forbidden


def test_v1_g11_required_validation_if_approved_is_complete() -> None:
    fixture = _load_fixture()

    assert fixture["required_validation_if_approved"] == [
        'cmd /c "python3 --version || python --version"',
        'cmd /c "python3 -m compileall lima || python -m compileall lima"',
        (
            'cmd /c "python3 -m pytest -q '
            'tests\\test_v1_g11_runtime_request_decision_gate.py || '
            'python -m pytest -q tests\\test_v1_g11_runtime_request_decision_gate.py"'
        ),
        'cmd /c "python3 -m pytest -q || python -m pytest -q"',
        "git diff --check",
        "git diff --cached --check",
    ]


def test_v1_g11_implementation_start_doc_and_state_match_fixture() -> None:
    fixture = _load_fixture()
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    state_text = STATE_PATH.read_text(encoding="utf-8")

    for phrase in fixture["doc_required_phrases"]:
        assert phrase in doc_text

    assert fixture["state_required_phrase"] in state_text
    assert "Runtime implementation allowed now: no." in doc_text
    assert "Runtime export cleanup approved: no." in doc_text
    assert "Final API freeze approved: no." in doc_text
    assert (
        fixture["recommended_next_step"]
        == "record_exactly_one_valid_operator_choice_in_decision_record"
    )
