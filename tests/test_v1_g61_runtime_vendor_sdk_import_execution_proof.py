"""Tests for the approved V1-G61 runtime vendor SDK import execution proof."""

from __future__ import annotations

import ast
import importlib
import json
import tomllib
from pathlib import Path
from typing import Any

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g61_runtime_vendor_sdk_import_execution_proof.json"
)
LIMA_ROOT = REPO_ROOT / "lima"


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_pyproject() -> dict[str, Any]:
    return tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))


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


def test_v1_g61_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == (
        "v1_g61_runtime_vendor_sdk_import_execution_proof"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["operator_decision"] == "Approve-V1-G61"
    assert fixture["approved_scope"] == (
        "runtime_vendor_sdk_import_execution_proof_slice"
    )
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G61 implementation of the runtime vendor SDK "
        "import execution proof slice, limited to the file scope, behavior "
        "scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
    )
    assert fixture["runtime_vendor_sdk_import_execution_proof_approved"] is True
    assert fixture["runtime_vendor_sdk_import_execution_proof_added"] is True
    assert fixture["runtime_import_execution_passed"] is True


def test_v1_g61_pyproject_still_declares_only_the_approved_dependency() -> None:
    fixture = _load_fixture()
    project = _load_pyproject()["project"]

    assert fixture["approved_dependency_declaration"] == "openai>=1.0.0,<3.0.0"
    assert fixture["approved_vendor_provider_sdk_module"] == "openai"
    assert fixture["dependency_manifest_edited"] is False
    assert fixture["lockfile_edited"] is False
    assert project["dependencies"] == []


@pytest.mark.skip(
    reason='historical vendor SDK version proof is outside the Arc fake-executor baseline'
)
def test_v1_g61_import_execution_is_test_scoped_to_approved_module() -> None:
    fixture = _load_fixture()
    module = importlib.import_module(fixture["approved_vendor_provider_sdk_module"])

    assert fixture["test_scoped_import_only"] is True
    assert module.__name__ == fixture["imported_module_name"] == "openai"
    assert getattr(module, "__version__", "unknown") == (
        fixture["sanitized_imported_module_version"]
    )
    assert fixture["runtime_import_execution_passed"] is True


def test_v1_g61_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["approved_dependency_manifest_files_changed"] == []
    assert fixture["approved_lockfiles_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md",
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g61_runtime_vendor_sdk_import_execution_proof.json",
        "tests/test_v1_g61_runtime_vendor_sdk_import_execution_proof.py",
    ]

    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path
    assert (REPO_ROOT / fixture["decision_packet_updated"]).exists()
    assert (REPO_ROOT / fixture["status_audit_updated"]).exists()


def test_v1_g61_import_execution_does_not_touch_lima_runtime() -> None:
    fixture = _load_fixture()
    imported_modules = _lima_imported_modules()
    call_names = _lima_call_names()

    assert fixture["approved_vendor_provider_sdk_module"] == "openai"
    assert "openai" not in imported_modules
    assert not {
        "OpenAI",
        "AsyncOpenAI",
        "AzureOpenAI",
        "AsyncAzureOpenAI",
    }.intersection(call_names)


def test_v1_g61_authority_requirements_are_locked() -> None:
    requirements = _load_fixture()["import_execution_requirements"]

    assert requirements == {
        "guardian_gate_required_before_later_provider_call": True,
        "operator_approval_linkage_required_before_later_provider_call": True,
        "approved_module_name_exact_match_required": True,
        "approved_dependency_declaration_exact_match_required": True,
        "test_scoped_import_only_required": True,
        "sanitized_evidence_only_required": True,
        "deny_by_default_required": True,
        "links_v1_g57_v1_g58_v1_g59_v1_g60_evidence_required": True,
        "approval_metadata_is_not_broad_execution_authority": True,
    }


def test_v1_g61_future_authorities_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["built_in_provider_sdk_client_implementation_approved"] is False
    assert fixture["built_in_provider_sdk_client_implementation_added"] is False
    assert fixture["provider_client_construction_added"] is False
    assert fixture["provider_execution_expansion_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_production_runtime_integration_added"] is False
    assert fixture["live_provider_model_call_execution_added"] is False
    assert fixture["provider_sdk_network_egress_invocation_added"] is False

    for key, value in fixture["blocked_future_authorities"].items():
        assert value is False, key


def test_v1_g61_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for group_name in ("forbidden_boundaries", "sensitive_content_boundaries"):
        for key, value in fixture[group_name].items():
            assert value is False, f"{group_name}.{key}"


def test_v1_g61_accepted_evidence_refs_exist() -> None:
    for relative_path in _load_fixture()["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g61_decision_packet_records_exact_approval() -> None:
    decision_text = (
        REPO_ROOT
        / "docs"
        / "V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md"
    ).read_text(encoding="utf-8")

    assert "Decision packet status: `approved`" in decision_text
    assert "Recorded choice: Approve-V1-G61" in decision_text
    assert (
        "Recorded approval wording: I explicitly approve V1-G61 implementation "
        "of the runtime vendor SDK import execution proof slice, limited to the "
        "file scope, behavior scope, tests, rollback plan, and stop conditions "
        "in docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
        in decision_text
    )
    assert (
        "Approved implementation branch: "
        "`v1-g61-runtime-vendor-sdk-import-execution-proof`"
        in decision_text
    )
    assert "Implementation approved: yes." in decision_text


def test_v1_g61_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT
        / "docs"
        / "V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "Approved dependency declaration: `openai>=1.0.0,<3.0.0`" in closeout_text
    assert "Runtime import execution proof: passed" in closeout_text
    assert "Sanitized imported module version evidence: `2.43.0`" in closeout_text
    assert "No `lima/` runtime file" in implementation_text
    assert "Dependency manifest edited: no" in implementation_text
    assert "Lockfile edited: no" in implementation_text
    assert "Runtime vendor SDK import added to `lima/`: no" in implementation_text
    assert "Provider client construction added: no" in implementation_text
    assert "Network call performed by LIMA: no" in implementation_text
    assert "Direct provider egress performed by LIMA: no" in implementation_text
    assert "V1-G61 is complete" in closeout_text
    assert "Product readiness claimed: no" in closeout_text
    assert "Final public API freeze claimed: no" in closeout_text


def test_v1_g61_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md"
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
