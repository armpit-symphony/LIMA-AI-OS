# Phase 1.15 HumanInput Fake Pipeline Bridge

## Purpose

Create a test-only bridge from HumanInput to FakeGuardianPipeline.

This validates that HumanInput records can enter the fake Guardian pipeline without production wiring or real enforcement.

## Boundary Rule

SparkbotHumanInputAdapter stops at HumanInput.

HumanInputFakePipelineBridge is separate.

The bridge may create test-only ConsequentialActionRequest objects only from explicit metadata.

The bridge must not infer real intent from natural language.

## Pipeline

```text
HumanInput
  -> HumanInputFakePipelineBridge
  -> ConsequentialActionRequest from explicit metadata
  -> FakeGuardianPipeline
  -> FakeGuardianPipelineResult
  -> fake lineage
```

## Non-Goals

- no production Sparkbot wiring
- no Sparkbot imports
- no real IntentCompiler
- no natural language intent inference
- no Guardian enforcement
- no policy enforcement
- no approval enforcement
- no model calls
- no tool execution
- no driver calls
- no terminal/PTY
- no Robo-OS physical action
- no audit persistence
- no redaction runtime
- no autonomy enforcement

## Explicit Metadata Only

The bridge may use only explicit HumanInput.metadata keys:

- action_type
- risk_class
- target_ref
- requested_tool_pack
- typed_args
- evidence_refs
- request_id

If missing:

- action_type defaults to UNKNOWN
- critical/unknown requests must not auto-approve through fake pipeline

The bridge must not parse raw_text or content_ref to decide action type, risk, target, tool pack, or evidence.

## Autonomy Metadata

trusted_context_ref and autonomy_notes may pass through metadata.

They must not:

- approve actions
- reduce risk
- change action_type
- bypass Guardian
- affect fake policy unless explicitly provided in test metadata

## Acceptance Criteria

- bridge is separate from adapter
- adapter still returns HumanInput only
- bridge creates ConsequentialActionRequest only from explicit metadata
- no natural-language inference
- no IntentEnvelope creation
- no direct GuardianDecision creation
- fake pipeline only
- no production wiring
- no model/tool/driver execution
- critical/unknown requests do not auto-approve
- tests prove boundary separation
