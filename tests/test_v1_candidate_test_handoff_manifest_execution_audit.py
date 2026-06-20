"""Static checks for the V1 candidate handoff manifest execution audit."""

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
    / "v1_candidate_test_handoff_manifest_execution_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_candidate_handoff_execution_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == (
        "v1_candidate_test_handoff_manifest_execution_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["audit_branch"] == (
        "audit-v1-candidate-test-handoff-manifest-execution"
    )
    assert fixture["source_lima_commit_before_audit"] == (
        "3b21251e2c6dff8b9df7906eb2da708dc809a26a"
    )
    assert fixture["audit_verdict"] == "PASS_WITH_BLOCKERS"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_candidate_handoff_execution_audit_records_checkpoints() -> None:
    checkpoints = _load_fixture()["executed_checkpoints"]

    assert checkpoints["lima_ai_os"] == {
        "local_path": "C:\\Users\\limap\\LIMA-AI-OS",
        "source_branch": "docs-v1-candidate-test-handoff-manifest",
        "source_commit": "3b21251e2c6dff8b9df7906eb2da708dc809a26a",
        "clean_before_audit_branch": True,
    }
    assert checkpoints["public_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "branch": "v1-g56-runtime-authority-chain-audit",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "clean": True,
        "target_repository": "sparkpit-labs/Sparkbot",
        "target_branch_published": False,
    }
    assert checkpoints["accessible_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ddaa4ccaacd328ddcc1f00a040c2c140abee428e",
        "clean": True,
        "pushed": True,
    }
    assert checkpoints["arc_bot_shell"] == {
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ec06e7670f18eeae192fc0f995b6ffd07481d8c9",
        "pushed": True,
        "unrelated_dirty_worktree_files_present": True,
    }


def test_v1_candidate_handoff_execution_audit_records_validation_results() -> None:
    validation = _load_fixture()["validation_results"]

    for key in (
        "public_sparkbot_g56_smoke",
        "accessible_sparkbot_g56_smoke",
        "arc_bot_shell_g56_smoke",
    ):
        assert validation[key]["passed"] is True
        assert validation[key]["tests_passed"] == 8

    assert validation["lima_manifest_static_test"] == {
        "command": (
            "python -m pytest -q "
            "tests/test_v1_candidate_test_handoff_manifest.py "
            "-p no:cacheprovider"
        ),
        "passed": True,
        "tests_passed": 7,
    }
    assert validation["lima_focused_manifest_g56_g57_readiness_status_set"] == {
        "passed": True,
        "tests_passed": 89,
    }
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"] == {
        "command": "python -m pytest -q tests -p no:cacheprovider",
        "passed": True,
        "tests_passed": 5009,
    }
    assert validation["lima_diff_check"] == {
        "command": "git diff --check",
        "passed": True,
    }


def test_v1_candidate_handoff_execution_audit_accepts_expected_evidence() -> None:
    fixture = _load_fixture()

    assert fixture["evidence_accepted"] == [
        "public_sparkbot_local_g56_fake_executor_smoke_passed",
        "accessible_sparkbot_g56_fake_executor_smoke_passed",
        "arc_bot_shell_g56_fake_executor_smoke_passed",
        "lima_manifest_g56_g57_authority_readiness_assertions_aligned",
        "full_lima_suite_passed_at_manifest_checkpoint",
    ]


def test_v1_candidate_handoff_execution_audit_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_candidate_handoff_execution_audit_records_blockers_and_stops() -> None:
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
    assert fixture["stop_conditions_preserved"] == [
        "public_sparkbot_push_without_write_credentials",
        "v1_g57_implementation_without_exact_approval",
        "consumer_repo_edit_from_execution_audit_lane",
        "runtime_or_public_api_change_from_execution_audit_lane",
        "secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]
    assert fixture["recommended_next_step"] == (
        "provide_public_sparkbot_write_credentials_or_record_exactly_one_v1_g57_operator_choice"
    )


def test_v1_candidate_handoff_execution_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["execution_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Candidate Test Handoff Manifest Execution Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert "PASS_WITH_BLOCKERS" in text
    assert "5009 passed" in text
    assert "Public Sparkbot remote publication remains blocked" in text
    assert "V1-G57 remains unapproved" in text
    assert "V1-G57 implementation approval recorded: no." in text
    assert "Provider SDK clients added: no." in text
    assert "V1.0 completion, product-readiness, or production-readiness claimed: no." in text


def test_v1_candidate_handoff_execution_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["execution_audit"]).read_text(
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
