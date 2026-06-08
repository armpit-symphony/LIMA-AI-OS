# LIMA Sparkbot / Arc Dry-Run Boundary Proof Design Audit

## Branch

`audit-lima-sparkbot-arc-dry-run-boundary-proof-design`

## Base Commit

`2fbe8ebeea3811328e570037cd6b11d34544bff1`

## Audit Verdict

PASS.

The dry-run boundary proof design is safe to use as LIMA-local guidance for future Sparkbot and Arc Bot repo-team-owned proof branches. It preserves the current proof-stage public API, keeps consumer repositories out of this LIMA lane, requires redacted already-normalized metadata, and blocks production integration, runtime expansion, live wiring, model/tool/connector behavior, persistence, live discovery, Robo-OS access, device control, robotics, drones, and physical-world behavior.

## Scope And File Safety

The design branch changed only:

- `docs/design/LIMA_SPARKBOT_ARC_DRY_RUN_BOUNDARY_PROOF.md`
- `docs/audits/LIMA_SPARKBOT_ARC_DRY_RUN_BOUNDARY_PROOF_READINESS_REVIEW.md`

This audit branch adds only:

- `docs/audits/LIMA_SPARKBOT_ARC_DRY_RUN_BOUNDARY_PROOF_DESIGN_AUDIT.md`

No `lima/`, `tests/`, `tests/support/`, package metadata, public Sparkbot repository files, Arc Bot / LIMA Office files, adapter implementation files, provider/model files, storage/persistence files, shell wiring files, Robo-OS files, or physical-world control files are modified.

## Design Boundary Review

The design correctly frames the proof as:

- consumer repo-team owned
- dry-run only
- LIMA-local guidance only
- not product integration
- not public Sparkbot release work
- not Arc Bot production work
- not runtime expansion

The expected consumer-owned branches are:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot / LIMA Office: `arc-lima-dry-run-boundary-proof`

The design explicitly states the LIMA repo team must not create, edit, or push those branches.

## Public API Review

The design allows only current proof-stage public imports:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

This matches `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`.

The design also treats `LimaKernel.preview_guardian_lifecycle(...)` as method-level dry-run candidate metadata only, matching the public API metadata audit. It does not approve lifecycle preview result dataclasses as public imports.

Forbidden consumer imports remain blocked:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Sparkbot Proof Review

The Sparkbot proof shape is appropriately narrow. It requires Sparkbot to prove:

- exact LIMA commit or package reference
- proof-stage imports only
- redacted already-normalized intent metadata
- no raw chat text sent to LIMA
- explicit `LimaKernel.evaluate(...)` dry-run call
- optional explicit `SimulatedDiscoveryAdapter` for synthetic metadata only
- optional `LimaKernel.preview_guardian_lifecycle(...)` preview metadata only
- redacted proof packet with non-execution invariants
- no production route, task flow, model route, connector route, tool route, memory write, storage write, scheduler, external send, browser/file/process/network action, device action, Robo-OS action, robot action, drone action, or physical-world action wired through LIMA

This is sufficient for a dependency dry-run proof and insufficient for production integration, which is the correct boundary.

## Arc Bot Proof Review

The Arc Bot / LIMA Office proof shape is appropriately narrow. It requires Arc to prove:

- exact LIMA commit or package reference
- proof-stage imports only
- redacted already-normalized office-task metadata
- no raw office-task text or customer record payload sent to LIMA
- explicit `LimaKernel.evaluate(...)` dry-run call
- optional explicit `SimulatedDiscoveryAdapter` for synthetic metadata only
- optional `LimaKernel.preview_guardian_lifecycle(...)` preview metadata only
- redacted proof packet with non-execution invariants
- no production route, customer workflow, project mutation, note mutation, form submission, connector route, tool route, model route, memory write, storage write, scheduler, external send, browser/file/process/network action, office-system adapter, device action, Robo-OS action, robot action, drone action, or physical-world action wired through LIMA

This keeps Arc proof work aligned to small-business office control-plane safety and avoids premature office automation behavior.

## Proof Packet Evidence Review

The required proof packet fields are complete enough for LIMA-side intake and results audit:

- consumer repo and branch
- consumer team owner
- LIMA repository URL
- exact LIMA commit or package version
- package name and package version
- import method and public imports used
- redacted already-normalized metadata evidence
- capability profile evidence
- kernel call evidence
- optional simulated discovery evidence
- optional Guardian lifecycle preview evidence
- dry-run result sample
- non-execution invariant evidence
- redaction attestation
- forbidden surface attestation
- rollback or disable plan
- repo-team proof verdict

The design properly rejects production or live-readiness verdicts.

## Non-Execution Invariant Review

The design requires every accepted proof packet to show:

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

Missing evidence is not accepted. Contradictory evidence blocks the proof. This preserves fail-closed review behavior.

## Simulated Discovery Review

The optional simulated discovery path is correctly limited to:

- explicit adapter use
- `dry_run=True`
- `simulated_only=True`
- `discovery_mode="simulated"`
- synthetic surfaces
- inert surfaces
- non-connectable surfaces
- non-controllable surfaces

The design blocks live discovery, scanning, connection attempts, pairing, credential use, device access, Robo-OS access, robotics, drones, and physical-world behavior.

## Guardian Lifecycle Preview Review

The optional lifecycle preview path is correctly limited to:

- `LimaKernel.preview_guardian_lifecycle(...)`
- already-normalized metadata
- preview metadata only
- no lifecycle result dataclass public imports
- no runtime `IntentEnvelope` authority
- no real `GuardianDecision`
- no approval enforcement
- no execution approval
- redacted in-memory/result-local events only

Any claim that lifecycle preview output is a real Guardian decision blocks the proof.

## Redaction Review

The design blocks raw or sensitive evidence including:

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

This is sufficient for a consumer-owned proof handoff and protects Sparkbot/Arc evidence from becoming an unsafe data-ingestion path.

## Forbidden Surfaces Checked

The design does not approve:

- public Sparkbot repo modification from this lane
- Arc Bot repo modification from this lane
- production integration
- live shell wiring
- runtime behavior expansion
- raw natural-language execution
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real GuardianDecision authority
- approval enforcement
- model/provider routing
- tool execution
- connector access
- memory writes
- task-state writes
- storage/persistence
- event spine persistence
- scheduler/background work
- browser/file/process/network actions
- sockets
- live discovery
- connection attempts
- pairing
- credential use/storage
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Readiness Decision

Ready for consumer-team handoff as guidance only.

Not ready for live Sparkbot or Arc integration. Not ready for consumer proof acceptance until redacted proof packets are received and independently audited.

The next LIMA-side action after proof packets arrive should use the existing consumer proof intake and proof-results audit templates. If no packets are available, LIMA should continue with non-runtime readiness hardening rather than inventing consumer evidence.

## Validation Result

Passed on this branch:

- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider` - 2699 passed
- `git diff --check`
- `git status --short --branch`

## Key Findings

- PASS: design is docs-only and LIMA-local.
- PASS: consumer proof branches remain repo-team owned.
- PASS: proof-stage public API imports match the manifest.
- PASS: method-level Guardian lifecycle preview remains non-authoritative.
- PASS: optional simulated discovery remains explicit, synthetic, inert, and dry-run only.
- PASS: non-execution invariants are complete and fail-closed.
- PASS: redaction requirements are explicit.
- PASS: production and live-readiness claims remain blocked.

## Recommended Next Branch

If Sparkbot or Arc proof packets are supplied:

`audit-consumer-owned-proof-results`

If no proof packets are supplied and LIMA continues internally:

`design-lima-dry-run-consumer-compatibility-freeze`
