from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_proof_ledger_package_readiness_gate"
    / "consumer_proof_ledger_package_readiness_gate.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _gate_text() -> str:
    return _text("gate_design_path")


def _gate_audit_text() -> str:
    return _text("gate_audit_path")


def _static_design_text() -> str:
    return _text("static_tests_design_path")


def _static_design_audit_text() -> str:
    return _text("static_tests_design_audit_path")


def _implementation_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_package_readiness_gate_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_consumer_proof_ledger_package_readiness_gate_only"
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
    assert fixture["response_sending_added"] is False
    assert fixture["ledger_persistence_added"] is False
    assert fixture["compatibility_freeze_started"] is False
    assert fixture["automated_intake_added"] is False
    assert fixture["storage_or_persistence_added"] is False
    assert fixture["runtime_wiring_added"] is False
    assert fixture["production_readiness_claimed"] is False


def test_package_readiness_static_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "gate_design_path",
        "gate_audit_path",
        "audit_readiness_review_path",
        "static_tests_design_path",
        "static_tests_readiness_review_path",
        "static_tests_design_audit_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_package_readiness_source_artifacts_exist_and_remain_strict() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    design = _static_design_text()
    audit = _static_design_audit_text()

    for path in fixture["source_artifacts"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in design

    for path in fixture["package_readiness_gates_path"]:
        assert (REPO_ROOT / path).exists(), path
        assert f"`{path}`" in gate
        assert f"`{path}`" in design

    assert "the stricter source artifact controls" in gate
    assert "the stricter source artifact remains authoritative" in design
    assert "The stricter-source rule remains in force" in audit


def test_gate_verdict_remains_operator_handoff_request_only() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _gate_audit_text()
    design = _static_design_text()

    verdict = fixture["gate_verdict"]
    assert verdict == "ready_for_operator_handoff_request_only"
    assert f"`{verdict}`" in gate
    assert f"`{verdict}`" in audit
    assert verdict in design
    assert "Sparkbot and Arc Bot proof packets are still missing." in gate
    assert "It does not mean:" in audit


def test_current_package_state_remains_missing_and_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    design = _static_design_text()
    state = fixture["package_state"]

    assert f"| LIMA proof package | `{state['lima_proof_package']}` |" in gate
    assert f"| Sparkbot proof packet | `{state['sparkbot_proof_packet']}` |" in gate
    assert f"| Arc Bot proof packet | `{state['arc_bot_proof_packet']}` |" in gate
    assert f"| Sparkbot redaction review | `{state['sparkbot_redaction_review']}` |" in gate
    assert f"| Arc Bot redaction review | `{state['arc_bot_redaction_review']}` |" in gate
    assert f"| Sparkbot proof audit | `{state['sparkbot_proof_audit']}` |" in gate
    assert f"| Arc Bot proof audit | `{state['arc_bot_proof_audit']}` |" in gate
    assert f"| Compatibility freeze | `{state['compatibility_freeze']}` |" in gate
    assert f"| Product readiness | `{state['product_readiness']}` |" in gate
    assert "Sparkbot packet remains `not_received`" in design
    assert "Arc Bot packet remains `not_received`" in design
    assert "compatibility freeze remains `blocked`" in design


def test_public_import_set_and_forbidden_imports_are_locked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for import_line in fixture["proof_public_imports"]:
        assert f"`{import_line}`" in gate

    for import_line in fixture["forbidden_consumer_proof_imports"]:
        assert import_line in gate

    assert "Optional proof-stage method" in gate
    assert "`LimaKernel.preview_guardian_lifecycle(...)`" in gate


def test_consumer_branch_ownership_remains_outside_lima_repo() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _gate_audit_text()

    boundary = fixture["consumer_boundary"]
    assert f"`{boundary['sparkbot_branch']}`" in gate
    assert f"`{boundary['arc_bot_branch']}`" in gate
    assert boundary["lima_repo_must_not_create_or_inspect_consumer_branches"] is True
    assert "must not create, edit, push, fetch, clone, scan, inspect, or validate those branches" in gate
    assert "the LIMA repo team must not create, edit, push, fetch, clone, scan, inspect, or validate" in audit


def test_required_proof_shape_remains_dry_run_and_repo_team_owned() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    for proof_item in fixture["required_proof_shape"]:
        assert proof_item in gate

    assert "The request must not ask consumer teams to wire production routes" in gate
    assert "call models" in gate
    assert "execute tools" in gate
    assert "discover live devices" in gate
    assert "control devices, robots, drones, or physical-world systems" in gate


def test_non_execution_invariants_remain_required() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    design = _static_design_text()
    invariants = fixture["non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in gate

    assert "Missing invariant evidence means the packet is not ready for proof acceptance." in gate
    assert "`blocked_by_runtime_boundary`" in gate
    assert "all non-execution invariants remain" in design


def test_redaction_blockers_and_unredacted_archive_block_remain_present() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    design = _static_design_text()
    policy = fixture["redaction_policy"]

    assert policy["unsafe_packet_status"] == "needs_redaction_before_review"
    assert policy["do_not_archive_unredacted_evidence"] is True
    assert "`needs_redaction_before_review`" in gate
    assert "Do not archive unredacted evidence." in gate

    for blocker in policy["redaction_blockers"]:
        assert blocker in gate

    assert "redaction blockers remain present" in design


def test_sparkbot_and_arc_evidence_requirements_remain_missing_until_supplied() -> None:
    fixture = _load_fixture()
    gate = _gate_text()

    assert "Sparkbot proof must remain missing until the Sparkbot repo team supplies" in gate
    for requirement in fixture["sparkbot_requirements"]:
        assert requirement in gate

    assert "Arc Bot / LIMA Office proof must remain missing until the Arc Bot / LIMA Office repo team supplies" in gate
    for requirement in fixture["arc_bot_requirements"]:
        assert requirement in gate


def test_compatibility_freeze_remains_blocked_until_consumer_proof_audits_pass() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _gate_audit_text()
    design = _static_design_text()

    assert fixture["compatibility_freeze"]["status"] == "blocked"
    assert "| Compatibility freeze | `blocked` |" in gate
    assert "Compatibility freeze remains blocked" in audit
    assert "compatibility freeze remains `blocked`" in design
    assert "both proof audits must pass first" in gate

    assert fixture["compatibility_freeze"]["unblock_requires"] == [
        "Sparkbot packet is received",
        "Arc Bot packet is received",
        "both packets pass redaction checks",
        "Sparkbot proof audit passes as `pass_for_dry_run_dependency_proof`",
        "Arc Bot proof audit passes as `pass_for_dry_run_dependency_proof`",
        "no missing evidence blockers remain",
        "no forbidden import blockers remain",
        "no runtime boundary blockers remain",
        "no consumer repo boundary blockers remain",
        "no production/live-readiness claim blockers remain",
        "a compatibility freeze branch is separately designed and audited",
    ]


def test_forbidden_claims_remain_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    audit = _gate_audit_text()

    assert "This gate must not be described as:" in gate
    for claim in fixture["forbidden_claims"]:
        assert claim in gate
        assert claim in audit


def test_forbidden_actions_and_runtime_behaviors_remain_blocked() -> None:
    fixture = _load_fixture()
    gate = _gate_text()
    design = _static_design_text()
    implementation_audit = _implementation_audit_text()

    assert "This gate must not trigger:" in gate
    for action in fixture["forbidden_actions"]:
        assert action in gate

    for behavior in fixture["prohibited_runtime_behaviors"]:
        assert behavior in design

    assert "proof packet receipt automation" in implementation_audit
    assert "response sending" in implementation_audit
    assert "ledger persistence" in implementation_audit
    assert "runtime behavior" in implementation_audit
    assert "physical-world behavior" in implementation_audit


def test_allowed_files_and_forbidden_later_surfaces_are_bounded() -> None:
    fixture = _load_fixture()
    design = _static_design_text()
    audit = _static_design_audit_text()
    implementation_audit = _implementation_audit_text()

    for path in fixture["allowed_later_files"]:
        assert f"`{path}`" in design
        assert f"`{path}`" in audit
        assert f"`{path}`" in implementation_audit

    for surface in fixture["forbidden_later_surfaces"]:
        assert surface in audit

    assert "Still required before LIMA can be considered ready" in implementation_audit
    assert "Sparkbot-owned proof packet" in implementation_audit
    assert "Arc-owned proof packet" in implementation_audit
    assert "compatibility freeze audit" in implementation_audit
    assert "runtime behavior" in implementation_audit
    assert "physical-world behavior" in implementation_audit
    assert "forbidden-surface boundaries are explicit" in design


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


def test_static_tests_implementation_recommends_independent_audit() -> None:
    fixture = _load_fixture()
    implementation_audit = _implementation_audit_text()

    assert fixture["recommended_next_branch"] == (
        "audit-lima-consumer-proof-ledger-package-readiness-gate-static-tests-implementation"
    )
    assert f"`{fixture['recommended_next_branch']}`" in implementation_audit
    assert fixture["independent_audit_path"].endswith(
        "LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md"
    )
