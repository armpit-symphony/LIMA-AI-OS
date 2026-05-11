"""Non-runtime checks for Phase 3.5 human-safety doctrine metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
HUMAN_SAFETY_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "safety" / "human_safety_doctrine.json"
)

REQUIRED_DOCTRINE = {
    "human_safety_first",
    "authorized_human_intent_second",
    "runtime_preservation_third",
    "accountability_always",
    "least_dangerous_adequate_path",
}

REQUIRED_LIMITATIONS = {
    "not_executable_policy",
    "not_guardian_enforcement",
    "not_robot_safety_certification",
    "not_physical_world_authorization",
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
ROBOT_CONTROL_OR_ENFORCEMENT_RE = re.compile(
    r"\b(robot command|robot control implementation|runtime enforcement implementation|physical-world authorization granted)\b",
    re.IGNORECASE,
)


def _load_human_safety() -> dict[str, Any]:
    assert HUMAN_SAFETY_PATH.exists()
    with HUMAN_SAFETY_PATH.open(encoding="utf-8") as fixture_file:
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


def test_human_safety_fixture_exists_and_is_valid_json() -> None:
    assert _load_human_safety()


def test_human_safety_phase_and_status_are_non_runtime() -> None:
    metadata = _load_human_safety()
    assert metadata["phase"] == "3.5"
    assert metadata["status"] == "non_runtime_human_safety_doctrine"
    assert metadata["non_runtime"] is True


def test_three_laws_are_inspiration_only() -> None:
    inspiration = set(_load_human_safety()["inspiration"])
    assert "three_laws_reference" in inspiration


def test_lima_doctrine_priorities_are_present() -> None:
    doctrine = set(_load_human_safety()["lima_doctrine"])
    assert REQUIRED_DOCTRINE <= doctrine


def test_human_safety_limitations_block_execution_enforcement_and_authorization() -> None:
    limitations = set(_load_human_safety()["limitations"])
    assert REQUIRED_LIMITATIONS <= limitations
    assert "not_deterministic_driver_safety" in limitations
    assert "not_emergency_stop_system" in limitations
    assert "not_formal_safety_standard" in limitations


def test_physical_world_action_remains_blocked() -> None:
    metadata = _load_human_safety()
    assert metadata["physical_world_status"] == "blocked_until_later_explicit_phases"


def test_doctrine_language_does_not_imply_robot_control_or_runtime_enforcement() -> None:
    for string_value in _all_strings(_load_human_safety()):
        assert not ROBOT_CONTROL_OR_ENFORCEMENT_RE.search(string_value), string_value


def test_human_safety_fixture_has_no_commands_secrets_hosts_or_private_data() -> None:
    for string_value in _all_strings(_load_human_safety()):
        assert not SECRET_OR_PRIVATE_RE.search(string_value), string_value
        assert not HOST_OR_URL_RE.search(string_value), string_value
        assert not COMMAND_OR_RUNTIME_RE.search(string_value), string_value


def test_no_lima_robot_control_or_safety_runtime_modules_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "robot_control.py",
        REPO_ROOT / "lima" / "human_safety.py",
        REPO_ROOT / "lima" / "io" / "robo" / "driver.py",
        REPO_ROOT / "lima" / "guardian" / "safety_enforcement.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
