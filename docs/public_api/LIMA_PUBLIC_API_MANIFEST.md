# LIMA Public API Manifest

## Manifest Status

This manifest records the current proof-stage public API posture for LIMA Runtime consumers.

It is metadata only. It does not change package metadata, modify `lima/`, add runtime behavior, re-export top-level runtime APIs, wire Sparkbot, wire Arc Bot, call models, execute tools, access connectors, persist data, run background work, perform live discovery, connect to devices, invoke Robo-OS, or touch physical-world systems.

## Package Metadata

- package name: `lima-runtime`
- current version: `0.0.1`
- version stage: `proof_only_runtime_candidate`
- Python requirement: `>=3.11`
- package discovery: `include = ["lima*"]`

`0.0.1` is an import and dry-run proof candidate only. It is not a production integration version.

## Top-Level Package Exports

Current top-level `lima` export posture:

- `import lima` is allowed for package import proof.
- `lima.__all__` exposes `contracts`.
- top-level runtime exports are not approved.
- `from lima import LimaKernel` is not a supported proof-stage import.

Consumer proof branches should import runtime proof APIs from `lima.kernel`.

## Public Import Classifications

Every consumer-visible import is classified as one of:

- `proof_public`
- `dry_run_candidate`
- `method_level_dry_run_candidate`
- `experimental_internal`
- `forbidden_consumer_import`

### Proof Public

Proof-public imports are allowed for Sparkbot and Arc Bot repo-owned dry-run proof branches only.

| Import | Classification | Execution Authority |
| --- | --- | --- |
| `import lima` | `proof_public` | none |
| `from lima.kernel import LimaKernel` | `proof_public` | none |
| `from lima.kernel import CapabilityProfile` | `proof_public` | none |
| `from lima.kernel import KernelRequest` | `proof_public` | none |
| `from lima.kernel import ExecutionResult` | `proof_public` | none |
| `from lima.kernel import KernelEvent` | `proof_public` | none |
| `from lima.kernel import GuardianStubDecision` | `proof_public` | none |
| `from lima.kernel import SimulatedDiscoveryAdapter` | `proof_public` | none |

### Dry-Run Candidate

Dry-run candidate imports are visible today but not yet stable for consumer-owned proof branches without branch-specific review.

| Import | Classification | Execution Authority |
| --- | --- | --- |
| `from lima.kernel import ALLOWED_CANDIDATE_STATUSES` | `dry_run_candidate` | none |
| `from lima.kernel import CandidatePreview` | `dry_run_candidate` | none |
| `from lima.kernel import CandidateStatusError` | `dry_run_candidate` | none |
| `from lima.kernel import DiscoveryAdapterManifest` | `dry_run_candidate` | none |
| `from lima.kernel import DiscoveryAdapterRequest` | `dry_run_candidate` | none |
| `from lima.kernel import DiscoveryAdapterResult` | `dry_run_candidate` | none |
| `from lima.kernel import DiscoveryAdapterSurface` | `dry_run_candidate` | none |
| `from lima.kernel import IntakeCandidateError` | `dry_run_candidate` | none |
| `from lima.kernel import RuntimeStateSnapshot` | `dry_run_candidate` | none |
| `from lima.kernel import build_intake_candidate` | `dry_run_candidate` | none |
| `from lima.kernel import inspect_runtime_state` | `dry_run_candidate` | none |
| `from lima.kernel import normalize_candidate_status` | `dry_run_candidate` | none |
| `from lima.kernel import preview_candidate` | `dry_run_candidate` | none |
| `from lima.kernel import validate_candidate` | `dry_run_candidate` | none |

### Method-Level Dry-Run Candidate

Method-level dry-run candidates are existing methods reachable through proof-public symbols, but they are not standalone public exports and do not expose their internal result dataclasses as public API.

| Import | Method | Classification | Execution Authority |
| --- | --- | --- | --- |
| `from lima.kernel import LimaKernel` | `LimaKernel.preview_guardian_lifecycle(...)` | `method_level_dry_run_candidate` | none |
| `from lima.kernel import LimaKernel` | `LimaKernel.preview_guardian_decision_authority(...)` | `method_level_dry_run_candidate` | none |

`LimaKernel.preview_guardian_lifecycle(...)` remains an explicit, dry-run-only Guardian lifecycle preview method for already-normalized `KernelRequest` metadata. Its preview result dataclasses remain internal and are not added to `lima.kernel.__all__`.

`LimaKernel.preview_guardian_decision_authority(...)` remains an explicit, dry-run-only Guardian decision authority preview method for already-normalized `KernelRequest` metadata. Its preview result dataclasses remain internal and are not added to `lima.kernel.__all__`.

## Forbidden Or Internal Consumer Surfaces

The following are not approved consumer proof APIs:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

These surfaces may exist as package namespaces, contracts, stubs, or future internal boundaries, but Sparkbot and Arc proof branches must not treat them as stable public APIs.

## Consumer Pinning Requirements

Sparkbot and Arc Bot proof branches must record:

- LIMA repository URL
- LIMA commit
- package name
- package version
- public imports used
- proof branch name
- proof verdict
- non-execution invariant evidence

Expected proof branches:

- `sparkbot-lima-dry-run-boundary-proof`
- `arc-lima-dry-run-boundary-proof`

## Non-Execution Invariants

Every proof branch that imports this API must preserve:

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

This manifest does not allow claims that LIMA is:

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

## Allowed Consumer Proof Use

Allowed proof-stage use:

- import `lima`
- import proof-public symbols from `lima.kernel`
- construct already-normalized metadata
- call dry-run `LimaKernel.evaluate(...)`
- optionally use explicit `SimulatedDiscoveryAdapter`
- assert non-execution invariants
- archive redacted proof evidence

Forbidden proof-stage use:

- Sparkbot repo changes
- Arc Bot repo changes
- runtime behavior
- top-level runtime re-exports
- raw chat execution
- raw office-task execution
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real GuardianDecision authority
- real Guardian enforcement
- approval enforcement
- provider/model calls
- tool execution
- connector access
- storage/persistence
- shell route wiring
- live discovery
- connection attempts
- pairing
- credential use or storage
- browser/file/process/network actions
- sockets
- scheduler/background workers
- subprocesses or threads
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Next Review Gate

The next safe branch after this manifest implementation is:

`audit-lima-guardian-decision-authority-public-api-metadata`

No package version bump, runtime export change, or Sparkbot/Arc integration should occur before that audit passes.
