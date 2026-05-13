"""Static checks for Phase 4.18 HumanInput to IntentEnvelope schema proposal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_18_HUMANINPUT_TO_INTENTENVELOPE_BOUNDARY_SCHEMA_CONTRACT_PROPOSAL.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_18_humaninput_to_intentenvelope_boundary_schema_contract_proposal.json"
)

REQUIRED_EXPLICIT_METADATA = {
    "intent_type",
    "action_type",
    "risk_class",
    "target_ref",
    "typed_args",
    "evidence_refs",
    "requested_tool_packs",
    "approval_level",
    "privacy_class",
    "redaction_class",
    "lineage_id",
    "reason",
    "confidence",
}

REQUIRED_SAFETY_MARKERS = {
    "raw_text_inert",
    "explicit_metadata_only",
    "no_hidden_parser",
    "no_model_call",
    "no_tool_execution",
    "no_guardian_decision",
    "no_authorization",
    "guardian_required_before_consequential_behavior",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_four_eighteen_schema_proposal() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "4.18"
    assert fixture["status"] == (
        "non_runtime_humaninput_to_intentenvelope_boundary_schema_contract_proposal"
    )
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_proposal_is_not_bridge_or_compiler() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "not a bridge implementation" in phase_doc
    assert "not a real IntentCompiler" in phase_doc
    assert "must not produce an IntentEnvelope" in phase_doc


def test_phase_seventeen_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "4.17"
    assert fixture["source_tag"] == "phase-4.17-humaninput-to-intentenvelope-boundary-planning"
    assert fixture["source_merge_commit"] == "29f8993b5adb34b9fc6d9d0155e6bd79e915847a"


def test_proposal_is_metadata_only_and_not_intentenvelope_creation() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["key_rule"] == "schema_contract_proposal_is_not_bridge_or_intentcompiler"
    assert all(fixture["proposal_is"].values())
    assert all(fixture["proposal_is_not"].values())


def test_proposed_groups_include_humaninput_refs_explicit_metadata_and_safety_markers() -> None:
    groups = _load_json(FIXTURE_PATH)["proposed_input_groups"]
    assert "input_ref" in groups["humaninput_refs"]
    assert "lineage_seed_ref" in groups["humaninput_refs"]
    assert REQUIRED_EXPLICIT_METADATA == set(groups["explicit_typed_intent_metadata"])
    assert REQUIRED_SAFETY_MARKERS == set(groups["safety_markers"])


def test_required_invariants_preserve_safety_gate() -> None:
    invariants = _load_json(FIXTURE_PATH)["required_invariants"]
    assert all(invariants.values())
    assert invariants["humaninput_is_not_intentenvelope"] is True
    assert invariants["raw_text_is_inert"] is True
    assert invariants["explicit_typed_metadata_required"] is True
    assert invariants["no_hidden_parser"] is True
    assert invariants["no_model_calls"] is True


def test_ready_for_is_limited_to_readiness_review_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == {
        "phase_4_19_humaninput_to_intentenvelope_boundary_readiness_review",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_implementation_and_authority_paths() -> None:
    not_ready_for = set(_load_json(FIXTURE_PATH)["not_ready_for"])
    assert "humaninput_to_intentenvelope_implementation" in not_ready_for
    assert "test_only_bridge_code" in not_ready_for
    assert "real_intentcompiler" in not_ready_for
    assert "real_guardiandecision" in not_ready_for
    assert "approval_enforcement" in not_ready_for
    assert "execution" in not_ready_for
    assert "physical_world_action" in not_ready_for


def test_boundary_results_show_no_runtime_or_bridge_behavior() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["test_only_bridge_code_added"] is False
    assert boundary["intentenvelope_created"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_four_eighteen_runtime_bridge_or_lima_files_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "humaninput_to_intentenvelope.py",
        REPO_ROOT / "tests" / "support" / "humaninput_to_intentenvelope_bridge.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_to_intentenvelope_bridge.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
