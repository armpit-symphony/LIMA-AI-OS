"""Static checks for the current V1-G61 decision-log status."""

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
    / "v1_g61_decision_log_status.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g61_decision_log_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["decision_log_status_id"] == "v1_g61_decision_log_status"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["request_stage_lane_label"] == (
        "prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_commit_before_refresh"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["decision_log_adr"] == "ADR-0340"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g61_decision_log_records_current_gate_without_approval() -> None:
    fixture = _load_fixture()

    assert fixture["current_gate"] == "V1-G61"
    assert fixture["latest_completed_gate"] == "V1-G60"
    assert fixture["latest_authority_chain_audit"] == "V1-G56"
    assert fixture["operator_decision_packet_status_audit_complete"] is True
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert fixture["next_smallest_safe_step"] == (
        "record_one_valid_operator_choice_in_v1_g61_operator_decision_packet"
    )
    assert fixture["current_validation_focused_current_gate_tests_passed"] == 153
    assert fixture["current_validation_full_lima_suite_tests_passed"] == 5350


def test_v1_g61_decision_log_supersedes_historical_v1_adrs_for_current_gate() -> None:
    fixture = _load_fixture()

    assert fixture["historical_v1_adrs_superseded_for_current_gate"] == [
        "ADR-0338",
        "ADR-0339",
    ]


def test_v1_g61_decision_log_refresh_adds_no_forbidden_behavior() -> None:
    forbidden = _load_fixture()["forbidden_by_decision_log_refresh"]

    for key, value in forbidden.items():
        assert value is False, key


def test_v1_g61_decision_log_text_matches_current_gate() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["decision_log"]).read_text(
        encoding="utf-8"
    )
    operator_packet = (
        REPO_ROOT / fixture["documents"]["operator_decision_packet"]
    ).read_text(encoding="utf-8")

    assert (
        "## ADR-0340: V1-G61 Supersedes Earlier V1 Decision-Log Gates As Current Blocker"
        in text
    )
    assert (
        "The V1 decision log records `V1-G61` as the current operator-decision gate"
        in text
    )
    assert (
        "Earlier V1 ADRs, including the V1-G55 decision-log status and consumer "
        "target refresh, remain historical evidence only"
    ) in text
    assert "Valid V1-G61 operator choices are `Approve-V1-G61`, `Revise-V1-G61`, or `Pause`." in text
    assert "operator decision packet status audit" in text
    assert "exactly one valid operator choice is still required" in text
    assert "V1-G61 runtime implementation remains unapproved." in text
    assert "153 focused current-gate/release-readiness tests, 5350 full LIMA suite tests" in text
    assert "latest LIMA readiness freshness evidence with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests" in text
    assert "latest handoff freshness evidence with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests passing" in text
    assert "No runtime behavior is added by this decision-log refresh." in text
    assert "No `lima/` runtime files are changed by this decision-log refresh." in text
    assert "No public API exports are changed by this decision-log refresh." in text
    assert "No Sparkbot, public Sparkbot, Sparkbot_shell, or Arc-Bot-shell files" in text
    assert "No dependency manifest or lockfile is changed by this decision-log refresh." in text
    assert "No runtime vendor SDK import execution proof" in text
    assert "product-readiness claim" in text
    assert "production-readiness claim" in text
    assert "Approve-V1-G61" in operator_packet
    assert "Valid choice: Approve-V1-G61" in operator_packet
    assert "Template for `Approve-V1-G61`" in operator_packet
