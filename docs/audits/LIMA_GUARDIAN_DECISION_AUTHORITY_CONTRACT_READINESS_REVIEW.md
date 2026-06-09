# LIMA Guardian Decision Authority Contract Readiness Review

## Branch

`design-lima-guardian-decision-authority-contract`

## Base Commit

`200e45569f2890a11d4fc4c3ec090983e894fe00`

## Readiness Verdict

PASS for design-only readiness.

The Guardian decision authority contract is narrow enough to audit. It defines the future authority boundary without
creating authority, enforcing approval, dispatching work, persisting events, calling models, executing tools, accessing
connectors, wiring Sparkbot or Arc Bot, touching Robo-OS, controlling devices, or enabling physical-world behavior.

## Scope Review

This branch adds only:

- `docs/design/LIMA_GUARDIAN_DECISION_AUTHORITY_CONTRACT.md`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_CONTRACT_READINESS_REVIEW.md`

It does not modify:

- `lima/`
- `tests/`
- `tests/support/`
- `pyproject.toml`
- package metadata
- public exports
- public Sparkbot repository files
- Arc Bot repository files
- provider/model files
- adapter files
- storage/persistence files
- shell wiring files
- Robo-OS files

## Does The Design Preserve Guardian Authority Separation?

Yes.

The design separates:

- `KernelRequest` as input metadata
- normalized shell metadata as non-authority
- `IntentEnvelope` candidates as non-authority
- `GuardianRequest` as request-for-review, not a decision
- `GuardianStubDecision` as non-authoritative
- lifecycle preview results as non-authoritative
- `ApprovalMetadata` as evidence, not a decision
- future `GuardianDecision` as the first possible authority record

This prevents shells, adapters, proof packets, lifecycle previews, or approvals from being mistaken for execution
permission.

## Does It Preserve Fail-Closed Behavior?

Yes.

The design requires blocking for missing decisions, unknown statuses, expired/revoked/superseded decisions, scope
mismatch, capability mismatch, target mismatch, approval mismatch, disabled capabilities, approval-bypass wording,
unsafe metadata, and any downstream action requiring an unapproved execution boundary.

Unknown status and unknown scope both block.

## Does It Avoid Runtime Execution?

Yes.

The branch is design-only and does not add:

- real `GuardianDecision` creation
- approval enforcement
- execution approval
- dispatch
- persistence
- model calls
- tool execution
- connector access
- storage
- scheduler/background work
- browser/file/process/network behavior
- live discovery
- device or physical-world behavior

## Does It Preserve Public API Boundaries?

Yes.

The design does not change:

- top-level `lima`
- `lima.kernel.__all__`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- package metadata
- proof-public import set
- method-level dry-run candidate classification for `LimaKernel.preview_guardian_lifecycle(...)`

No new public API is introduced.

## Does It Avoid Sparkbot Coupling?

Yes.

The design keeps Sparkbot as a consumer-owned proof path. It forbids touching the public Sparkbot repository, wiring
Sparkbot routes, calling Sparkbot tools/connectors/models/memory/storage/schedulers, sending Sparkbot messages, or
treating proof packets as production readiness.

## Does It Avoid Arc Bot Coupling?

Yes.

The design keeps Arc Bot / LIMA Office as a consumer-owned proof path. It forbids touching Arc repos, wiring Arc routes,
calling office-system adapters, mutating customer data, triggering schedulers/workers, or sending customer
communications.

## Does It Avoid Robo-OS Unsafe Coupling?

Yes.

The design keeps Robo-OS and physical-world behavior blocked. It does not approve live discovery, connections, pairing,
credentials, device control, robotics, drones, or physical-world actuation.

## Event And Redaction Review

The design defines future event names only. It implements none.

It requires future events to avoid raw prompts, raw chat text, raw office-task text, raw customer records, raw provider
payloads, raw tool arguments, raw connector records, credentials, headers, cookies, tokens, passwords, API keys,
pairing codes, unsafe command payloads, scan dumps, private SSIDs, raw network/device identifiers, precise physical
location, robot/drone command payloads, and actuator payloads.

Durable event persistence remains separately blocked.

## Is It Narrow Enough For Later Implementation?

Yes, if the later branch is limited to non-executing preview metadata.

Allowed later implementation files should be limited to:

- `lima/kernel/guardian_decision_authority.py`
- `lima/kernel/kernel.py` only if adding an explicit preview method is approved
- `lima/kernel/__init__.py` only if safe export review approves a candidate export
- `tests/test_lima_guardian_decision_authority_preview.py`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_PREVIEW_IMPLEMENTATION_AUDIT.md`

Allowed later behavior should be limited to:

- non-authoritative preview metadata
- required-decision classification
- missing/scope/status/approval mismatch blockers
- redacted in-memory/result-local events
- dry-run-only results

## Forbidden Later Surfaces

Forbidden surfaces remain:

- real `GuardianDecision` authority
- approval enforcement
- execution approval
- dispatch
- persistence
- model calls
- provider routing
- tool execution
- connector access
- memory writes
- task-state writes
- storage
- event-spine persistence
- live HumanInput bridge
- raw natural-language parsing
- Sparkbot wiring
- Arc Bot wiring
- Robo-OS wiring
- live adapters
- browser/file/process/network mutation
- sockets
- live discovery
- scanning
- connection attempts
- pairing
- credential use or storage
- scheduler/background workers
- queues, daemons, subprocesses, or threads
- device control
- robotics
- drones
- physical-world behavior

## Validation Run

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests/test_lima_guardian_lifecycle_preview.py -p no:cacheprovider` - passed, 13 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2848 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended design and readiness review files before commit

## Recommended Next Branch

`audit-lima-guardian-decision-authority-contract`
