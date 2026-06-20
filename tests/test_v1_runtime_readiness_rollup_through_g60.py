"""Static checks for the V1 runtime readiness rollup through G60."""

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
    / "v1_runtime_readiness_rollup_through_g60.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_runtime_readiness_rollup_g60_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["rollup_id"] == "v1_runtime_readiness_rollup_through_g60"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_commit_before_refresh"] == (
        "0550acdbd4cd2c9f1817a0ca163b3b6d3e9d09cc"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_runtime_readiness_rollup_g60_required_verdicts() -> None:
    verdicts = _load_fixture()["required_verdicts"]

    assert verdicts["v1_runtime_authority_chain"] == "CANDIDATE_ONLY"
    assert verdicts["provider_execution_hardening_authorization_metadata"] == (
        "CANDIDATE_ONLY"
    )
    assert verdicts["built_in_provider_sdk_client_authority_contract_metadata"] == (
        "CANDIDATE_ONLY"
    )
    assert verdicts["sdk_dependency_vendor_provider_sdk_import_authority_metadata"] == (
        "CANDIDATE_ONLY"
    )
    assert verdicts[
        "sdk_dependency_declaration_vendor_provider_sdk_import_boundary_evidence"
    ] == "CANDIDATE_ONLY"
    assert verdicts["sdk_dependency_additions"] == "CANDIDATE_ONLY"
    assert verdicts["dependency_manifest_edits"] == "CANDIDATE_ONLY"
    assert verdicts["approved_dependency_declaration"] == "openai>=1.0.0,<3.0.0"
    assert verdicts["lockfile_edits"] == "NOT_APPROVED"
    assert verdicts["runtime_vendor_provider_sdk_imports_in_lima"] == "NOT_APPROVED"
    assert verdicts["runtime_vendor_sdk_import_execution_proof"] == "NOT_APPROVED"
    assert verdicts["built_in_provider_sdk_client_implementation"] == "NOT_APPROVED"
    assert verdicts["provider_client_construction"] == "NOT_APPROVED"
    assert verdicts["lima_owned_provider_endpoint_resolution_execution"] == "NOT_APPROVED"
    assert verdicts["lima_owned_direct_provider_network_egress"] == "NOT_APPROVED"
    assert verdicts["secret_lookup_and_credential_value_access"] == "NOT_APPROVED"
    assert verdicts["fallback_execution"] == "NOT_APPROVED"
    assert verdicts["consumer_production_runtime_integration"] == "NOT_APPROVED"
    assert verdicts["physical_world_readiness"] == "BLOCKED"
    assert verdicts["product_readiness"] == "NOT_READY"
    assert verdicts["final_public_api_freeze"] == "NOT_APPROVED"


def test_runtime_readiness_rollup_g60_current_status_advances_with_g60_evidence() -> None:
    current = _load_fixture()["current_status"]

    assert current["latest_completed_gate"] == "V1-G60"
    assert current["latest_independent_audit"] == "V1-G60"
    assert current["latest_readiness_rollup"] == "V1-G60"
    assert current["current_gate"] == "runtime_vendor_sdk_import_execution_proof_request"
    assert current["next_recommended_lane"] == (
        "prepare_runtime_vendor_sdk_import_execution_proof_approval_request"
    )
    assert current["next_lane_request_only"] is True
    assert current["v1_product_ready"] is False
    assert current["production_ready"] is False


def test_runtime_readiness_rollup_g60_status() -> None:
    status = _load_fixture()["g60_status"]

    assert status["sdk_dependency_vendor_provider_sdk_import_approved"] is True
    assert status["sdk_dependency_vendor_provider_sdk_import_implemented"] is True
    assert status["sdk_dependency_vendor_provider_sdk_import_audited"] is True
    assert status["approved_dependency_declaration"] == "openai>=1.0.0,<3.0.0"
    assert status["dependency_manifest_edited"] is True
    assert status["dependency_manifest"] == "pyproject.toml"
    assert status["metadata_and_manifest_only"] is True
    assert status["lima_runtime_files_changed"] is False
    assert status["lima_public_api_expanded"] is False
    assert status["sparkbot_files_changed"] is False
    assert status["arc_bot_shell_files_changed"] is False
    assert status["consumer_production_runtime_integration_added"] is False
    assert status["lockfile_edited"] is False
    assert status["vendor_provider_sdk_runtime_import_added_to_lima"] is False
    assert status["runtime_import_execution_claimed"] is False
    assert status["built_in_provider_sdk_client_implementation_added"] is False
    assert status["provider_client_construction_added"] is False
    assert status["provider_execution_expansion_added"] is False
    assert status["provider_network_egress_added"] is False
    assert status["credential_value_access_added"] is False
    assert status["product_readiness_claimed"] is False
    assert status["final_public_api_freeze_approved"] is False


def test_runtime_readiness_rollup_g60_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["blocked_authorities"].items():
        assert value is False, key


def test_runtime_readiness_rollup_g60_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_v1_g60_validation"] == {
        "passed": True,
        "tests_passed": 12,
    }
    assert validation["focused_v1_g60_audit_validation"] == {
        "passed": True,
        "tests_passed": 11,
    }
    assert validation["focused_v1_g60_rollup_validation"] == {
        "passed": True,
        "tests_passed": 375,
    }
    assert validation["full_lima_suite_before_refresh"] == {
        "passed": True,
        "tests_passed": 5239,
    }


def test_runtime_readiness_rollup_g60_doc_contains_next_lane_and_boundaries() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["rollup"]).read_text(encoding="utf-8")

    assert "# V1 Runtime Readiness Rollup Through G60" in text
    assert (
        "SDK dependency declaration and vendor provider SDK import-boundary evidence: "
        "`CANDIDATE_ONLY`"
        in text
    )
    assert "Approved dependency declaration: `openai>=1.0.0,<3.0.0`" in text
    assert "Runtime vendor provider SDK imports in `lima/`: `NOT_APPROVED`" in text
    assert "Runtime vendor SDK import execution proof: `NOT_APPROVED`" in text
    assert "Final public API freeze: `NOT_APPROVED`" in text
    assert "Product readiness: `NOT_READY`" in text
    assert "runtime vendor SDK import execution proof lane" in text
