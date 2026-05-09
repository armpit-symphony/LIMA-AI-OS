# Phase 1.14 HumanInput Adapter Readiness Review

## Purpose

Review whether the non-production Sparkbot HumanInput adapter skeleton is ready to be composed with the fake Guardian pipeline in a future test-only branch.

This review does not implement that composition.
This review does not authorize production wiring.
This review does not authorize real enforcement or execution.

## Current State

- Phase 1.8 created the fake Guardian pipeline.
- Phase 1.13 created the neutral payload-to-HumanInput adapter skeleton.
- The adapter returns HumanInput only.
- The fake pipeline accepts ConsequentialActionRequest, not raw HumanInput.
- IntentEnvelope / ConsequentialActionRequest creation is still blocked outside fake/test design.
- No production Sparkbot integration exists.

The current adapter is a LIMA-owned neutral conversion boundary. It does not import Sparkbot, does not wire routes, does not call models or tools, does not create IntentEnvelope, does not create GuardianDecision, and does not write audit data.

The fake pipeline is in-memory contract validation. It creates fake PolicyDecision, GuardianDecision, ApprovalMetadata, and Spine/Audit lineage records from ConsequentialActionRequest objects for tests only. It is not real enforcement and cannot authorize production execution.

## Readiness Question

Are we ready for a test-only branch that composes:

```text
neutral Sparkbot payload
  -> HumanInput
  -> test-only request builder
  -> FakeGuardianPipeline
```

Or do we need more design first?

Decision: GO for Phase 1.15 test-only HumanInput-to-fake-pipeline bridge design/skeleton, but with strict limits.

The current metadata is sufficient for fake/test composition because HumanInput carries actor_id, shell_id, source, input_id, raw_text/content_ref, confidence, privacy_class, and metadata references. It is not sufficient for production identity, session, privacy, policy, autonomy, or redaction enforcement.

## Key Boundary Clarification

The SparkbotHumanInputAdapter must continue to stop at HumanInput.

Any future bridge from HumanInput to fake pipeline must be separate from the adapter.

The adapter must not:

- create IntentEnvelope
- create ConsequentialActionRequest
- create GuardianDecision
- call FakeGuardianPipeline
- call models
- call tools
- persist audit data

This separation prevents the adapter from becoming a shortcut from raw input to planning, policy, Guardian, lineage, or execution.

## Recommended Next Branch

Recommended next branch:

`phase-1-15-humaninput-fake-pipeline-bridge`

Allowed scope:

- test-only bridge
- neutral HumanInput objects only
- creates fake/test ConsequentialActionRequest objects
- calls FakeGuardianPipeline
- records fake lineage in memory
- no Sparkbot imports
- no production wiring
- no model/tool execution
- no real enforcement
- no persistence

Alternative branch if new review findings contradict this decision:

`phase-1-15-identity-session-privacy-mapping-review`

The alternative is not required for Phase 1.15 because current metadata is enough for a test-only bridge. It remains the right fallback if implementation review finds identity/session/privacy metadata too vague even for tests.

## Phase 1.15 Allowed Design

If proceeding, Phase 1.15 may define `HumanInputFakePipelineBridge`.

Allowed behavior:

- accepts HumanInput
- builds a test-only ConsequentialActionRequest
- chooses action_type UNKNOWN by default
- chooses MODEL_CALL or TOOL_CALL only if explicitly provided by test metadata
- defaults unknown/risky requests to denied/escalated through fake pipeline
- calls FakeGuardianPipeline
- returns FakeGuardianPipelineResult

Required constraints:

- test-only
- not production
- does not infer real action intent from natural language
- does not call IntentCompiler
- does not execute anything
- not used by Sparkbot routes
- not used as real Guardian enforcement

## Identity / Session / Privacy Readiness

For test-only bridge work, enough metadata exists:

- actor_id
- shell_id
- session_ref
- source_ref
- trusted_context_ref
- autonomy_notes
- privacy_class
- redaction_class
- confidence

Decision: for test-only bridge, enough metadata exists.

For production adapter work, not enough metadata exists. Identity/session/privacy still require later review before any live Sparkbot route wiring, real auth, real privacy enforcement, redaction runtime, audit persistence, or production adapter path.

The test bridge may pass references through metadata. It must not claim session trust, verify identity, reduce risk, or enforce privacy/redaction.

## Owner Autonomy Readiness

Owner autonomy metadata is passive only and must remain passive.

Phase 1.15 may pass autonomy_notes through metadata, but must not:

- grant autonomy
- reduce approval
- approve actions
- bypass Guardian
- change risk class based on trust

Trusted context and autonomy notes are evidence for future policy and Guardian review. They are not permission and do not replace Guardian.

## Still Blocked

- production Sparkbot route wiring
- stream_chat_with_tools import/extraction
- raw chat-to-tool shortcut
- model execution
- tool execution
- terminal/PTY
- Robo-OS physical action
- audit persistence
- redaction runtime
- real IntentCompiler
- real Guardian enforcement
- real policy enforcement
- real approval enforcement
- autonomy enforcement
- live auth/vault adapters

## Acceptance Criteria for Phase 1.15

If GO, Phase 1.15 must satisfy:

- test-only bridge only
- no Sparkbot imports
- no production wiring
- HumanInput adapter remains separate
- adapter still returns HumanInput only
- bridge may create ConsequentialActionRequest only from explicit test metadata
- bridge does not infer real intent from natural language
- bridge calls fake pipeline only
- no model/tool/driver execution
- no persistence
- critical/unknown requests do not auto-approve
- tests prove boundary separation

## Risk Register

| Risk | Severity | Mitigation | Phase target |
| --- | --- | --- | --- |
| Bridge accidentally becomes production path | High | Keep bridge under test-only scope, no route imports, no Sparkbot imports, no external services. | Phase 1.15 |
| Adapter starts creating ConsequentialActionRequest | High | Keep bridge separate and test adapter source for HumanInput-only output. | Phase 1.15 |
| Fake pipeline mistaken for real enforcement | Critical | Document fake pipeline as contract validation only and keep real enforcement blocked. | Phase 1.15 |
| Autonomy metadata mistaken for autonomy decision | High | Pass autonomy_notes as passive metadata only; no approval/risk/autonomy changes. | Phase 1.15 |
| Natural language intent inferred too early | Critical | Bridge may use explicit test metadata only; no natural language parsing or IntentCompiler call. | Phase 1.15 |
| Identity/session metadata treated as verified auth | High | Treat actor/session/trusted refs as unverified metadata in tests; real auth remains separate. | Later auth/session review |
| Privacy/redaction metadata treated as enforcement | High | Carry privacy/redaction hints only; no redaction runtime or persistence. | Later privacy/redaction review |

## Final Decision

GO for Phase 1.15 HumanInput Fake Pipeline Bridge only if it is test-only and separated from SparkbotHumanInputAdapter.

NO-GO for production integration, real IntentCompiler, real Guardian enforcement, tool/model execution, persistence, or live Sparkbot wiring.

The adapter remains the input boundary. The bridge may prove contract composition in memory, but it must not become a runtime path.
