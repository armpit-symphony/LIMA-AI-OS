from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_gap_response_playbook"
    / "gap_response_playbook.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _playbook_text() -> str:
    return _text("playbook_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_gap_response_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_gap_response_playbook_only"
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["lima_runtime_files_touched"] is False
    assert fixture["tests_support_touched"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["package_metadata_changed"] is False
    assert fixture["public_exports_changed"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_repo_scanned"] is False
    assert fixture["consumer_proof_packet_received"] is False
    assert fixture["consumer_proof_packet_archived"] is False
    assert fixture["consumer_proof_packet_audited"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["response_sending_added"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_gap_response_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "playbook_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_gap_response_preserves_current_missing_state() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_playbook_text(), _review_text(), _audit_text()))

    assert (
        fixture["current_closeout_verdict"]
        == "lima_local_prerequisites_closed_waiting_on_consumer_proof"
    )
    assert f"`{fixture['current_closeout_verdict']}`" in combined
    assert f"`{fixture['current_freeze_state']}`" in combined
    assert f"`{fixture['current_product_state']}`" in combined

    for state in fixture["current_missing_inputs"].values():
        assert f"`{state}`" in combined

    assert "This design does not change those states." in _playbook_text()


def test_gap_response_references_source_artifacts() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_playbook_text(), _audit_text()))

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in combined

    assert "the stricter artifact controls" in _playbook_text()


def test_gap_categories_and_response_statuses_are_bounded() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_playbook_text(), _audit_text()))

    for category in fixture["allowed_gap_categories"]:
        assert f"`{category}`" in combined
    for category in fixture["forbidden_gap_categories"]:
        assert f"`{category}`" in combined
    for status in fixture["allowed_response_statuses"]:
        assert f"`{status}`" in combined
    for status in fixture["forbidden_response_statuses"]:
        assert f"`{status}`" in combined

    forbidden_serialized = json.dumps(
        {
            "forbidden_gap_categories": fixture["forbidden_gap_categories"],
            "forbidden_response_statuses": fixture["forbidden_response_statuses"],
        }
    )
    assert "production_ready" in forbidden_serialized
    assert "dependency_use_approved" in forbidden_serialized


def test_gap_to_response_mapping_is_fail_closed() -> None:
    fixture = _load_fixture()
    playbook = _playbook_text()
    mapping = fixture["gap_to_response_mapping"]

    expected_mappings = {
        "missing_packet": "waiting_for_consumer_packet",
        "missing_required_field": "needs_missing_evidence",
        "missing_redaction_attestation": "needs_redaction_before_review",
        "redaction_failure": "needs_redaction_before_review",
        "forbidden_public_import": "blocked_by_consumer_repo_boundary",
        "unreviewed_dry_run_candidate_import": "requires_lima_design_followup",
        "runtime_boundary_violation": "blocked_by_runtime_boundary",
        "consumer_repo_boundary_violation": "blocked_by_consumer_repo_boundary",
        "forbidden_product_or_production_claim": "blocked_by_claim_boundary",
    }

    assert mapping.items() >= expected_mappings.items()
    for gap, status in mapping.items():
        assert f"| `{gap}` | `{status}` |" in playbook
        assert status in fixture["allowed_response_statuses"]

    for forbidden in fixture["forbidden_response_statuses"]:
        assert forbidden not in mapping.values()

    assert "No mapping may produce product readiness" in playbook


def test_response_packet_shape_is_redacted_and_not_ready() -> None:
    fixture = _load_fixture()
    playbook = _playbook_text()

    for field in fixture["response_packet_fields"]:
        assert field in playbook

    for field, value in fixture["response_packet_required_values"].items():
        assert f"{field}: {value}" in playbook

    assert "redacted summaries only" in playbook
    assert "must not contain raw proof evidence" in playbook


def test_public_api_gap_rules_preserve_proof_public_boundary() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_playbook_text(), _audit_text()))

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in combined

    for forbidden in fixture["forbidden_public_import_claims"]:
        assert forbidden in combined

    assert "No public exports are changed." in _audit_text()


def test_non_execution_gap_rules_preserve_invariants() -> None:
    fixture = _load_fixture()
    playbook = _playbook_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in playbook

    assert "`needs_missing_evidence`" in playbook
    assert "`blocked_by_runtime_boundary`" in playbook


def test_redaction_gap_rules_block_sensitive_content() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_playbook_text(), _review_text(), _audit_text()))

    for blocker in fixture["redaction_blockers"]:
        assert blocker in combined

    assert "Do not copy the sensitive content into the LIMA repo" in combined


def test_consumer_specific_gap_rules_preserve_sparkbot_and_arc_boundaries() -> None:
    fixture = _load_fixture()
    playbook = _playbook_text()

    for requirement in fixture["sparkbot_evidence_requirements"]:
        assert requirement in playbook
    for requirement in fixture["arc_bot_evidence_requirements"]:
        assert requirement in playbook

    assert "Missing consumer-specific evidence should map to `needs_missing_evidence`." in playbook


def test_recommended_branch_rules_preserve_ownership() -> None:
    fixture = _load_fixture()
    playbook = _playbook_text()

    for branch_or_instruction in fixture["recommended_branch_rules"].values():
        assert f"`{branch_or_instruction}`" in playbook or branch_or_instruction in playbook

    assert "owner: consumer repo team" in playbook
    assert "owner: LIMA repo team" in playbook
    assert "still design-only unless separately approved" in playbook


def test_forbidden_actions_remain_blocked() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_playbook_text(), _audit_text()))

    for action in fixture["forbidden_actions"]:
        assert action in combined

    assert "This playbook must not trigger:" in combined


def test_static_fixture_paths_do_not_reference_live_or_external_surfaces() -> None:
    fixture = _load_fixture()
    serialized = json.dumps(fixture, sort_keys=True)

    forbidden_path_fragments = (
        "http://",
        "https://",
        "app://",
        "file://",
        "socket://",
        "sparkbot-lima-dry-run-boundary-proof/",
        "arc-lima-dry-run-boundary-proof/",
        "public/Sparkbot",
    )

    for fragment in forbidden_path_fragments:
        assert fragment not in serialized


def test_static_tests_allowed_files_and_forbidden_surfaces_are_bounded() -> None:
    fixture = _load_fixture()
    static_tests_audit = _static_tests_audit_text()

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in static_tests_audit

    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in static_tests_audit


def test_static_tests_implementation_recommends_independent_audit() -> None:
    fixture = _load_fixture()
    static_tests_audit = _static_tests_audit_text()

    assert (
        fixture["recommended_next_branch"]
        == "audit-lima-consumer-proof-gap-response-playbook-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
