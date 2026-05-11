# Phase 3.1 Non-production Kernel Pipeline Fixture Map

## Purpose

Map existing fixture families across the proposed non-production kernel pipeline stages.

This phase does not implement a pipeline.
This phase does not create runtime behavior.
This phase does not authorize production integration.

## Proposed Pipeline Stages

1. Sparkbot-shaped payload / HumanInput fixture
2. HumanInput
3. IntentEnvelope fixture shape
4. Guardian request fixture shape
5. Fake GuardianDecision fixture shape
6. Fake approval / fake spine / fake lineage / report artifact placeholder

## Fixture Families

### `tests/fixtures/sparkbot_payloads/`

Purpose: LIMA-owned synthetic mirrors of Sparkbot-shaped input payloads that validate adapter-adjacent HumanInput mapping.

Current count: 19 fixtures across 11 JSON files.

Status types: source-surface categories such as chat, frontend chat, voice, meeting, Workstation, SparkBud, auth/session context, model routing context, MCP approval, operator terminal, and robotics request surfaces. The fixture regression harness reports `passed`, `unsupported_nonexecuting`, or `failed`; current fixtures are expected to pass without execution.

Safety notes:

- fixtures are synthetic mirrors, not authority
- adapter returns HumanInput only
- unsupported categories must not pass silently
- MCP and robot fixtures remain non-executing
- critical, robot, operator, unknown, auth, and model-routing paths must not auto-approve

Must not imply production Sparkbot wiring, Sparkbot imports, live routes, `stream_chat_with_tools`, `execute_tool`, model calls, tool execution, terminal/PTY, Robo-OS physical action, audit persistence, redaction runtime, live auth/session lookup, trusted device enforcement, autonomy enforcement, real IntentCompiler, real Guardian enforcement, or approval enforcement.

### `tests/fixtures/intent_envelopes/`

Purpose: synthetic IntentEnvelope-shaped fixtures that validate explicit typed metadata and expected envelope shape without a real IntentCompiler.

Current count: 15 fixtures across 4 JSON files.

Status types:

- `typed_intent`: 6
- `invalid_missing_metadata`: 3
- `clarification_needed`: 2
- `safety_critical_intent`: 4

Safety notes:

- `raw_text` is inert
- explicit metadata drives shape validation
- invalid and clarification fixtures do not create envelopes
- safety-critical fixtures require later Guardian/policy/approval review
- IntentEnvelope is not authorization

Must not imply real IntentCompiler behavior, natural-language inference, `raw_text` parsing, hidden parsing, model calls, tool execution, GuardianDecision creation, approval, production wiring, audit persistence, or redaction runtime.

### `tests/fixtures/guardian_requests/`

Purpose: synthetic Guardian request-shaped fixtures that validate explicit request fields and expected request shape without creating GuardianDecision or enforcing policy.

Current count: 19 fixtures across 4 JSON files.

Status types:

- `valid_guardian_request`: 4
- `invalid_guardian_request`: 5
- `safety_critical_guardian_request`: 4
- `approval_required_guardian_request`: 6

Safety notes:

- Guardian request is not GuardianDecision
- Guardian request is not approval
- requested tool packs are requests only
- approval requirement refs remain descriptive
- autonomy context refs remain passive
- privacy/redaction metadata is not enforcement

Must not imply real GuardianDecision creation, Guardian enforcement, policy enforcement, approval enforcement, ApprovalMetadata recording, action approval, tool execution, model calls, audit persistence, real IntentCompiler, natural-language inference, production Sparkbot wiring, terminal/PTY, Robo-OS physical action, live auth/session lookup, autonomy enforcement, or redaction runtime.

### `tests/fixtures/fake_guardian_decisions/`

Purpose: synthetic fake GuardianDecision-shaped fixtures that validate test-only decision statuses without creating real GuardianDecision or authorizing production behavior.

Current count: 23 fixtures across 6 JSON files.

Status types:

- `allow_test_only`: 3
- `deny_test_only`: 4
- `needs_approval_test_only`: 7
- `blocked_test_only`: 6
- `expired_test_only`: 1
- `revoked_test_only`: 1
- `superseded_test_only`: 1

Safety notes:

- fake GuardianDecision is test-only
- fake GuardianDecision is not production authorization
- `allow_test_only` is not production allow
- `needs_approval_test_only` is not approval granted
- `approval_ref` is reference-only and is not ApprovalMetadata
- blocked, expired, revoked, and superseded fake decisions are non-executable
- safety-critical fake decisions do not auto-approve

Must not imply real GuardianDecision, production authorization, approval, enforcement, ApprovalMetadata recording, action approval, tool execution, model calls, audit persistence, real IntentCompiler, natural-language inference, Sparkbot wiring, terminal/PTY, Robo-OS physical action, live auth/session lookup, autonomy enforcement, or redaction runtime.

## Fixture Relationship Map

This table maps scenario families only. It does not define transform logic, runtime flow, or executable relationships.

| Scenario | Sparkbot/HumanInput fixture | IntentEnvelope fixture | Guardian request fixture | Fake GuardianDecision fixture | Expected final fake/report posture | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| low-risk informational | `chat-stream-message-basic`, `chat-websocket-message-basic`, or `frontend-chat-message-variant` | `intent-typed-info-low-001` | `guardian-request-valid-info-low-001` | `fake-guardian-decision-allow-info-low-001` | review-only report may show low-risk shape compatibility; no model call | Fake allow remains test-only and not production authorization. |
| calendar/scheduling | `meeting-artifact-create` or `workstation-launch-context` | `intent-typed-calendar-medium-001` | `guardian-request-valid-calendar-medium-001` | `fake-guardian-decision-allow-schedule-plan-001` | review-only report may show planning shape compatibility; no task mutation | Scheduling relation is partial because no shared scenario ID links payload and intent fixtures yet. |
| draft-only communication | `voice-message-upload`, `frontend-chat-body-variant`, or `sparkbud-prompt-launch-context` | `intent-typed-draft-comms-001` | `guardian-request-valid-draft-comms-001` | `fake-guardian-decision-allow-draft-comms-001` | draft-only posture; no send action | Draft allow is not permission to send external communications. |
| email send requiring approval | no direct Sparkbot payload fixture today; future map may relate chat/frontend/voice payload to explicit send metadata | `intent-typed-email-send-high-001` | `guardian-request-valid-email-high-001` and `guardian-request-approval-email-high-001` | `fake-guardian-decision-needs-approval-email-001` | needs approval test-only; no ApprovalMetadata and no send | Approval requirement is descriptive only. |
| terminal critical request | `operator-terminal-session-create` or `operator-terminal-websocket-input` | `intent-typed-terminal-critical-001` or `intent-safety-terminal-command-001` | `guardian-request-safety-terminal-critical-001` | `fake-guardian-decision-safety-terminal-pty-001` or `fake-guardian-decision-blocked-terminal-critical-001` | blocked or needs approval test-only; no terminal/PTY | Terminal fixtures remain safety-critical and non-executing. |
| robot safety-critical request | `robotics-command-request` or `robotics-emergency-stop-request` | `intent-typed-robot-critical-001` or `intent-safety-robot-motion-001` | `guardian-request-safety-robot-critical-001` | `fake-guardian-decision-safety-robot-physical-001` or `fake-guardian-decision-blocked-robot-unsafe-001` | safety-critical fake posture; no physical action | Robot fixtures must never imply Robo-OS readiness or physical action. |
| secret access | no direct Sparkbot payload fixture today; auth/session context remains passive metadata only | `intent-safety-secret-access-001` | `guardian-request-safety-secret-critical-001` or `guardian-request-approval-secret-critical-001` | `fake-guardian-decision-safety-secret-001` or `fake-guardian-decision-needs-approval-secret-001` | needs approval test-only; no secret access and no ApprovalMetadata | Secret refs are not access grants. |
| payment/deploy/admin/destructive | no direct Sparkbot payload fixture today | `intent-safety-payment-deploy-admin-001` | `guardian-request-approval-payment-critical-001`, `guardian-request-approval-deploy-critical-001`, `guardian-request-approval-admin-critical-001`, or `guardian-request-approval-file-delete-critical-001` | `fake-guardian-decision-needs-approval-payment-001`, `fake-guardian-decision-needs-approval-deploy-001`, `fake-guardian-decision-needs-approval-admin-001`, `fake-guardian-decision-safety-admin-destructive-001`, or `fake-guardian-decision-blocked-filesystem-destructive-001` | approval-required or blocked test-only; no payment, deploy, admin, or destructive action | Critical fixtures require later Guardian/policy/approval review. |
| invalid/missing metadata | no direct Sparkbot payload fixture today | `intent-invalid-raw-text-only-001`, `intent-invalid-missing-intent-type-001`, or `intent-invalid-missing-target-001` | `guardian-request-invalid-missing-request-id-001`, `guardian-request-invalid-missing-risk-001`, `guardian-request-invalid-missing-action-001`, `guardian-request-invalid-missing-intent-ref-001`, or `guardian-request-invalid-tool-packs-malformed-001` | `fake-guardian-decision-deny-malformed-001`, `fake-guardian-decision-deny-missing-actor-session-001`, `fake-guardian-decision-deny-disallowed-pack-001`, or `fake-guardian-decision-deny-unknown-action-001` | invalid/deny test-only; no inferred repair | Missing metadata must not trigger free-text inference. |
| clarification needed | no direct Sparkbot payload fixture today | `intent-clarification-ambiguous-target-001` or `intent-clarification-low-confidence-001` | invalid or needs-review Guardian request fixture family | `fake-guardian-decision-deny-unknown-action-001` or future needs-review fake decision mapping | clarification/needs-review posture; no execution | Clarification does not authorize proceeding. |
| blocked unsafe request | `mcp-run-deny-request`, operator terminal fixtures, or robot fixtures | safety-critical intent fixture family | safety-critical Guardian request fixture family | blocked fake decision fixture family | blocked test-only; no action | Blocked fake decisions are non-authorizing and non-executable. |
| expired/revoked/superseded fake decision | no direct Sparkbot payload fixture today | no direct IntentEnvelope fixture today | no direct Guardian request fixture today | `fake-guardian-decision-expired-001`, `fake-guardian-decision-revoked-001`, or `fake-guardian-decision-superseded-001` | lifecycle status is non-executable and not production authorization | Current lifecycle fake decisions are decision-stage-only fixtures. |

## Compatibility Matrix

| Stage pair | Compatible today? yes/no/partial | Reason | Gap | Next action |
| --- | --- | --- | --- | --- |
| Sparkbot payload fixture -> HumanInput | yes | Adapter fixture harness validates current LIMA-owned payload fixtures into HumanInput and fake reports. | No shared scenario IDs across later fixture families. | Preserve adapter safety gate and map scenario IDs only after readiness review. |
| HumanInput -> IntentEnvelope fixture | partial | IntentEnvelope fixtures include HumanInput refs and explicit metadata, but no real compiler or transform exists. | No relationship metadata connects specific payload fixtures to specific IntentEnvelope fixtures. | Review whether explicit fixture relationship metadata is safe. |
| IntentEnvelope fixture -> Guardian request fixture | partial | Guardian request fixtures reference IntentEnvelope-like request inputs and matching action/risk families. | No automated compatibility assertion or shared scenario ID exists. | Define docs/tests-only compatibility assertions after Phase 3.2 review if approved. |
| Guardian request fixture -> fake GuardianDecision fixture | partial | Fake decisions align with request scenarios such as low-risk, approval-required, blocked, and safety-critical. | No executable mapping or decision generator exists, and none is approved. | Keep mapping descriptive and review fake decision relationship metadata separately. |
| Fake GuardianDecision fixture -> report artifact | partial | Existing harnesses produce in-memory report artifacts for review. | No non-executable cross-stage pipeline report format exists. | Propose report format only after map readiness review. |

## Non-runtime Rule

The fixture map is not an executable pipeline.
The fixture map does not transform data.
The fixture map does not validate runtime behavior.
The fixture map does not authorize actions.
The fixture map does not persist audit data.

## Safety Gates Required

- `docs/ADAPTER_SAFETY_GATE.md`
- `docs/INTENTENVELOPE_SAFETY_GATE.md`
- `docs/GUARDIAN_REQUEST_SAFETY_GATE.md`
- `docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md`

## Gaps Before Pipeline Harness

- stable shared scenario IDs across fixture families
- explicit fixture relationship metadata
- stage compatibility assertions
- non-executable pipeline report format
- missing fake approval/spine/lineage fixture placeholders if needed

## Recommended Next Branch

`phase-3-2-nonproduction-kernel-pipeline-map-readiness-review`

Purpose:

Review whether the fixture map is sufficient before adding any test-only pipeline map harness or relationship metadata.

## Still Blocked

- runtime pipeline
- production Sparkbot integration
- real IntentCompiler
- natural-language inference
- real GuardianDecision
- Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- redaction runtime
- terminal/PTY
- Robo-OS physical action
- live auth/session/trust/autonomy enforcement

## Final Decision

GO for Phase 3.2 Non-production Kernel Pipeline Map Readiness Review.

NO-GO for runtime pipeline, production integration, real IntentCompiler, real GuardianDecision, enforcement, approval, execution, or audit persistence.
