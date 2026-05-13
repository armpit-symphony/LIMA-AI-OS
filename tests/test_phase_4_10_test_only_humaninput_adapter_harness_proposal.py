"""Static checks for Phase 4.10 test-only HumanInput adapter harness proposal."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_10_NONPRODUCTION_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_PROPOSAL.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_10_test_only_humaninput_adapter_harness_proposal.json"
)
PHASE_4_9_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_9_humaninput_adapter_implementation_readiness_review.json"
)

REQUIRED_SYNTHETIC_INPUTS = {
    "synthetic_text_intake_metadata",
    "synthetic_voice_transcript_metadata",
    "shell_ref",
    "channel_ref",
    "room_ref",
    "actor_ref",
    "session_ref",
    "passive_trust_context_ref",
    "owner_autonomy_ref",
    "redacted_content_ref_or_summary",
    "transcript_confidence_for_voice",
    "privacy_redaction_retention_visibility_hints",
    "lineage_seed_ref",
}

REQUIRED_HUMANINPUT_SHAPE = {
    "fixture_id",
    "boundary_id",
    "input_kind",
    "synthetic",
    "non_runtime",
    "content",
    "source",
    "actor",
    "session",
    "trust_context",
    "privacy",
    "lineage",
    "handoff",
    "capability_flags",
    "blocked_capabilities",
}

REQUIRED_NOT_READY = {
    "test_only_adapter_harness_code",
    "live_adapter_code",
    "runtime_wiring",
    "production_sparkbot_integration",
    "sparkbot_import_or_wiring",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval",
    "approval_enforcement",
    "policy_enforcement",
    "execution",
    "audit_persistence",
    "model_calls",
    "tool_execution",
    "terminal_pty_behavior",
    "robotics_behavior",
    "physical_world_action",
    "live_auth_session_trust_lookup",
    "production_shell_implementation",
}

FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE = re.compile(
    r"("
    r"api[_-]?key|password|credential|private[_-]?key|bearer\s+[a-z0-9._-]+|"
    r"secret=|token=|approval[_ -]?token|"
    r"https?://|www\.|\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|dev|cloud|local)\b|"
    r"runtime[_ -]?config|deploy[_ -]?config|model prompt|tool call|"
    r"\b(?:python|python3|git|curl|wget|powershell|cmd|bash|sh|npm|uv|pytest)\s+"
    r")",
    re.IGNORECASE,
)


def _load_json(path: Path) -> dict[str, Any]:
    assert path.exists()
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _load_fixture() -> dict[str, Any]:
    return _load_json(FIXTURE_PATH)


def _all_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, list):
        for item in value:
            strings.extend(_all_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            strings.extend(_all_strings(item))
    return strings


def test_fixture_is_valid_phase_four_ten_non_runtime_proposal() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.10"
    assert fixture["status"] == "non_runtime_test_only_humaninput_adapter_harness_proposal"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_document_exists_and_states_proposal_is_not_harness_code() -> None:
    assert DOC_PATH.exists()
    doc = DOC_PATH.read_text(encoding="utf-8")
    assert "proposal metadata only" in doc
    assert "not harness code" in doc
    assert "NO-GO for test-only harness implementation" in doc


def test_phase_four_nine_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.9"
    assert fixture["source_tag"] == "phase-4.9-humaninput-adapter-implementation-readiness-review"
    assert fixture["source_merge_commit"] == "a9d18fa8788fb70a0ed0cf131a972e6eb37206a1"


def test_proposal_is_metadata_only_and_not_runtime_or_harness_code() -> None:
    fixture = _load_fixture()
    assert fixture["key_rule"] == "test_only_harness_proposal_is_not_test_only_harness_implementation"
    assert all(fixture["proposal_is"].values())
    assert all(fixture["proposal_is_not"].values())


def test_expected_inputs_and_output_shape_are_synthetic_humaninput_only() -> None:
    fixture = _load_fixture()
    assert REQUIRED_SYNTHETIC_INPUTS <= set(fixture["expected_synthetic_inputs"])
    assert REQUIRED_HUMANINPUT_SHAPE <= set(fixture["expected_humaninput_output_shape"])


def test_future_harness_must_not_create_runtime_or_authority_objects() -> None:
    blocked = set(_load_fixture()["future_harness_must_not_create"])
    assert "intentenvelope" in blocked
    assert "guardiandecision" in blocked
    assert "approvalmetadata" in blocked
    assert "execution_record" in blocked
    assert "audit_record" in blocked
    assert "runtime_object" in blocked


def test_safety_boundaries_block_harness_live_adapter_and_runtime_paths() -> None:
    boundaries = set(_load_fixture()["safety_boundaries"])
    assert "no_harness_code" in boundaries
    assert "no_live_adapter_code" in boundaries
    assert "no_files_under_lima" in boundaries
    assert "no_sparkbot_imports_or_wiring" in boundaries
    assert "no_runtime_behavior" in boundaries
    assert "no_real_intentcompiler" in boundaries
    assert "no_real_guardiandecision" in boundaries
    assert "no_approval_enforcement" in boundaries
    assert "no_execution" in boundaries
    assert "no_audit_persistence" in boundaries


def test_future_validation_requirements_keep_harness_test_only() -> None:
    requirements = _load_fixture()["future_validation_requirements"]
    assert all(requirements.values())
    assert requirements["harness_validates_humaninput_shape_only"] is True
    assert requirements["no_runtime_adapter_behavior"] is True
    assert requirements["does_not_imply_production_adapter_readiness"] is True


def test_phase_four_nine_readiness_continuity_remains_non_runtime() -> None:
    continuity = _load_fixture()["phase_4_9_readiness_continuity"]
    phase_4_9 = _load_json(PHASE_4_9_FIXTURE_PATH)
    assert continuity["remains_non_runtime"] is True
    assert continuity["ready_only_for_future_explicit_test_only_harness_proposal"] is True
    assert phase_4_9["non_runtime"] is True
    assert phase_4_9["decision"][
        "conditional_go_for_future_explicitly_approved_test_only_adapter_harness_proposal_docs_tests_fixtures_only"
    ] is True


def test_ready_for_is_limited_to_phase_four_eleven_readiness_review() -> None:
    assert set(_load_fixture()["ready_for"]) == {
        "phase_4_11_test_only_humaninput_adapter_harness_proposal_readiness_review",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_implementation_runtime_and_authority_paths() -> None:
    assert REQUIRED_NOT_READY <= set(_load_fixture()["not_ready_for"])


def test_boundary_results_show_no_behavior_lima_files_harness_or_live_integration() -> None:
    boundary = _load_fixture()["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["test_only_adapter_harness_added"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_four_ten_runtime_modules_live_adapters_or_harness_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_runtime.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "tests" / "helpers" / "runtime_extraction_harness.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_adapter_harness.py",
        REPO_ROOT / "tests" / "helpers" / "test_only_humaninput_adapter_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
