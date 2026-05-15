"""Static and behavioral checks for Phase 11.5 runtime slice archive closeout."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any

from lima.kernel import normalize_candidate_status, validate_candidate
from lima.kernel.intake_candidate import build_intake_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_11_5_PHASE_11_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_11_5_phase_11_runtime_slice_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _candidate(**overrides: Any) -> dict[str, Any]:
    intake = {
        "synthetic": True,
        "test_only": True,
        "intake_id": "intake-11-5",
        "source": "test_shell",
        "source_channel": "test_room",
        "operator_intent": "Phil says this trusted admin note should be summarized",
        "normalized_request": "summarize trusted admin note",
        "requested_action": "summarize",
        "action_category": "informational",
        "provenance": {"fixture": "phase_11_5", "lineage_seed": "seed-11-5"},
    }
    intake.update(overrides)
    return build_intake_candidate(intake)


def test_phase_is_docs_tests_fixtures_only_archive() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "11.5"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_12_requires_explicit_phil_approval"] is True


def test_phase_eleven_zero_through_four_are_listed_complete() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_11_scope"]
    assert completed == [
        "phase_11_0_runtime_slice_preflight_audit_eligible_file_confirmation",
        "phase_11_1_candidate_status_acceptance_test_scaffolding",
        "phase_11_2_candidate_status_normalization_runtime_implementation",
        "phase_11_3_candidate_validation_runtime_implementation",
        "phase_11_4_runtime_slice_readiness_review",
    ]


def test_only_approved_phase_ten_two_runtime_files_were_touched() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    eligible = set(fixture["phase_10_2_eligible_runtime_files"])
    touched = set(fixture["approved_runtime_files_touched"])
    assert eligible == {
        "lima/kernel/intake_candidate.py",
        "lima/kernel/__init__.py",
        "lima/kernel/candidate_status.py",
    }
    assert touched == {
        "lima/kernel/candidate_status.py",
        "lima/kernel/__init__.py",
    }
    assert touched.issubset(eligible)
    assert fixture["eligible_runtime_files_not_touched"] == ["lima/kernel/intake_candidate.py"]


def test_phase_eleven_archive_lists_added_and_not_added_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    added = set(fixture["phase_11_added"])
    not_added = set(fixture["phase_11_did_not_add"])
    assert "candidate_status_normalization" in added
    assert "candidate_validation" in added
    assert "safe_kernel_exports" in added
    assert "humaninput_runtime_bridge" in not_added
    assert "sparkbot_wiring" in not_added
    assert "live_adapter" in not_added
    assert "intentcompiler_runtime_behavior" in not_added
    assert "guardiandecision_runtime_behavior" in not_added
    assert "approval_enforcement" in not_added
    assert "execution" in not_added
    assert "dispatch" in not_added
    assert "audit_persistence" in not_added
    assert "runtime_files_outside_phase_10_2_file_map" in not_added


def test_runtime_guarantees_remain_non_executing_and_authority_free() -> None:
    candidate = _candidate()
    candidate["approval_state"] = "approved"
    candidate["candidate_status"] = "approved"
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)
    assert normalized["candidate_status"] == "blocked"
    assert normalized["execution_allowed"] is False
    assert normalized["side_effects_allowed"] is False
    assert normalized["approved"] is False
    assert normalized["approval_state"] != "approved"
    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert validated["execution_allowed"] is False
    assert validated["side_effects_allowed"] is False
    assert validated["approved"] is False
    assert validated["approval_state"] != "approved"
    assert validated["phase_5_humaninput_runtime_bridge_gated"] is True


def test_malformed_unknown_stale_and_replayed_candidates_are_safe() -> None:
    unknown_candidate = _candidate()
    unknown_candidate["candidate_status"] = "mystery"
    stale_candidate = _candidate()
    stale_candidate["freshness"] = "stale"
    replayed_candidate = _candidate()
    replayed_candidate["replay_status"] = "replayed"
    unknown = validate_candidate(unknown_candidate)
    stale = validate_candidate(stale_candidate)
    replayed = validate_candidate(replayed_candidate)
    malformed = validate_candidate({"candidate_id": "incomplete"})
    assert unknown["candidate_status"] == "blocked"
    assert unknown["execution_allowed"] is False
    assert unknown["side_effects_allowed"] is False
    assert unknown["approved"] is False
    for result in (stale, replayed, malformed):
        assert result["validation_state"] == "invalid"
        assert result["candidate_status"] == "blocked"
        assert result["execution_allowed"] is False
        assert result["side_effects_allowed"] is False
        assert result["approved"] is False


def test_phase_document_archives_phase_eleven_and_gates_phase_twelve() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "archives Phase 11 as a completed narrow runtime slice" in phase_doc
    assert "Approved Runtime Files Touched" in phase_doc
    assert "`lima/kernel/candidate_status.py`" in phase_doc
    assert "`lima/kernel/__init__.py`" in phase_doc
    assert "Phase 12 remains gated and requires explicit Phil approval" in phase_doc
    assert "The repo should stop here before Phase 12" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified_by_phase_11_5"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed_by_phase_11_5"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["files_outside_phase_10_2_runtime_list_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_behavior_changed"] is False
    assert boundary["guardiandecision_runtime_behavior_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_eleven_five_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_11_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_11_5*"))


def test_candidate_status_module_has_no_forbidden_imports_or_side_effect_words() -> None:
    import lima.kernel.candidate_status as candidate_status

    source = inspect.getsource(candidate_status)
    forbidden_terms = [
        "subprocess",
        "requests",
        "urllib",
        "socket",
        "threading",
        "multiprocessing",
        "Sparkbot",
        "IntentCompiler",
        "GuardianDecision",
        "dispatch(",
        "execute(",
    ]
    for term in forbidden_terms:
        assert term not in source
