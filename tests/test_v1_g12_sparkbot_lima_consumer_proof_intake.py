"""Static checks for the V1-G12 Sparkbot LIMA consumer proof intake."""

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
    / "v1_g12_sparkbot_lima_consumer_proof_intake.json"
)
DOCS = {
    "intake": REPO_ROOT / "docs" / "V1_G12_SPARKBOT_LIMA_CONSUMER_PROOF_INTAKE.md",
    "audit": REPO_ROOT / "docs" / "V1_G12_SPARKBOT_LIMA_CONSUMER_PROOF_AUDIT.md",
    "closeout": REPO_ROOT / "docs" / "V1_G12_SPARKBOT_LIMA_CONSUMER_PROOF_CLOSEOUT.md",
    "current_state": REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g12_intake_summary_and_docs_exist() -> None:
    summary = _load_json(FIXTURE_PATH)
    assert FIXTURE_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()

    assert summary["gap_id"] == "V1-G12"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["branch"] == "v1-g12-sparkbot-lima-consumer-proof-intake"
    assert summary["source_branch"] == "v1-g11-runtime-request-decision-gate"
    assert summary["base_commit"] == "50425b41bb64cca8174c6fc21983cf44f8c41e6b"
    assert summary["sparkbot_branch"] == "proof-sparkbot-shell-lima-consumer-packet"
    assert summary["sparkbot_commit"] == "842a6757a2fbdc87451042eec465eb76be5bea80"
    assert summary["proof_packet_received"] is True
    assert summary["proof_audit_received"] is True
    assert summary["machine_readable_fixture_received"] is True
    assert summary["proof_accepted_as_static_evidence"] is True
    assert summary["proof_accepted_as_live_parity"] is False


def test_v1_g12_intake_preserves_boundaries() -> None:
    summary = _load_json(FIXTURE_PATH)

    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "runtime_exports_changed",
        "consumer_integration_added",
        "live_adapter_added",
        "sparkbot_touched",
        "sparkbot_shell_touched",
        "arc_bot_shell_touched",
        "sparkbot_wiring_added",
        "sparkbot_shell_wiring_added",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "provider_model_routing_added",
        "provider_model_calls_added",
        "guardian_authority_expanded",
        "lima_guardian_decision_authority_added",
        "approval_enforcement_added",
        "humaninput_bridge_activated",
        "connector_behavior_added",
        "browser_file_network_action_behavior_added",
        "external_sends_added",
        "device_robotics_physical_world_behavior_added",
        "haptic_device_behavior_added",
        "durable_persistence_added",
        "product_readiness_claimed",
        "production_readiness_claimed",
        "final_freeze_approved",
        "runtime_export_cleanup_approved",
    ):
        assert summary[key] is False


def test_v1_g12_consumer_status_and_contract_mapping() -> None:
    summary = _load_json(FIXTURE_PATH)

    assert summary["consumer_statuses"] == [
        "preview_only",
        "explain_plan",
        "blocked",
        "deferred",
    ]
    assert {
        "ConsumerRequest",
        "HumanInput",
        "TaskIntent",
        "TypedIntentEnvelope",
        "CandidatePreview",
        "RuntimeStateSnapshot",
        "GuardianDecision",
        "audit_spine",
    }.issubset(set(summary["mapped_lima_concepts"]))
    assert summary["candidate_preview_embodiment_profile_present"] is True
    assert "unmediated_model_routing_dispatch" in summary["blocked_surfaces"]
    assert "robotics_motion" in summary["blocked_surfaces"]


def test_v1_g12_accepts_and_rejects_correct_claims() -> None:
    summary = _load_json(FIXTURE_PATH)

    accepted = set(summary["accepted_evidence"])
    assert "Sparkbot proof packet delivered" in accepted
    assert "Sparkbot audit delivered" in accepted
    assert "Sparkbot machine-readable summary delivered" in accepted
    assert "candidate mappings documented" in accepted
    assert "CandidatePreview embodiment_profile documented" in accepted
    assert "Sparkbot accepted as substantial behavior-reference evidence" in accepted

    rejected = set(summary["rejected_claims"])
    assert "live_lima_runtime_consumer_parity" in rejected
    assert "sparkbot_on_lima_runtime_parity" in rejected
    assert "lima_guardian_decision_authority" in rejected
    assert "lima_approval_enforcement" in rejected
    assert "lima_provider_model_routing" in rejected
    assert "runtime_export_cleanup_approval" in rejected
    assert "final_api_freeze" in rejected


def test_v1_g12_records_top_blockers_and_recommendation() -> None:
    summary = _load_json(FIXTURE_PATH)

    blockers = set(summary["top_blockers"])
    assert blockers == {
        "no_live_consumer_request_intake_contract_in_shell",
        "no_shared_intent_adapter_for_taskintent_typedintentenvelope",
        "no_canonical_shell_to_lima_runtime_state_snapshot_event_contract",
        "no_lima_native_guardian_decision_authority_in_current_paths",
        "high_risk_actions_still_route_through_sparkbot_native_runtime_paths",
    }
    assert summary["recommended_option"] == "V1-G13"
    assert "strict non-execution Sparkbot LIMA Intake Adapter" in summary["recommended_next_step"]


def test_v1_g12_docs_state_static_only_verdict() -> None:
    intake_text = DOCS["intake"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    current_state_text = DOCS["current_state"].read_text(encoding="utf-8")

    assert "LIMA can accept the Sparkbot packet as static consumer-reference evidence." in intake_text
    assert "LIMA cannot treat the packet as live LIMA runtime consumer parity." in intake_text
    assert "API status remains `CANDIDATE_ONLY`" in intake_text
    assert "accept_static_consumer_reference_evidence_only" in audit_text
    assert "Do not treat this audit as approval to implement that adapter." in audit_text
    assert "Runtime behavior added by this intake: no." in closeout_text
    assert "Recommended: `V1-G13`." in closeout_text
    assert "## V1-G12 - Sparkbot LIMA Consumer Proof Intake" in current_state_text
