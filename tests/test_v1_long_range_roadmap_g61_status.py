"""Static checks for the current V1 long-range roadmap status."""

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
    / "v1_long_range_roadmap_g61_status.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_long_range_roadmap_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["status_id"] == "v1_long_range_roadmap_g61_status"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["request_stage_lane_label"] == (
        "prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_commit_before_refresh"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_long_range_roadmap_current_gate_is_g61_request_prep() -> None:
    fixture = _load_fixture()

    assert fixture["current_gate"] == "V1-G61"
    assert fixture["latest_completed_gate"] == "V1-G60"
    assert fixture["latest_authority_chain_audit"] == "V1-G56"
    assert (
        fixture["latest_request_stage_readiness_refresh"]
        == "V1_POST_G61_REQUEST_READINESS_REFRESH"
    )
    assert fixture["request_packet_prepared"] is True
    assert fixture["request_gate_audit_complete"] is True
    assert fixture["preapproval_runtime_tree_guard_audit_complete"] is True
    assert fixture["operator_decision_packet_status_audit_complete"] is True
    assert fixture["current_gate_consistency_audit_complete"] is True
    assert fixture["current_candidate_validation_refresh_complete"] is True
    assert fixture["current_validation_focused_current_gate_tests_passed"] == 153
    assert fixture["current_validation_full_lima_suite_tests_passed"] == 5350
    assert (
        fixture[
            "current_validation_latest_readiness_freshness_focused_final_blocker_index_tests_passed"
        ]
        == 15
    )
    assert (
        fixture[
            "current_validation_latest_readiness_freshness_broader_v1_readiness_tests_passed"
        ]
        == 89
    )
    assert (
        fixture[
            "current_validation_latest_readiness_freshness_full_lima_suite_tests_passed"
        ]
        == 5361
    )
    assert (
        fixture[
            "current_validation_latest_handoff_freshness_post_g61_request_focused_tests_passed"
        ]
        == 8
    )
    assert (
        fixture[
            "current_validation_latest_handoff_freshness_post_g61_request_broader_tests_passed"
        ]
        == 117
    )
    assert (
        fixture[
            "current_validation_latest_handoff_freshness_post_g61_request_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert (
        fixture[
            "current_validation_latest_handoff_freshness_quickstart_focused_tests_passed"
        ]
        == 7
    )
    assert (
        fixture[
            "current_validation_latest_handoff_freshness_quickstart_adjacent_tests_passed"
        ]
        == 64
    )
    assert (
        fixture[
            "current_validation_latest_handoff_freshness_quickstart_broader_tests_passed"
        ]
        == 133
    )
    assert (
        fixture[
            "current_validation_latest_handoff_freshness_quickstart_full_lima_suite_tests_passed"
        ]
        == 5364
    )
    assert (
        fixture[
            "arc_bot_shell_clean_checkpoint_required_before_release_final_branch_tag_cutover_or_readiness_claim"
        ]
        is True
    )
    assert fixture["release_candidate_acceptance_checklist_verdict"] == (
        "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS"
    )
    assert fixture["release_candidate_cutover_runbook_verdict"] == (
        "CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS"
    )
    assert fixture["final_readiness_audit_template_current"] is True
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False
    assert fixture["next_smallest_safe_step"] == "record_v1_g61_operator_decision"


def test_v1_long_range_roadmap_refresh_adds_no_forbidden_behavior() -> None:
    forbidden = _load_fixture()["forbidden_by_refresh"]

    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "public_api_exports_changed",
        "sparkbot_or_arc_bot_shell_changed",
        "g61_runtime_vendor_sdk_import_execution_proof_added",
        "lockfile_edited",
        "built_in_provider_sdk_client_added",
        "provider_client_construction_added",
        "runtime_vendor_sdk_import_added_to_lima",
        "provider_endpoint_resolution_by_lima_added",
        "network_call_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
    ):
        assert forbidden[key] is False, key


def test_v1_long_range_roadmap_text_points_to_g61_request_prep() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["long_range_roadmap"]
    ).read_text(encoding="utf-8")

    assert "## V1 Product Readiness Target" in text
    assert "public `Sparkbot`" in text
    assert (
        "The active V1 gate is operator decision for the prepared request-only `V1-G61` runtime vendor SDK import execution proof packet."
        in text
    )
    assert "Completed implementation evidence is refreshed through `V1-G60`" in text
    assert "No V1-G61 implementation is approved." in text
    assert "Current V1-G60 completed dependency/import-boundary documents:" in text
    assert "`docs/audits/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUDIT.md`" in text
    assert "`docs/readiness/V1_POST_G60_NEXT_LANE_DECISION_MATRIX.md`" in text
    assert "Current V1-G61 request-only authority documents:" in text
    assert "`docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md`" in text
    assert "`docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`" in text
    assert "operator decision packet status audit" in text
    assert "exactly one valid operator choice is still required" in text
    assert "Current V1.0.0 candidate-readiness control documents:" in text
    assert "`docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`" in text
    assert "`docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`" in text
    assert "`docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`" in text
    assert "focused current-gate/release-readiness validation passing 153 tests and the full LIMA suite passing 5350 tests" in text
    assert "latest LIMA readiness freshness evidence passing 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests" in text
    assert "latest handoff freshness evidence passing 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests" in text
    assert "That evidence and clean Arc-Bot-shell checkpoint proof are required before any future release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim" in text
    assert (
        "The next smallest safe V1 action is to record exactly one operator choice "
        "in the V1-G61 runtime vendor SDK import execution proof operator decision packet"
    ) in text
    assert "`Approve-V1-G61`, `Revise-V1-G61`, or `Pause`" in text
    assert "approved vendor SDK module can be imported in a controlled local test context" in text
    assert "lockfile edits" in text
    assert "runtime imports in `lima/`" in text
    assert "built-in provider SDK clients" in text
    assert "LIMA-owned DNS/HTTP/socket/network calls" in text
    assert "secret lookup, credential value access" in text
    assert "product-readiness claims" in text
    assert "This roadmap update is product-direction evidence only." in text
