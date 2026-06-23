"""Static checks for the V1-G61 preapproval runtime-tree guard audit."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
LIMA_ROOT = REPO_ROOT / "lima"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g61_preapproval_runtime_tree_guard_audit.json"
)
REQUEST_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_request_fixture() -> dict[str, Any]:
    fixture = json.loads(REQUEST_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _lima_imported_modules() -> set[str]:
    modules: set[str] = set()
    for path in sorted(LIMA_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
    return modules


def _lima_call_names() -> set[str]:
    names: set[str] = set()
    for path in sorted(LIMA_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    names.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    names.add(node.func.attr)
    return names


def test_v1_g61_preapproval_guard_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g61_preapproval_runtime_tree_guard_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-22"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_commit_before_guard_audit"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["audit_verdict"] == "PASS_POST_APPROVAL_RUNTIME_TREE_GUARD"
    assert fixture["reviewed_gate"] == "V1-G61"
    assert fixture["operator_decision_status"] == "approved"
    assert fixture["implementation_approved"] is True

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path

    assert fixture["current_gate_inputs"] == {
        "operator_decision_packet_date": "2026-06-22",
        "operator_decision_packet_status_audit_date": "2026-06-22",
        "current_gate_consistency_audit_date": "2026-06-21",
        "post_validation_readiness_change_freshness_full_suite_tests_passed": 5359,
        "latest_quickstart_post_refresh_full_lima_suite_tests_passed": 5360,
        "latest_final_blocker_index_refresh_focused_tests_passed": 15,
        "latest_final_blocker_index_refresh_broader_tests_passed": 89,
        "latest_final_blocker_index_refresh_full_lima_suite_tests_passed": 5361,
    }


def test_v1_g61_preapproval_guard_matches_request_fixture_scan() -> None:
    fixture = _load_fixture()
    request = _load_request_fixture()

    assert request["preapproval_runtime_tree_scan"] == {
        "lima_runtime_vendor_sdk_import_present": False,
        "provider_sdk_client_constructor_present_in_lima": False,
        "approved_future_implementation_files_present": True,
        "scan_scope": "lima_runtime_tree_and_future_g61_docs_tests_fixture_paths",
    }
    assert fixture["guarded_conditions"] == {
        "lima_runtime_vendor_sdk_import_present": False,
        "provider_sdk_client_constructor_present_in_lima": False,
        "approved_g61_implementation_files_present_after_approval": True,
        "request_fixture_records_runtime_tree_scan": True,
    }


def test_v1_g61_preapproval_guard_inspects_live_lima_runtime_tree() -> None:
    fixture = _load_fixture()
    imported_modules = _lima_imported_modules()
    call_names = _lima_call_names()
    future_paths = [REPO_ROOT / path for path in fixture["future_g61_implementation_files"]]

    assert "openai" not in imported_modules
    assert not {
        "OpenAI",
        "AsyncOpenAI",
        "AzureOpenAI",
        "AsyncAzureOpenAI",
    }.intersection(call_names)
    assert all(path.exists() for path in future_paths)


def test_v1_g61_preapproval_guard_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    assert boundaries["v1_g61_operator_approval_recorded"] is True
    assert boundaries["runtime_vendor_sdk_import_execution_proof_implemented"] is True

    for key, value in boundaries.items():
        if key in {
            "v1_g61_operator_approval_recorded",
            "runtime_vendor_sdk_import_execution_proof_implemented",
        }:
            continue
        assert value is False, key


def test_v1_g61_preapproval_guard_stop_conditions_are_bounded() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "treat_guard_audit_as_broader_v1_g61_authority",
        "runtime_vendor_sdk_import_in_lima_after_import_proof",
        "provider_sdk_client_construction_after_import_proof_without_new_gate",
        "endpoint_dns_http_socket_network_or_provider_egress_after_import_proof_without_new_gate",
        "secret_credential_provider_token_or_api_key_access_after_import_proof_without_new_gate",
        "dependency_manifest_or_lockfile_edit_from_guard_audit_lane",
        "consumer_repo_edit_from_guard_audit_lane",
        "approved_g61_implementation_file_scope_expanded",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_g61_preapproval_guard_doc_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1-G61 Preapproval Runtime Tree Guard Audit" in text
    assert "PASS_POST_APPROVAL_RUNTIME_TREE_GUARD" in text
    assert fixture["source_commit_before_guard_audit"] in text
    assert "Date: 2026-06-22" in text
    assert "G61 operator decision packet status audit" in text
    assert "Current gate consistency audit" in text
    assert "Post-validation readiness-change freshness audit" in text
    assert "no `openai` import is present in `lima/` runtime source" in text
    assert "no provider SDK client constructor call is present" in text
    assert "V1-G61 operator approval recorded: yes." in text
    assert "Current G61 operator decision packet status: approved." in text
    assert "Current gate consistency audit date: 2026-06-21." in text
    assert "current same-turn full-suite freshness evidence passing 5359 tests" in text
    assert "latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests" in text
    assert "Recommended next step: complete post-G61 release-candidate readiness refresh" in text


def test_v1_g61_preapproval_guard_has_no_sensitive_markers() -> None:
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
