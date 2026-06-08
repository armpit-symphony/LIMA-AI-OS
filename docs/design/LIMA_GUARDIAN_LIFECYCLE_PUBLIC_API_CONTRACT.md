# LIMA Guardian Lifecycle Public API Contract

## Purpose

This document defines the public API posture for the new Guardian lifecycle preview surface.

The goal is to decide what future Sparkbot and Arc Bot consumer proof branches may rely on, without changing exports or implementation in this branch.

This branch is design-only. It does not modify `lima/`, `lima.kernel.__all__`, top-level `lima`, `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`, public API fixture JSON, tests, package metadata, runtime behavior, Sparkbot, Arc Bot, providers, adapters, storage, persistence, shell wiring, live discovery, Robo-OS, devices, robotics, drones, or physical-world behavior.

## Current Implementation Baseline

The audited implementation branch added:

```python
LimaKernel.preview_guardian_lifecycle(request)
```

Current behavior:

- accepts `KernelRequest` or mapping request metadata
- returns a non-authoritative dry-run lifecycle preview
- prepares `IntentEnvelopeCandidatePreview`
- prepares `GuardianRequestPreview`
- returns redacted result-local events
- blocks unsafe metadata fail-closed
- keeps real `GuardianDecision` absent
- keeps approval enforcement absent
- keeps dispatch and persistence absent

Current export posture:

- `LimaKernel` is proof-public.
- `preview_guardian_lifecycle(...)` is available as a method on proof-public `LimaKernel`.
- lifecycle preview result classes are not exported from `lima.kernel.__all__`.
- top-level `lima` remains unchanged.
- public API manifest has not been updated yet.

## Classification Decision

Recommended classification:

`method_level_dry_run_candidate`

Meaning:

- consumer proof teams may observe the method during LIMA-side review
- consumer proof teams must not depend on it as stable proof-public API yet
- lifecycle preview result objects remain internal implementation-preview shapes
- future manifest update is required before Sparkbot or Arc Bot proof packets may treat the method or return objects as approved proof-public API

This is more conservative than promoting the method immediately to proof-public.

## Public API Categories

The public API model should add one future classification value:

`method_level_dry_run_candidate`

Definitions:

- `proof_public`: allowed in consumer-owned proof branches without branch-specific API review
- `dry_run_candidate`: module-level import exists but requires branch-specific review before consumer use
- `method_level_dry_run_candidate`: callable available through an existing proof-public object but not yet stable proof-public behavior
- `experimental_internal`: internal module or symbol, not approved for consumer proof use
- `forbidden_consumer_import`: consumers must not import or depend on this surface

## Proposed Future Manifest Entries

Future manifest implementation may add a method-level entry:

```json
{
  "import": "from lima.kernel import LimaKernel",
  "member": "LimaKernel.preview_guardian_lifecycle",
  "module": "lima.kernel",
  "symbol": "LimaKernel",
  "classification": "method_level_dry_run_candidate",
  "execution_authority": false
}
```

Future manifest implementation may leave these as internal until separately approved:

- `lima.kernel.guardian_lifecycle.GuardianLifecyclePreviewResult`
- `lima.kernel.guardian_lifecycle.IntentEnvelopeCandidatePreview`
- `lima.kernel.guardian_lifecycle.GuardianRequestPreview`
- `lima.kernel.guardian_lifecycle.GuardianLifecyclePreviewEvent`

Those symbols must not be added to `lima.kernel.__all__` in the first public API metadata update unless a later audit explicitly approves them.

## Consumer Proof Use Rules

Until manifest implementation and audit pass, Sparkbot and Arc proof branches should not use `preview_guardian_lifecycle(...)` as required evidence.

After a future manifest implementation and audit, consumer proof branches may use it only if they record:

- exact LIMA commit or package version
- public API classification in effect
- method call sample
- dry-run lifecycle preview result sample
- non-execution invariant evidence
- proof no real `IntentEnvelope` was created
- proof no real `GuardianDecision` was created
- proof no approval was enforced
- proof no dispatch, persistence, model call, tool call, connector access, shell wiring, device action, Robo-OS action, robotics, drones, or physical-world behavior occurred

The method must remain optional in consumer proof packets until it graduates from dry-run candidate status.

## Non-Execution Invariants

Any future manifest update or consumer proof packet involving lifecycle preview must preserve:

- `dry_run is True`
- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `guardian_decision_created is False`
- `approval_enforced is False`
- `approval_metadata_recorded is False`
- `tool_execution_allowed is False`
- `connector_access_allowed is False`
- `storage_persistence_allowed is False`
- `event_spine_persistence_allowed is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `arc_bot_wiring_active is False`
- `robo_os_wiring_active is False`
- `live_discovery_executed is False`
- `connection_attempted is False`
- `pairing_attempted is False`
- `credentials_used is False`
- `session_opened is False`
- `device_control_executed is False`
- `physical_world_allowed is False`
- `physical_world_executed is False`

## Result Shape Stability

The current lifecycle preview result shape is not stable proof-public API.

Future public API work should decide whether to:

1. keep raw dataclass result objects internal and document only `to_dict()` fields
2. expose a stable `GuardianLifecyclePreviewResult` as `dry_run_candidate`
3. expose only selected metadata inside existing `ExecutionResult.metadata`

Recommended decision for now:

`keep_result_objects_internal`

Reason:

- Sparkbot and Arc still owe consumer-owned proof packets for existing proof-public APIs.
- lifecycle preview is useful but not required for current dry-run dependency proof.
- exposing more objects too early increases compatibility burden before Guardian runtime authority exists.

## Top-Level Export Rule

Do not add:

```python
from lima import GuardianLifecyclePreviewResult
from lima import LimaKernel
```

Top-level `lima` should remain narrow until a broader package API policy is approved.

## Method Stability Rule

`LimaKernel.preview_guardian_lifecycle(...)` may be documented as:

- explicit
- dry-run only
- non-authoritative
- fail-closed
- redacted
- in-memory only
- optional for consumer proof

It must not be documented as:

- required for Sparkbot product integration
- required for Arc Bot product integration
- stable production API
- Guardian enforcement
- approval enforcement
- execution authority
- dispatch authority
- persistence authority
- real GuardianDecision creation

## Forbidden Public API Claims

This contract does not allow claims that LIMA is ready for:

- production Sparkbot integration
- production Arc Bot integration
- public Sparkbot release wiring
- raw natural-language execution
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real GuardianDecision authority
- approval enforcement
- provider/model calls
- tool execution
- connector access
- storage/persistence
- event spine persistence
- scheduler/background work
- browser/file/process/network actions
- live discovery
- connection attempts
- pairing
- credential use
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Future Implementation Branch

If this design passes audit, the next implementation-shaped branch may be:

`implement-lima-guardian-lifecycle-public-api-metadata`

That branch may only:

- update `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- update `tests/fixtures/public_api/lima_public_api_manifest.json`
- update public API manifest tests
- add an implementation audit report
- classify `LimaKernel.preview_guardian_lifecycle(...)` as method-level dry-run candidate
- keep lifecycle preview dataclasses out of `lima.kernel.__all__`
- avoid top-level `lima` runtime exports

That branch must not:

- modify runtime behavior
- change `LimaKernel.preview_guardian_lifecycle(...)` behavior
- add real GuardianDecision authority
- enforce approval
- dispatch work
- persist events
- call models
- execute tools
- access connectors
- wire Sparkbot or Arc Bot
- touch Robo-OS, devices, robotics, drones, or physical-world systems

## Recommended Next Branch

`audit-lima-guardian-lifecycle-public-api-contract`
