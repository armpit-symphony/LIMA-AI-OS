"""Tests for non-authoritative Guardian decision authority preview behavior."""

from __future__ import annotations

import ast
from pathlib import Path

from lima.kernel import CapabilityProfile, KernelRequest, LimaKernel
from lima.kernel.guardian_decision_authority import GuardianDecisionAuthorityPreviewResult


REPO_ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = REPO_ROOT / "lima" / "kernel" / "guardian_decision_authority.py"
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


def _assert_preview_invariants(result: GuardianDecisionAuthorityPreviewResult) -> None:
    assert result.dry_run is True
    assert result.executable is False
    assert result.execution_allowed is False
    assert result.side_effects_allowed is False
    assert result.dispatch_allowed is False
    assert result.persistence_allowed is False
    assert result.model_calls_allowed is False
    assert result.model_calls_executed is False
    assert result.guardian_decision_created is False
    assert result.decision_authority_created is False
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
    assert result.authority_preview.decision_authority_created is False
    assert result.authority_preview.guardian_decision_created is False
    assert result.authority_preview.approval_enforced is False
    assert result.authority_preview.execution_allowed is False
    assert result.authority_preview.dispatch_allowed is False
    assert result.authority_preview.persistence_allowed is False


def test_lima_kernel_exposes_explicit_decision_authority_preview_method() -> None:
    result = LimaKernel().preview_guardian_decision_authority(_request("planning"))

    assert isinstance(result, GuardianDecisionAuthorityPreviewResult)
    assert result.state == "authority_not_required"
    assert result.reason_code == "guardian_decision_not_required_for_text_preview"
    assert result.authority_preview.decision_required is False
    assert "GuardianDecisionAuthorityPreviewResult" not in KERNEL_INIT_PATH.read_text(
        encoding="utf-8"
    )
    _assert_preview_invariants(result)


def test_consequential_enabled_capability_requires_decision_but_creates_none() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request("model_call", profile=CapabilityProfile(model_calls=True))
    )

    assert result.state == "authority_required"
    assert result.reason_code == "guardian_decision_required:model_calls"
    assert result.authority_preview.decision_required is True
    assert "decision_required_not_created" in result.warnings
    _assert_preview_invariants(result)


def test_disabled_capability_blocks_before_authority() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request("model_call", profile=CapabilityProfile(model_calls=False))
    )

    assert result.state == "blocked"
    assert result.reason_code == "disabled_capability_blocked:model_calls"
    _assert_preview_invariants(result)


def test_dangerous_capability_blocks_even_when_enabled() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request("process_execute", profile=CapabilityProfile(process_execute=True))
    )

    assert result.state == "blocked"
    assert result.reason_code == "dangerous_capability_blocked:process_execute"
    _assert_preview_invariants(result)


def test_execution_seeking_request_without_decision_blocks() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request(
            "external_send",
            profile=CapabilityProfile(external_send=True),
            normalized_intent={"execution_requested": True},
        )
    )

    assert result.state == "blocked"
    assert result.reason_code == "guardian_decision_absent_for_execution"
    assert result.authority_preview.decision_required is True
    _assert_preview_invariants(result)


def test_unknown_decision_status_blocks() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request(
            "external_send",
            profile=CapabilityProfile(external_send=True),
            metadata={"guardian_decision_preview": {"decision_status": "maybe"}},
        )
    )

    assert result.state == "blocked"
    assert result.reason_code == "unknown_guardian_decision_status_blocked"
    assert result.authority_preview.existing_decision_status == "maybe"
    _assert_preview_invariants(result)


def test_non_eligible_decision_status_blocks() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request(
            "external_send",
            profile=CapabilityProfile(external_send=True),
            metadata={"guardian_decision_preview": {"decision_status": "revoked"}},
        )
    )

    assert result.state == "blocked"
    assert result.reason_code == "guardian_decision_status_blocked:revoked"
    _assert_preview_invariants(result)


def test_scope_mismatch_blocks() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request(
            "external_send",
            profile=CapabilityProfile(external_send=True),
            metadata={
                "guardian_decision_preview": {
                    "decision_status": "approved",
                    "actor_id": "other-actor",
                    "action_category": "external_send",
                    "requested_capability": "external_send",
                }
            },
        )
    )

    assert result.state == "blocked"
    assert result.reason_code == "guardian_decision_scope_mismatch:actor_id"
    _assert_preview_invariants(result)


def test_approval_required_without_approval_ref_blocks() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request(
            "external_send",
            profile=CapabilityProfile(external_send=True),
            metadata={
                "guardian_decision_preview": {
                    "decision_status": "approved",
                    "actor_id": "actor-ref",
                    "shell_id": "test-shell",
                    "session_id": "session-ref",
                    "action_category": "external_send",
                    "requested_capability": "external_send",
                    "approval_required": True,
                }
            },
        )
    )

    assert result.state == "blocked"
    assert result.reason_code == "approval_required_but_missing"
    _assert_preview_invariants(result)


def test_matching_approved_decision_still_returns_authority_required_not_created() -> None:
    result = LimaKernel().preview_guardian_decision_authority(
        _request(
            "external_send",
            profile=CapabilityProfile(external_send=True),
            metadata={
                "guardian_decision_preview": {
                    "decision_status": "approved",
                    "actor_id": "actor-ref",
                    "shell_id": "test-shell",
                    "session_id": "session-ref",
                    "action_category": "external_send",
                    "requested_capability": "external_send",
                    "approval_required": True,
                    "approval_ref": "approval-preview-ref",
                }
            },
        )
    )

    assert result.state == "authority_required"
    assert result.reason_code == "guardian_decision_required_not_created"
    assert result.authority_preview.status_reviewed is True
    assert result.authority_preview.scope_reviewed is True
    assert result.authority_preview.approval_reviewed is True
    _assert_preview_invariants(result)


def test_raw_input_and_authority_claims_block() -> None:
    raw_result = LimaKernel().preview_guardian_decision_authority(
        _request("planning", normalized_intent={"raw_chat": "raw chat must stay out"})
    )
    authority_result = LimaKernel().preview_guardian_decision_authority(
        _request("planning", metadata={"guardian_decision_created": True})
    )

    assert raw_result.state == "blocked"
    assert raw_result.reason_code == "raw_executable_input_not_allowed"
    assert authority_result.state == "blocked"
    assert authority_result.reason_code == "decision_authority_claim_not_allowed"
    _assert_preview_invariants(raw_result)
    _assert_preview_invariants(authority_result)


def test_runtime_dependency_presence_blocks_preview() -> None:
    result = LimaKernel(storage=object()).preview_guardian_decision_authority(_request("planning"))

    assert result.state == "blocked"
    assert result.reason_code == "runtime_dependency_not_allowed:storage"
    _assert_preview_invariants(result)


def test_events_are_redacted_and_in_memory_only() -> None:
    result = LimaKernel().preview_guardian_decision_authority(_request("planning"))

    for event in result.events:
        event_dict = event.to_dict()
        assert event.in_memory_only is True
        assert event.durable is False
        assert event.contains_secret is False
        assert event.contains_raw_prompt is False
        assert event.contains_unsafe_payload is False
        assert "password" not in str(event_dict).lower()
        assert "token" not in str(event_dict).lower()
    _assert_preview_invariants(result)


def test_decision_authority_module_has_no_forbidden_imports_or_calls() -> None:
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

    tree = ast.parse(AUTHORITY_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls


def test_decision_authority_module_has_no_forbidden_wiring_strings() -> None:
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

    text = AUTHORITY_PATH.read_text(encoding="utf-8")
    for forbidden in forbidden_strings:
        assert forbidden not in text
