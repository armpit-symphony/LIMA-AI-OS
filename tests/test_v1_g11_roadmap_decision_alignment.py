"""Static checks for V1-G11 roadmap and decision alignment."""

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
    / "v1_g11_roadmap_decision_alignment.json"
)
ROADMAP_PATH = REPO_ROOT / "docs" / "ROADMAP.md"
DECISIONS_PATH = REPO_ROOT / "docs" / "DECISIONS.md"
OPERATOR_DECISION_PATH = (
    REPO_ROOT
    / "docs"
    / "V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_alignment_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()
    assert FIXTURE_PATH.exists()
    assert ROADMAP_PATH.exists()
    assert DECISIONS_PATH.exists()
    assert OPERATOR_DECISION_PATH.exists()
    assert fixture["alignment_id"] == "v1_g11_roadmap_decision_alignment"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert fixture["base_commit"] == "a1dfc5e4952b099e7a083382a9429a84831bc8d7"
    assert fixture["documents"]["roadmap"] == "docs/ROADMAP.md"
    assert fixture["documents"]["decisions"] == "docs/DECISIONS.md"
    assert fixture["documents"]["approval_request"] == (
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md"
    )
    assert fixture["documents"]["operator_decision_packet"] == (
        "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md"
    )


def test_v1_g11_alignment_preserves_unapproved_runtime_boundary() -> None:
    fixture = _load_fixture()
    assert fixture["roadmap_alignment_added"] is True
    assert fixture["decision_record_added"] is True
    assert fixture["decision_id"] == "ADR-0336"
    assert fixture["decision_ids"] == ["ADR-0336", "ADR-0337"]
    assert fixture["operator_decision_packet_added"] is True
    assert fixture["operator_decision_packet_ready"] is True
    assert fixture["operator_decision_record_slot_added"] is True
    assert fixture["operator_decision_recorded_choice"] is None
    assert fixture["operator_decision_packet_records_approval"] is False
    assert fixture["approval_request_ready"] is True
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_behavior_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["shell_repos_changed"] is False
    assert fixture["sparkbot_code_copied"] is False
    assert fixture["sparkbot_import_added"] is False
    assert fixture["provider_model_routing_added"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["final_freeze_approved"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_g11_alignment_accepts_request_readiness_only() -> None:
    fixture = _load_fixture()
    accepted = set(fixture["accepted_alignment"])
    assert "v1_g11_approval_request_is_ready_for_operator_decision" in accepted
    assert "v1_g11_request_packet_does_not_record_operator_approval" in accepted
    assert "v1_g11_operator_decision_packet_records_valid_choices_without_approval" in accepted
    assert "v1_g11_operator_decision_packet_has_empty_decision_record_slot" in accepted
    assert "runtime_remains_unapproved" in accepted
    assert "approved_future_scope_must_match_v1_g11_request_exactly" in accepted

    rejected = set(fixture["rejected_claims"])
    assert "implicit_runtime_approval_from_broad_product_goal" in rejected
    assert "runtime_implementation_approved" in rejected
    assert "real_guardian_decision_runtime_added" in rejected
    assert "live_approval_enforcement_added" in rejected
    assert "provider_model_routing_added" in rejected
    assert "shell_runtime_wiring_added" in rejected
    assert "runtime_export_cleanup_approved" in rejected
    assert "final_api_freeze_approved" in rejected
    assert "v1_product_readiness_approved" in rejected
    assert "production_readiness_approved" in rejected
    assert (
        fixture["recommended_next_step"]
        == "record_one_valid_operator_choice_in_v1_g11_decision_record"
    )


def test_v1_g11_roadmap_and_decision_text_match_fixture() -> None:
    roadmap = ROADMAP_PATH.read_text(encoding="utf-8")
    decisions = DECISIONS_PATH.read_text(encoding="utf-8")

    assert "## V1-G11 - Runtime Request Decision Gate Approval Request" in roadmap
    assert "next step is to record one valid operator choice in the V1-G11 operator decision packet's Decision Record section" in roadmap
    assert "empty Decision Record section" in roadmap
    assert "The request and operator decision packet do not approve runtime implementation." in roadmap
    assert "No `lima/` files" in roadmap

    assert "## ADR-0336: V1-G11 Approval Request Is Ready But Runtime Remains Unapproved" in (
        decisions
    )
    assert "## ADR-0337: V1-G11 Operator Decision Packet Records Choices But Not Approval" in (
        decisions
    )
    assert "runtime implementation remains unapproved" in decisions
    assert "does not record approval or authorize runtime implementation" in decisions
    assert "empty Decision Record section" in decisions
    assert "Operator approval is not recorded by the request packet." in decisions
    assert "Destructive edit/delete must map to approval-required status" in decisions
