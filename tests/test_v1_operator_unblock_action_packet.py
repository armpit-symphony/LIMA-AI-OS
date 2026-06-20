"""Static checks for the V1 operator unblock action packet."""

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
    / "v1_operator_unblock_action_packet.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_operator_unblock_packet_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["packet_id"] == "v1_operator_unblock_action_packet"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "docs-v1-operator-unblock-action-packet"
    assert fixture["source_lima_commit_before_packet"] == (
        "d1b3d5ae02d6d363876eaf6369dbdba6f1cb7f48"
    )
    assert fixture["packet_verdict"] == "AWAITING_OPERATOR_UNBLOCK_ACTIONS"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_operator_unblock_packet_records_public_sparkbot_action() -> None:
    action = _load_fixture()["required_operator_actions"]["public_sparkbot_publication"]

    assert action["required_action"] == (
        "provide_or_switch_to_write_credential_then_publish_branch"
    )
    assert action["local_path"] == "C:\\Users\\limap\\Sparkbot-public"
    assert action["target_repository"] == "sparkpit-labs/Sparkbot"
    assert action["branch"] == "v1-g56-runtime-authority-chain-audit"
    assert action["commit"] == "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    assert action["current_blocker"] == "github_http_403_current_credential"
    assert action["branch_pushed_to_target_by_packet"] is False
    assert action["validation_before_retry"] == [
        "python -m pytest -q tests\\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider",
        "git diff --check",
    ]
    assert "push origin v1-g56-runtime-authority-chain-audit" in action[
        "publication_command_after_credentials"
    ]
    assert action["close_evidence_required"] == [
        "branch_pushed_to_sparkpit_labs_sparkbot_or_authorized_pr_compare_evidence",
        "public_sparkbot_g56_smoke_still_passing",
        "no_secret_credential_token_raw_diff_or_raw_file_content_persisted",
    ]


def test_v1_operator_unblock_packet_records_exact_g57_decision_action() -> None:
    action = _load_fixture()["required_operator_actions"]["v1_g57_operator_decision"]

    assert action["required_action"] == (
        "record_exactly_one_valid_v1_g57_operator_choice"
    )
    assert action["valid_choices"] == ["Approve-V1-G57", "Revise-V1-G57", "Pause"]
    assert action["operator_choice_recorded_by_packet"] is False
    assert action["exact_approve_text"] == (
        "Approve-V1-G57\n\n"
        "I explicitly approve V1-G57 implementation of the LIMA-side provider "
        "execution hardening authorization metadata slice, limited to the file "
        "scope, behavior scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md."
    )
    assert action["approved_future_file_scope_if_approved"] == [
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION.md",
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g57_provider_execution_hardening_authorization.json",
        "tests/test_v1_g57_provider_execution_hardening_authorization.py",
    ]
    assert action["close_evidence_required"] == [
        "exactly_one_valid_operator_choice_recorded",
        "if_approve_v1_g57_then_implementation_stays_in_approved_metadata_scope",
        "if_revise_or_pause_then_implementation_does_not_begin",
    ]


def test_v1_operator_unblock_packet_preserves_current_evidence_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["current_evidence_to_preserve"] == [
        "v1_final_blocker_register_after_arc_drift_audit",
        "v1_arc_bot_shell_local_drift_exclusion_audit",
        "v1_candidate_handoff_manifest_execution_audit",
        "v1_g57_request_audit",
        "v1_g57_approval_request",
    ]

    for key, value in fixture["boundaries_preserved"].items():
        assert value is False, key


def test_v1_operator_unblock_packet_stop_conditions_and_next_step_are_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["stop_conditions"] == [
        "public_sparkbot_push_without_write_credentials",
        "v1_g57_implementation_without_exact_approval",
        "treat_this_packet_as_g57_approval",
        "consumer_repo_edit_from_packet_lane",
        "runtime_or_public_api_change_from_packet_lane",
        "secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]
    assert fixture["next_step_after_both_actions"] == (
        "run_final_v1_readiness_audit_after_public_sparkbot_publication_and_v1_g57_decision_are_resolved"
    )


def test_v1_operator_unblock_packet_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["operator_unblock_packet"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Operator Unblock Action Packet" in text
    assert fixture["source_lima_commit_before_packet"] in text
    assert "AWAITING_OPERATOR_UNBLOCK_ACTIONS" in text
    assert "Approve-V1-G57" in text
    assert "I explicitly approve V1-G57 implementation" in text
    assert "push origin v1-g56-runtime-authority-chain-audit" in text
    assert "Public Sparkbot branch pushed by this packet: no." in text
    assert "V1-G57 operator decision recorded by this packet: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_operator_unblock_packet_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["operator_unblock_packet"]).read_text(
        encoding="utf-8"
    )

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
