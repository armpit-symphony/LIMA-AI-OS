# LIMA Guardian Decision Authority Public API Contract

## Purpose

This document defines the public API posture for the new Guardian decision authority preview surface.

The goal is to decide how future Sparkbot and Arc Bot consumer proof branches may treat
`LimaKernel.preview_guardian_decision_authority(...)`, without changing exports, package metadata, public API manifest
metadata, runtime behavior, or consumer repositories in this branch.

This branch is design-only. It does not modify `lima/`, `lima.kernel.__all__`, top-level `lima`,
`docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`, public API fixture JSON, tests, package metadata, runtime behavior,
Sparkbot, Arc Bot, providers, adapters, storage, persistence, shell wiring, live discovery, Robo-OS, devices, robotics,
drones, or physical-world behavior.

## Current Implementation Baseline

The audited implementation branch added:

```python
LimaKernel.preview_guardian_decision_authority(request)
```

Current behavior:

- accepts `KernelRequest` or mapping request metadata
- returns non-authoritative decision-authority preview metadata
- classifies whether future `GuardianDecision` authority would be required
- blocks missing, unknown, revoked, expired, superseded, escalated, mismatched, or overbroad decision-shaped metadata
- blocks approval-required preview metadata without an approval reference
- blocks raw input and authority claims
- returns result-local redacted events
- keeps real `GuardianDecision` absent
- keeps approval enforcement absent
- keeps dispatch and persistence absent
- keeps model/tool/connector execution absent

Current export posture:

- `LimaKernel` is proof-public.
- `preview_guardian_decision_authority(...)` is available as a method on proof-public `LimaKernel`.
- decision authority preview result classes are not exported from `lima.kernel.__all__`.
- top-level `lima` remains unchanged.
- public API manifest has not been updated for this method yet.

## Classification Decision

Recommended classification:

`method_level_dry_run_candidate`

Meaning:

- consumer proof teams may observe the method during LIMA-side review
- consumer proof teams must not depend on it as stable proof-public API yet
- decision authority preview result objects remain internal implementation-preview shapes
- future manifest update is required before Sparkbot or Arc proof packets may treat the method or return objects as
  approved proof-public API
- the method remains optional, not required, for consumer dry-run proof packets

This is more conservative than promoting the method immediately to proof-public.

## Proposed Future Manifest Entry

A future metadata-only implementation may add:

```json
{
  "import": "from lima.kernel import LimaKernel",
  "member": "LimaKernel.preview_guardian_decision_authority",
  "module": "lima.kernel",
  "symbol": "LimaKernel",
  "classification": "method_level_dry_run_candidate",
  "execution_authority": false,
  "public_export_added": false,
  "result_objects_exported": false
}
```

The future metadata implementation must not add these to `lima.kernel.__all__`:

- `GuardianDecisionAuthorityPreview`
- `GuardianDecisionAuthorityPreviewEvent`
- `GuardianDecisionAuthorityPreviewResult`
- `preview_guardian_decision_authority`

Those remain internal implementation-preview objects until separately designed and audited.

## Consumer Proof Use Rules

Until manifest implementation and audit pass, Sparkbot and Arc proof branches should not use
`preview_guardian_decision_authority(...)` as required evidence.

After a future manifest implementation and audit, consumer proof branches may use it only if they record:

- exact LIMA commit or package version
- public API classification in effect
- method call sample
- dry-run decision-authority preview result sample
- non-execution invariant evidence
- proof no real `GuardianDecision` was created
- proof no decision authority was created
- proof no approval was enforced
- proof no dispatch, persistence, model call, tool call, connector access, shell wiring, device action, Robo-OS action,
  robotics, drones, or physical-world behavior occurred

The method must remain optional until it graduates from method-level dry-run candidate status.

## Non-Execution Invariants

Any future manifest update or consumer proof packet involving decision authority preview must preserve:

- `dry_run is True`
- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `guardian_decision_created is False`
- `decision_authority_created is False`
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

The current decision authority preview result shape is not stable proof-public API.

Future public API work should decide whether to:

1. keep raw dataclass result objects internal and document only method-level availability
2. expose selected `to_dict()` fields as proof evidence guidance only
3. expose stable result dataclasses later as `dry_run_candidate`
4. fold selected decision-authority preview metadata into a future broader Guardian preview result

Recommended decision for now:

`keep_result_objects_internal`

Reason:

- Sparkbot and Arc still owe consumer-owned proof packets for existing proof-public APIs.
- decision authority preview is useful but not required for current dry-run dependency proof.
- exposing more objects early creates compatibility burden before real Guardian authority semantics exist.
- keeping result classes internal prevents consumers from treating preview metadata as real decision authority.

## Top-Level Export Rule

Do not add:

```python
from lima import LimaKernel
from lima import GuardianDecisionAuthorityPreviewResult
```

Top-level `lima` should remain narrow until a broader package API policy is approved.

## Method Stability Rule

`LimaKernel.preview_guardian_decision_authority(...)` may be documented as:

- explicit
- dry-run only
- non-authoritative
- fail-closed
- redacted
- in-memory/result-local only
- optional for consumer proof after manifest metadata review
- useful for showing whether future `GuardianDecision` authority would be required

It must not be documented as:

- stable production API
- required for Sparkbot product integration
- required for Arc Bot product integration
- Guardian enforcement
- approval enforcement
- execution authority
- dispatch authority
- persistence authority
- real `GuardianDecision` creation
- proof that future actions may execute

## Consumer Boundary

This public API contract does not change consumer ownership.

Sparkbot remains responsible for:

- raw chat handling
- local redaction
- shell actor/session/source-surface metadata
- consumer-owned proof packet generation
- production route decisions

Arc Bot / LIMA Office remains responsible for:

- raw office-task handling
- customer-data redaction
- tenant/actor/session/source-surface metadata
- consumer-owned proof packet generation
- office workflow integration decisions

This branch does not approve LIMA to touch public Sparkbot or Arc repositories.

## Forbidden Public API Claims

This contract does not allow claims that LIMA is ready for:

- production Sparkbot integration
- production Arc Bot integration
- public Sparkbot release wiring
- raw natural-language execution
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real `GuardianDecision` authority
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

If this design passes audit, the next metadata-only branch may be:

`implement-lima-guardian-decision-authority-public-api-metadata`

That branch may only:

- update `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- update `tests/fixtures/public_api/lima_public_api_manifest.json`
- update public API manifest tests
- add an implementation audit report
- classify `LimaKernel.preview_guardian_decision_authority(...)` as method-level dry-run candidate
- keep decision authority preview dataclasses out of `lima.kernel.__all__`
- avoid top-level `lima` runtime exports

That branch must not:

- modify runtime behavior
- change `LimaKernel.preview_guardian_decision_authority(...)` behavior
- add real `GuardianDecision` authority
- enforce approval
- dispatch work
- persist events
- call models
- execute tools
- access connectors
- wire Sparkbot or Arc Bot
- touch Robo-OS, devices, robotics, drones, or physical-world systems

## Recommended Next Branch

`audit-lima-guardian-decision-authority-public-api-contract`
