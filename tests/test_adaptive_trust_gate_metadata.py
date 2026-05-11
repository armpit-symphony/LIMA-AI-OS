"""Non-runtime checks for Phase 3.5 adaptive trust gate metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
ADAPTIVE_TRUST_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "safety" / "adaptive_trust_gates.json"
)

REQUIRED_GATE_CATEGORIES = {
    "silent_or_logged",
    "normal_confirmation",
    "screen_confirmation",
    "step_up_auth",
    "companion_device_confirmation",
    "voice_challenge_confirmation",
    "dual_control",
    "dry_run_required",
    "physical_safety_interlock_required",
    "breakglass_required",
}

REQUIRED_RISK_DIMENSIONS = {
    "reversibility",
    "data_sensitivity",
    "financial_impact",
    "security_impact",
    "operational_impact",
    "physical_world_consequence",
    "actor_trust",
    "environment_trust",
    "shell_type",
    "tool_or_driver_capability",
}

SECRET_OR_PRIVATE_RE = re.compile(
    r"(api[_-]?key|password|credential|private[_-]?key|bearer\s+[a-z0-9._-]+|token=|secret=)",
    re.IGNORECASE,
)
HOST_OR_URL_RE = re.compile(
    r"(https?://|www\.|\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|dev|cloud|local)\b)",
    re.IGNORECASE,
)
COMMAND_OR_RUNTIME_RE = re.compile(
    r"(^|\s)(python|python3|git|curl|wget|powershell|cmd|bash|sh|npm|uv|pytest)\s+|runtime[_ -]?config|model prompt|tool call|shell script",
    re.IGNORECASE,
)


def _load_adaptive_trust() -> dict[str, Any]:
    assert ADAPTIVE_TRUST_PATH.exists()
    with ADAPTIVE_TRUST_PATH.open(encoding="utf-8") as fixture_file:
        metadata = json.load(fixture_file)
    assert isinstance(metadata, dict)
    return metadata


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


def test_adaptive_trust_fixture_exists_and_is_valid_json() -> None:
    assert _load_adaptive_trust()


def test_adaptive_trust_phase_and_status_are_non_runtime() -> None:
    metadata = _load_adaptive_trust()
    assert metadata["phase"] == "3.5"
    assert metadata["status"] == "non_runtime_adaptive_trust_doctrine"
    assert metadata["non_runtime"] is True


def test_gate_categories_cover_low_friction_confirmation_step_up_and_breakglass() -> None:
    categories = set(_load_adaptive_trust()["gate_categories"])
    assert REQUIRED_GATE_CATEGORIES <= categories
    assert {"silent_or_logged", "normal_confirmation"} <= categories
    assert {"step_up_auth", "dual_control"} <= categories
    assert {"dry_run_required", "physical_safety_interlock_required"} <= categories
    assert "breakglass_required" in categories


def test_risk_dimensions_are_documented() -> None:
    dimensions = set(_load_adaptive_trust()["risk_dimensions"])
    assert REQUIRED_RISK_DIMENSIONS <= dimensions


def test_breakglass_posture_is_override_not_default_ux() -> None:
    posture = _load_adaptive_trust()["breakglass_posture"]
    assert posture["emergency_or_privileged_override"] is True
    assert posture["not_default_ux"] is True


def test_screen_voice_and_physical_world_examples_exist() -> None:
    examples = _load_adaptive_trust()["channel_examples"]
    assert set(examples) == {"screen_based", "voice_based", "physical_world"}
    assert "screen_confirmation" in examples["screen_based"]
    assert "voice_challenge_confirmation" in examples["voice_based"]
    assert "physical_safety_interlock_required" in examples["physical_world"]


def test_no_runtime_trust_gate_or_approval_engine_is_implemented() -> None:
    metadata = _load_adaptive_trust()
    not_implemented = set(metadata["not_implemented"])
    assert "trust_gate_engine" in not_implemented
    assert "approval_engine" in not_implemented
    assert "runtime_enforcement" in not_implemented
    assert "GuardianDecision behavior" in not_implemented
    assert "execution behavior" in not_implemented


def test_adaptive_trust_fixture_has_no_commands_secrets_hosts_or_private_data() -> None:
    for string_value in _all_strings(_load_adaptive_trust()):
        assert not SECRET_OR_PRIVATE_RE.search(string_value), string_value
        assert not HOST_OR_URL_RE.search(string_value), string_value
        assert not COMMAND_OR_RUNTIME_RE.search(string_value), string_value


def test_no_lima_adaptive_trust_runtime_modules_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "adaptive_trust.py",
        REPO_ROOT / "lima" / "guardian" / "adaptive_trust.py",
        REPO_ROOT / "lima" / "guardian" / "approval_engine.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
