# V1-G10 Minimum Runtime Implementation Gate

Date: 2026-06-14
Branch: `v1-g10-minimum-runtime-implementation-gate`
Source branch: `v1-g9-product-release-boundary-audit`
Source commit: `f6cf8dc9de0f1f50828a614e0b5cbd6830e7314f`
API status: `CANDIDATE_ONLY`

Gate verdict: `defined_not_approved_for_runtime`

This gate defines the minimum implementation scope required before LIMA-AI-OS can start moving from static V1 evidence toward usable V1 runtime behavior for `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`.

It does not approve implementation. It does not change runtime behavior.

## Purpose

V1-G9 found that the V1 release boundary is not passed because static evidence does not prove runtime behavior.

V1-G10 converts that release-boundary failure into an exact future implementation gate. The next runtime lane must be narrow, auditable, reversible, and directly tied to the V1 blockers:

- typed bridge runtime behavior
- real `GuardianDecision` runtime path
- live approval enforcement for destructive edit/delete
- audit/evidence linkage

Provider/model routing, durable audit persistence, and shell wiring remain required for V1, but they should not be smuggled into the first runtime slice unless a later approval explicitly names them.

## Current Runtime Surface Reviewed

Current runtime files inspected for this gate:

- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`
- `lima/kernel/candidate_preview.py`
- `lima/kernel/runtime_state.py`
- `lima/kernel/__init__.py`
- `lima/contracts/guardian.py`
- `lima/contracts/intent.py`
- `lima/contracts/approval.py`
- `lima/contracts/events.py`
- `lima/guardian/decision_fakes.py`
- `lima/guardian/pipeline_fakes.py`

Current runtime truth:

- LIMA can build non-executing intake candidates from already-normalized synthetic intake.
- LIMA can normalize and validate candidate statuses fail-closed.
- LIMA can preview and inspect candidate metadata as advisory, local-only state.
- Guardian, approval, and spine pipeline behavior is still fake/test-oriented.
- LIMA does not have a live typed bridge, real runtime `GuardianDecision`, approval enforcement, durable audit persistence, provider/model routing, or shell wiring.

## Future V1-G11 Runtime Slice

Recommended next implementation lane: `V1-G11`.

Proposed lane name: `typed_request_guardian_decision_preflight_runtime_slice`.

Future V1-G11 objective:

Create the smallest in-process runtime slice that converts a validated non-executing candidate into a typed `ConsequentialActionRequest`, evaluates it through a real fail-closed Guardian decision gate, and emits non-persistent audit/evidence linkage metadata.

The slice must not execute actions.

## Future Eligible Runtime Files

Future V1-G11 may touch only these runtime files if a later approval explicitly authorizes implementation:

- `lima/kernel/v1_runtime_request.py` (new)
- `lima/kernel/__init__.py` (candidate export only)
- `lima/guardian/v1_decision_gate.py` (new)
- `lima/guardian/__init__.py` (candidate export only)

Future V1-G11 may add only these test/fixture/docs files:

- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`
- `tests/test_v1_g11_runtime_request_decision_gate.py`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`

Any different file requires a new gate update before implementation.

## Explicitly Forbidden In V1-G11

The first runtime slice must not touch or add:

- `tests/support/`
- `lima/harness/`
- `lima/io/`
- `lima/persistence/`
- `lima/services/`
- `lima/shells/`
- shell repositories
- Sparkbot imports
- Sparkbot_shell imports
- Arc-Bot-shell imports
- provider/model calls
- tool execution
- file mutation
- browser/network behavior
- device/robotics/physical-world behavior
- durable persistence
- database writes
- background workers, queues, daemons, subprocesses, or threads
- runtime export cleanup
- final API freeze

## Required Runtime Behavior For Future V1-G11

The future runtime slice must prove:

- raw natural language is still not accepted
- only validated candidate metadata can enter the slice
- missing candidate provenance fails closed
- caller-supplied `approved=true` fails closed
- caller-supplied `GuardianDecision` authority fails closed
- unknown action category fails closed
- destructive edit/delete maps to approval-required status, not execution
- model/tool/file/browser/network/device/robotics action claims fail closed or require future policy review
- `ConsequentialActionRequest` carries `request_id`, `intent_id` or candidate reference, `input_id`, `actor_id`, `shell_id`, `action_type`, `target_ref`, `risk_class`, typed args, and evidence refs
- real runtime `GuardianDecision` metadata is produced for reviewed requests
- approval-required decisions do not execute and do not issue approval tokens
- audit/evidence linkage metadata carries `lineage_id`, `decision_id`, `input_id`, `intent_id`, `actor_id`, `shell_id`, `action_type`, `target_ref`, `risk_class`, and redacted summary
- output remains deterministic, local-only, in-process, and side-effect free

## Required Future Acceptance Tests

Future V1-G11 must include tests for:

- safe informational candidate produces a reviewed decision without execution
- planning/drafting candidate stays non-executing
- destructive edit candidate requires operator approval
- destructive delete candidate requires operator approval
- caller-supplied approval claim is blocked
- caller-supplied decision authority is blocked
- stale or replayed candidate is blocked
- missing provenance is blocked
- unknown action type is denied or blocked
- provider/model request is not routed
- file/browser/network/device/robotics claims do not execute
- audit/evidence linkage is present and non-persistent
- no raw secret, raw prompt, raw file contents, or approval PIN/token is emitted

## Rollback Plan

Future V1-G11 must be reversible by removing only:

- `lima/kernel/v1_runtime_request.py`
- `lima/guardian/v1_decision_gate.py`
- candidate exports added to `lima/kernel/__init__.py`
- candidate exports added to `lima/guardian/__init__.py`
- V1-G11 docs/tests/fixtures

Rollback must not require edits to shell repositories, Sparkbot, persistence stores, external services, provider configuration, or production deployments.

## Stop Conditions

Stop before implementation or revert the future implementation if any of these appear:

- file scope exceeds the V1-G11 eligible files
- raw natural language reaches the runtime slice
- request metadata can execute directly
- approval metadata is treated as execution authority
- destructive edit/delete can become approved without operator approval evidence
- `GuardianDecision` can be forged by caller metadata
- provider/model calls are made
- tools, files, browsers, networks, devices, robots, or physical-world systems are invoked
- persistent storage or database writes are added
- shell runtime wiring is added
- Sparkbot code is imported or copied
- runtime exports are cleaned up or frozen
- validation fails

## Boundary Confirmation

- Docs/tests/fixtures-only in V1-G10: yes.
- Runtime implementation approved by V1-G10: no.
- Runtime behavior added by V1-G10: no.
- `lima/` runtime files changed by V1-G10: no.
- `tests/support` changed by V1-G10: no.
- Shell repositories changed by V1-G10: no.
- Provider/model calls added by V1-G10: no.
- Runtime `GuardianDecision` added by V1-G10: no.
- Approval enforcement added by V1-G10: no.
- Durable persistence added by V1-G10: no.
- Haptic device behavior added by V1-G10: no.
- Physical-world behavior added by V1-G10: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.
- V1 product readiness approved: no.

## Recommendation

Recommended next lane: `V1-G11`.

Do not start runtime export cleanup or final freeze. The next product-moving step is an explicitly approved first runtime implementation slice limited to the V1-G11 file-touch map above.
