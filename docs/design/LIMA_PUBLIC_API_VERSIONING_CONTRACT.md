# LIMA Public API Versioning Contract

## Purpose

This document defines the future public API and versioning policy needed before LIMA Runtime can be treated as a dependency candidate by Sparkbot, Arc Bot / LIMA AI Office, and other Spark Pit Labs shells.

This branch is design-only. It does not modify `pyproject.toml`, `lima/`, tests/support helpers, packaging behavior, runtime behavior, consumer repositories, shell wiring, provider/model routing, storage, persistence, connectors, tools, browser/file/process/network behavior, live discovery, connection attempts, devices, Robo-OS, robotics, drones, or physical-world behavior.

## Current Baseline

Current package metadata:

- package name: `lima-runtime`
- package version: `0.0.1`
- Python requirement: `>=3.11`
- build backend: `setuptools.build_meta`
- package discovery: `include = ["lima*"]`

Current top-level import posture:

- `import lima` works.
- Top-level `lima.__all__` exposes only `contracts`.
- Top-level `lima` does not re-export `LimaKernel`.

Current kernel import posture:

- `from lima.kernel import LimaKernel` works.
- `from lima.kernel import CapabilityProfile` works.
- `from lima.kernel import KernelRequest` works.
- `from lima.kernel import ExecutionResult` works.
- `from lima.kernel import KernelEvent` works.
- `from lima.kernel import GuardianStubDecision` works.
- `from lima.kernel import SimulatedDiscoveryAdapter` works.

The current repo has already proven local package/example-shell and external-consumer import shapes, but it does not yet define a durable versioning policy for Sparkbot or Arc Bot to depend on.

## Version Stage Definitions

### `0.0.x`: Proof-Only Runtime Candidate

The `0.0.x` line means:

- install/import proof only
- non-executing dry-run kernel proof only
- static contract and fixture compatibility proof only
- no production integration guarantee
- no live shell integration guarantee
- no stable long-term API guarantee without branch-specific audit

Sparkbot and Arc Bot may use a `0.0.x` version or exact commit only for repo-owned proof branches.

They must not use `0.0.x` to claim production readiness, live integration readiness, model/tool/connector readiness, Robo-OS readiness, or physical-world readiness.

### Future `0.1.x`: First Consumer Dry-Run API Candidate

A future `0.1.x` line may be introduced only after a separate implementation and audit branch proves:

- public import manifest is documented and tested
- package metadata exposes the intended version
- example shell proof passes
- external-consumer import proof passes
- Sparkbot/Arc proof handoff packet format is ready
- non-execution invariants remain enforced by tests
- no runtime execution, model calls, tools, connectors, storage, live discovery, shell wiring, or physical-world behavior is added

`0.1.x` should still mean dry-run dependency candidate, not production integration.

### Future `1.0.0`: Production Runtime Contract

`1.0.0` is forbidden until separate product-readiness work proves:

- real Guardian request and decision lifecycle
- explicit approval flow and enforcement
- HumanInput bridge contract and implementation
- model/provider boundary with Guardian gating
- tool/connector boundary with Guardian gating
- event/spine persistence policy and implementation
- storage interface and migration policy
- shell-owned integration audits
- operational runbooks
- rollback/disable procedures
- security/threat-model closeout

This document does not approve any of those features.

## Public API Tiers

### Tier 0: Import-Proof API

Tier 0 is safe only for proof branches.

Allowed:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Allowed behavior:

- construct already-normalized metadata
- call `LimaKernel.evaluate(...)`
- receive dry-run `ExecutionResult`
- optionally call explicit simulated discovery path
- assert non-execution invariants

Forbidden behavior:

- raw natural-language parsing
- live HumanInput ingestion
- real `IntentEnvelope` creation
- real `GuardianDecision` authority
- approval enforcement
- model/provider calls
- tool execution
- connector access
- storage/persistence
- shell wiring
- Sparkbot route wiring
- Arc Bot workflow wiring
- live discovery
- connection attempts
- credential use
- device control
- Robo-OS access
- robotics, drones, or physical-world behavior

### Tier 1: Dry-Run Consumer API

Tier 1 is a future candidate API for Sparkbot and Arc proof branches.

It may include:

- public kernel request/result dataclasses
- capability profile contract
- explicit simulated adapter dependency shape
- public import manifest
- deprecation policy
- compatibility test fixture

Tier 1 must remain non-executing until a later approved lane.

### Tier 2: Governed Runtime API

Tier 2 is future production-directed API work.

It may include real Guardian, HumanInput, provider, connector, spine, storage, and shell integration boundaries only after separate contracts, threat models, implementations, and audits.

Tier 2 is out of scope for this design.

## Public Import Manifest Policy

Every consumer-visible import must be classified as one of:

- `proof_public`
- `dry_run_candidate`
- `experimental_internal`
- `forbidden_consumer_import`

Current proposed classifications:

| Import | Classification | Consumer Guidance |
| --- | --- | --- |
| `import lima` | `proof_public` | Import package only; do not assume top-level runtime exports. |
| `from lima.kernel import LimaKernel` | `proof_public` | Allowed for dry-run proof calls. |
| `from lima.kernel import CapabilityProfile` | `proof_public` | Allowed for default-deny capability profiles. |
| `from lima.kernel import KernelRequest` | `proof_public` | Allowed for already-normalized metadata only. |
| `from lima.kernel import ExecutionResult` | `proof_public` | Allowed for dry-run result assertions. |
| `from lima.kernel import KernelEvent` | `proof_public` | Allowed only as redacted in-memory event metadata. |
| `from lima.kernel import GuardianStubDecision` | `proof_public` | Non-authoritative stub metadata only. |
| `from lima.kernel import SimulatedDiscoveryAdapter` | `proof_public` | Explicit synthetic-only simulated discovery proof path. |
| `from lima.kernel import DiscoveryAdapter*` | `dry_run_candidate` | Adapter shape metadata only; no live discovery. |
| `from lima.kernel import preview_candidate` | `dry_run_candidate` | Candidate preview helper; no execution authority. |
| `from lima.kernel import build_intake_candidate` | `dry_run_candidate` | Non-executing candidate construction only. |
| `from lima.kernel import inspect_runtime_state` | `dry_run_candidate` | Read-only runtime state snapshot only. |
| `lima.io.*` | `forbidden_consumer_import` | Future driver boundary; not consumer proof API. |
| `lima.persistence.*` | `forbidden_consumer_import` | Future persistence boundary; not consumer proof API. |
| `lima.harness.*` | `experimental_internal` | Not approved as direct consumer execution API. |
| `lima.guardian.*` | `experimental_internal` | Not approved as consumer-created authority. |

## Compatibility Rules

For `0.0.x`:

- breaking changes are allowed only with a documented audit note
- consumer proof branches must pin an exact commit or exact package version
- no consumer should float on an unpinned branch
- proof artifacts must record the LIMA commit or version used

For a future `0.1.x`:

- removals or breaking field changes require a compatibility review
- public import changes require a public import manifest update
- result invariant changes require a dedicated non-execution audit
- renamed fields require an explicit migration note
- any new capability must default to disabled/fail-closed

For a future `1.0.0`:

- semantic versioning must apply
- breaking changes require major version changes
- deprecations require at least one minor release window
- security boundary changes require threat-model and Guardian review

## Deprecation Rules

No public dry-run API may be removed silently once it is classified as `dry_run_candidate` or higher.

Deprecation records should include:

- import or field name
- first deprecated version
- removal target version
- replacement import or field
- consumer impact
- non-execution invariant impact
- migration test requirement

Deprecation must not be used to weaken Guardian boundaries or broaden execution.

## Consumer Pinning Rules

Sparkbot and Arc Bot proof branches should record:

- LIMA repository URL
- LIMA commit
- package name
- package version
- public imports used
- proof branch name
- proof verdict
- non-execution invariant evidence

Allowed proof branch names remain:

- `sparkbot-lima-dry-run-boundary-proof`
- `arc-lima-dry-run-boundary-proof`

Consumer proof branches must not claim production readiness from a `0.0.x` or `0.1.x` dry-run candidate.

## Non-Execution Version Invariants

No version bump may imply execution unless an explicitly approved runtime lane implements and audits that behavior.

Current required invariants:

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

## Forbidden Version Claims

Until separately approved, LIMA package versions must not claim:

- production-ready AI OS
- Sparkbot integrated
- Arc Bot integrated
- live HumanInput bridge ready
- raw natural-language execution ready
- real GuardianDecision authority ready
- approval enforcement ready
- model/provider routing ready
- tool execution ready
- connector access ready
- storage/persistence ready
- event spine persistence ready
- live discovery ready
- connection/pairing ready
- credential use ready
- Robo-OS ready
- device/robot/drone/physical-world control ready

## Later Implementation Branch

The next implementation-shaped branch may be:

`implement-lima-public-api-versioning-metadata`

That branch may only add:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- `tests/test_lima_public_api_versioning_contract.py`
- `docs/audits/LIMA_PUBLIC_API_VERSIONING_IMPLEMENTATION_AUDIT.md`

It may modify `pyproject.toml` only if the audit explicitly approves a metadata-only version declaration change.

It must not modify `lima/` runtime behavior.

## Forbidden Later Implementation Surfaces

The later implementation branch must not add:

- Sparkbot repo changes
- Arc Bot repo changes
- runtime behavior
- top-level runtime re-exports without audit
- provider/model calls
- tool execution
- connector access
- storage/persistence
- live HumanInput bridge
- real Guardian enforcement
- approval enforcement
- shell route wiring
- browser/file/process/network actions
- sockets
- live discovery
- connection attempts
- pairing
- credential use or storage
- scheduler/background workers
- subprocesses or threads
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Readiness Verdict

This design is ready for independent audit.

It does not approve a version bump, public API manifest implementation, Sparkbot integration, Arc Bot integration, model calls, tool execution, connector access, storage, live discovery, Robo-OS access, device control, robotics, drones, or physical-world behavior.
