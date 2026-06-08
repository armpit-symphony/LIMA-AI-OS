"""Tests for non-authoritative Guardian lifecycle preview behavior."""

from __future__ import annotations

import ast
from pathlib import Path

from lima.kernel import CapabilityProfile, KernelRequest, LimaKernel
from lima.kernel.guardian_lifecycle import GuardianLifecyclePreviewResult


REPO_ROOT = Path(__file__).resolve().parents[1]
LIFECYCLE_PATH = REPO_ROOT / "lima" / "kernel" / "guardian_lifecycle.py"
KERNEL_INIT_PATH = REPO_ROOT / "lima" / "kernel" / "__init__.py"


def _request(
    action_category: str,
    *,
    profile: CapabilityProfile | None = None,
    normalized_intent: dict[str, object] | None = None,
    metadata: dict[str, object] | None = None,
    source_surface: dict[str, object] | None = None,
) -> KernelRequest:
    intent = {
        "action_category": action_category,
        "risk_class": "low",
        "summary": "redacted normalized summary",
    }
    if normalized_intent:
        intent.update(normalized_intent)
    return KernelRequest(
        request_id=f"req-{action_category}",
        shell_id="test-shell",
        actor_id="actor-ref",
        session_id="session-ref",
        normalized_intent=intent,
        capability_profile=profile or CapabilityProfile(),
        source_surface=source_surface or {"surface": "unit_test", "privacy_class": "private"},
        metadata=metadata or {},
    )


def _assert_preview_invariants(result: GuardianLifecyclePreviewResult) -> None:
    assert result.dry_run is True
    assert result.executable is False
    assert result.execution_allowed is False
    assert result.side_effects_allowed is False
    assert result.dispatch_allowed is False
    assert result.persistence_allowed is False
    assert result.model_calls_allowed is False
    assert result.model_calls_executed is False
    assert result.guardian_decision_created is False
    assert result.approval_enforced is False
    assert result.approval_metadata_recorded is False
    assert result.tool_execution_allowed is False
    assert result.connector_access_allowed is False
    assert result.storage_persistence_allowed is False
    assert result.event_spine_persistence_allowed is False
    assert result.humaninput_bridge_active is False
    assert result.sparkbot_wiring_active is False
    assert result.arc_bot_wiring_active is False
    assert result.robo_os_wiring_active is False
    assert result.live_discovery_executed is False
    assert result.connection_attempted is False
    assert result.pairing_attempted is False
    assert result.credentials_used is False
    assert result.session_opened is False
    assert result.device_control_executed is False
    assert result.physical_world_allowed is False
    assert result.physical_world_executed is False
    assert result.guardian_request.decision_ref is None
    assert result.guardian_request.approval_ref is None
    assert result.guardian_request.guardian_decision_created is False
    assert result.guardian_request.approval_enforced is False
    assert result.intent_candidate.authority_created is False


def test_lima_kernel_exposes_explicit_lifecycle_preview_method() -> None:
    kernel = LimaKernel()

    result = kernel.preview_guardian_lifecycle(_request("planning"))

    assert isinstance(result, GuardianLifecyclePreviewResult)
    assert result.state == "proposed"
    assert result.reason_code == "guardian_lifecycle_preview_proposed"
    assert result.intent_candidate.state == "ready_for_guardian_request"
    assert result.guardian_request.state == "ready_for_policy_review"
    assert result.event_refs == (
        "guardian-lifecycle-preview-event:1",
        "guardian-lifecycle-preview-event:2",
    )
    _assert_preview_invariants(result)


def test_lifecycle_preview_accepts_mapping_request_without_public_export_expansion() -> None:
    result = LimaKernel().preview_guardian_lifecycle(
        {
            "request_id": "req-map-lifecycle",
            "shell_id": "test-shell",
            "actor_id": "actor-ref",
            "session_id": "session-ref",
            "normalized_intent": {"action_category": "drafting", "risk_class": "low"},
            "capability_profile": {},
            "source_surface": {"surface": "mapping_test"},
        }
    )

    assert result.state == "proposed"
    assert "GuardianLifecyclePreviewResult" not in KERNEL_INIT_PATH.read_text(encoding="utf-8")
    _assert_preview_invariants(result)


def test_unknown_action_blocks_before_decision_authority() -> None:
    result = LimaKernel().preview_guardian_lifecycle(_request("unknown_action"))

    assert result.state == "blocked"
    assert result.reason_code == "unknown_action_category_blocked"
    assert result.intent_candidate.state == "blocked_before_guardian"
    assert result.guardian_request.state == "blocked_before_decision"
    _assert_preview_invariants(result)


def test_raw_chat_or_office_task_text_blocks() -> None:
    result = LimaKernel().preview_guardian_lifecycle(
        _request(
            "planning",
            normalized_intent={"raw_chat": "send this raw chat through LIMA"},
        )
    )

    assert result.state == "blocked"
    assert result.reason_code == "raw_executable_input_not_allowed"
    _assert_preview_invariants(result)


def test_authority_claim_blocks_without_decision_or_approval() -> None:
    result = LimaKernel().preview_guardian_lifecycle(
        _request(
            "planning",
            metadata={"approval_granted": "trusted override dispatch now"},
        )
    )

    assert result.state == "blocked"
    assert result.reason_code == "authority_claim_not_allowed"
    _assert_preview_invariants(result)


def test_disabled_capability_blocks() -> None:
    result = LimaKernel().preview_guardian_lifecycle(
        _request("model_call", profile=CapabilityProfile(model_calls=False))
    )

    assert result.state == "blocked"
    assert result.reason_code == "disabled_capability_blocked:model_calls"
    _assert_preview_invariants(result)


def test_consequential_enabled_capability_returns_approval_required_preview_only() -> None:
    result = LimaKernel().preview_guardian_lifecycle(
        _request("model_call", profile=CapabilityProfile(model_calls=True))
    )

    assert result.state == "approval_required"
    assert result.reason_code == "guardian_lifecycle_requires_future_decision:model_calls"
    assert "approval_not_enforced" in result.warnings
    _assert_preview_invariants(result)


def test_dangerous_capability_blocks_even_when_enabled() -> None:
    result = LimaKernel().preview_guardian_lifecycle(
        _request("process_execute", profile=CapabilityProfile(process_execute=True))
    )

    assert result.state == "blocked"
    assert result.reason_code == "dangerous_capability_blocked:process_execute"
    _assert_preview_invariants(result)


def test_requested_tool_pack_must_not_be_granted_by_request() -> None:
    result = LimaKernel().preview_guardian_lifecycle(
        _request(
            "planning",
            normalized_intent={"requested_tool_packs": ["browser"]},
            profile=CapabilityProfile(allowed_tool_packs=()),
        )
    )

    assert result.state == "blocked"
    assert result.reason_code == "requested_tool_pack_not_allowed"
    assert result.guardian_request.allowed_tool_packs == ()
    _assert_preview_invariants(result)


def test_runtime_dependency_presence_blocks_preview() -> None:
    result = LimaKernel(provider_registry=object()).preview_guardian_lifecycle(_request("planning"))

    assert result.state == "blocked"
    assert result.reason_code == "runtime_dependency_not_allowed:provider_registry"
    _assert_preview_invariants(result)


def test_events_are_redacted_and_in_memory_only() -> None:
    result = LimaKernel().preview_guardian_lifecycle(
        _request(
            "planning",
            metadata={"evidence_refs": ["safe-ref", "token-secret-ref"]},
        )
    )

    assert result.intent_candidate.evidence_refs == ("safe-ref",)
    for event in result.events:
        event_dict = event.to_dict()
        assert event.in_memory_only is True
        assert event.durable is False
        assert event.contains_secret is False
        assert event.contains_raw_prompt is False
        assert event.contains_unsafe_payload is False
        assert "token-secret-ref" not in str(event_dict)
    _assert_preview_invariants(result)


def test_lifecycle_preview_module_has_no_forbidden_imports_or_calls() -> None:
    forbidden_imports = {
        "asyncio",
        "http",
        "multiprocessing",
        "openai",
        "os",
        "pathlib",
        "queue",
        "requests",
        "socket",
        "sqlite3",
        "subprocess",
        "threading",
        "urllib",
        "webbrowser",
    }
    forbidden_calls = {
        "__import__",
        "eval",
        "exec",
        "open",
    }

    tree = ast.parse(LIFECYCLE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls


def test_lifecycle_preview_module_has_no_forbidden_wiring_strings() -> None:
    forbidden_strings = (
        "SparkbotHumanInputAdapter(",
        "backend.app",
        "app.crud",
        "app.models",
        "robo_os_adapter(",
        "LIMA-Robo-OS",
        "sqlite3",
        "requests.",
        "socket",
        "subprocess",
        "threading",
        "connect(",
        "dispatch(",
        "execute(",
        "open(",
        "scan(",
    )

    text = LIFECYCLE_PATH.read_text(encoding="utf-8")
    for forbidden in forbidden_strings:
        assert forbidden not in text
