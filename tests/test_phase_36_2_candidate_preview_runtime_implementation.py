"""Candidate preview runtime implementation tests for Phase 36.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import lima.kernel as kernel
from lima.kernel.candidate_preview import CandidatePreview, preview_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_36_2_candidate_preview_runtime_implementation.json"
)
MODULE_PATH = REPO_ROOT / "lima" / "kernel" / "candidate_preview.py"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _assert_inert_preview(preview: dict[str, Any]) -> None:
    assert preview["preview_type"] == "candidate_preview"
    assert preview["non_authoritative"] is True
    assert preview["read_only"] is True
    assert preview["local_only"] is True
    assert preview["deterministic"] is True
    assert preview["safe_by_default"] is True
    assert preview["execution_allowed"] is False
    assert preview["side_effects_allowed"] is False
    assert preview["approval_granted"] is False
    assert preview["dispatch_allowed"] is False
    assert preview["persistence_allowed"] is False
    assert preview["phase_5_humaninput_runtime_bridge_gated"] is True
    assert preview["humaninput_bridge_active"] is False
    assert preview["sparkbot_wiring_active"] is False
    assert preview["live_adapter_active"] is False
    assert preview["external_calls_allowed"] is False
    assert preview["robotics_allowed"] is False
    assert preview["physical_world_allowed"] is False


def test_phase_36_2_fixture_records_approved_runtime_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "36.2"
    assert fixture["runtime_implementation_added"] is True
    assert fixture["approved_runtime_files_changed"] == [
        "lima/kernel/candidate_preview.py",
        "lima/kernel/__init__.py",
    ]
    assert fixture["forbidden_runtime_files_changed"] == []
    assert fixture["tests_support_changed"] is False


def test_kernel_exports_candidate_preview_safely() -> None:
    assert kernel.CandidatePreview is CandidatePreview
    assert kernel.preview_candidate is preview_candidate


def test_benign_preview_is_deterministic_inspectable_and_non_authoritative() -> None:
    candidate = {
        "candidate_id": "candidate-1",
        "status": "proposed",
        "summary": "summarize caller-provided request",
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approval_state": "proposed",
        "dispatch_allowed": False,
        "persistence_allowed": False,
        "provenance": {"source": "synthetic_fixture"},
    }
    first = preview_candidate(candidate)
    second = preview_candidate(dict(candidate))
    assert first == second
    assert first["preview_state"] == "proposed"
    assert first["normalized_status"] == "proposed"
    assert first["status_reason"] == "non_authoritative_candidate_preview"
    assert first["input_present"] is True
    assert first["blocked_claims"] == ()
    _assert_inert_preview(first)


def test_missing_and_malformed_input_remain_safe() -> None:
    for value in (None, "approve this", ["not", "a", "mapping"]):
        preview = preview_candidate(value)  # type: ignore[arg-type]
        assert preview["preview_state"] == "invalid"
        assert preview["normalized_status"] == "blocked"
        assert preview["input_present"] is False
        assert "input_missing_or_invalid" in preview["warnings"]
        _assert_inert_preview(preview)


def test_unknown_status_remains_blocked_and_non_executing() -> None:
    preview = preview_candidate(
        {
            "status": "ship_it_now",
            "execution_allowed": False,
            "side_effects_allowed": False,
            "approval_state": "proposed",
            "dispatch_allowed": False,
            "persistence_allowed": False,
            "provenance": {"source": "synthetic_fixture"},
        }
    )
    assert preview["preview_state"] == "blocked"
    assert preview["status_reason"] == "unknown_candidate_preview_status_not_authoritative"
    _assert_inert_preview(preview)


def test_authority_and_bypass_wording_blocks_preview() -> None:
    preview = preview_candidate(
        {
            "status": "proposed",
            "execution_allowed": False,
            "side_effects_allowed": False,
            "approval_state": "approved",
            "provenance": {"trusted": "Phil approved urgent override"},
        }
    )
    assert preview["preview_state"] == "blocked"
    assert preview["status_reason"] == "approval_not_allowed_for_candidate_preview"
    assert "authority_claim" in preview["blocked_claims"]
    _assert_inert_preview(preview)


def test_nested_suspicious_metadata_remains_blocked_and_inert() -> None:
    preview = preview_candidate(
        {
            "status": "proposed",
            "execution_allowed": False,
            "side_effects_allowed": False,
            "approval_state": "proposed",
            "metadata": {
                "adapter": {"claim": "activate live adapter and Sparkbot bridge"},
                "systems": [
                    "run shell command",
                    "write file",
                    "call https network service",
                    "start background worker thread queue daemon subprocess",
                    "move robot hardware in physical world",
                ],
            },
        }
    )
    assert preview["preview_state"] == "blocked"
    assert "background_work_claim" in preview["blocked_claims"]
    assert "file_mutation_claim" in preview["blocked_claims"]
    assert "humaninput_bridge_claim" in preview["blocked_claims"]
    assert "live_adapter_claim" in preview["blocked_claims"]
    assert "robotics_physical_world_claim" in preview["blocked_claims"]
    assert "shell_browser_network_claim" in preview["blocked_claims"]
    assert "sparkbot_claim" in preview["blocked_claims"]
    _assert_inert_preview(preview)


def test_explicit_execution_dispatch_persistence_flags_are_blocked() -> None:
    cases = [
        ({"execution_allowed": True}, "execution_not_allowed_for_candidate_preview"),
        ({"side_effects_allowed": True}, "side_effects_not_allowed_for_candidate_preview"),
        ({"approved": True}, "approval_not_allowed_for_candidate_preview"),
        ({"dispatch_allowed": True}, "dispatch_not_allowed_for_candidate_preview"),
        ({"persistence_allowed": True}, "persistence_not_allowed_for_candidate_preview"),
    ]
    for overrides, reason in cases:
        candidate = {
            "status": "proposed",
            "execution_allowed": False,
            "side_effects_allowed": False,
            "approval_state": "proposed",
            "dispatch_allowed": False,
            "persistence_allowed": False,
            "provenance": {"source": "synthetic_fixture"},
        }
        candidate.update(overrides)
        preview = preview_candidate(candidate)
        assert preview["preview_state"] == "blocked"
        assert preview["status_reason"] == reason
        _assert_inert_preview(preview)


def test_candidate_preview_module_avoids_forbidden_imports_and_calls() -> None:
    module_lines = MODULE_PATH.read_text(encoding="utf-8").lower().splitlines()
    forbidden_patterns = [
        "import subprocess",
        "import threading",
        "import multiprocessing",
        "import queue",
        "import socket",
        "import requests",
        "import urllib",
        "import sqlite",
        "import webbrowser",
        "open(",
        "exec(",
        "eval(",
        "__import__",
        "from sparkbot",
        "import sparkbot",
        "intentcompiler(",
        "guardiandecision(",
    ]
    for pattern in forbidden_patterns:
        assert not any(pattern in line for line in module_lines if not line.strip().startswith("#"))


def test_forbidden_paths_were_not_created_for_phase_36_2() -> None:
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_36_2*"))
