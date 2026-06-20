"""Static checks for the V1 candidate test handoff manifest."""

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
    / "v1_candidate_test_handoff_manifest.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_candidate_test_handoff_manifest_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["manifest_id"] == "v1_candidate_test_handoff_manifest"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "docs-v1-candidate-test-handoff-manifest"
    assert fixture["source_lima_commit_before_manifest"] == (
        "992c17107830f2e0ea464301d864b24a855b5d6d"
    )
    assert fixture["handoff_verdict"] == (
        "READY_FOR_LOCAL_CANDIDATE_TESTING_WITH_BLOCKERS"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_candidate_test_handoff_manifest_records_repo_checkpoints() -> None:
    checkpoints = _load_fixture()["repository_checkpoints"]

    assert checkpoints["lima_ai_os"] == {
        "local_path": "C:\\Users\\limap\\LIMA-AI-OS",
        "branch": "audit-v1-g56-public-sparkbot-target-publication",
        "commit": "992c17107830f2e0ea464301d864b24a855b5d6d",
        "pushed": True,
    }
    assert checkpoints["public_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "repository": "sparkpit-labs/Sparkbot",
        "branch": "v1-g56-runtime-authority-chain-audit",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "local_dirty_state": "clean",
        "target_branch_present": False,
        "target_push_blocked": True,
        "target_push_blocker": "missing_write_credentials_for_sparkpit_labs_sparkbot",
    }
    assert checkpoints["accessible_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot",
        "repository": "armpit-symphony/Sparkbot",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ddaa4ccaacd328ddcc1f00a040c2c140abee428e",
        "pushed": True,
        "local_dirty_state": "clean",
    }
    assert checkpoints["arc_bot_shell"] == {
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ec06e7670f18eeae192fc0f995b6ffd07481d8c9",
        "pushed": True,
        "unrelated_dirty_worktree_files_present": True,
    }


def test_v1_candidate_test_handoff_manifest_validation_commands_are_complete() -> None:
    commands = _load_fixture()["validation_commands"]

    assert [item["step"] for item in commands] == list(range(1, 10))
    assert commands[0]["repo"] == "C:\\Users\\limap\\Sparkbot-public"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands[0]["command"]
    assert commands[0]["expected_result"] == "8 passed"
    assert commands[2]["repo"] == "C:\\Users\\limap\\Sparkbot"
    assert commands[2]["expected_result"] == "8 passed"
    assert commands[4]["repo"] == "C:\\Users\\limap\\Arc-Bot-shell"
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in commands[4]["command"]
    assert commands[5]["repo"] == "C:\\Users\\limap\\LIMA-AI-OS"
    assert "test_v1_g57_provider_execution_hardening_authorization_request_audit.py" in commands[5]["command"]
    assert commands[6]["command"] == "python -m compileall lima"
    assert commands[7]["command"] == "python -m pytest -q tests -p no:cacheprovider"
    assert commands[8]["command"] == "git diff --check"


def test_v1_candidate_test_handoff_manifest_scope_and_boundaries_are_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["candidate_scope_proven"] == [
        "public_sparkbot_local_fake_executor_g55_wrapper_smoke",
        "accessible_sparkbot_pushed_g56_fake_executor_smoke_checkpoint",
        "arc_bot_shell_pushed_g56_fake_executor_smoke_checkpoint",
        "lima_runtime_authority_chain_complete_through_g56",
        "g57_request_only_operator_gate_recorded",
    ]

    for key, value in fixture["required_false_boundaries"].items():
        assert value is False, key


def test_v1_candidate_test_handoff_manifest_records_blockers_and_stop_conditions() -> None:
    fixture = _load_fixture()

    assert fixture["current_blockers"] == {
        "public_sparkbot_publication": (
            "missing_write_credentials_for_sparkpit_labs_sparkbot"
        ),
        "v1_g57_implementation": "requires_exact_operator_choice",
        "arc_bot_shell_local_worktree": (
            "unrelated_dirty_files_outside_pushed_g56_evidence"
        ),
    }
    assert fixture["stop_conditions"] == [
        "public_sparkbot_push_without_write_credentials",
        "v1_g57_implementation_without_exact_approval",
        "consumer_repo_edit_from_manifest_lane",
        "runtime_or_public_api_change_from_manifest_lane",
        "secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]
    assert fixture["next_operator_actions"] == [
        "provide_public_sparkbot_write_credentials",
        "record_exactly_one_v1_g57_operator_choice",
        "if_g57_is_approved_implement_only_metadata_file_scope",
    ]


def test_v1_candidate_test_handoff_manifest_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["manifest"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Candidate Test Handoff Manifest" in text
    assert fixture["source_lima_commit_before_manifest"] in text
    assert "READY_FOR_LOCAL_CANDIDATE_TESTING_WITH_BLOCKERS" in text
    assert "public Sparkbot" in text
    assert "Arc-Bot-shell" in text
    assert "target branch absent on `sparkpit-labs/Sparkbot`" in text
    assert "V1-G57 remains unapproved" in text
    assert "No" not in text[:300]
    assert "does not approve V1-G57 implementation" in text
    assert "claim V1.0 completion, product readiness, or production readiness" in text


def test_v1_candidate_test_handoff_manifest_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["manifest"]).read_text(
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
