"""Phase 38.0 Sparkbot alignment audit charter tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_38_0_PHASE_37_SPARKBOT_ALIGNMENT_AUDIT_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_38_0_phase_37_sparkbot_alignment_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_38_0_records_starting_lima_audit_pass() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "38.0"
    assert fixture["starting_lima_audit_result"] == "PASS"
    assert fixture["lima_checkpoint_commit"] == "99055495ef593b5c50f99f0a76b958b3459da3f3"
    assert len(fixture["phase_37_tags_verified"]) == 5
    assert "Phase 37 audit result: PASS." in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_38_0_records_read_only_sparkbot_sources() -> None:
    source = _load_json(PHASE_FIXTURE_PATH)["sparkbot_source_access"]
    assert source["source"] == "local_read_only_repository"
    assert source["current_tag"] == "desktop-v1.6.80"
    assert source["current_commit"] == "3449187"
    assert source["baseline_v1_6_42_commit"] == "a7a1433"
    assert source["modified_by_phase_38"] is False


def test_phase_38_0_selects_required_sparkbot_documents() -> None:
    sources = set(_load_json(PHASE_FIXTURE_PATH)["sparkbot_sources_selected"])
    assert "README.md" in sources
    assert "SECURITY.md" in sources
    assert "docs/capabilities.md" in sources
    assert "docs/lima-robo-os-integration.md" in sources
    assert "docs/guardian-spine.md" in sources
    assert "docs/release-notes/v1.6.42.txt" in sources
    assert "docs/release-notes/v1.6.80.txt" in sources


def test_phase_38_0_keeps_boundaries_closed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["phase_5_runtime_bridge_gated"] is True
    assert fixture["forbidden_behavior_added"] is False


def test_no_phase_38_0_files_exist_under_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_38_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_38_0*"))
