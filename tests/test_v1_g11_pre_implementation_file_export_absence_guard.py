"""Static guard for V1-G11 pre-approval file/export absence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    REPO_ROOT / "docs" / "V1_G11_PRE_IMPLEMENTATION_FILE_EXPORT_ABSENCE_GUARD.md"
)
STATE_PATH = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g11_pre_implementation_file_export_absence_guard.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_pre_implementation_guard_fixture_and_doc_exist() -> None:
    fixture = _load_fixture()

    assert DOC_PATH.exists()
    assert fixture["guard_id"] == "v1_g11_pre_implementation_file_export_absence_guard"
    assert fixture["gap_id"] == "V1-G11"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert fixture["guard_status"] == "retired_after_approve_v1_g11_recorded"
    assert fixture["docs_tests_fixtures_only"] is True


def test_v1_g11_pre_implementation_approval_record_is_present() -> None:
    fixture = _load_fixture()

    assert fixture["runtime_implementation_approved"] is True
    assert fixture["operator_approval_recorded"] is True
    assert fixture["current_decision_record_empty"] is False
    assert fixture["approved_implementation_branch"] == "v1-g11-runtime-request-decision-gate"


def test_v1_g11_pre_implementation_runtime_boundaries_are_false() -> None:
    fixture = _load_fixture()

    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_import_added",
        "sparkbot_shell_import_added",
        "arc_bot_shell_import_added",
        "sparkbot_code_copied",
        "provider_model_routing_added",
        "shell_wiring_added",
        "persistence_added",
        "haptic_device_behavior_added",
        "browser_file_network_device_robotics_physical_world_added",
        "runtime_exports_changed",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
        "v1_product_ready",
        "production_ready",
    ):
        assert fixture[key] is False


def test_v1_g11_current_decision_record_is_approval() -> None:
    fixture = _load_fixture()

    assert fixture["current_decision_record_empty"] is False
    assert fixture["current_decision_record"] == {
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


def test_v1_g11_previously_forbidden_files_are_approved_file_map() -> None:
    fixture = _load_fixture()

    assert fixture["previously_forbidden_pre_approval_files"] == [
        "lima/kernel/v1_runtime_request.py",
        "lima/guardian/v1_decision_gate.py",
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md",
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json",
        "tests/test_v1_g11_runtime_request_decision_gate.py",
    ]


def test_v1_g11_previous_kernel_exports_are_recorded_as_historical_boundary() -> None:
    fixture = _load_fixture()

    assert fixture["current_kernel_exports"] == [
        "ALLOWED_CANDIDATE_STATUSES",
        "CandidatePreview",
        "CandidateStatusError",
        "IntakeCandidateError",
        "RuntimeStateSnapshot",
        "build_intake_candidate",
        "inspect_runtime_state",
        "normalize_candidate_status",
        "preview_candidate",
        "validate_candidate",
    ]


def test_v1_g11_previous_guardian_exports_are_recorded_as_historical_boundary() -> None:
    fixture = _load_fixture()

    assert fixture["current_guardian_exports"] == [
        "FakeApprovalRecorder",
        "FakeAuthProvider",
        "FakeBreakglassProvider",
        "FakeGuardianDecisionEvaluator",
        "FakeGuardianPipeline",
        "FakeGuardianPipelineResult",
        "FakePolicyRiskEvaluator",
        "FakeSpineAuditRecorder",
        "FakeVaultProvider",
        "AdapterFixtureHarness",
        "AdapterFixtureHarnessResult",
        "HumanInputFakePipelineBridge",
        "HumanInputPipelineBridgeConfig",
    ]


def test_v1_g11_future_symbols_are_recorded_as_now_eligible_if_approved() -> None:
    fixture = _load_fixture()

    assert fixture["proposed_future_symbols_if_approved"] == [
        "V1RuntimeRequestError",
        "build_v1_runtime_request",
        "V1GuardianDecisionGateError",
        "review_v1_runtime_request",
    ]


def test_v1_g11_pre_implementation_guard_doc_and_state_match_fixture() -> None:
    fixture = _load_fixture()
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    state_text = STATE_PATH.read_text(encoding="utf-8")

    for phrase in fixture["doc_required_phrases"]:
        assert phrase in doc_text

    assert fixture["state_required_phrase"] in state_text
    assert "Runtime export cleanup approved: no." in doc_text
    assert "Final API freeze approved: no." in doc_text
    assert (
        fixture["recommended_next_step"]
        == "create_approved_v1_g11_implementation_branch"
    )
