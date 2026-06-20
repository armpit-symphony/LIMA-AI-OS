"""Static checks for the V1 final candidate branch index."""

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
    / "v1_final_candidate_branch_index.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_final_candidate_branch_index_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["index_id"] == "v1_final_candidate_branch_index"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "docs-v1-final-candidate-branch-index"
    assert fixture["source_lima_commit_before_index"] == (
        "a10a81fb0ff0096911ab3e62d69463b590520055"
    )
    assert fixture["index_verdict"] == "CANDIDATE_INDEX_READY_WITH_EXTERNAL_UNBLOCKS"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_candidate_branch_index_records_lima_checkpoints() -> None:
    checkpoints = _load_fixture()["lima_branch_checkpoints"]

    assert [checkpoint["branch"] for checkpoint in checkpoints] == [
        "docs-v1-final-readiness-audit-template",
        "docs-v1-operator-unblock-action-packet",
        "docs-v1-final-blocker-register-after-arc-drift-audit",
        "audit-v1-arc-bot-shell-local-drift-exclusion",
        "audit-v1-g56-public-sparkbot-target-publication",
    ]
    assert [checkpoint["commit"] for checkpoint in checkpoints] == [
        "a10a81fb0ff0096911ab3e62d69463b590520055",
        "8270cb1b01be3798d2b974b85ca14d851e4aedeb",
        "d1b3d5a87739cfbc0a1e54a57951ab8cc975c502",
        "687637829ed652a341f94f0696cf8ba1afb7993c",
        "992c1714eab6d74a0a67de322942e4c9d1adb55e",
    ]


def test_v1_final_candidate_branch_index_records_consumer_checkpoints() -> None:
    consumers = _load_fixture()["consumer_checkpoints"]

    public_sparkbot = consumers["public_sparkbot_target_checkout"]
    assert public_sparkbot["local_path"] == "C:\\Users\\limap\\Sparkbot-public"
    assert public_sparkbot["branch"] == "v1-g56-runtime-authority-chain-audit"
    assert public_sparkbot["commit"] == (
        "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    )
    assert "blocked_by_write_credentials" in public_sparkbot["status"]

    accessible_sparkbot = consumers["accessible_sparkbot_checkpoint"]
    assert accessible_sparkbot["local_path"] == "C:\\Users\\limap\\Sparkbot"
    assert accessible_sparkbot["commit"] == (
        "ddaa4ccaacd328ddcc1f00a040c2c140abee428e"
    )
    assert accessible_sparkbot["status"] == "clean_pushed_branch"

    arc_bot_shell = consumers["arc_bot_shell_checkpoint"]
    assert arc_bot_shell["local_path"] == "C:\\Users\\limap\\Arc-Bot-shell"
    assert arc_bot_shell["commit"] == "ec06e7670f18eeae192fc0f995b6ffd07481d8c9"
    assert "unrelated_local_drift_excluded_from_proof" in arc_bot_shell["status"]


def test_v1_final_candidate_branch_index_requires_external_unblocks() -> None:
    fixture = _load_fixture()

    assert fixture["required_external_unblocks"] == [
        "public_sparkbot_write_credential_and_branch_publication",
        "exactly_one_valid_v1_g57_operator_choice_recorded",
        "if_approve_v1_g57_then_metadata_only_g57_implementation_complete",
    ]
    assert fixture["valid_v1_g57_choices"] == [
        "Approve-V1-G57",
        "Revise-V1-G57",
        "Pause",
    ]
    assert fixture["post_unblock_sequence"] == [
        "rerun_public_sparkbot_g56_smoke_and_diff_check",
        "rerun_accessible_sparkbot_g56_smoke_and_diff_check",
        "rerun_arc_bot_shell_g56_smoke_and_drift_state_check",
        "rerun_lima_compileall_full_suite_and_diff_check",
        "if_g57_approved_include_focused_g57_implementation_test_and_closeout",
        "run_final_readiness_audit_on_separate_branch",
    ]


def test_v1_final_candidate_branch_index_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_final_candidate_branch_index_stop_conditions_are_bounded() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "public_sparkbot_push_without_write_credentials",
        "v1_g57_implementation_without_exact_approval",
        "treat_this_index_as_g57_approval",
        "consumer_repo_edit_from_index_lane",
        "runtime_or_public_api_change_from_index_lane",
        "secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_final_candidate_branch_index_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["final_candidate_branch_index"]
    ).read_text(encoding="utf-8")

    assert "# V1 Final Candidate Branch Index" in text
    assert fixture["source_lima_commit_before_index"] in text
    assert "CANDIDATE_INDEX_READY_WITH_EXTERNAL_UNBLOCKS" in text
    assert "docs-v1-final-readiness-audit-template" in text
    assert "sparkpit-labs/Sparkbot" in text
    assert "Approve-V1-G57" in text
    assert "Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot` by this index: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_final_candidate_branch_index_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT / fixture["documents"]["final_candidate_branch_index"]
    ).read_text(encoding="utf-8")

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
