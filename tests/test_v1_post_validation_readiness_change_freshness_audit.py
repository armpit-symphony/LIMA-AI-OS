"""Static checks for the V1 post-validation readiness-change freshness audit."""

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
    / "v1_post_validation_readiness_change_freshness_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_post_validation_freshness_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == (
        "v1_post_validation_readiness_change_freshness_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-21"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["audit_verdict"] == (
        "POST_VALIDATION_READINESS_CHANGES_REQUIRE_SAME_TURN_VALIDATION"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_post_validation_freshness_rule_is_explicit() -> None:
    rule = _load_fixture()["freshness_rule"]

    assert rule == {
        "current_validation_refresh_predates_later_readiness_changes": True,
        "later_readiness_changes_require_same_turn_validation": True,
        "accepted_dispositions": [
            "no_later_readiness_docs_fixtures_or_tests_changed",
            "same_turn_focused_full_suite_and_diff_check_evidence_recorded",
        ],
        "current_lane_disposition": (
            "same_turn_focused_full_suite_and_diff_check_evidence_required"
        ),
    }


def test_v1_post_validation_freshness_records_changed_artifacts() -> None:
    artifacts = _load_fixture()["changed_readiness_artifacts_covered"]

    assert artifacts == [
        "README.md",
        "docs/CURRENT_PROJECT_STATE.md",
        "docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md",
        "docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md",
        "docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md",
        "docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md",
        "docs/audits/V1_CANDIDATE_TEST_HANDOFF_MANIFEST_EXECUTION_AUDIT.md",
        "docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md",
        "docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md",
        "docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md",
        "docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md",
        "docs/readiness/V1_FINAL_BLOCKER_REGISTER.md",
        "docs/readiness/V1_FINAL_CANDIDATE_BRANCH_INDEX.md",
        "docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md",
        "docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md",
        "tests/fixtures/runtime_extraction/v1_current_gate_consistency_audit.json",
        "tests/fixtures/runtime_extraction/v1_g61_preapproval_runtime_tree_guard_audit.json",
        "tests/fixtures/runtime_extraction/v1_arc_bot_shell_local_drift_exclusion_audit.json",
        "tests/fixtures/runtime_extraction/v1_candidate_harness_quickstart_execution_audit.json",
        "tests/fixtures/runtime_extraction/v1_candidate_harness_quickstart.json",
        "tests/fixtures/runtime_extraction/v1_candidate_test_handoff_manifest_execution_audit.json",
        "tests/fixtures/runtime_extraction/v1_release_candidate_acceptance_checklist.json",
        "tests/fixtures/runtime_extraction/v1_release_candidate_cutover_runbook.json",
        "tests/fixtures/runtime_extraction/v1_final_readiness_audit_template.json",
        "tests/fixtures/runtime_extraction/v1_final_blocker_register.json",
        "tests/fixtures/runtime_extraction/v1_final_candidate_branch_index.json",
        "tests/fixtures/runtime_extraction/v1_post_g61_request_readiness_refresh.json",
        "tests/fixtures/runtime_extraction/v1_readme_status_alignment.json",
        "tests/fixtures/runtime_extraction/v1_post_validation_readiness_change_freshness_audit.json",
        "tests/test_v1_current_gate_consistency_audit.py",
        "tests/test_v1_g61_preapproval_runtime_tree_guard_audit.py",
        "tests/test_v1_arc_bot_shell_local_drift_exclusion_audit.py",
        "tests/test_v1_candidate_harness_quickstart_execution_audit.py",
        "tests/test_v1_candidate_harness_quickstart.py",
        "tests/test_v1_candidate_test_handoff_manifest_execution_audit.py",
        "tests/test_v1_release_candidate_acceptance_checklist.py",
        "tests/test_v1_release_candidate_cutover_runbook.py",
        "tests/test_v1_final_readiness_audit_template.py",
        "tests/test_v1_final_blocker_register.py",
        "tests/test_v1_final_candidate_branch_index.py",
        "tests/test_v1_post_g61_request_readiness_refresh.py",
        "tests/test_v1_readme_status_alignment.py",
        "tests/test_v1_post_validation_readiness_change_freshness_audit.py",
    ]


def test_v1_post_validation_freshness_requires_same_turn_validation() -> None:
    validation = _load_fixture()["required_same_turn_validation"]

    assert validation["focused_post_validation_freshness_tests"] == [
        "tests\\test_v1_post_validation_readiness_change_freshness_audit.py",
        "tests\\test_v1_current_gate_consistency_audit.py",
        "tests\\test_v1_g61_preapproval_runtime_tree_guard_audit.py",
        "tests\\test_v1_arc_bot_shell_local_drift_exclusion_audit.py",
        "tests\\test_v1_release_candidate_acceptance_checklist.py",
        "tests\\test_v1_release_candidate_cutover_runbook.py",
        "tests\\test_v1_final_readiness_audit_template.py",
        "tests\\test_v1_readme_status_alignment.py",
    ]
    assert validation["broad_v1_release_readiness_regression_includes_freshness_audit"]
    assert validation["compileall_lima_required"]
    assert validation["full_lima_suite_required"]
    assert validation["current_same_turn_full_lima_suite_tests_passed"] == 5359
    assert validation["latest_quickstart_post_refresh_full_lima_suite_tests_passed"] == 5360
    assert validation["latest_final_blocker_index_refresh_focused_tests_passed"] == 15
    assert validation["latest_final_blocker_index_refresh_broader_tests_passed"] == 89
    assert (
        validation["latest_final_blocker_index_refresh_full_lima_suite_tests_passed"]
        == 5361
    )
    assert validation["latest_post_g61_request_refresh_focused_tests_passed"] == 8
    assert validation["latest_post_g61_request_refresh_broader_tests_passed"] == 117
    assert (
        validation["latest_post_g61_request_refresh_full_lima_suite_tests_passed"]
        == 5362
    )
    assert validation["latest_quickstart_artifact_refresh_focused_tests_passed"] == 7
    assert validation["latest_quickstart_artifact_refresh_adjacent_tests_passed"] == 64
    assert validation["latest_quickstart_artifact_refresh_broader_tests_passed"] == 133
    assert (
        validation["latest_quickstart_artifact_refresh_full_lima_suite_tests_passed"]
        == 5364
    )
    assert validation["git_diff_check_required"]
    assert validation["git_diff_cached_check_required"]
    assert validation["protected_path_status_check_required"]


def test_v1_post_validation_freshness_interpretation_preserves_gates() -> None:
    fixture = _load_fixture()

    assert fixture["evidence_interpretation"] == [
        "current_validation_refresh_remains_earlier_153_and_5350_evidence",
        "this_audit_covers_later_readiness_docs_fixtures_tests_only_by_same_turn_validation_requirement",
        "this_audit_covers_g61_preapproval_runtime_tree_guard_refresh_current_with_2026_06_21_operator_decision_chain",
        "this_audit_covers_arc_bot_shell_drift_traceability_only_as_compatibility_evidence_7_tracked_modified_49_untracked",
        "this_audit_covers_same_turn_consumer_smoke_refresh_public_accessible_arc_8_each_and_quickstart_post_refresh_lima_5360",
        "this_audit_covers_final_blocker_and_branch_index_refresh_with_arc_proof_path_cleanliness_and_lima_15_89_5361",
        "this_audit_covers_post_g61_request_refresh_later_freshness_supplement_lima_8_117_5362",
        "this_audit_covers_latest_quickstart_artifact_refresh_lima_7_64_133_5364",
        "future_final_readiness_audit_must_cite_this_audit_if_relying_on_later_readiness_changes",
        "successful_same_turn_tests_do_not_approve_g61_or_release_readiness",
    ]


def test_v1_post_validation_freshness_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_post_validation_freshness_stop_conditions_are_bounded() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "treat_this_audit_as_g61_approval",
        "treat_this_audit_as_passed_release_candidate_checklist_cutover_or_final_readiness_audit",
        "treat_this_audit_as_branch_tag_cutover_or_readiness_claim_authority",
        "treat_same_turn_validation_as_arc_bot_shell_clean_checkpoint_proof",
        "consumer_repo_edit_from_audit_lane",
        "runtime_or_public_api_change_from_audit_lane",
        "runtime_vendor_sdk_import_dependency_lockfile_secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_post_validation_freshness_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Post-Validation Readiness Change Freshness Audit" in text
    assert fixture["audit_verdict"] in text
    assert "same-turn focused validation, full-suite validation, and diff-check evidence" in text
    assert "current validation refresh predates later readiness docs, fixtures, and tests" in text
    assert "does not replace the current validation refresh audit" in text
    assert "docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in text
    assert "docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "docs/audits/V1_CANDIDATE_TEST_HANDOFF_MANIFEST_EXECUTION_AUDIT.md" in text
    assert "docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md" in text
    assert "docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "docs/readiness/V1_FINAL_BLOCKER_REGISTER.md" in text
    assert "docs/readiness/V1_FINAL_CANDIDATE_BRANCH_INDEX.md" in text
    assert "docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md" in text
    assert "tests/test_v1_readme_status_alignment.py" in text
    assert "tests/test_v1_post_g61_request_readiness_refresh.py" in text
    assert "tests\\test_v1_current_gate_consistency_audit.py" in text
    assert "tests\\test_v1_g61_preapproval_runtime_tree_guard_audit.py" in text
    assert "tests\\test_v1_release_candidate_acceptance_checklist.py" in text
    assert "G61 preapproval runtime-tree guard refresh" in text
    assert "7 tracked modified files, and 64 untracked files as compatibility-only evidence" in text
    assert "same-turn consumer smoke refresh evidence" in text
    assert "public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 smoke tests" in text
    assert "post-refresh LIMA validation passing 5360 full-suite tests" in text
    assert "latest final blocker/register and branch-index refresh evidence" in text
    assert "15 focused final blocker/index tests, 89 broader affected readiness tests, and 5361 full-suite tests" in text
    assert "latest post-G61 request readiness-refresh supplement evidence" in text
    assert "8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "latest quickstart artifact refresh evidence" in text
    assert "7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "post-G61 request readiness-refresh supplement that keeps the request-stage handoff current" in text
    assert "latest candidate harness quickstart artifact refresh" in text
    assert "7 focused quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and the full LIMA suite passing 5364 tests" in text
    assert "same-day Arc approved G56 smoke proof-path cleanliness as compatibility-only evidence" in text
    assert "focused post-validation freshness tests" in text
    assert "latest quickstart post-refresh full LIMA suite evidence: 5360 tests passing" in text
    assert "python -m compileall lima" in text
    assert "python -m pytest -q tests -p no:cacheprovider" in text
    assert "git diff --cached --check" in text
    assert "protected-path status check" in text
    assert "future final readiness audit must cite this audit" in text
    assert "V1-G61 operator decision recorded by this audit: no." in text
    assert "Release-candidate checklist passed by this audit: no." in text
    assert "Arc-Bot-shell clean-checkpoint proof claimed by this audit: no." in text
    assert "treat same-turn validation as Arc-Bot-shell clean-checkpoint proof" in text
    assert "claim V1.0 completion, product readiness, or production readiness" in text


def test_v1_post_validation_freshness_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

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
