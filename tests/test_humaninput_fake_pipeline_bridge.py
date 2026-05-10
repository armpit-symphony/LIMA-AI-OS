"""Tests for the test-only HumanInput to fake pipeline bridge."""

from __future__ import annotations

import ast
from pathlib import Path

from lima.contracts import (
    ConsequentialActionType,
    GuardianDecision,
    GuardianDecisionStatus,
    HumanInput,
    HumanInputSource,
    PolicyExposure,
    ToolPackRiskRule,
    ToolPackRiskPolicy,
)
from lima.guardian import (
    FakeApprovalRecorder,
    FakeGuardianDecisionEvaluator,
    FakeGuardianPipeline,
    FakePolicyRiskEvaluator,
    FakeSpineAuditRecorder,
    HumanInputFakePipelineBridge,
)


def _policy(*rules: ToolPackRiskRule) -> ToolPackRiskPolicy:
    return ToolPackRiskPolicy(
        policy_id="policy-bridge",
        policy_version="phase-1.15-fake",
        shell_id="test-shell",
        rules=rules,
        created_at="fake",
    )


def _bridge(*rules: ToolPackRiskRule) -> tuple[HumanInputFakePipelineBridge, FakeSpineAuditRecorder]:
    spine = FakeSpineAuditRecorder()
    pipeline = FakeGuardianPipeline(
        policy_evaluator=FakePolicyRiskEvaluator(policy=_policy(*rules)),
        decision_evaluator=FakeGuardianDecisionEvaluator(),
        approval_recorder=FakeApprovalRecorder(),
        spine_recorder=spine,
    )
    return HumanInputFakePipelineBridge(pipeline), spine


def _human_input(metadata: dict[str, object] | None = None) -> HumanInput:
    return HumanInput(
        input_id="input-bridge-1",
        source=HumanInputSource.TEXT,
        actor_id="actor-bridge",
        shell_id="test-shell",
        raw_text="do the thing",
        privacy_class="private",
        metadata=metadata or {},
    )


def _public_callables(provider: type) -> set[str]:
    return {
        name
        for name, value in provider.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def test_explicit_low_risk_metadata_evaluates_through_fake_pipeline() -> None:
    rule = ToolPackRiskRule(
        pack_name="model",
        default_risk_class="low",
        default_exposure=PolicyExposure.ALLOW,
    )
    bridge, spine = _bridge(rule)
    human_input = _human_input(
        {
            "request_id": "request-low",
            "action_type": "model_call",
            "risk_class": "low",
            "target_ref": "model-route-ref",
            "requested_tool_pack": "model",
            "typed_args": {"summary_ref": "args-low"},
            "evidence_refs": ("evidence-low",),
        }
    )

    result = bridge.evaluate_human_input(human_input)

    assert result.request.action_type is ConsequentialActionType.MODEL_CALL
    assert result.request.risk_class == "low"
    assert result.guardian_decision.decision_id
    assert result.guardian_decision.status is GuardianDecisionStatus.APPROVED
    assert result.metadata["non_executing"] is True
    assert spine.get_lineage(result.lineage_id)
    assert spine.get_lineage_record(result.lineage_id).decision_id == result.guardian_decision.decision_id
    assert result.request.typed_args == {"summary_ref": "args-low"}
    assert result.request.evidence_refs == ("evidence-low",)


def test_missing_action_type_defaults_unknown_and_does_not_auto_approve() -> None:
    bridge, spine = _bridge()
    human_input = _human_input({"request_id": "request-unknown"})

    result = bridge.evaluate_human_input(human_input)

    assert result.request.action_type is ConsequentialActionType.UNKNOWN
    assert result.guardian_decision.status is GuardianDecisionStatus.DENIED
    assert result.status == "denied"
    assert spine.get_lineage(result.lineage_id)
    assert spine.get_lineage_record(result.lineage_id).status == "denied"


def test_raw_text_does_not_drive_action_type_inference() -> None:
    bridge, _spine = _bridge()
    human_input = HumanInput(
        input_id="input-terminal-words",
        source=HumanInputSource.TEXT,
        actor_id="actor-bridge",
        shell_id="test-shell",
        raw_text="run a terminal command",
        privacy_class="private",
        metadata={"request_id": "request-raw-text-only"},
    )

    result = bridge.evaluate_human_input(human_input)

    assert result.request.action_type is ConsequentialActionType.UNKNOWN
    assert result.guardian_decision.status is GuardianDecisionStatus.DENIED


def test_critical_terminal_metadata_does_not_auto_approve() -> None:
    rule = ToolPackRiskRule(
        pack_name="terminal",
        default_risk_class="critical",
        default_exposure=PolicyExposure.ALLOW,
        required_approval_level="operator_pin",
    )
    bridge, _spine = _bridge(rule)
    human_input = _human_input(
        {
            "request_id": "request-terminal",
            "action_type": "terminal_command",
            "risk_class": "critical",
            "target_ref": "terminal-ref",
            "requested_tool_pack": "terminal",
        }
    )

    result = bridge.evaluate_human_input(human_input)

    assert result.request.action_type is ConsequentialActionType.TERMINAL_COMMAND
    assert result.guardian_decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN
    assert result.guardian_decision.status is not GuardianDecisionStatus.APPROVED
    assert result.approval is not None
    assert result.metadata["non_executing"] is True


def test_critical_robot_payment_deploy_and_secret_metadata_do_not_auto_approve() -> None:
    cases = (
        (ConsequentialActionType.ROBOT_ACTION, "robo", "robot-ref"),
        (ConsequentialActionType.PAYMENT_ACTION, "payments", "payment-ref"),
        (ConsequentialActionType.DEPLOY_ACTION, "deploy", "deploy-ref"),
        (ConsequentialActionType.SECRET_ACCESS, "vault", "secret-ref"),
    )

    for action_type, pack_name, target_ref in cases:
        rule = ToolPackRiskRule(
            pack_name=pack_name,
            default_risk_class="critical",
            default_exposure=PolicyExposure.ALLOW,
            required_approval_level="operator_pin",
        )
        bridge, _spine = _bridge(rule)
        human_input = _human_input(
            {
                "request_id": f"request-{action_type.value}",
                "action_type": action_type.value,
                "risk_class": "critical",
                "target_ref": target_ref,
                "requested_tool_pack": pack_name,
            }
        )

        result = bridge.evaluate_human_input(human_input)

        assert result.request.action_type is action_type
        assert result.guardian_decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN
        assert result.guardian_decision.status is not GuardianDecisionStatus.APPROVED
        assert result.approval is not None
        assert result.metadata["non_executing"] is True


def test_autonomy_metadata_is_passive() -> None:
    bridge, _spine = _bridge()
    human_input = _human_input(
        {
            "request_id": "request-autonomy",
            "trusted_context_ref": "trusted-test-session",
            "autonomy_notes": {"level": "trusted"},
        }
    )

    result = bridge.evaluate_human_input(human_input)

    assert result.request.action_type is ConsequentialActionType.UNKNOWN
    assert result.request.risk_class == "medium"
    assert result.guardian_decision.status is GuardianDecisionStatus.DENIED
    assert result.request.metadata["trusted_context_ref"] == "trusted-test-session"
    assert result.request.metadata["autonomy_notes"] == {"level": "trusted"}


def test_adapter_remains_separate_from_bridge() -> None:
    from lima.adapters import SparkbotChatInputPayload, SparkbotHumanInputAdapter

    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotChatInputPayload(
        message_id="msg-bridge-separation",
        actor_ref="actor-1",
        shell_id="sparkbot-shell",
        text="summarize this",
    )

    result = adapter.adapt_chat_payload(payload)
    source = (
        Path(__file__).resolve().parents[1]
        / "lima"
        / "adapters"
        / "sparkbot_humaninput.py"
    ).read_text(encoding="utf-8")

    assert type(result) is HumanInput
    assert "HumanInputFakePipelineBridge" not in source
    assert "ConsequentialActionRequest" not in source
    assert "FakeGuardianPipeline" not in source


def test_bridge_does_not_create_intent_envelope_directly() -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "lima"
        / "guardian"
        / "humaninput_pipeline_fakes.py"
    ).read_text(encoding="utf-8")

    assert "IntentEnvelope" not in source
    assert "IntentCompiler" not in source
    assert "GuardianDecision(" not in source
    assert not isinstance(HumanInputFakePipelineBridge, GuardianDecision)


def test_bridge_forbidden_methods_are_absent() -> None:
    forbidden_methods = {
        "execute",
        "enforce",
        "run",
        "call_model",
        "call_tool",
        "call_driver",
        "approve_and_execute",
        "authorize_execution",
        "bypass",
        "persist",
        "save_to_db",
        "open_db",
        "write_file",
        "send",
        "parse_intent",
        "infer_intent",
        "call_intent_compiler",
    }

    assert _public_callables(HumanInputFakePipelineBridge).isdisjoint(forbidden_methods)


def test_bridge_forbidden_imports_absent() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "lima"
        / "guardian"
        / "humaninput_pipeline_fakes.py"
    )
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported_modules.append(node.module)

    imported_text = "\n".join(imported_modules)
    forbidden_imports = {
        "Sparkbot",
        "sparkbot",
        "FastAPI",
        "WebSocket",
        "app.api.routes",
        "backend.app",
        "terminal",
        "pty",
        "Robo",
        "robo",
    }
    forbidden_symbols = {
        "stream_chat_with_tools",
        "execute_tool",
    }

    violations = [
        forbidden
        for forbidden in forbidden_imports
        if forbidden.lower() in imported_text.lower()
    ]
    violations.extend(
        forbidden for forbidden in forbidden_symbols if forbidden in text
    )

    assert violations == []
