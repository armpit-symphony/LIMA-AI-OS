"""Static checks for the V1 post-G60 request readiness refresh."""

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
    / "v1_post_g60_request_readiness_refresh.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_post_g60_request_readiness_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["refresh_id"] == "v1_post_g60_request_readiness_refresh"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-post-g60-request-readiness-refresh"
    assert fixture["source_branch"] == (
        "audit-v1-g60-sdk-dependency-vendor-provider-sdk-import-approval-request"
    )
    assert fixture["source_commit_before_refresh"] == (
        "bab82507d4694751904ea1c9a3729169c82e01e4"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_post_g60_request_readiness_records_real_blocker() -> None:
    fixture = _load_fixture()

    assert fixture["readiness_verdict"] == (
        "READY_FOR_OPERATOR_DECISION_BLOCKED_FOR_IMPLEMENTATION"
    )
    assert fixture["implementation_blocker"] == "Approve-V1-G60 has not been recorded"
    assert fixture["required_operator_choice_to_unblock_implementation"] == (
        "Approve-V1-G60"
    )
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G60 implementation of the LIMA-side SDK "
        "dependency addition and vendor provider SDK import approval slice, "
        "limited to the file scope, behavior scope, tests, rollback plan, and "
        "stop conditions in "
        "docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_APPROVAL_REQUEST.md."
    )


def test_post_g60_request_readiness_required_verdicts_remain_blocked() -> None:
    verdicts = _load_fixture()["required_verdicts"]

    assert verdicts["v1_runtime_authority_chain"] == "CANDIDATE_ONLY"
    assert verdicts["v1_g60_approval_request"] == "READY_FOR_OPERATOR_DECISION"
    assert verdicts["v1_g60_implementation"] == "NOT_APPROVED"
    assert verdicts["sdk_dependency_additions"] == "NOT_APPROVED"
    assert verdicts["dependency_manifest_edits"] == "NOT_APPROVED"
    assert verdicts["lockfile_edits"] == "NOT_APPROVED"
    assert verdicts["vendor_provider_sdk_imports"] == "NOT_APPROVED"
    assert verdicts["provider_client_construction"] == "NOT_APPROVED"
    assert verdicts["lima_owned_direct_provider_network_egress"] == "NOT_APPROVED"
    assert verdicts["product_readiness"] == "NOT_READY"
    assert verdicts["final_public_api_freeze"] == "NOT_APPROVED"


def test_post_g60_request_readiness_boundary_confirmation() -> None:
    boundary = _load_fixture()["boundary_confirmation"]

    assert boundary["docs_tests_fixtures_only"] is True
    for key, value in boundary.items():
        if key != "docs_tests_fixtures_only":
            assert value is False, key


def test_post_g60_request_readiness_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_v1_g60_request_audit_validation"] == {
        "passed": True,
        "tests_passed": 10,
    }
    assert validation["focused_v1_g60_request_audit_chain_validation"] == {
        "passed": True,
        "tests_passed": 53,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite_before_refresh"] == {
        "passed": True,
        "tests_passed": 5209,
    }


def test_post_g60_request_readiness_doc_contains_exact_gate() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["refresh"]).read_text(encoding="utf-8")

    assert "Readiness verdict: `READY_FOR_OPERATOR_DECISION_BLOCKED_FOR_IMPLEMENTATION`" in text
    assert "`Approve-V1-G60` has not been recorded" in text
    assert "V1-G60 implementation cannot begin" in text
    assert "SDK dependency additions: `NOT_APPROVED`" in text
    assert "Vendor provider SDK imports: `NOT_APPROVED`" in text
    assert "Product readiness: `NOT_READY`" in text
    assert "Final public API freeze: `NOT_APPROVED`" in text


def test_post_g60_request_readiness_next_choices_are_exact() -> None:
    assert _load_fixture()["next_valid_operator_choices"] == [
        "Approve-V1-G60",
        "Revise-V1-G60",
        "Pause",
    ]
