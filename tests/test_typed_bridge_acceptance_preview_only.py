"""Static V1-G2 typed bridge positive acceptance proof."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
SUMMARY_PATH = FIXTURE_DIR / "v1_g2_typed_bridge_acceptance_proof.json"
PREVIEW_PATH = FIXTURE_DIR / "typed_bridge_acceptance_preview_only_positive.json"
DOCS = {
    "proof": REPO_ROOT / "docs" / "V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md",
    "audit": REPO_ROOT / "docs" / "V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF_AUDIT.md",
    "closeout": REPO_ROOT / "docs" / "V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF_CLOSEOUT.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g2_summary_and_docs_exist_and_accept_static_proof_only() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert SUMMARY_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()
    assert summary["gap_id"] == "V1-G2"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["v1_g2_status"] == "complete_static_docs_tests_fixtures_proof"
    assert summary["proof_completed"] is True
    assert summary["proof_accepted_as_static_evidence"] is True
    assert summary["proof_accepted_as_runtime_parity"] is False
    assert summary["v1_product_ready"] is False


def test_v1_g2_summary_tracks_all_expected_case_fixtures() -> None:
    summary = _load_json(SUMMARY_PATH)
    expected = {
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_preview_only_positive.json",
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_approval_bypass.json",
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_runtime_claim.json",
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_missing_guardian_request.json",
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_execution_claim.json",
        (
            "tests/fixtures/runtime_extraction/"
            "typed_bridge_acceptance_fail_closed_provider_model_tool_driver_claim.json"
        ),
        (
            "tests/fixtures/runtime_extraction/"
            "typed_bridge_acceptance_fail_closed_browser_file_network_device_robotics_claim.json"
        ),
    }
    assert set(summary["case_fixture_files"]) == expected
    for relative_path in expected:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g2_metadata_chain_and_status_mappings_are_proven() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert summary["metadata_chain_under_proof"] == [
        "source_request_metadata",
        "typed_intentenvelope_candidate_metadata",
        "guardian_request_metadata",
        "future_guardian_decision_metadata_absent_pending_or_blocked",
        "still_no_execution",
    ]
    assert set(summary["packet_statuses"]) == {
        "preview_only",
        "explain_plan",
        "blocked",
        "deferred",
    }
    mappings = {
        entry["kernel_status"]: entry["packet_status"]
        for entry in summary["kernel_status_mappings"]
    }
    assert mappings == {
        "proposed": "preview_only",
        "needs_review": "explain_plan",
        "blocked": "blocked",
    }


def test_v1_g2_preview_only_fixture_has_complete_metadata_chain() -> None:
    fixture = _load_json(PREVIEW_PATH)
    assert fixture["case_id"] == "typed_bridge_acceptance_preview_only_positive"
    assert fixture["case_family"] == "positive_non_authoritative_preview"
    assert fixture["docs_tests_fixtures_only"] is True
    source = fixture["source_request_metadata"]
    assert source["source_kind"] == "shell_request"
    assert source["tenant_id"]
    assert source["actor_id"]
    assert source["lineage_ref"]
    candidate = fixture["typed_intentenvelope_candidate_metadata"]
    assert candidate["candidate_status"] == "proposed"
    assert candidate["non_authoritative"] is True
    assert candidate["intent_kind"] == "drafting"
    guardian_request = fixture["guardian_request_metadata"]
    assert guardian_request["request_state"] == "needs_review"
    assert guardian_request["approval_posture"] == "not_granted"
    future_decision = fixture["future_guardian_decision_metadata"]
    assert future_decision["state"] == "absent"
    assert future_decision["decision_id"] is None
    assert future_decision["approval_granted"] is False
    assert future_decision["execution_allowed"] is False


def test_v1_g2_preview_only_fixture_maps_to_preview_only_without_authority() -> None:
    fixture = _load_json(PREVIEW_PATH)
    assert fixture["kernel_status"] == "proposed"
    assert fixture["packet_status"] == "preview_only"
    assert set(fixture["packet_status_catalog"]) == {
        "preview_only",
        "explain_plan",
        "blocked",
        "deferred",
    }
    assert fixture["expected_blocked_claims"] == []
    flags = fixture["control_flags"]
    assert flags["non_authoritative"] is True
    assert flags["safe_by_default"] is True
    assert flags["local_only"] is True
    assert flags["deterministic"] is True
    for key in (
        "execution_allowed",
        "dispatch_allowed",
        "persistence_allowed",
        "approval_granted",
        "external_calls_allowed",
        "provider_model_routing_allowed",
        "model_calls_allowed",
        "tool_calls_allowed",
        "driver_calls_allowed",
        "adapter_calls_allowed",
        "browser_file_network_device_robotics_allowed",
        "haptic_device_behavior_allowed",
        "physical_world_allowed",
        "guardian_decision_created",
        "runtime_test_harness_active",
    ):
        assert flags[key] is False


def test_v1_g2_summary_boundary_results_add_no_runtime_behavior() -> None:
    summary = _load_json(SUMMARY_PATH)
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
        "shell_repos_changed",
        "sparkbot_shell_wiring_added",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "arc_bot_shell_wiring_added",
        "provider_model_routing_added",
        "guardian_decision_runtime_added",
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "haptic_device_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert summary[key] is False


def test_v1_g2_docs_state_static_only_verdict_and_next_gap() -> None:
    proof_text = DOCS["proof"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    assert "V1-G2 is complete as static docs/tests/fixtures acceptance proof only." in proof_text
    assert "It is not runtime parity and does not approve runtime implementation." in proof_text
    assert "Verdict: `accept_static_typed_bridge_acceptance_proof_only`." in audit_text
    assert "Recommended: `V1-G3`." in closeout_text
