from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_packet_receipt_response_examples"
    / "consumer_proof_packet_receipt_response_examples.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _examples_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["examples_path"]).read_text(encoding="utf-8")


def _audit_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["audit_path"]).read_text(encoding="utf-8")


def test_receipt_response_examples_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_packet_receipt_response_examples_only"
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_proof_packet_audited"] is False
    assert fixture["real_packet_receipt_recorded"] is False
    assert fixture["receipt_ledger_updated"] is False
    assert fixture["proof_archive_written"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_receipt_response_examples_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in ("examples_path", "readiness_review_path", "audit_path"):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_receipt_response_examples_reference_source_artifacts_without_overriding() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for path in fixture["source_artifacts"]:
        assert f"`{path}`" in examples
        assert (REPO_ROOT / path).exists(), path
    assert "These examples must not override those artifacts." in examples


def test_receipt_response_examples_preserve_global_no_runtime_rules() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for rule in fixture["global_rules"]:
        assert rule in examples


def test_receipt_response_examples_include_expected_synthetic_ids() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for response_id in fixture["example_response_ids"]:
        assert response_id in examples
    for receipt_id in fixture["ledger_example_receipt_ids"]:
        assert receipt_id in examples
    assert "This example does not represent an actual received packet." in examples
    assert "Example only; not a real Sparkbot receipt." in examples
    assert "Example only; not a real Arc Bot receipt." in examples


def test_receipt_response_examples_use_expected_statuses_and_not_production_ready() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for status in fixture["expected_statuses"]:
        assert f"response_status: {status}" in examples or f"audit_status: {status}" in examples
    assert examples.count("production_readiness: not_production_ready") >= 8
    assert "proof audit still required" in examples


def test_receipt_response_examples_route_next_branches() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for branch in fixture["required_next_branches"]:
        assert branch in examples


def test_receipt_response_examples_require_non_execution_evidence_when_missing() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for evidence in fixture["non_execution_missing_evidence"]:
        assert evidence in examples
    assert "Missing evidence is not a runtime approval." in examples
    assert "Do not proceed to compatibility freeze." in examples


def test_receipt_response_examples_block_forbidden_runtime_surfaces() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for surface in fixture["forbidden_runtime_surfaces"]:
        assert surface in examples
    assert "blocked_by_runtime_boundary" in examples
    assert "Do not implement workaround behavior in LIMA." in examples


def test_receipt_response_examples_block_forbidden_claims() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for claim in fixture["forbidden_claims"]:
        assert claim in examples
    assert "blocked_by_claim_boundary" in examples
    assert "Passing dry-run dependency proof is not production readiness." in examples


def test_receipt_response_examples_preserve_consumer_repo_boundary() -> None:
    examples = _examples_text()

    assert "blocked_by_consumer_repo_boundary" in examples
    assert "Request crosses the consumer repo ownership boundary." in examples
    assert "LIMA reviewers must not modify or push consumer proof branches." in examples
    assert "Consumer repo teams own proof packets." in examples


def test_receipt_response_examples_forbid_unsafe_interpretations() -> None:
    fixture = _load_fixture()
    examples = _examples_text()

    for interpretation in fixture["forbidden_example_interpretations"]:
        assert interpretation in examples


def test_receipt_response_examples_audit_confirms_synthetic_docs_only_boundary() -> None:
    audit = _audit_text()

    assert "synthetic, docs-only reference material" in audit
    assert "They do not record real proof packets" in audit
    assert "They do not approve proof audit, compatibility freeze" in audit
    assert "Compatibility freeze remains blocked." in audit


def test_receipt_response_examples_recommend_independent_static_test_audit() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_branch"] == "audit-lima-consumer-proof-packet-receipt-response-examples-static-tests"
