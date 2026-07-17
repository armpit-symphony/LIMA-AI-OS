"""Static checks for the V1 post-G61 request readiness refresh."""

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
    / "v1_post_g61_request_readiness_refresh.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_post_g61_request_readiness_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["refresh_id"] == "v1_post_g61_request_readiness_refresh"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["readiness_refresh_lane_label"] == (
        "docs-v1-post-g61-request-readiness-refresh"
    )
    assert fixture["source_audit_lane_label"] == (
        "audit-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_commit_before_refresh"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_post_g61_request_readiness_records_real_blocker() -> None:
    fixture = _load_fixture()

    assert fixture["readiness_verdict"] == (
        "READY_FOR_OPERATOR_DECISION_BLOCKED_FOR_IMPLEMENTATION"
    )
    assert fixture["implementation_blocker"] == "Approve-V1-G61 has not been recorded"
    assert fixture["required_operator_choice_to_unblock_implementation"] == (
        "Approve-V1-G61"
    )
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G61 implementation of the runtime vendor SDK "
        "import execution proof slice, limited to the file scope, behavior "
        "scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
    )


def test_post_g61_request_readiness_required_verdicts_remain_blocked() -> None:
    verdicts = _load_fixture()["required_verdicts"]

    assert verdicts["v1_runtime_authority_chain"] == "CANDIDATE_ONLY"
    assert verdicts["v1_g61_approval_request"] == "READY_FOR_OPERATOR_DECISION"
    assert verdicts["v1_g61_implementation"] == "NOT_APPROVED"
    assert verdicts["runtime_vendor_sdk_import_execution_proof"] == "NOT_APPROVED"
    assert verdicts["runtime_vendor_sdk_imports_in_lima"] == "NOT_APPROVED"
    assert verdicts["dependency_manifest_edits"] == "NOT_APPROVED"
    assert verdicts["lockfile_edits"] == "NOT_APPROVED"
    assert verdicts["provider_client_construction"] == "NOT_APPROVED"
    assert verdicts["lima_owned_direct_provider_network_egress"] == "NOT_APPROVED"
    assert verdicts["secret_lookup_and_credential_value_access"] == "NOT_APPROVED"
    assert verdicts["product_readiness"] == "NOT_READY"
    assert verdicts["final_public_api_freeze"] == "NOT_APPROVED"


def test_post_g61_request_readiness_boundary_confirmation() -> None:
    boundary = _load_fixture()["boundary_confirmation"]

    assert boundary["docs_tests_fixtures_only"] is True
    assert boundary["preapproval_runtime_tree_guard_added_to_request_stage_tests"] is True
    for key, value in boundary.items():
        if key not in {
            "docs_tests_fixtures_only",
            "preapproval_runtime_tree_guard_added_to_request_stage_tests",
        }:
            assert value is False, key


def test_post_g61_request_readiness_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_v1_g61_request_audit_validation"] == {
        "passed": True,
        "tests_passed": 11,
    }
    assert validation["focused_v1_g61_request_audit_chain_validation"] == {
        "passed": True,
        "tests_passed": 42,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite_before_refresh"] == {
        "passed": True,
        "tests_passed": 5273,
    }
    assert validation["current_g61_decision_packet_hardening_validation"] == {
        "passed": True,
        "tests_passed": 35,
    }
    assert validation["full_lima_suite_after_decision_packet_hardening"] == {
        "passed": True,
        "tests_passed": 5280,
    }
    assert validation["diff_check_after_decision_packet_hardening"] == {
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert validation["cached_diff_check_after_decision_packet_hardening"] == {
        "passed": True,
    }
    assert validation["current_g61_branch_metadata_hardening_validation"] == {
        "passed": True,
        "tests_passed": 51,
    }
    assert validation["full_lima_suite_after_branch_metadata_hardening"] == {
        "passed": True,
        "tests_passed": 5280,
    }
    assert validation["compileall_after_branch_metadata_hardening"] == {
        "passed": True,
    }
    assert validation["diff_check_after_branch_metadata_hardening"] == {
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert validation["cached_diff_check_after_branch_metadata_hardening"] == {
        "passed": True,
    }
    assert validation["current_g61_preapproval_runtime_tree_guard_validation"] == {
        "passed": True,
        "tests_passed": 32,
    }
    assert validation["full_lima_suite_after_preapproval_runtime_tree_guard_audit"] == {
        "passed": True,
        "tests_passed": 5289,
    }
    assert validation["compileall_after_preapproval_runtime_tree_guard_audit"] == {
        "passed": True,
    }
    assert validation["diff_check_after_preapproval_runtime_tree_guard_audit"] == {
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert validation["cached_diff_check_after_preapproval_runtime_tree_guard_audit"] == {
        "passed": True,
    }
    assert validation["current_consumer_harness_usability_matrix_validation"] == {
        "passed": True,
        "tests_passed": 39,
    }
    assert validation["full_lima_suite_after_consumer_harness_usability_matrix"] == {
        "passed": True,
        "tests_passed": 5297,
    }
    assert validation["compileall_after_consumer_harness_usability_matrix"] == {
        "passed": True,
    }
    assert validation["current_release_candidate_acceptance_checklist_validation"] == {
        "passed": True,
        "tests_passed": 47,
    }
    assert validation["full_lima_suite_after_release_candidate_acceptance_checklist"] == {
        "passed": True,
        "tests_passed": 5305,
    }
    assert validation["compileall_after_release_candidate_acceptance_checklist"] == {
        "passed": True,
    }
    assert validation["current_release_candidate_cutover_runbook_validation"] == {
        "passed": True,
        "tests_passed": 56,
    }
    assert validation["full_lima_suite_after_release_candidate_cutover_runbook"] == {
        "passed": True,
        "tests_passed": 5313,
    }
    assert validation["compileall_after_release_candidate_cutover_runbook"] == {
        "passed": True,
    }
    assert validation["current_candidate_harness_quickstart_validation"] == {
        "passed": True,
        "tests_passed": 61,
    }
    assert validation["full_lima_suite_after_candidate_harness_quickstart"] == {
        "passed": True,
        "tests_passed": 5319,
    }
    assert validation["compileall_after_candidate_harness_quickstart"] == {
        "passed": True,
    }
    assert validation["current_candidate_harness_quickstart_execution_audit_validation"] == {
        "passed": True,
        "tests_passed": 83,
    }
    assert validation["full_lima_suite_after_candidate_harness_quickstart_execution_audit"] == {
        "passed": True,
        "tests_passed": 5326,
    }
    assert validation["compileall_after_candidate_harness_quickstart_execution_audit"] == {
        "passed": True,
    }
    assert validation["current_gate_consistency_validation_refresh"] == {
        "passed": True,
        "tests_passed": 31,
    }
    assert validation["full_lima_suite_after_current_gate_consistency_validation_refresh"] == {
        "passed": True,
        "tests_passed": 5350,
    }
    assert validation["compileall_after_current_gate_consistency_validation_refresh"] == {
        "passed": True,
    }
    assert validation["diff_check_after_current_gate_consistency_validation_refresh"] == {
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert validation["cached_diff_check_after_current_gate_consistency_validation_refresh"] == {
        "passed": True,
    }


def test_post_g61_request_readiness_records_later_freshness_supplements() -> None:
    supplements = _load_fixture()["later_readiness_freshness_supplements"]

    assert supplements == {
        "current_candidate_validation_refresh_latest_final_blocker_index_focused_tests_passed": 15,
        "current_candidate_validation_refresh_latest_final_blocker_index_broader_tests_passed": 89,
        "current_candidate_validation_refresh_latest_final_blocker_index_full_lima_suite_tests_passed": 5361,
        "post_validation_readiness_change_freshness_full_suite_tests_passed": 5359,
        "latest_quickstart_post_refresh_full_lima_suite_tests_passed": 5360,
        "latest_final_blocker_index_refresh_focused_tests_passed": 15,
        "latest_final_blocker_index_refresh_broader_tests_passed": 89,
        "latest_final_blocker_index_refresh_full_lima_suite_tests_passed": 5361,
        "latest_post_g61_request_refresh_focused_tests_passed": 8,
        "latest_post_g61_request_refresh_broader_tests_passed": 117,
        "latest_post_g61_request_refresh_full_lima_suite_tests_passed": 5362,
        "latest_quickstart_artifact_refresh_focused_tests_passed": 7,
        "latest_quickstart_artifact_refresh_adjacent_tests_passed": 64,
        "latest_quickstart_artifact_refresh_broader_tests_passed": 133,
        "latest_quickstart_artifact_refresh_full_lima_suite_tests_passed": 5364,
        "implementation_authority_created": False,
        "release_candidate_authority_created": False,
        "cutover_authority_created": False,
        "final_readiness_pass_created": False,
        "production_use_authority_created": False,
    }


def test_post_g61_request_readiness_doc_contains_exact_gate() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["refresh"]).read_text(encoding="utf-8")

    assert "Readiness verdict: `READY_FOR_OPERATOR_DECISION_BLOCKED_FOR_IMPLEMENTATION`" in text
    assert (
        "Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`"
        in text
    )
    assert (
        "Readiness refresh lane label: `docs-v1-post-g61-request-readiness-refresh`"
        in text
    )
    assert (
        "Source audit lane label: `audit-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`"
        in text
    )
    assert "`Approve-V1-G61` has not been recorded" in text
    assert "V1-G61 implementation cannot begin" in text
    assert "V1-G61 preapproval runtime-tree guard audit exists and passes" in text
    assert "Runtime vendor SDK import execution proof: `NOT_APPROVED`" in text
    assert "Runtime vendor SDK imports in `lima/`: `NOT_APPROVED`" in text
    assert "Lockfile edits: `NOT_APPROVED`" in text
    assert "Product readiness: `NOT_READY`" in text
    assert "Final public API freeze: `NOT_APPROVED`" in text
    assert "Preapproval runtime-tree guard added to request-stage tests: yes." in text
    assert "## Validation Evidence" in text
    assert "Focused G61/operator packet validation: passed, 35 tests." in text
    assert "Full LIMA suite: passed, 5280 tests." in text
    assert "`git diff --check`: passed with LF-to-CRLF warnings only." in text
    assert "Current validation after G61 branch metadata hardening:" in text
    assert "Focused G61/status metadata validation: passed, 51 tests." in text
    assert "Current validation after G61 preapproval runtime-tree guard audit:" in text
    assert "Focused G61 guard/readiness validation: passed, 32 tests." in text
    assert "Full LIMA suite: passed, 5289 tests." in text
    assert "Current validation after V1 consumer harness usability matrix:" in text
    assert "Focused harness usability/readiness validation: passed, 39 tests." in text
    assert "Full LIMA suite: passed, 5297 tests." in text
    assert "Current validation after V1 release-candidate acceptance checklist:" in text
    assert "Focused release-candidate/readiness validation: passed, 47 tests." in text
    assert "Full LIMA suite: passed, 5305 tests." in text
    assert "Current validation after V1 release-candidate cutover runbook:" in text
    assert "Focused release-candidate cutover/readiness validation: passed, 56 tests." in text
    assert "Full LIMA suite: passed, 5313 tests." in text
    assert "Current validation after V1 candidate harness quickstart:" in text
    assert "Focused candidate harness quickstart/readiness validation: passed, 61 tests." in text
    assert "Full LIMA suite: passed, 5319 tests." in text
    assert "Current validation after V1 candidate harness quickstart execution audit:" in text
    assert "Focused candidate harness quickstart execution/readiness validation: passed, 83 tests." in text
    assert "Full LIMA suite: passed, 5326 tests." in text
    assert "Current validation after V1 current gate consistency and validation refresh:" in text
    assert "Focused current-gate consistency/readiness validation: passed, 153 tests." in text
    assert "Full LIMA suite: passed, 5350 tests." in text
    assert "Later readiness freshness supplements after this request-stage refresh:" in text
    assert "Current candidate validation refresh later LIMA readiness freshness supplement: passed, 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests." in text
    assert "Post-validation readiness-change freshness audit: current, including same-turn 5359 full-suite evidence after release/cutover freshness checks, latest quickstart 5360 full-suite evidence, and latest final blocker/index 15/89/5361 evidence." in text
    assert "Latest post-G61 request readiness-refresh supplement: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests." in text
    assert "Latest quickstart artifact refresh: passed, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "they do not approve V1-G61 implementation, release-candidate acceptance, cutover, final readiness, or production use" in text


def test_post_g61_request_readiness_next_choices_are_exact() -> None:
    assert _load_fixture()["next_valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
