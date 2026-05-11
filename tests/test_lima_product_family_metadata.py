"""Non-runtime checks for Phase 3.5 LIMA product-family metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_FAMILY_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "product_family" / "lima_product_family.json"
)
RELATIONSHIP_METADATA_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "kernel_pipeline" / "pipeline_relationships.json"
)
READINESS_METADATA_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "kernel_pipeline"
    / "relationship_metadata_readiness_review.json"
)

REQUIRED_PRODUCTS = {
    "lima_ai_os",
    "sparkbot",
    "arc_bot",
    "custom_business_bots",
    "robo_automation_consumers",
}

REQUIRED_PRODUCT_FIELDS = {
    "role",
    "current_status",
    "future_status",
    "implementation_status",
    "non_runtime",
    "not_implemented_in_phase",
    "blocked_runtime_implications",
}

SECRET_OR_PRIVATE_RE = re.compile(
    r"(api[_-]?key|password|credential|private[_-]?key|bearer\s+[a-z0-9._-]+|token=|secret=)",
    re.IGNORECASE,
)
HOST_OR_URL_RE = re.compile(
    r"(https?://|www\.|\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|dev|cloud|local)\b)",
    re.IGNORECASE,
)
COMMAND_OR_CONFIG_RE = re.compile(
    r"(^|\s)(python|python3|git|curl|wget|powershell|cmd|bash|sh|npm|uv|pytest)\s+|runtime[_ -]?config|model prompt|tool call|shell script",
    re.IGNORECASE,
)


def _load_product_family() -> dict[str, Any]:
    assert PRODUCT_FAMILY_PATH.exists()
    with PRODUCT_FAMILY_PATH.open(encoding="utf-8") as fixture_file:
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


def test_product_family_fixture_exists_and_is_valid_json() -> None:
    metadata = _load_product_family()
    assert metadata


def test_product_family_phase_and_status_are_non_runtime() -> None:
    metadata = _load_product_family()
    assert metadata["phase"] == "3.5"
    assert metadata["status"] == "non_runtime_product_family_doctrine"
    assert metadata["non_runtime"] is True


def test_required_product_family_members_are_present() -> None:
    products = _load_product_family()["products"]
    assert REQUIRED_PRODUCTS <= set(products)


def test_every_product_family_item_is_non_runtime_and_not_implemented() -> None:
    products = _load_product_family()["products"]
    for product in products.values():
        assert REQUIRED_PRODUCT_FIELDS <= set(product)
        assert product["non_runtime"] is True
        assert product["not_implemented_in_phase"] is True
        assert product["blocked_runtime_implications"]


def test_sparkbot_is_reference_shell_only_not_runtime_dependency() -> None:
    sparkbot = _load_product_family()["products"]["sparkbot"]
    sparkbot_text = " ".join(_all_strings(sparkbot)).lower()
    assert "open-source" in sparkbot_text
    assert "r&d" in sparkbot_text
    assert "reference" in sparkbot_text
    assert "not imported or wired" in sparkbot_text
    assert "runtime dependency" in sparkbot["blocked_runtime_implications"]


def test_arc_bot_and_custom_business_bots_are_future_shell_doctrine_only() -> None:
    products = _load_product_family()["products"]
    arc_text = " ".join(_all_strings(products["arc_bot"])).lower()
    custom_text = " ".join(_all_strings(products["custom_business_bots"])).lower()
    assert "future commercial office-worker shell" in arc_text
    assert "not implemented" in arc_text
    assert "future client-specific shells" in custom_text
    assert "not generated or implemented" in custom_text


def test_robo_automation_consumers_are_future_driver_plane_only() -> None:
    robo = _load_product_family()["products"]["robo_automation_consumers"]
    robo_text = " ".join(_all_strings(robo)).lower()
    assert "future deterministic driver-plane consumers" in robo_text
    assert "not implemented" in robo_text
    assert "robot control" in robo["blocked_runtime_implications"]
    assert "physical-world action" in robo["blocked_runtime_implications"]


def test_product_family_fixture_has_no_commands_secrets_hosts_or_private_data() -> None:
    for string_value in _all_strings(_load_product_family()):
        assert not SECRET_OR_PRIVATE_RE.search(string_value), string_value
        assert not HOST_OR_URL_RE.search(string_value), string_value
        assert not COMMAND_OR_CONFIG_RE.search(string_value), string_value


def test_no_lima_runtime_product_family_modules_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "product_family.py",
        REPO_ROOT / "lima" / "adaptive_trust.py",
        REPO_ROOT / "lima" / "arc_bot.py",
        REPO_ROOT / "lima" / "robot_control.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)


def test_existing_phase_three_three_and_three_four_metadata_remains_non_runtime() -> None:
    with RELATIONSHIP_METADATA_PATH.open(encoding="utf-8") as metadata_file:
        relationships = json.load(metadata_file)
    with READINESS_METADATA_PATH.open(encoding="utf-8") as readiness_file:
        readiness = json.load(readiness_file)
    assert len(relationships) == 60
    assert all(relationship["non_runtime"] is True for relationship in relationships)
    assert readiness["status"] == "non_runtime_readiness_review"
