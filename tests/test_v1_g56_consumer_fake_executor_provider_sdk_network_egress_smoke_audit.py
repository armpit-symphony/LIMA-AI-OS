"""Static checks for the V1-G56 consumer SDK/network smoke audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRES_CONSUMER_CHECKOUTS = pytest.mark.skipif(
    not (REPO_ROOT.parent / 'Sparkbot-public').is_dir()
    or not (REPO_ROOT.parent / 'Arc-Bot-shell').is_dir(),
    reason='optional historical consumer proof requires explicit sibling checkouts',
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke_audit.json"
)
G56_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_fixture() -> dict[str, Any]:
    return _load_json(FIXTURE_PATH)


def _load_g56_fixture() -> dict[str, Any]:
    return _load_json(G56_FIXTURE_PATH)


def _load_consumer_fixture(consumer_key: str) -> dict[str, Any]:
    consumer = _load_fixture()["consumer_repositories"][consumer_key]
    consumer_root = (REPO_ROOT / consumer["local_path"]).resolve()
    return _load_json(consumer_root / consumer["fixture_ref"])


def test_v1_g56_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == (
        "v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "audit-v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke"
    )
    assert fixture["source_branch"] == (
        "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke"
    )
    assert fixture["source_commit_before_audit"] == (
        "af6d59acd2549899012d8def6be1a3ae14ab778d"
    )
    assert fixture["audit_verdict"] == "PASS_WITH_PUBLIC_SPARKBOT_PUSH_BLOCKER"
    assert fixture["operator_decision"] == "Approve-V1-G56"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["lima_files_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["evidence_fixtures_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["tests_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g56_audit_matches_implementation_fixture() -> None:
    audit = _load_fixture()
    g56 = _load_g56_fixture()

    assert g56["operator_decision"] == audit["operator_decision"]
    assert g56["api_status"] == audit["api_status"]
    assert g56["branch"] == audit["source_branch"]
    assert g56["approved_scope"] == audit["approved_scope"]
    assert g56["consumer_fake_executor_provider_sdk_network_egress_smoke_added"]
    assert g56["approved_lima_docs_tests_fixtures_changed"] == audit[
        "lima_files_reviewed"
    ]
    assert g56["approved_lima_runtime_files_changed"] == audit[
        "lima_runtime_files_reviewed"
    ]
    assert g56["lima_runtime_files_changed"] is False
    assert g56["lima_public_api_changed"] is False


def test_v1_g56_audit_consumer_scope_and_commits_match_implementation() -> None:
    audit_consumers = _load_fixture()["consumer_repositories"]
    g56_consumers = _load_g56_fixture()["consumer_repositories"]

    assert audit_consumers == {
        "sparkbot": {
            "repository": "sparkpit-labs/Sparkbot",
            "local_path": "../Sparkbot-public",
            "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
            "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
            "push_status": "blocked_github_403_current_credential",
            "approved_files_changed": [
                "tests/test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py",
                "tests/fixtures/sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json",
            ],
            "fixture_ref": (
                "tests/fixtures/"
                "sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json"
            ),
            "test_ref": (
                "tests/test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py"
            ),
        },
        "arc_bot_shell": {
            "repository": "armpit-symphony/Arc-Bot-shell",
            "local_path": "../Arc-Bot-shell",
            "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
            "commit": "ec06e7670f18eeae192fc0f995b6ffd07481d8c9",
            "push_status": "pushed_to_origin",
            "approved_files_changed": [
                "tests/test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py",
                "tests/fixtures/arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json",
            ],
            "fixture_ref": (
                "tests/fixtures/"
                "arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json"
            ),
            "test_ref": (
                "tests/test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py"
            ),
        },
    }
    for consumer_key, consumer in audit_consumers.items():
        assert consumer == {
            key: value
            for key, value in g56_consumers[consumer_key].items()
            if key
            in {
                "repository",
                "local_path",
                "branch",
                "commit",
                "push_status",
                "approved_files_changed",
                "fixture_ref",
                "test_ref",
            }
        }


@REQUIRES_CONSUMER_CHECKOUTS
def test_v1_g56_audit_consumer_files_exist_and_are_candidate_only() -> None:
    fixture = _load_fixture()

    for consumer_key, consumer in fixture["consumer_repositories"].items():
        consumer_root = (REPO_ROOT / consumer["local_path"]).resolve()
        consumer_fixture = _load_consumer_fixture(consumer_key)

        assert consumer_root.exists(), consumer_key
        assert consumer_fixture["api_status"] == "CANDIDATE_ONLY"
        assert consumer_fixture["proof_gap_id"] == "V1-G56"
        assert consumer_fixture["proof_branch"] == consumer["branch"]
        assert consumer_fixture["approved_file_scope"] == consumer[
            "approved_files_changed"
        ]
        for relative_path in consumer["approved_files_changed"]:
            assert (consumer_root / relative_path).exists(), relative_path


def test_v1_g56_audit_public_sparkbot_push_blocker_is_recorded() -> None:
    fixture = _load_fixture()
    results = fixture["audit_results"]
    blocker = fixture["publication_blockers"][0]
    validation = fixture["validation_evidence"]

    assert results["public_sparkbot_branch_saved_locally"] is True
    assert results["public_sparkbot_remote_push_blocked"] is True
    assert results["public_sparkbot_remote_push_required_before_public_release"] is True
    assert fixture["consumer_repositories"]["sparkbot"]["push_status"] == (
        "blocked_github_403_current_credential"
    )
    assert validation["public_sparkbot_branch_push"] == {
        "passed": False,
        "blocked_reason": "github_403_permission_denied_to_current_credential",
    }
    assert blocker == {
        "blocker_id": "public_sparkbot_branch_push",
        "repository": "sparkpit-labs/Sparkbot",
        "blocked": True,
        "reason": "github_403_permission_denied_to_current_credential",
        "resolution": "provide_write_credential_or_push_from_authorized_identity",
        "is_lima_runtime_blocker": False,
        "is_product_readiness": False,
    }


def test_v1_g56_audit_authority_and_fake_executor_links_are_required() -> None:
    results = _load_fixture()["audit_results"]
    g56 = _load_g56_fixture()

    assert results["v1_g48_g50_g51_g53_g54_g55_authority_metadata_used"] is True
    assert results["v1_g55_public_wrapper_import_only"] is True
    assert results["fake_in_process_provider_sdk_network_executor_only"] is True
    assert results["sanitized_evidence_only"] is True
    assert g56["public_lima_harness_symbols_imported_by_consumers"] == [
        "V1RealProviderSdkNetworkEgressError",
        "execute_v1_real_provider_sdk_network_egress",
    ]
    assert (
        g56["fake_in_process_provider_sdk_network_executor_invoked_by_consumer_tests"]
        is True
    )
    assert g56["g55_public_wrapper_invoked_by_consumer_tests"] is True


def test_v1_g56_audit_forbidden_boundaries_remain_false() -> None:
    results = _load_fixture()["audit_results"]

    for key in (
        "lima_runtime_files_changed",
        "lima_public_api_changed",
        "lima_runtime_behavior_added_by_v1_g56",
        "consumer_production_runtime_source_files_changed",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "shell_runtime_wiring_added",
        "actual_external_provider_invoked",
        "live_provider_credentials_used",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_provider_sdk_import_added",
        "direct_provider_sdk_added",
        "direct_network_code_added",
        "provider_endpoint_resolution_added",
        "network_call_performed_by_lima",
        "direct_provider_egress_performed_by_lima",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "tool_execution_added_outside_local_tests",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "scheduled_task_execution_added",
        "external_send_added",
        "raw_sensitive_content_persisted",
        "product_ready",
        "production_ready",
    ):
        assert results[key] is False, key


def test_v1_g56_audit_blocked_future_authorities_remain_false() -> None:
    blocked = _load_fixture()["still_blocked_authorities"]

    for key, value in blocked.items():
        assert value is False, key


def test_v1_g56_audit_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]
    audit_validation = _load_fixture()["audit_branch_validation_evidence"]

    assert validation["public_sparkbot_focused_v1_g56"] == {
        "passed": True,
        "tests_passed": 8,
    }
    assert validation["sparkbot_reference_focused_v1_g52"] == {
        "passed": True,
        "tests_passed": 8,
    }
    assert validation["arc_bot_shell_focused_v1_g56"] == {
        "passed": True,
        "tests_passed": 8,
    }
    assert validation["arc_bot_shell_focused_v1_g52"] == {
        "passed": True,
        "tests_passed": 8,
    }
    assert validation["focused_v1_g56_validation"] == {
        "passed": True,
        "tests_passed": 12,
    }
    assert validation[
        "focused_v1_g56_g55_g54_g53_g52_g51_g50_g48_g22_validation"
    ] == {
        "passed": True,
        "tests_passed": 383,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 4931,
    }
    assert audit_validation["focused_v1_g56_audit_validation"] == {
        "passed": True,
        "tests_passed": 12,
    }
    assert audit_validation["focused_v1_g56_audit_chain_validation"] == {
        "passed": True,
        "tests_passed": 404,
    }
    assert audit_validation["compileall_lima"] == {"passed": True}
    assert audit_validation["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 4943,
    }


def test_v1_g56_audit_docs_contain_required_boundary_language() -> None:
    audit = _load_fixture()
    text = (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

    assert "PASS_WITH_PUBLIC_SPARKBOT_PUSH_BLOCKER" in text
    assert "fake in-process provider SDK/network executor only" in text
    assert "LIMA `lima/` runtime files changed by V1-G56: none, pass." in text
    assert "LIMA public API changed by V1-G56: none, pass." in text
    assert "Public Sparkbot remote branch push is blocked by GitHub 403" in text
    assert "Direct provider egress by LIMA remains absent: pass." in text
    assert "Product-readiness and production-readiness claims remain absent: pass." in text
    assert "V1-G56 passes independent audit" in text


def test_v1_g56_audit_fixture_and_doc_do_not_include_sensitive_markers() -> None:
    audit = _load_fixture()
    output = json.dumps(audit, sort_keys=True)
    output += (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

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


def test_v1_g56_audit_next_steps_remain_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["next_recommended_steps"] == [
        "public_sparkbot_branch_push_after_write_credentials",
        "v1_runtime_authority_chain_audit_through_g56",
        "readiness_next_lane_metadata_refresh_through_g56",
    ]
    assert fixture["audit_results"]["product_ready"] is False
    assert fixture["audit_results"]["production_ready"] is False
