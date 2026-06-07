# LIMA Arc-Owned Integration Boundary Audit

## Branch

`audit-lima-arc-owned-integration-boundary`

## Base Commit

`f8ebf76fa9ef1a21e686c543bccf5d18e8413a47`

## Scope

This audit reviews the design-only Arc-owned integration boundary before any LIMA-side Arc fixture work or Arc-owned proof branch begins.

The audited design branch added only:

- `docs/design/LIMA_ARC_OWNED_INTEGRATION_BOUNDARY.md`
- `docs/audits/LIMA_ARC_OWNED_INTEGRATION_BOUNDARY_READINESS_REVIEW.md`

No `lima/` runtime code, tests, fixtures, examples, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior were approved by the design.

## Audit Verdict

PASS.

The design is safe to audit forward because it keeps Arc integration Arc-owned, preserves LIMA's dry-run-only runtime boundary, preserves Arc's stricter office-task posture, avoids production claims, and limits the next LIMA-side branch to handoff fixtures and tests only.

## Scope and File Safety

Verdict: PASS.

The design branch added docs-only files under `docs/design/` and `docs/audits/`.

It did not authorize or require changes to:

- `lima/`
- `tests/support/`
- public Sparkbot repository files
- Arc Bot repository files
- adapter implementation files
- provider/model implementation files
- storage/persistence files
- shell wiring files
- scheduler/background files
- Robo-OS files
- device, robot, drone, or physical-world control surfaces

## Arc Ownership Boundary

Verdict: PASS.

The design states that future Arc integration must be owned by the Arc team in a separate Arc branch. It explicitly forbids this LIMA lane from editing Arc repository files, importing Arc internals, wiring Arc routes, creating Arc tasks, scheduling Arc work, sending Arc messages, or mutating Arc state.

It also keeps public Sparkbot untouched.

## Arc Role and Product Boundary

Verdict: PASS.

The design correctly frames Arc Bot / LIMA AI Office as a guarded office-task consumer.

It explicitly says Arc is not:

- a Sparkbot clone
- a personal workstation shell
- a browser automation surface
- a terminal or code execution surface
- a connector executor
- an approval executor
- a dispatch system
- a scheduler runtime
- an audit persistence system
- a Robo-OS driver
- a robotics or physical-world controller

This preserves Arc's stricter product boundary and avoids inheriting Sparkbot-only workstation affordances.

## Current LIMA Public Surface

Verdict: PASS.

The design accurately frames LIMA as dependency-shaped but not production-ready. It identifies the current usable surfaces as:

- importable `lima`
- importable `lima.kernel`
- `LimaKernel`
- `KernelRequest`
- `CapabilityProfile`
- `ExecutionResult`
- `SimulatedDiscoveryAdapter`
- non-executing dry-run evaluation
- explicit simulated discovery path
- package metadata for `lima-runtime`
- local minimal shell proof
- Sparkbot/Arc normalized metadata fixtures
- shell-owned translator fixtures
- local synthetic external-consumer import proof
- Sparkbot boundary handoff fixtures

The design does not claim production readiness or live Arc integration.

## Dry-Run and Non-Execution Boundary

Verdict: PASS.

The proposed future Arc-owned proof is limited to normalized office-task metadata in and dry-run `ExecutionResult` out.

Required invariants remain:

- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `dry_run is True`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `live_discovery_executed is False`
- `connection_attempted is False`
- `pairing_attempted is False`
- `credentials_used is False`
- `session_opened is False`
- `device_control_executed is False`
- `physical_world_allowed is False`
- `physical_world_executed is False`
- `guardian_decision_created is False`
- `approval_enforced is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `robo_os_wiring_active is False`
- `adapter_active is False`
- `tool_execution_allowed is False`
- `driver_execution_allowed is False`
- `scheduler_active is False`
- `external_calls_allowed is False`

## Input and Redaction Boundary

Verdict: PASS.

The design allows future Arc consumers to send only redacted identity metadata, already-normalized office-task metadata, task candidate metadata, default-deny capability profiles, source-surface metadata, context refs, synthetic/simulated discovery metadata, and redacted approval-boundary hints.

It forbids raw chat text, raw office-task text, prompts, attachments, connector records, provider payloads, tool arguments, credentials, headers, cookies, tokens, unsafe command bodies, live scan dumps, customer records, unredacted HR/finance/legal/medical/regulated data, device serials, physical location, and robot/drone command payloads.

This is stricter than a general shell boundary and fits Arc's office-operations risk profile.

## Guardian Boundary

Verdict: PASS.

The design does not approve real `GuardianDecision` creation, approval enforcement, model/tool/provider execution, connector access, persistence, scheduler execution, external sends, live discovery, or physical-world behavior.

It preserves Guardian as the future syscall boundary while avoiding claims that current LIMA can enforce production approvals.

## Arc-Specific Risk Review

Verdict: PASS.

The design names Arc-specific risk classes that must remain blocked or approval-required until later contracts exist:

- external customer communications
- calendar or scheduling changes
- ticket status changes
- CRM/customer record changes
- document/file mutation
- connector setup or credential use
- admin or IT remediation actions
- background recurring work
- regulated or sensitive customer data access
- device or local office network actions

It does not approve any of these behaviors.

## Production Claim Review

Verdict: PASS.

The design explicitly says LIMA has local dependency-shape proof, not production Arc integration readiness.

It identifies remaining blockers before production Arc use, including:

- audited install/package verification beyond Mode A if needed
- stable public API versioning policy
- real Guardian request/decision lifecycle
- approval-required flow design
- approval enforcement implementation
- HumanInput bridge contract and implementation
- `IntentEnvelope` runtime creation contract and implementation
- provider/model boundary design and implementation
- tool execution boundary design
- connector boundary design
- scheduler/background-work boundary design
- event/spine persistence design
- storage interface implementation
- consumer compatibility test matrix
- Arc-owned integration design and audit
- rollback and disable strategy

## Future LIMA Fixture Lane Review

Verdict: PASS.

The proposed next implementation-shaped branch, `implement-lima-arc-boundary-handoff-fixtures`, is narrow enough if it is limited to:

- Arc handoff fixture metadata inside LIMA tests
- tests validating Arc handoff checklist shape
- tests proving no Arc imports are introduced
- tests proving dry-run invariants remain expected
- implementation audit report

That branch must remain LIMA-local and must not touch Arc repositories or public Sparkbot.

## Forbidden Surfaces

Verdict: PASS.

The design continues to forbid:

- Arc Bot repository changes from this LIMA lane
- public Sparkbot repo changes from this LIMA lane
- production Arc integration
- raw office-task execution
- prompt parsing in LIMA
- customer record mutation
- production route handling
- background agent loops
- scheduled job execution
- model calls
- provider routing
- tool execution
- connector reads/writes
- memory writes
- task state writes
- file writes
- browser control
- process execution
- external sends
- approval enforcement
- real Guardian decisions
- persistence
- live discovery
- network access
- device control
- Robo-OS access
- robot/drone/physical-world behavior
- credentials or secret storage

## Key Findings

- The boundary is correctly repo-owned: Arc integration remains Arc work, not LIMA work.
- The design aligns with existing Arc docs that define Arc as a guarded office-task consumer.
- The design is stricter than Sparkbot where office workflows create higher customer-record, scheduling, and external-write risk.
- The LIMA-side next step is Arc evidence and fixtures, not runtime expansion.
- The repo is still not ready to be described as a plug-and-play production AI OS for Sparkbot or Arc Bot.

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2513 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except intended audit report before commit

## Recommended Next Branch

`implement-lima-arc-boundary-handoff-fixtures`

That branch should not touch Arc Bot repositories or public Sparkbot. It should only add LIMA-local Arc handoff fixtures and tests that prove a future Arc-owned branch can consume normalized dry-run LIMA results without model calls, tool execution, connector access, persistence, scheduler execution, shell wiring, live discovery, device access, Robo-OS access, robotics, drones, or physical-world behavior.
