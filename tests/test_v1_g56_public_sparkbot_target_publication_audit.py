"""Static checks for the V1-G56 public Sparkbot target publication audit."""

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
    / "v1_g56_public_sparkbot_target_publication_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g56_public_sparkbot_publication_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g56_public_sparkbot_target_publication_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["audit_branch"] == "audit-v1-g56-public-sparkbot-target-publication"
    assert fixture["source_lima_commit_before_audit"] == (
        "e1808ef057524b3aa409015439e4435e72a384d2"
    )
    assert fixture["audit_verdict"] == "LOCAL_PASS_REMOTE_PUBLICATION_BLOCKED"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g56_public_sparkbot_branch_state_is_local_only() -> None:
    public = _load_fixture()["public_sparkbot"]

    assert public == {
        "local_repository": "C:\\Users\\limap\\Sparkbot-public",
        "local_branch": "v1-g56-runtime-authority-chain-audit",
        "local_commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "local_dirty_state": "clean",
        "target_repository": "https://github.com/sparkpit-labs/Sparkbot",
        "target_branch": "v1-g56-runtime-authority-chain-audit",
        "target_branch_present": False,
        "target_branch_sha": None,
        "direct_push_attempted_by_this_audit": False,
        "direct_push_state": (
            "blocked_by_known_github_403_and_missing_write_credentials"
        ),
        "target_pull_request_created_by_this_audit": False,
    }


def test_v1_g56_public_sparkbot_scope_is_fake_executor_only() -> None:
    fixture = _load_fixture()

    assert fixture["public_sparkbot_g56_scope"] == {
        "consumer_fake_executor_smoke_test": True,
        "sanitized_consumer_fixture": True,
        "g55_public_wrapper_import": True,
        "fake_in_process_provider_sdk_network_executor_only": True,
    }

    for key, value in fixture["public_sparkbot_forbidden_scope"].items():
        assert value is False, key


def test_v1_g56_public_sparkbot_publication_validation_is_recorded() -> None:
    validation = _load_fixture()["validation"]

    assert validation["public_sparkbot_focused_v1_g56"] == {
        "command": (
            "python -m pytest -q "
            "tests\\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py "
            "-p no:cacheprovider"
        ),
        "passed": True,
        "tests_passed": 8,
    }
    assert validation["public_sparkbot_diff_check"] == {
        "command": "git diff --check",
        "passed": True,
    }
    assert validation["target_branch_probe"] == {
        "command": "git ls-remote --heads origin v1-g56-runtime-authority-chain-audit",
        "target_branch_present": False,
        "result": "",
    }
    assert validation["target_push_probe"] == {
        "command": "not_repeated_by_this_audit",
        "result": "blocked_by_known_github_403_and_missing_write_credentials",
    }


def test_v1_g56_public_sparkbot_publication_preserves_lima_boundaries() -> None:
    boundaries = _load_fixture()["lima_boundary_results"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_g56_public_sparkbot_publication_stop_conditions_remain_closed() -> None:
    fixture = _load_fixture()

    assert fixture["stop_conditions_preserved"] == [
        "public_sparkbot_push_without_write_credential",
        "v1_g57_implementation_without_exact_approve_v1_g57",
        "lima_runtime_behavior_or_public_api_export_change",
        "sparkbot_or_arc_bot_shell_file_change",
        "secret_credential_token_sdk_endpoint_or_network_required",
        "product_production_or_v1_completion_claim",
    ]
    assert fixture["recommended_next_step"] == (
        "public_sparkbot_write_credential_unblock_or_explicit_v1_g57_operator_decision"
    )


def test_v1_g56_public_sparkbot_publication_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["publication_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1-G56 Public Sparkbot Target Publication Audit" in text
    assert "LOCAL_PASS_REMOTE_PUBLICATION_BLOCKED" in text
    assert fixture["public_sparkbot"]["local_commit"] in text
    assert "Target branch present: no" in text
    assert "not present on `sparkpit-labs/Sparkbot`" in text
    assert "The direct push probe was not repeated by this audit" in text
    assert "No provider SDK clients" not in text
    assert "Provider SDK client added by this audit: no." in text
    assert "V1-G57 implementation approved by this audit: no." in text
    assert "Product-readiness, production-readiness, or V1.0 completion claim" in text


def test_v1_g56_public_sparkbot_publication_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["publication_audit"]).read_text(
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
