from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_readiness_release_candidate_gate"
    / "consumer_proof_readiness_release_candidate_gate.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _gate_text() -> str:
    return _text("gate_design_path")


def _review_text() -> str:
    return _text("readiness_review_path")


def _audit_text() -> str:
    return _text("audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def _public_api_fixture() -> Mapping[str, Any]:
    fixture = _load_fixture()
    return json.loads(
        (REPO_ROOT / fixture["public_api_manifest_fixture_path"]).read_text(encoding="utf-8")
    )


def test_release_candidate_gate_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_readiness_release_candidate_gate_only"
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
    assert fixture["automated_proof_intake_added"] is False
    assert fixture["response_sending_added"] is False
    assert fixture["ledger_persistence_added"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_release_candidate_gate_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "gate_design_path",
        "readiness_review_path",
        "audit_path",
        "static_tests_audit_path",
        "public_api_manifest_fixture_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_release_candidate_gate_source_artifacts_exist_and_are_referenced() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for path in fixture["required_source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in gate

    assert "the stricter source artifact controls" in gate


def test_release_candidate_verdict_is_request_only() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    review = _review_text()
    audit = _audit_text()

    verdict = fixture["gate_verdict"]
    assert verdict == "ready_for_consumer_proof_request_release_candidate_only"
    assert f"`{verdict}`" in gate
    assert f"`{verdict}`" in review
    assert f"`{verdict}`" in audit
    assert "ready enough to request redacted consumer-owned dry-run proof packets" in gate
    assert "It does not mean those packets exist" in audit


def test_current_gate_state_remains_missing_and_not_ready() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    review = _review_text()
    audit = _audit_text()
    state = fixture["current_state"]

    assert f"| LIMA-local proof package | `{state['lima_local_proof_package']}` |" in gate
    assert f"| Sparkbot proof packet | `{state['sparkbot_proof_packet']}` |" in gate
    assert f"| Arc Bot proof packet | `{state['arc_bot_proof_packet']}` |" in gate
    assert f"| Sparkbot redaction review | `{state['sparkbot_redaction_review']}` |" in gate
    assert f"| Arc Bot redaction review | `{state['arc_bot_redaction_review']}` |" in gate
    assert f"| Sparkbot proof audit | `{state['sparkbot_proof_audit']}` |" in gate
    assert f"| Arc Bot proof audit | `{state['arc_bot_proof_audit']}` |" in gate
    assert f"| Public API compatibility freeze | `{state['public_api_compatibility_freeze']}` |" in gate
    assert f"| Product readiness | `{state['product_readiness']}` |" in gate

    assert "NOT READY for product use, compatibility freeze, or consumer dependency-use claims." in review
    assert "NOT READY for Sparkbot product use" in audit
    assert "Proof audits have not started." in audit


def test_release_candidate_imports_match_proof_public_manifest_entries() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    public_api = _public_api_fixture()

    manifest_proof_imports = {
        entry["import"]
        for entry in public_api["public_imports"]
        if entry["classification"] == "proof_public"
    }
    assert set(fixture["proof_public_imports"]) == manifest_proof_imports

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in gate

    for forbidden_import in fixture["forbidden_consumer_proof_imports"]:
        assert forbidden_import in gate


def test_method_level_candidates_match_manifest_and_remain_non_authoritative() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()
    public_api = _public_api_fixture()

    manifest_method_candidates = {
        f"{entry['member']}(...)"
        for entry in public_api["public_imports"]
        if entry["classification"] == "method_level_dry_run_candidate"
    }
    assert set(fixture["method_level_candidates"]) == manifest_method_candidates

    for candidate in fixture["method_level_candidates"]:
        assert f"`{candidate}`" in gate

    assert "non-authoritative metadata only" in gate
    assert "Optional method-level dry-run candidates remain non-authoritative" in audit


def test_required_proof_shape_remains_dry_run_and_repo_team_owned() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()

    for proof_item in fixture["required_proof_shape"]:
        assert proof_item in gate

    assert "The request must not ask consumer teams to wire production routes" in gate
    assert "call models" in gate
    assert "execute tools" in gate
    assert "discover live devices" in gate
    assert "control devices, robots, drones, or physical-world systems" in gate
    assert "repo-team-owned proof report" in audit


def test_non_execution_invariants_match_public_api_manifest() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    public_api = _public_api_fixture()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants == public_api["required_non_execution_invariants"]
    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in gate

    assert "Missing invariant evidence means the packet is not ready for proof acceptance." in gate
    assert "`blocked_by_runtime_boundary`" in gate


def test_consumer_branch_ownership_stays_outside_lima_repo() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()
    branches = fixture["consumer_branches"]

    assert f"`{branches['sparkbot']}`" in gate
    assert f"`{branches['arc_bot']}`" in gate
    assert branches["lima_repo_must_not_create_or_inspect"] is True
    assert "must not create, edit, push, fetch, clone, scan, inspect, or validate those branches" in gate
    assert "This audit did not touch public Sparkbot, Arc Bot, or any consumer repository." in audit


def test_sparkbot_and_arc_proof_requirements_remain_missing_until_supplied() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert "Sparkbot proof must remain missing until the Sparkbot repo team supplies" in gate
    for requirement in fixture["sparkbot_proof_requirements"]:
        assert requirement in gate

    assert "Arc Bot / LIMA Office proof must remain missing until the Arc Bot / LIMA Office repo team supplies" in gate
    for requirement in fixture["arc_bot_proof_requirements"]:
        assert requirement in gate


def test_redaction_blockers_and_unredacted_archive_block_remain_present() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()
    policy = fixture["redaction_policy"]

    assert policy["unsafe_packet_status"] == "needs_redaction_before_review"
    assert policy["do_not_archive_unredacted_evidence"] is True
    assert "`needs_redaction_before_review`" in gate
    assert "Do not archive unredacted evidence." in gate
    assert "The gate also says unredacted evidence must not be archived." in audit

    for blocker in policy["redaction_blockers"]:
        assert blocker in gate


def test_forbidden_claims_remain_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()
    combined = "\n".join((gate, audit))

    assert "This gate must not be described as:" in gate
    for claim in fixture["forbidden_claims"]:
        assert claim in combined


def test_forbidden_actions_and_runtime_surfaces_remain_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()
    combined = "\n".join((gate, audit))

    assert "This gate must not trigger:" in gate
    for action in fixture["forbidden_actions"]:
        assert action in combined

    assert "No runtime behavior is introduced." in audit
    assert "model/tool/connector/storage/scheduler execution" in audit
    assert "physical-world behavior" in audit


def test_manual_next_steps_preserve_no_packet_no_freeze_boundary() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _audit_text()

    for state in fixture["manual_next_step_states"]:
        assert state in gate

    assert "If consumer proof packets are supplied:" in audit
    assert "`audit-consumer-owned-proof-results`" in audit
    assert "If continuing LIMA-local machine-checkable guardrails before packets arrive:" in audit


def test_static_test_fixture_paths_do_not_reference_live_or_external_surfaces() -> None:
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
        == "audit-lima-consumer-proof-readiness-release-candidate-gate-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_tests_audit
