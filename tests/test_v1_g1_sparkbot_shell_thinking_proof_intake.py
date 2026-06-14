"""Static checks for the V1-G1 Sparkbot_shell thinking proof intake."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g1_sparkbot_shell_thinking_proof_intake.json"
)
DOCS = {
    "intake": REPO_ROOT / "docs" / "V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md",
    "audit": REPO_ROOT / "docs" / "V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE_AUDIT.md",
    "closeout": REPO_ROOT / "docs" / "V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE_CLOSEOUT.md",
}


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g1_intake_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()
    assert FIXTURE_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()
    assert fixture["gap_id"] == "V1-G1"
    assert fixture["gap_name"] == "sparkbot_shell_thinking_progress_proof"
    assert fixture["request_document"] == "docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_REQUEST.md"
    assert fixture["source_target"] == "docs/V1_PRODUCT_READINESS_TARGET.md"
    assert fixture["gap_matrix"] == "docs/V1_READINESS_GAP_MATRIX.md"


def test_v1_g1_intake_accepts_source_backed_thinking_only() -> None:
    fixture = _load_fixture()
    assert fixture["proof_received"] is True
    assert fixture["proof_accepted_as_source_backed_shell_evidence"] is True
    assert fixture["proof_accepted_as_live_parity"] is False
    assert fixture["v1_g1_status"] == "accepted_source_backed_local_shell_evidence"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["source_backed_thinking"] is True
    assert fixture["docs_fixture_only_thinking"] is False
    assert fixture["sparkbot_shell_local_ui_behavior_added"] is True


def test_v1_g1_intake_records_source_files_and_transitions() -> None:
    fixture = _load_fixture()
    assert {
        "src/types/shell.ts",
        "src/components/ChatShell.tsx",
        "src/styles.css",
    }.issubset(set(fixture["thinking_source_files"]))
    assert "ChatMessage.shellState" in set(fixture["thinking_render_entrypoints"])
    transitions = {(entry["from"], entry["to"]) for entry in fixture["state_transitions"]}
    assert ("received", "thinking") in transitions
    assert ("thinking", "completed") in transitions
    assert fixture["desktop_behavior_reviewed"] is True
    assert fixture["mobile_behavior_reviewed"] is True


def test_v1_g1_intake_keeps_haptics_shell_owned() -> None:
    fixture = _load_fixture()
    assert fixture["haptics_shell_owned"] is True
    assert fixture["lima_owns_haptics"] is False
    assert fixture["haptic_implementation_added"] is False
    assert "haptic implementation" in set(fixture["rejected_claims"])
    assert "haptic proof" in set(fixture["rejected_claims"])


def test_v1_g1_intake_boundary_results_add_no_lima_runtime_behavior() -> None:
    boundary = _load_fixture()["lima_boundary_results"]
    assert boundary["docs_tests_fixtures_only"] is True
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
        "sparkbot_shell_wiring_added",
        "sparkbot_shell_import_added",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "provider_model_routing_added",
        "guardian_decision_runtime_added",
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "audit_persistence_added",
        "production_readiness_claimed",
        "v1_product_ready",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert boundary[key] is False


def test_v1_g1_intake_remaining_blockers_and_next_step_are_honest() -> None:
    fixture = _load_fixture()
    blockers = set(fixture["remaining_v1_blockers"])
    assert "typed_bridge_acceptance_proof_missing" in blockers
    assert "destructive_edit_delete_operator_approval_contract_missing" in blockers
    assert "real_guardian_decision_path_not_implemented" in blockers
    assert "provider_model_routing_runtime_not_implemented" in blockers
    assert "haptics_proof_missing" in blockers
    assert "production_behavior_not_approved" in blockers
    assert fixture["recommended_next_step"] == "V1-G2"


def test_v1_g1_intake_docs_match_acceptance_and_rejection() -> None:
    intake_text = DOCS["intake"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    assert "Can LIMA accept this as source-backed shell UX evidence for `thinking`?" in intake_text
    assert "**Yes**" in intake_text
    assert "Can LIMA treat this as live Sparkbot-style runtime parity?" in intake_text
    assert "Verdict: `accept_source_backed_thinking_evidence_only`" in audit_text
    assert "`V1-G1` is accepted as source-backed local Sparkbot_shell `thinking` evidence." in closeout_text
    assert "Recommended: **V1-G2**" in closeout_text
