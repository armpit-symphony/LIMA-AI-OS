"""Static and behavior checks for Phase 4.14 test-only HumanInput harness."""

from __future__ import annotations

import ast
import copy
import json
from pathlib import Path
from typing import Any

import pytest

from tests.support.test_only_humaninput_adapter_harness import (
    HumanInputHarnessRejection,
    convert_synthetic_fixture_to_humaninput_shape,
    run_test_only_humaninput_harness,
    validate_humaninput_shape,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_14_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_IMPLEMENTATION.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_14_test_only_humaninput_adapter_harness.json"
)
HUMANINPUT_FIXTURE_CONTRACT_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_4_humaninput_intake_fixture_contract.json"
)
HARNESS_PATH = REPO_ROOT / "tests" / "support" / "test_only_humaninput_adapter_harness.py"

FORBIDDEN_IMPORT_ROOTS = {
    "lima",
    "sparkbot",
    "requests",
    "urllib",
    "http",
    "socket",
    "subprocess",
    "asyncio",
    "websocket",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _phase_four_four_records() -> list[dict[str, Any]]:
    fixture = _load_json(HUMANINPUT_FIXTURE_CONTRACT_PATH)
    records = fixture["fixture_records"]
    assert isinstance(records, list)
    return records


def _mutated_record(field_path: tuple[str, ...], value: Any) -> dict[str, Any]:
    record = copy.deepcopy(_phase_four_four_records()[0])
    target = record
    for field in field_path[:-1]:
        target = target[field]
    target[field_path[-1]] = value
    return record


def test_phase_fixture_declares_test_only_non_runtime_harness() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "4.14"
    assert fixture["status"] == "test_only_humaninput_adapter_harness_implementation"
    assert fixture["test_only"] is True
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["implementation_is"]["test_only_helper_under_tests"] is True


def test_docs_and_harness_files_exist_under_allowed_paths() -> None:
    assert PHASE_DOC_PATH.exists()
    assert HARNESS_PATH.exists()
    assert "tests/support" in HARNESS_PATH.as_posix()
    assert not (REPO_ROOT / "lima" / "test_only_humaninput_adapter_harness.py").exists()


def test_harness_uses_only_allowed_imports_and_no_runtime_or_sparkbot_imports() -> None:
    tree = ast.parse(HARNESS_PATH.read_text(encoding="utf-8"))
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_roots.add(alias.name.split(".")[0].lower())
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0].lower())
    assert not (FORBIDDEN_IMPORT_ROOTS & imported_roots)


def test_harness_converts_phase_four_four_synthetic_fixtures_to_humaninput_shapes() -> None:
    report = run_test_only_humaninput_harness(_phase_four_four_records())
    assert report.total == 2
    assert report.converted == 2
    assert report.rejected == 0
    assert report.metadata["test_only"] is True
    assert report.metadata["non_runtime"] is True
    for result in report.results:
        assert result.status == "converted_test_only"
        assert result.humaninput_shape is not None
        assert not validate_humaninput_shape(result.humaninput_shape)


def test_generated_shape_is_humaninput_only_and_not_authority_or_execution() -> None:
    shape = convert_synthetic_fixture_to_humaninput_shape(_phase_four_four_records()[0])
    assert shape["input_id"].startswith("test-only:")
    assert shape["synthetic"] is True
    assert shape["test_only"] is True
    assert shape["non_runtime"] is True
    assert "intent_envelope" not in shape
    assert "guardian_decision" not in shape
    metadata = shape["harness_metadata"]
    assert metadata["not_authorization"] is True
    assert metadata["no_intentenvelope"] is True
    assert metadata["no_guardiandecision"] is True
    assert metadata["no_approval"] is True
    assert metadata["no_enforcement"] is True
    assert metadata["no_execution"] is True
    assert metadata["no_audit_persistence"] is True


def test_voice_fixture_preserves_transcript_confidence_as_metadata_only() -> None:
    voice_record = _phase_four_four_records()[1]
    shape = convert_synthetic_fixture_to_humaninput_shape(voice_record)
    assert shape["input_kind"] == "voice_transcript"
    assert shape["voice"]["transcript_confidence"] == 0.92
    assert shape["voice"]["raw_audio_included"] is False
    assert shape["harness_metadata"]["humaninput_shape_only"] is True


@pytest.mark.parametrize(
    ("field_path", "value", "expected_reason"),
    [
        (("synthetic",), False, "synthetic marker must be true"),
        (("non_runtime",), False, "non_runtime marker must be true"),
        (("source", "live_route"), True, "source.live_route must be false"),
        (("source", "sparkbot_wired"), True, "source.sparkbot_wired must be false"),
        (("actor", "live_lookup_performed"), True, "actor.live_lookup_performed must be false"),
        (("session", "live_session"), True, "session.live_session must be false"),
        (
            ("session", "auth_lookup_performed"),
            True,
            "session.auth_lookup_performed must be false",
        ),
        (
            ("session", "trust_lookup_performed"),
            True,
            "session.trust_lookup_performed must be false",
        ),
        (("trust_context", "grants_trust"), True, "trust_context.grants_trust must be false"),
        (("lineage", "audit_persisted"), True, "lineage.audit_persisted must be false"),
        (("handoff", "authorizes_action"), True, "handoff.authorizes_action must be false"),
        (("handoff", "approves_action"), True, "handoff.approves_action must be false"),
        (("handoff", "executes_action"), True, "handoff.executes_action must be false"),
        (
            ("capability_flags", "can_call_model"),
            True,
            "capability_flags.can_call_model must be false",
        ),
        (
            ("capability_flags", "can_execute_tools"),
            True,
            "capability_flags.can_execute_tools must be false",
        ),
        (
            ("capability_flags", "can_import_sparkbot"),
            True,
            "capability_flags.can_import_sparkbot must be false",
        ),
    ],
)
def test_harness_fails_closed_on_live_runtime_or_authority_markers(
    field_path: tuple[str, ...], value: Any, expected_reason: str
) -> None:
    with pytest.raises(HumanInputHarnessRejection) as exc_info:
        convert_synthetic_fixture_to_humaninput_shape(_mutated_record(field_path, value))
    assert expected_reason in str(exc_info.value)


def test_harness_rejects_intentenvelope_and_guardiandecision_indicators() -> None:
    record = copy.deepcopy(_phase_four_four_records()[0])
    record["intent_envelope"] = {"intent_id": "forbidden"}
    record["guardian_decision"] = {"decision_id": "forbidden"}
    with pytest.raises(HumanInputHarnessRejection) as exc_info:
        convert_synthetic_fixture_to_humaninput_shape(record)
    assert "forbidden keys present" in str(exc_info.value)


def test_phase_fixture_boundary_results_keep_runtime_and_blocked_behavior_closed() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["test_only_adapter_harness_added_under_tests"] is True
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_phase_fixture_ready_for_only_readiness_review_or_further_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert set(fixture["ready_for"]) == {
        "phase_4_15_test_only_humaninput_adapter_harness_implementation_readiness_review",
        "further_non_runtime_review",
    }
    assert "live_adapter_code" in fixture["not_ready_for"]
    assert "runtime_wiring" in fixture["not_ready_for"]
    assert "production_sparkbot_integration" in fixture["not_ready_for"]


def test_no_files_under_lima_were_modified_for_phase_fourteen() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "adapters" / "humaninput_adapter.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "tests" / "helpers" / "test_only_humaninput_adapter_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
