# LIMA Public API Freeze Candidate

## Branch

`design-lima-public-api-freeze-candidate`

## Scope

This document defines a candidate public API surface for later consumer proof packets. It is evidence-based and names
only imports that already exist in the current package.

This is not a public API freeze, not runtime integration approval, not consumer wiring approval, and not product
readiness.

## Package Identity

Current package metadata:

- package name: `lima-runtime`
- package version: `0.0.1`
- Python requirement: `>=3.11`
- declared build backend: `setuptools.build_meta`
- declared build requirement: `setuptools>=68`
- package include pattern: `lima*`

Package proof prerequisites now recorded:

- controlled build-backend verification complete
- wheel/sdist proof complete outside the repository
- isolated install/import proof complete with `--no-index`
- package proof ledger complete

## Intended Consumer Imports

Candidate consumer imports are limited to the existing `lima.kernel` export surface.

Allowed candidate import path:

- `from lima.kernel import <exported-name>`

Known proof import:

- `from lima.kernel import LimaKernel`

Current top-level `lima` status:

- `import lima` is allowed for package import proof.
- `lima.__all__` exposes only `contracts`.
- top-level `lima` is not a runtime consumer API in this candidate.
- no consumer should import runtime objects directly from `lima`.

## Current `lima.kernel` Candidate Exports

The following names are exported from `lima.kernel.__all__` today and are candidate-public for proof packet review only:

- `ALLOWED_CANDIDATE_STATUSES`
- `CapabilityProfile`
- `CandidatePreview`
- `CandidateStatusError`
- `DiscoveryAdapterManifest`
- `DiscoveryAdapterRequest`
- `DiscoveryAdapterResult`
- `DiscoveryAdapterSurface`
- `ExecutionResult`
- `GuardianStubDecision`
- `IntakeCandidateError`
- `KernelEvent`
- `KernelRequest`
- `LimaKernel`
- `RuntimeStateSnapshot`
- `SimulatedDiscoveryAdapter`
- `build_intake_candidate`
- `inspect_runtime_state`
- `normalize_candidate_status`
- `preview_candidate`
- `validate_candidate`

These exports remain candidate surfaces until an independent API freeze audit passes. Consumer repos must not treat this
document as a final compatibility guarantee.

## Experimental Versus Candidate-Frozen Surfaces

Candidate-frozen for proof packet planning:

- package identity: `lima-runtime==0.0.1`
- `import lima`
- `import lima.kernel`
- `from lima.kernel import LimaKernel`
- `KernelRequest`
- `CapabilityProfile`
- `ExecutionResult`
- `KernelEvent`
- `GuardianStubDecision`
- `SimulatedDiscoveryAdapter`
- `DiscoveryAdapterManifest`
- `DiscoveryAdapterRequest`
- `DiscoveryAdapterSurface`
- `DiscoveryAdapterResult`

Candidate-public but still experimental:

- candidate metadata helpers:
  - `build_intake_candidate`
  - `normalize_candidate_status`
  - `validate_candidate`
  - `preview_candidate`
  - `inspect_runtime_state`
- helper dataclasses and exceptions:
  - `CandidatePreview`
  - `CandidateStatusError`
  - `IntakeCandidateError`
  - `RuntimeStateSnapshot`
  - `ALLOWED_CANDIDATE_STATUSES`

Not frozen:

- constructor internals
- private helper functions
- reason-code internals not documented here
- event ID formatting details
- metadata extension keys not explicitly named here
- module paths outside exported `lima.kernel` names

## Dry-Run-Only Kernel Behavior

`LimaKernel.evaluate(...)` is a dry-run-only evaluator for already-normalized request metadata.

It may:

- accept a `KernelRequest` or mapping shaped like a `KernelRequest`
- classify safe planning, drafting, informational, or text-preview requests as `proposed`
- classify some consequential capability requests as `approval_required`
- block unknown, disabled, dangerous, authority-claiming, execution-seeking, or unsafe physical/connection requests
- return an `ExecutionResult`
- emit redacted in-memory `KernelEvent` records
- optionally accept an explicit simulated discovery adapter argument for strict simulated-only metadata

It must not:

- parse raw natural language
- ingest live HumanInput
- create real `IntentEnvelope` authority
- create real `GuardianDecision` authority
- enforce approval
- call models
- execute tools
- dispatch adapters
- persist events
- connect to shells
- touch files, browsers, networks, devices, robots, drones, or physical-world systems

## Result State Vocabulary

Candidate result states:

- `proposed`: dry-run preview only; not executable
- `approval_required`: future approval would be required; no approval is enforced and no execution is allowed
- `blocked`: fail-closed denial of the requested path

Required result invariants:

- `executable: false`
- `execution_allowed: false`
- `side_effects_allowed: false`
- `dispatch_allowed: false`
- `persistence_allowed: false`
- `dry_run: true`
- `model_calls_executed: false`
- `live_discovery_executed: false`
- `connection_attempted: false`
- `pairing_attempted: false`
- `credentials_used: false`
- `session_opened: false`
- `device_control_executed: false`
- `physical_world_executed: false`

## Event And Audit Expectations

Candidate events are redacted and in-memory only.

Events must not contain:

- raw prompts
- raw provider payloads
- secrets
- credentials
- tokens
- headers
- pairing codes
- unsafe command payloads
- raw scan dumps
- raw SSIDs marked private or sensitive
- raw Bluetooth MAC addresses
- raw IP/MAC addresses
- device serial numbers
- precise physical location
- robot/drone command payloads

No durable event persistence is part of this freeze candidate.

## Simulated Discovery Boundary

`SimulatedDiscoveryAdapter` is candidate-public only for deterministic, in-process, simulated discovery proof.

Allowed candidate behavior:

- accepts synthetic/inert request metadata
- requires `dry_run=True`
- requires `simulated_only=True`
- returns synthetic/inert simulated surfaces
- keeps all non-execution invariants false
- emits or returns redacted result-local event-style metadata only

Forbidden:

- live discovery
- scanning
- connection attempts
- pairing
- credential use
- sockets
- OS network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- IoT adapters
- Robo-OS adapters
- device control
- robot/drone control
- physical-world behavior
- global adapter registry
- plugin auto-loading
- hidden adapter dispatch

## Forbidden Private And Runtime Surfaces

Consumers must not import or depend on:

- private functions, constants, or helpers beginning with `_`
- non-exported symbols from `lima.kernel.*`
- `lima.adapters`
- `lima.guardian`
- `lima.harness`
- `lima.io`
- `lima.packs`
- `lima.persistence`
- `lima.services`
- `lima.shells`
- `lima.spine`
- build scripts or local verification paths
- tests, fixtures, or test support helpers

## Forbidden Execution Surfaces

This freeze candidate does not authorize:

- Sparkbot wiring
- Arc Bot wiring
- LIMA Robo OS wiring
- LIMA Office wiring
- future shell wiring
- provider/model routing
- model calls
- real Guardian authority
- approval enforcement
- HumanInput bridge activation
- storage/persistence runtime
- connectors
- tool execution
- browser/file/network actions
- external sends
- schedulers or background workers
- live discovery
- scanning
- pairing
- credential use
- device control
- robotics
- drones
- IoT behavior
- physical-world behavior

## Consumer Compatibility Expectations

Sparkbot, Arc Bot, LIMA Robo OS, LIMA Office, and future shells may use this document only to prepare proof packets.

Consumer proof packets must show:

- expected import shape
- expected package version or commit/ref
- normalized metadata examples
- capability profile expectations
- Guardian/approval boundary expectations
- dry-run behavior expectations
- non-execution confirmation
- confirmation that no live product path calls LIMA yet
- validation commands
- independent audit plan

Consumer proof packets must not add live runtime integration.

## Versioning Expectations

Current version `0.0.1` is proof-only.

Before a real API freeze:

- public import paths must be independently audited
- static coverage must verify this freeze candidate
- consumer proof packets must be received and audited
- operator delivery confirmation must be complete
- release readiness must explicitly disposition the setuptools `project.license` TOML table warning before the
  2027-02-18 deadline

Any future compatibility promise must identify:

- package version
- exact exported names
- exact non-execution invariants
- deprecation policy
- consumer proof packet audit status

## Current Verdict

PUBLIC_API_FREEZE_CANDIDATE_ONLY.

This candidate is narrow enough for static coverage and independent audit.

It does not authorize runtime integration, consumer wiring, live execution, or product-readiness claims.

## Recommended Next Branch

`static-lima-public-api-freeze-candidate-coverage`
