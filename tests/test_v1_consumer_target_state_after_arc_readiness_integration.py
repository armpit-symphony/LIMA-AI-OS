"""Static checks for the V1 consumer target state refresh."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "readiness"
    / "V1_CONSUMER_TARGET_STATE_AFTER_ARC_READINESS_INTEGRATION.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_consumer_target_state_after_arc_readiness_integration.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_consumer_target_state_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert DOC_PATH.exists()
    assert fixture["document"] == (
        "docs/readiness/V1_CONSUMER_TARGET_STATE_AFTER_ARC_READINESS_INTEGRATION.md"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert (
        fixture["branch"]
        == "docs-v1-consumer-target-state-after-arc-readiness-integration"
    )
    assert fixture["source_commit_before_refresh"] == (
        "a1a0c95565982fb9c2e4e2a4d6240f09f2348b67"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_consumer_target_state_keeps_g55_as_unapproved_gate() -> None:
    fixture = _load_fixture()

    assert fixture["current_gate"] == "V1-G55"
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G55",
        "Revise-V1-G55",
        "Pause",
    ]
    assert fixture["v1_g55_operator_approval_recorded"] is False
    assert fixture["v1_g55_runtime_implementation_approved"] is False


def test_consumer_target_state_records_current_g61_refresh() -> None:
    refresh = _load_fixture()["current_status_refresh"]

    assert refresh["current_gate"] == "V1-G61"
    assert refresh["latest_completed_gate"] == "V1-G60"
    assert refresh["latest_authority_chain_audit"] == "V1-G56"
    assert refresh["required_next_action"] == "record_exactly_one_v1_g61_operator_choice"
    assert refresh["valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert refresh["v1_g61_operator_approval_recorded"] is False
    assert refresh["v1_g61_runtime_vendor_sdk_import_execution_proof_implemented"] is False
    assert refresh["g61_operator_decision_packet_status_audit"] == (
        "awaiting_exactly_one_valid_operator_choice"
    )
    assert refresh["historical_g55_gate_superseded_for_current_action"] is True
    assert refresh["latest_post_g61_request_refresh_focused_tests_passed"] == 8
    assert refresh["latest_post_g61_request_refresh_broader_tests_passed"] == 117
    assert refresh["latest_post_g61_request_refresh_full_lima_suite_tests_passed"] == 5362
    assert refresh["latest_quickstart_artifact_refresh_focused_tests_passed"] == 7
    assert refresh["latest_quickstart_artifact_refresh_adjacent_tests_passed"] == 64
    assert refresh["latest_quickstart_artifact_refresh_broader_tests_passed"] == 133
    assert refresh["latest_quickstart_artifact_refresh_full_lima_suite_tests_passed"] == 5364
    assert refresh["latest_handoff_freshness_authority_created"] is False


def test_consumer_target_state_records_first_consumer_targets() -> None:
    targets = _load_fixture()["consumer_targets"]

    assert targets["sparkbot_shell"] == {
        "repository": "armpit-symphony/Sparkbot_shell",
        "local_path": "C:\\Users\\limap\\Sparkbot_shell",
        "branch": "sparkbot-shell-work-settings-runtime-preview",
        "commit": "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc",
        "clean": True,
        "tracks_origin": True,
    }
    assert targets["public_sparkbot"] == {
        "repository": "sparkpit-labs/Sparkbot",
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "branch": "public-work-settings-preview",
        "commit": "81eed8c4067b1a73885bbc79003ea5870b1604a2",
        "clean": True,
        "remote_push_blocked": True,
        "remote_push_blocker": "github_403_permission_denied_to_armpit_symphony",
    }
    assert targets["arc_bot_shell"] == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "branch": "arc-bot-runtime-ui-scaffold-foundation-phase-chain",
        "commit": "3004367aa7aa96b4b2518c0e3783cf5afba979c0",
        "clean": True,
        "tracks_origin": True,
        "pushed_to_origin": True,
    }


def test_consumer_target_state_records_arc_readiness_integration_evidence() -> None:
    fixture = _load_fixture()
    evidence = set(fixture["accepted_arc_consumer_evidence"])

    assert evidence == {
        "V1_ARC_PHASE1_READINESS_BUNDLE_AUDIT",
        "V1_ARC_PHASE1_RUNTIME_AUTHORITY_GATING_AUDIT",
        "V1_ARC_RUNTIME_GATING_READINESS_INTEGRATION_AUDIT",
    }

    gating = fixture["arc_runtime_authority_gating_state"]
    assert gating["projection_in_default_readiness_bundle"] is True
    assert gating["required_future_gates_unresolved"] is True
    assert gating["runtime_authority_blocked"] is True
    assert gating["runtime_execution_blocked"] is True
    assert gating["connector_behavior_blocked"] is True
    assert gating["worker_dispatch_blocked"] is True
    assert gating["customer_system_mutation_blocked"] is True
    assert gating["product_readiness_claimed"] is False


def test_consumer_target_state_boundary_results_are_non_runtime() -> None:
    for key, value in _load_fixture()["boundary_results"].items():
        assert value is False, key


def test_consumer_target_state_text_matches_fixture() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "# V1 Consumer Target State After Arc Readiness Integration" in text
    assert "API status: `CANDIDATE_ONLY`" in text
    assert "The active implementation gate remains `V1-G55`." in text
    assert "## Current Status Refresh" in text
    assert "This document's original runtime-gate section is historical audit-time evidence" in text
    assert "Current active gate: `V1-G61`." in text
    assert "Valid V1-G61 choices: `Approve-V1-G61`, `Revise-V1-G61`, or `Pause`." in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "awaiting exactly one valid operator choice" in text
    assert "V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md" in text
    assert "latest post-G61 request readiness-refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART.md" in text
    assert "latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "does not override the current G61 operator-decision blocker" in text
    assert "`Approve-V1-G55`" in text
    assert "`Revise-V1-G55`" in text
    assert "`Pause`" in text
    assert "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc" in text
    assert "81eed8c4067b1a73885bbc79003ea5870b1604a2" in text
    assert "3004367aa7aa96b4b2518c0e3783cf5afba979c0" in text
    assert "GitHub 403" in text
    assert "all required future gates unresolved" in text
    assert "runtime execution disabled" in text
    assert "Provider SDK/network egress invocation added: no." in text
    assert "V1 product readiness claimed: no." in text
    assert (
        "Historical audit-time next step was to record exactly one valid operator choice in "
        "`docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md`"
        in text
    )
    assert (
        "Current next step is to record exactly one V1-G61 operator choice in "
        "`docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md`"
        in text
    )


def test_current_state_and_readme_reference_consumer_target_refresh() -> None:
    fixture = _load_fixture()
    state_text = (
        REPO_ROOT / fixture["documents"]["current_project_state"]
    ).read_text(encoding="utf-8")
    readme_text = (REPO_ROOT / fixture["documents"]["readme"]).read_text(
        encoding="utf-8"
    )

    for text in (state_text, readme_text):
        assert "V1 consumer target state after Arc readiness integration" in text
        assert (
            "docs/readiness/V1_CONSUMER_TARGET_STATE_AFTER_ARC_READINESS_INTEGRATION.md"
            in text
        )
        assert "V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md" in text
        assert "Sparkbot remote publication remains blocked by GitHub 403" not in text
        assert "audited through `V1-G56`" in text or (
            "V1 runtime authority chain audit through G56: complete." in text
        )
        assert "V1-G57" in text
        assert "product readiness" in text
