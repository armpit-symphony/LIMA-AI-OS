# LIMA Sparkbot / Arc Dry-Run Boundary Proof Readiness Review

## Branch

`design-lima-sparkbot-arc-dry-run-boundary-proof`

## Base Commit

`25446ab073af4f47caed1d139d2a11ea58bc9fa7`

## Readiness Verdict

PASS for design-only readiness.

The design is narrow enough to hand to Sparkbot and Arc Bot repo teams as proof-branch guidance, while keeping all production integration, live shell wiring, runtime expansion, model/tool/connector behavior, storage, live discovery, Robo-OS access, device control, robotics, drones, and physical-world behavior blocked.

## Scope Review

This branch adds only:

- `docs/design/LIMA_SPARKBOT_ARC_DRY_RUN_BOUNDARY_PROOF.md`
- `docs/audits/LIMA_SPARKBOT_ARC_DRY_RUN_BOUNDARY_PROOF_READINESS_REVIEW.md`

It does not modify:

- `lima/`
- `tests/`
- `tests/support/`
- `pyproject.toml`
- public Sparkbot repository files
- Arc Bot / LIMA Office repository files
- adapter implementation files
- provider/model files
- storage/persistence files
- shell wiring files
- Robo-OS files

## Consumer Repo Boundary

The design preserves repo ownership:

- Sparkbot proof branch must be owned by the Sparkbot repo team.
- Arc proof branch must be owned by the Arc Bot / LIMA Office repo team.
- The LIMA lane provides guidance and review criteria only.
- The LIMA lane must not create, edit, or push consumer repo branches.

## Public API Boundary

The design allows only proof-stage public imports:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

It treats `LimaKernel.preview_guardian_lifecycle(...)` as method-level dry-run candidate metadata only, not a new public result-object API and not Guardian authority.

It blocks consumer imports from internal namespaces including `lima.io.*`, `lima.persistence.*`, `lima.harness.*`, `lima.guardian.*`, `lima.spine.*`, `lima.services.*`, `lima.shells.*`, and `lima.adapters.*`.

## Non-Execution Boundary

The design requires consumer proof packets to preserve:

- no execution
- no dispatch
- no persistence
- no model calls
- no live discovery
- no connection attempts
- no pairing
- no credential use
- no sessions
- no device control
- no physical-world execution
- no GuardianDecision authority
- no approval enforcement
- no HumanInput runtime bridge
- no Sparkbot wiring
- no Robo-OS wiring
- no tool or driver execution
- no scheduler or external calls

This is sufficient for a dry-run dependency proof and insufficient for product integration.

## Simulated Discovery Boundary

The design keeps simulated discovery:

- optional
- explicit
- dry-run only
- simulated only
- synthetic
- inert
- non-connectable
- non-controllable
- local/in-process

Any live discovery, scan, connection, pairing, credential use, device access, Robo-OS access, robotics, drones, or physical-world behavior blocks proof acceptance.

## Guardian Lifecycle Boundary

The design allows lifecycle preview only as:

- `LimaKernel.preview_guardian_lifecycle(...)`
- already-normalized metadata in
- preview metadata out
- no public result dataclass import
- no runtime `IntentEnvelope` authority
- no real `GuardianDecision`
- no approval enforcement
- no execution approval

This preserves the current public API metadata audit outcome.

## Redaction Boundary

The design rejects proof evidence containing:

- raw chat text
- raw office-task text
- raw prompts
- customer records
- connector payloads
- provider payloads
- tool arguments
- credentials
- headers
- cookies
- tokens
- memory records
- file contents
- terminal commands
- live scan dumps
- device identifiers
- precise physical location
- robot/drone command payloads

That is adequate for consumer-owned proof intake.

## Readiness For Consumer-Team Handoff

Ready only for:

- delivering archive-ready proof instructions to Sparkbot repo team
- delivering archive-ready proof instructions to Arc Bot / LIMA Office repo team
- receiving redacted proof packets later
- auditing proof packets later using existing consumer proof intake and results-audit templates

Not ready for:

- public Sparkbot release modification
- Arc Bot product integration
- production integration
- live HumanInput bridge
- raw natural-language execution
- real GuardianDecision authority
- approval enforcement
- provider/model routing
- tool execution
- connector access
- storage/persistence
- event spine persistence
- scheduler/background work
- browser/file/process/network behavior
- live discovery
- connection/pairing
- credential use
- Robo-OS access
- device/robot/drone/physical-world behavior

## Validation Result

Passed on this branch:

- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider` - 2699 passed
- `git diff --check`
- `git status --short --branch`

## Recommended Next Branch

`audit-lima-sparkbot-arc-dry-run-boundary-proof-design`
