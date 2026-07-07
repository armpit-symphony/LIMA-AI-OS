"""Consumer-style public import smoke for V1 governed dry-run runtime surfaces."""

from __future__ import annotations

from lima.adapters import V1ShellRuntimeInput, run_v1_shell_governed_preflight
from lima.kernel import V1GovernedPreflightResult, run_v1_governed_preflight


def test_public_exports_support_consumer_style_governed_dry_run_call() -> None:
    shell_input = V1ShellRuntimeInput(
        input_id="consumer-import-smoke-001",
        consumer="sparkbot",
        actor_id="consumer-operator",
        shell_id="consumer-shell",
        tenant_ref="tenant:consumer-smoke",
        normalized_request="metadata-only consumer import smoke",
        requested_action="summarize governed dry-run posture",
        action_category="informational",
        source_channel="consumer-import-smoke",
        intent_id="intent:consumer-import-smoke",
        target_ref="target:consumer-import-smoke",
        session_ref="session:consumer-import-smoke",
        evidence_refs=("evidence:consumer-import-smoke",),
        metadata={"consumer_import_smoke": True},
    )

    result = run_v1_shell_governed_preflight(shell_input)

    assert callable(run_v1_governed_preflight)
    assert isinstance(result.preflight, V1GovernedPreflightResult)
    assert result.response["record_type"] == "v1_shell_governed_runtime_response"
    assert result.response["consumer"] == "sparkbot"
    assert result.response["request_id"].startswith("v1-request:")
    assert result.response["decision_id"].startswith("v1-decision:")
    assert result.response["audit_event_id"].startswith("event:v1-governed-preflight:")
    assert result.response["lineage_id"].startswith("v1-lineage:")
    assert result.response["execution_allowed"] is False
    assert result.response["side_effects_allowed"] is False
    assert result.response["provider_model_routed"] is False
    assert result.response["tool_executed"] is False
    assert result.response["file_mutation_executed"] is False
    assert result.response["network_action_executed"] is False
    assert result.response["connector_invoked"] is False
    assert result.response["proof_not_authority"] is True