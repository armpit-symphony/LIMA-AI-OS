from __future__ import annotations

from pathlib import Path
import tomllib

import lima
from lima.release import (
    BLOCKED_CAPABILITIES,
    MAIN_BASE_SHA,
    PACKAGED_NAMESPACES,
    RECOVERY_LINEAGE,
    SUPPORTED_ENTRYPOINTS,
    get_release_candidate_manifest,
)
from lima.runtime import run_governed_request


ROOT = Path(__file__).resolve().parents[1]


def _request(*, consumer: str, category: str, tool_name: str | None) -> dict[str, object]:
    return {
        "request_id": f"{consumer}-{category}-rc-test",
        "consumer": consumer,
        "surface": "release_candidate_test",
        "actor_id": "test-actor",
        "normalized_request": {"intent": category},
        "requested_action": category,
        "action_category": category,
        "tool_name": tool_name,
    }


def test_package_metadata_is_dependency_free_v0_1_prerelease() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["name"] == "lima-runtime"
    assert pyproject["project"]["version"] == "0.1.0rc1"
    assert pyproject["project"]["dependencies"] == []
    assert pyproject["tool"]["setuptools"]["packages"] == [
        "lima",
        "lima.contracts",
        "lima.governed_kernel",
    ]
    assert lima.__version__ == "0.1.0rc1"


def test_release_manifest_consolidates_recovery_lineage_on_current_main() -> None:
    manifest = get_release_candidate_manifest()

    assert MAIN_BASE_SHA == "deea1c4f5b6d3455a7e97e4b621e22b8d22a6244"
    assert manifest["main_base_sha"] == MAIN_BASE_SHA
    assert [checkpoint.commit for checkpoint in RECOVERY_LINEAGE] == [
        "702b0554203f83002815362c7fce783e18ddbf03",
        "17fab7cbf8befa846444437fd1108847c42ff9c0",
        "cbddc3c763565c6958d46711abc6195a792a2868",
        "04eb204a710c4e8f5f15759fbbe31e831a9a6029",
    ]
    assert SUPPORTED_ENTRYPOINTS == ("lima.runtime.run_governed_request",)
    assert manifest["supported_consumers"] == ["sparkbot", "arc-bot"]
    assert manifest["packaged_namespaces"] == list(PACKAGED_NAMESPACES)
    assert manifest["guardian_core_required"] is False
    assert manifest["execution_allowed"] is False
    assert manifest["side_effects_allowed"] is False
    assert manifest["production_ready"] is False


def test_sparkbot_and_arc_preview_decisions_cannot_execute() -> None:
    requests = (
        _request(
            consumer="sparkbot",
            category="preview",
            tool_name="sparkbot_decision_preview",
        ),
        _request(
            consumer="arc-bot",
            category="status",
            tool_name="arc_status_preview",
        ),
    )

    for request in requests:
        decision = run_governed_request(request)
        assert decision.status == "allowed_dry_run"
        assert decision.executable is False
        assert decision.execution_allowed is False
        assert decision.side_effects_allowed is False
        assert decision.audit_event.execution_allowed is False
        assert decision.audit_event.side_effects_allowed is False


def test_execution_provider_tool_connector_and_robotics_categories_fail_closed() -> None:
    categories = (
        "execute",
        "provider_call",
        "model_call",
        "tool_execution",
        "connector_call",
        "browser_network",
        "physical_world",
    )

    for category in categories:
        decision = run_governed_request(
            _request(consumer="consumer-test", category=category, tool_name=None)
        )
        assert decision.status == "denied"
        assert decision.allowed is False
        assert decision.requires_approval is False
        assert decision.execution_allowed is False
        assert decision.side_effects_allowed is False

    assert {
        "approval_execution",
        "provider_calls",
        "tool_calls",
        "connector_calls",
        "network_calls",
        "robotics",
        "physical_world_actions",
        "side_effects",
    }.issubset(BLOCKED_CAPABILITIES)


def test_release_documentation_preserves_candidate_only_boundary() -> None:
    release_doc = (
        ROOT / "docs" / "V0_1_GOVERNED_KERNEL_RELEASE_CANDIDATE.md"
    ).read_text(encoding="utf-8")
    current_state = (ROOT / "docs" / "CURRENT_PROJECT_STATE.md").read_text(
        encoding="utf-8"
    )

    assert "0.1.0rc1" in release_doc
    assert "Do not tag" in release_doc
    assert "does not authorize the V1.0.0 cutover" in current_state
    assert "lima.runtime.run_governed_request" in release_doc
