# V1-G14 Destructive Approval Enforcement Work Order

Date: 2026-06-14
Branch: `v1-g14-destructive-approval-enforcement-approval-request`
Source branch: `v1-g14-destructive-approval-enforcement-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_runtime`

This is a work order only. It does not record operator approval, does not approve runtime implementation, and does not change `lima/`.

## Approval Dependency

V1-G14 implementation may start only after the operator explicitly approves:

`docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_APPROVAL_REQUEST.md`

Until that approval is recorded, the allowed work remains docs/tests/fixtures-only.

## Existing Shapes To Reuse

The implementation must reuse or remain compatible with:

- `lima.contracts.guardian.ConsequentialActionRequest`
- `lima.contracts.guardian.GuardianDecision`
- `lima.contracts.guardian.GuardianDecisionStatus`
- V1-G11 request metadata from `build_v1_runtime_request`
- V1-G11 decision metadata from `review_v1_runtime_request`
- V1-G12 approval evidence fields: `approval_id` and `approval_evidence_ref`
- V1-G12 audit/evidence proof-not-authority flags

Do not create a parallel authorization model. Approval-enforcement metadata is a fail-closed prerequisite proof, not execution authority.

## Implementation Sequence If Approved

1. Add `lima/guardian/v1_approval_enforcement.py`.
2. In that file, add deterministic validators for destructive edit/delete/file-mutation approval evidence metadata.
3. Validate that the request and decision are V1-G11-style metadata and match on request ID, input ID, intent ID, actor ID, shell ID, action type, target reference, and risk class.
4. Validate that the request is destructive edit/delete/file-mutation shaped before the V1-G14 gate can produce an approval-enforcement record.
5. Require sanitized approval metadata with `approval_id`, `approval_evidence_ref`, `approving_actor_ref`, `approval_recorded_at`, `approval_scope`, `tenant_ref`, and `shell_id`.
6. Reject missing, stale, replayed, expired, revoked, denied, superseded, forged, or mismatched approval metadata.
7. Reject raw approval PINs, raw approval tokens, raw secrets, raw prompts, raw file contents, raw customer data, provider credentials, and executable commands.
8. Return a redacted approval-enforcement record with `execution_allowed: false`, `side_effects_allowed: false`, `approval_token_issued: false`, and `approval_enforcement_record_is_authority: false`.
9. Add candidate exports only in `lima/guardian/__init__.py`.
10. Add `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT.md`.
11. Add `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_CLOSEOUT.md`.
12. Add `tests/fixtures/runtime_extraction/v1_g14_destructive_approval_enforcement.json`.
13. Add `tests/test_v1_g14_destructive_approval_enforcement.py`.

## Expected Candidate Runtime Symbols If Approved

The implementation should expose only candidate V1 symbols such as:

- `V1ApprovalEnforcementError`
- `enforce_v1_destructive_approval`

The exact symbol names may change during implementation only if the V1-G14 implementation doc records the reason and tests lock the exported surface.

## Required Rules If Approved

- destructive edit/delete/file-mutation approval enforcement requires V1-G11 request/decision metadata
- approval evidence metadata must be sanitized and scoped
- approval evidence must link to request, decision, tenant, shell, actor, target, and V1-G12 evidence refs
- approval-enforcement records are proof, not authority
- execution and side effects remain disallowed
- approval tokens are never issued
- raw PINs and raw sensitive content fail closed
- provider/model/tool/browser/network/device/robotics claims fail closed
- non-destructive safe requests are not upgraded into destructive approval-enforcement records

## Required Output Boundaries If Approved

The runtime slice may output:

- redacted approval-enforcement dictionaries
- approval evidence references
- request/decision linkage references
- fail-closed error messages without raw sensitive values

The runtime slice must not output:

- raw secrets
- raw prompts
- raw file contents
- raw customer records
- approval PINs
- approval tokens
- provider credentials
- executable commands
- mutation instructions marked approved
- shell dispatch payloads

## Required Validation If Approved

Run at minimum:

- `cmd /c "python3 --version || python --version"`
- `cmd /c "python3 -m compileall lima || python -m compileall lima"`
- focused V1-G14 tests
- `cmd /c "python3 -m pytest -q tests -p no:cacheprovider || python -m pytest -q tests -p no:cacheprovider"`
- `git diff --check`
- `git diff --cached --check` before commit

## Rollback If Approved

Rollback must be possible by removing only:

- `lima/guardian/v1_approval_enforcement.py`
- V1-G14 candidate exports in `lima/guardian/__init__.py`
- V1-G14 docs/tests/fixtures

Rollback must not require shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, or production deployment changes.

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G14 file map
- approval metadata as execution authority
- raw sensitive content persistence
- approval-token issuance
- destructive edit/delete/file-mutation pass-through without approval evidence
- stale, replayed, expired, revoked, denied, superseded, forged, or mismatched approval evidence acceptance
- provider/model calls or routing
- tool execution
- arbitrary file/browser/network/connector behavior
- device, robotics, IoT, drone, robot, humanoid, or physical-world behavior
- live auth/trust lookup or HumanInput bridge activation
- shell runtime wiring
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy
- external database writes or migrations
- queues, workers, daemons, subprocesses, or threads
- runtime export cleanup
- final API freeze
- V1 product-readiness or production-readiness claims

## Boundary Confirmation

- Work order only: yes.
- Operator approval recorded: no.
- Runtime implementation approved by this work order: no.
- Runtime behavior added: no.
- Approval enforcement added: no.
- File mutation behavior added: no.
- Provider/model calls added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/file/network/device/robotics/physical-world behavior added: no.
- External database writes added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Shell repositories changed: no.
- Sparkbot code copied or imported: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.

## Recommended Next Step

Operator decision on the exact V1-G14 approval request.

If approved, create the V1-G14 implementation branch and execute this work order exactly. If not approved, keep LIMA at `CANDIDATE_ONLY` or revise the request.
