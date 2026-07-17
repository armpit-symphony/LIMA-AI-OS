# V1-G5 Provider/Model Routing Contract

## Verdict

`V1-G5` is complete as a static provider/model routing contract and acceptance-test design.

This document is docs/tests/fixtures-only. It does not add provider calls, model calls, runtime routing, live credentials, secret access, shell wiring, runtime `GuardianDecision`, approval enforcement, execution, dispatch, persistence, haptic device behavior, robotics behavior, or production behavior.

## Purpose

V1 requires provider/model routing for the first shell consumers:

- `Sparkbot_shell`
- `Sparkbot`
- `Arc-Bot-shell`

Sparkbot is the R&D behavior reference. Its documented behavior supports live model switching, model stacks, provider seats, agent overrides, local providers, Codex subscription routing, Token Guardian recommendations, provider readiness checks, latency reporting, and governed secret storage.

LIMA must capture the contract shape without copying Sparkbot code or preserving unsafe shortcuts. Model routing is consequential when it carries user/project context, private data, tool manifests, expensive models, external providers, or fallback chains. It must be constrained by Guardian, shell scope, tool-pack scope, secret policy, budget/cost posture, privacy/redaction rules, and audit/evidence requirements.

## Source Evidence

- `docs/V1_PRODUCT_READINESS_TARGET.md` accepts provider/model routing as a future V1 capability.
- `docs/V1_READINESS_GAP_MATRIX.md` identifies `V1-G5` as provider/model routing contract and acceptance-test design.
- `docs/GUARDIAN_DECISION_CONTRACT.md` requires `decision_id` for consequential model/tool calls.
- `docs/TOOL_PACK_RISK_POLICY.md` defines the `model` pack as scoped and Guardian-constrained.
- `docs/REDACTION_PRIVACY_CONTRACT.md` forbids raw secrets in audit events and requires secret refs.
- `docs/SPINE_AUDIT_LINEAGE_CONTRACT.md` requires decision lineage and redacted evidence.
- `docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md` defines the decision/approval gate that routing must obey.
- `Sparkbot/docs/capabilities.md` documents model/provider setup, model stack routing, agent overrides, provider readiness, Token Guardian recommendations, latency tracking, and backend-owned credentials.
- `Sparkbot/docs/PUBLIC_RELEASE_CAPABILITY_MODEL.md` documents shell capability profiles where model routing is allowed while risky writes and credential access remain guarded.

## Route Families

The future routing contract must cover:

- primary model route
- backup/fallback route
- heavy-hitter route
- agent override route
- Workstation or model-seat route
- local endpoint route
- Codex subscription route
- provider-readiness or self-inspection route

Fallback does not relax policy. Every fallback candidate must satisfy the same Guardian, shell, secret, budget, tool-pack, privacy, and audit constraints as the primary route.

## Required Route Metadata

Any future route candidate must carry:

- `route_id`
- `source_shell`
- `actor_id`
- `session_id`
- `intent_id`
- `decision_id`
- `provider_id`
- `model_id`
- `model_role`
- `route_family`
- `data_sensitivity`
- `prompt_context_class`
- `requested_tool_packs`
- `allowed_tool_packs`
- `secret_ref`
- `budget_class`
- `estimated_cost_class`
- `latency_tier`
- `fallback_chain`
- `audit_evidence_ref`
- `policy_version`

Raw provider keys, OAuth tokens, CLI auth contents, endpoint credentials, prompt transcripts, private context, and full tool payloads must not be embedded in route metadata. Use secret refs and redacted evidence refs.

## Required Routing Gates

A future runtime route may proceed only when all required gates pass:

- shell allows the `model` pack
- actor/session policy allows model use
- a scoped `GuardianDecision` permits model routing
- requested provider and model are configured for the shell/room/agent
- required secret ref exists or the provider is explicitly no-key local
- data sensitivity is allowed for the provider class
- budget/cost policy allows the model
- requested tool packs are allowed by the decision and shell scope
- fallback candidates pass the same checks
- audit evidence can be recorded without raw secrets or raw private content

If any gate fails, the route must fail closed.

## Static V1-G5 Acceptance Rules

For this branch:

- no provider/model route executes
- no model call is made
- no provider SDK, API, CLI, or local endpoint is called
- no secret is read
- no live provider readiness check runs
- no Token Guardian live route is activated
- no fallback route executes
- no runtime `GuardianDecision` is created
- no approval is granted
- no execution, dispatch, persistence, external call, tool call, driver call, browser/file/network/device/robotics call, haptic device behavior, or physical-world action is allowed

Static fixture claims of a live route, raw secret, forged decision, unknown provider, missing secret ref, disallowed shell route, tool-capable model without tool scope, private data route without Guardian review, or expensive model route without budget review must fail closed.

## What V1-G5 Proves

V1-G5 proves as static evidence:

- provider/model route families are identified
- required route metadata is defined
- Guardian, shell, tool-pack, secret, budget, privacy, and audit gates are explicit
- fallback inheritance is constrained
- fail-closed cases are represented
- LIMA remains `CANDIDATE_ONLY`

## What V1-G5 Does Not Prove

V1-G5 does not prove:

- runtime model routing
- provider/model calls
- provider readiness checks
- live Token Guardian routing
- fallback execution
- secret lookup
- model latency telemetry
- runtime `GuardianDecision`
- approval enforcement
- audit persistence
- shell runtime wiring
- haptic device behavior
- production readiness
- V1 product readiness

## Boundary Confirmation

- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Provider/model routing added: no.
- Provider/model calls added: no.
- Secret access added: no.
- Runtime `GuardianDecision` added: no.
- Approval enforcement added: no.
- Sparkbot_shell wired into LIMA: no.
- Sparkbot imported into LIMA: no.
- Sparkbot code copied into LIMA: no.
- Arc-Bot-shell wired into LIMA: no.
- Execution, dispatch, or persistence added: no.
- Browser/file/network/device/robotics behavior added: no.
- Haptic device behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.

## Recommended Next Step

Recommended: `V1-G6`.

The next smallest safe step is haptic intent metadata as shell-contract metadata only. Shells own rendering and device behavior.
