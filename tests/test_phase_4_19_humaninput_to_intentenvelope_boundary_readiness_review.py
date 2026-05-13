"""Static checks for Phase 4.19 HumanInput to IntentEnvelope readiness review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_19_HUMANINPUT_TO_INTENTENVELOPE_BOUNDARY_READINESS_REVIEW.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_19_humaninput_to_intentenvelope_boundary_readiness_review.json"
)
PHASE_4_18_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_18_humaninput_to_intentenvelope_boundary_schema_contract_proposal.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_four_nineteen_readiness_review() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "4.19"
    assert fixture["status"] == (
        "non_runtime_humaninput_to_intentenvelope_boundary_readiness_review"
    )
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_review_is_not_implementation() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "not a bridge implementation" in phase_doc
    assert "not a test-only bridge" in phase_doc
    assert "not a real IntentCompiler" in phase_doc
    assert "not authorization" in phase_doc


def test_phase_eighteen_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "4.18"
    assert fixture["source_tag"] == (
        "phase-4.18-humaninput-to-intentenvelope-boundary-schema-contract-proposal"
    )
    assert fixture["source_merge_commit"] == "93d6bd116a56788f0acf0b95460229fe84e90e8d"


def test_review_is_metadata_only_and_not_bridge_or_intent_creation() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["review_question"] == (
        "is_phase_4_18_clear_safe_constrained_and_non_runtime_enough_for_phase_5_gate_closeout"
    )
    assert all(fixture["review_is"].values())
    assert all(fixture["review_is_not"].values())


def test_phase_eighteen_proposal_remains_metadata_only() -> None:
    fixture = _load_json(PHASE_4_18_FIXTURE_PATH)
    assert fixture["phase"] == "4.18"
    assert fixture["proposal_is"]["schema_contract_metadata_only"] is True
    assert fixture["proposal_is"]["explicit_metadata_only"] is True
    assert fixture["proposal_is_not"]["bridge_implementation"] is True
    assert fixture["proposal_is_not"]["intentenvelope_created"] is True
    assert fixture["boundary_results"]["runtime_behavior_added"] is False
    assert fixture["boundary_results"]["test_only_bridge_code_added"] is False


def test_findings_preserve_safety_gate_invariants() -> None:
    findings = _load_json(FIXTURE_PATH)["findings"]
    assert all(findings.values())
    assert findings["humaninput_is_not_intentenvelope"] is True
    assert findings["intentenvelope_is_not_authorization"] is True
    assert findings["raw_text_remains_inert"] is True
    assert findings["explicit_typed_metadata_required"] is True
    assert findings["hidden_parser_rejected"] is True
    assert findings["guardian_decision_remains_mandatory"] is True


def test_ready_for_is_limited_to_phase_five_gate_closeout_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == {
        "phase_4_20_phase_5_gate_implementation_readiness_closeout",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_implementation_authority_and_physical_paths() -> None:
    not_ready_for = set(_load_json(FIXTURE_PATH)["not_ready_for"])
    assert "humaninput_to_intentenvelope_implementation" in not_ready_for
    assert "test_only_bridge_code" in not_ready_for
    assert "runtime_wiring" in not_ready_for
    assert "real_intentcompiler" in not_ready_for
    assert "real_guardiandecision" in not_ready_for
    assert "approval_enforcement" in not_ready_for
    assert "execution" in not_ready_for
    assert "audit_persistence" in not_ready_for
    assert "physical_world_action" in not_ready_for
    assert "sparkbot_import_or_wiring" in not_ready_for


def test_boundary_results_show_no_runtime_bridge_or_blocked_behavior() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["test_only_bridge_code_added"] is False
    assert boundary["intentenvelope_created"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_four_nineteen_runtime_bridge_or_lima_files_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "humaninput_to_intentenvelope.py",
        REPO_ROOT / "tests" / "support" / "humaninput_to_intentenvelope_bridge.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_to_intentenvelope_bridge.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
