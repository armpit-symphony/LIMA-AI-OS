# LIMA Sparkbot and Arc Request Metadata Contract Readiness Review

## Branch

`design-lima-sparkbot-arc-request-metadata-contract`

## Base Commit

`8563d6ae92be972227dc15a450fdf9d00313a13f`

## Scope

This readiness review evaluates the design-only Sparkbot/Arc normalized request metadata contract.

This branch does not implement behavior. It does not modify `lima/`, tests, examples, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Readiness Verdict

PASS.

The design is narrow enough for independent audit and a later fixture-only implementation lane. It preserves fail-closed, dry-run, normalized-metadata-only behavior and avoids repo coupling.

Recommended next branch:

`audit-lima-sparkbot-arc-request-metadata-contract`

## Does the Design Preserve the Normalized Metadata Boundary?

Yes.

The design requires Sparkbot and Arc to normalize request metadata before calling LIMA. It explicitly rejects raw chat text, raw prompts, raw provider payloads, raw tool payloads, connector records, credentials, unsafe command payloads, live scan dumps, and physical-world command payloads.

Verdict:

- PASS.

## Does It Avoid Sparkbot and Arc Repo Coupling?

Yes.

The design says this lane does not touch the public Sparkbot repo or Arc Bot repository surfaces. It defines handoff notes only.

Verdict:

- PASS.

## Does It Preserve Fail-Closed Behavior?

Yes.

The design requires:

- default-deny capability profiles
- blocked missing required fields in a later implementation
- safe initial categories only
- all unknown action categories blocked until separately designed
- live discovery and connection attempts out of scope
- non-execution invariants asserted by future tests

Verdict:

- PASS.

## Does It Avoid Runtime Execution?

Yes.

The design explicitly forbids:

- model calls
- tool execution
- connector access
- file mutation
- browser control
- network calls
- persistence
- scheduler/background work
- HumanInput live bridge
- IntentEnvelope runtime creation
- Guardian enforcement
- approval enforcement
- device, robot, drone, or physical-world behavior

Verdict:

- PASS.

## Does It Align With Current `KernelRequest`?

Yes.

The design maps shell, actor, session, normalized intent, capability profile, source surface, memory refs, and metadata into current `KernelRequest` fields without requiring runtime changes.

Verdict:

- PASS.

## Does It Keep Guardian Boundaries Intact?

Yes.

The design treats current Guardian output as non-authoritative stub metadata only. It does not approve real `GuardianDecision` creation, approval enforcement, or execution authority.

Verdict:

- PASS.

## Does It Keep Sparkbot and Arc Product Use Honest?

Yes.

The design states LIMA is now dependency-shape ready for local proof, not integration-ready for public Sparkbot or Arc. It also provides archive-ready notes for those teams.

Verdict:

- PASS.

## Is It Narrow Enough for a Later Fixture Implementation?

Yes.

The allowed later branch is limited to:

- synthetic Sparkbot-shaped normalized request fixtures
- synthetic Arc-shaped normalized request fixtures
- focused tests mapping fixtures into existing `KernelRequest`
- dry-run result invariant checks
- an implementation audit report

Verdict:

- PASS.

## Files Allowed in the Later Implementation Branch

Allowed later files:

- `tests/fixtures/sparkbot_arc_request_metadata/`
- `tests/test_lima_sparkbot_arc_request_fixtures.py`
- `docs/audits/LIMA_SPARKBOT_ARC_REQUEST_FIXTURES_IMPLEMENTATION_AUDIT.md`
- optional docs notes under `docs/design/` only if they clarify fixture scope

Any `lima/` runtime change requires separate approval.

## Surfaces That Remain Forbidden

The later fixture branch must not add:

- public Sparkbot repo changes
- Arc Bot repo changes
- production shell wiring
- `lima/` runtime behavior
- provider/model calls
- storage/persistence
- real Guardian enforcement
- real approval enforcement
- live HumanInput bridge
- IntentEnvelope runtime creation
- live adapters
- tool execution
- connector access
- browser control
- file mutation
- network calls
- socket APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- scheduler/background workers
- subprocesses/threads
- device control
- robot/drone control
- physical-world behavior
- credentials or secret storage

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2488 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except intended design docs before commit

## Recommended Next Branch

`audit-lima-sparkbot-arc-request-metadata-contract`

After that audit passes, the next implementation-shaped branch should be:

`implement-lima-sparkbot-arc-request-fixtures`
