# Phase 2.14 IntentEnvelope Test Design Review

## Purpose

Review how LIMA should safely design a test-only HumanInput-to-IntentEnvelope path in a future phase.

This review is review/design only.
This review does not implement runtime behavior.
This review does not implement real IntentCompiler.
This review does not infer intent from natural language.
This review does not authorize production wiring.
This review does not authorize execution.

## Current Boundary State

- `SparkbotHumanInputAdapter` returns `HumanInput` only.
- `HumanInputFakePipelineBridge` is test-only.
- Current bridge creates `ConsequentialActionRequest` from explicit metadata/default config.
- No production IntentCompiler exists.
- No production adapter wiring exists.
- Adapter Safety Gate is now standing review gate.

## IntentEnvelope Boundary Rule

HumanInput may become IntentEnvelope only through a separate IntentCompiler boundary.

The IntentCompiler:

- translates/clarifies/revises only
- does not execute
- does not approve
- does not call tools
- does not call drivers
- does not authorize actions

In this test-design stage, no component may call models to infer intent.

## Test-Only Design Direction

Recommend future Phase 2.15:

`phase-2-15-intent-envelope-test-fixtures`

Purpose:

Create synthetic test fixtures for explicit typed intent payloads and expected IntentEnvelope shapes.

Allowed:

- fixtures only
- explicit typed intent data only
- no natural-language inference
- no model calls
- no execution
- no GuardianDecision creation

## Explicit Typed Intent Metadata

Future fixtures may use explicit test metadata keys:

- `intent_type`
- `action_type`
- `risk_class`
- `target_ref`
- `typed_args`
- `evidence_refs`
- `requested_tool_packs`
- `approval_level`
- `privacy_class`
- `redaction_class`
- `lineage_id`
- `reason`
- `confidence`

These fields are explicit test metadata only.

They do not come from natural-language inference.

## Natural-Language Inference Block

Future test fixtures may include `raw_text`, but `raw_text` must not be parsed to infer intent.

If intent metadata is missing:

- `IntentEnvelope` must not be created, or
- result must be `clarification_needed` / `invalid` / `unknown` depending on the future contract.

No hidden parser.
No model call.
No heuristic interpretation of free text.

## Adapter Separation Rule

`SparkbotHumanInputAdapter` must not create `IntentEnvelope`.

The adapter must remain HumanInput-only.

Any future HumanInput-to-IntentEnvelope test component must be separate.

## Guardian Boundary

IntentEnvelope does not authorize execution.

IntentEnvelope must later go to GuardianDecision before consequential behavior.

No GuardianDecision is created in Phase 2.14.

## Owner Autonomy Boundary

Owner autonomy metadata is passive.

It must not:

- infer intent
- approve execution
- reduce risk
- bypass Guardian
- authorize tool/driver use

## Still Blocked

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation from adapter
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device/autonomy enforcement
- audit persistence
- redaction runtime
- real Guardian / policy / approval enforcement

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| `raw_text` accidentally parsed as intent | High | Current fake bridge ignores raw text for action inference | Phase 2.15 fixtures must require explicit typed metadata |
| Fixture metadata mistaken for production intent | Medium | This review labels metadata as test-only | Keep fixture docs and tests explicit about non-production scope |
| IntentEnvelope mistaken for authorization | High | Guardian boundary remains separate | Future tests must assert IntentEnvelope does not authorize execution |
| Adapter starts creating IntentEnvelope | High | Adapter boundary tests require HumanInput-only returns | Keep adapter safety gate mandatory for adapter-adjacent PRs |
| Real IntentCompiler started too early | High | Phase 2.14 is review-only | Limit Phase 2.15 to fixtures only |
| Model calls added too early | High | Model calls remain blocked | Test design must avoid model providers and hidden inference |
| Owner autonomy metadata mistaken for approval | High | Autonomy metadata remains passive | Future fixtures must keep trust/autonomy metadata non-authorizing |
| References mistaken for authority | Medium | Adapter Safety Gate states references are not authority | Keep evidence/reference fields passive until Guardian review |

## Final Decision

GO for Phase 2.15 IntentEnvelope Test Fixtures.

NO-GO for real IntentCompiler, natural-language inference, production wiring, execution, or GuardianDecision creation.
