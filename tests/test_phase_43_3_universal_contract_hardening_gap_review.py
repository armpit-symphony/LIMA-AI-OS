"""Phase 43.3 universal contract hardening gap review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_43_3_universal_contract_hardening_gap_review.json"
)
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_43_3_UNIVERSAL_CONTRACT_HARDENING_GAP_REVIEW.md"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_43_3_reviews_phase_43_evidence() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "43.3"
    assert fixture["evidence_reviewed"] == [
        "phase_43_0_charter",
        "phase_43_1_fixture_corpus",
        "phase_43_2_regression_tests",
    ]
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["test_only_hardening"] is True


def test_phase_43_3_records_safe_hardening_findings() -> None:
    findings = _load_json(PHASE_FIXTURE_PATH)["findings"]
    assert findings["universal_consumer_profiles_inert"] is True
    assert findings["risky_action_profiles_blocked"] is True
    assert findings["physical_world_profiles_blocked"] is True
    assert findings["adversarial_profiles_blocked"] is True
    assert findings["safe_planning_profiles_may_be_conservatively_blocked"] is True
    assert findings["conservative_blocking_accepted"] is True
    assert findings["preview_outputs_preserve_inert_flags"] is True
    assert findings["approval_execution_dispatch_persistence_not_granted"] is True
    assert findings["adapter_robotics_physical_world_paths_inactive"] is True


def test_phase_43_3_finds_no_runtime_gap() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == []
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert "No concrete runtime gap was found." in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_43_3_recommends_archive_not_runtime() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_43_4_recommended"] is True
    assert fixture["phase_43_4_lane"] == "docs_tests_fixtures_only_archive_closeout"
    assert fixture["next_runtime_implementation_recommended"] is False


def test_phase_43_3_stays_in_approved_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_43_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_43_3*"))
