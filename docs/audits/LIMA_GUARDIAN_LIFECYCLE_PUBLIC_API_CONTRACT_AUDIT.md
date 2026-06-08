# LIMA Guardian Lifecycle Public API Contract Audit

## Branch

`audit-lima-guardian-lifecycle-public-api-contract`

## Base Commit

`a36b66162df1aff4c77c6c14e19313589ae9b9e0`

## Audit Verdict

PASS.

The Guardian lifecycle public API contract is appropriately conservative. It does not promote lifecycle preview result objects to proof-public API. It recommends a future metadata-only branch to classify `LimaKernel.preview_guardian_lifecycle(...)` as `method_level_dry_run_candidate`.

The design is ready for a metadata-only implementation branch.

## Scope And File Safety

The audited design branch added only:

- `docs/design/LIMA_GUARDIAN_LIFECYCLE_PUBLIC_API_CONTRACT.md`
- `docs/audits/LIMA_GUARDIAN_LIFECYCLE_PUBLIC_API_CONTRACT_READINESS_REVIEW.md`

This audit branch adds only:

- `docs/audits/LIMA_GUARDIAN_LIFECYCLE_PUBLIC_API_CONTRACT_AUDIT.md`

The audited design did not modify:

- `lima/`
- `lima.kernel.__all__`
- top-level `lima`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- tests
- package metadata
- public Sparkbot repository files
- Arc Bot repository files
- provider/model files
- adapter files
- storage/persistence files
- shell wiring files
- Robo-OS wiring files

No runtime behavior or public export behavior was changed.

## Current API Baseline Review

The current implementation exposes:

```python
LimaKernel.preview_guardian_lifecycle(request)
```

through the already proof-public `LimaKernel` class.

The implementation does not export these objects from `lima.kernel.__all__`:

- `GuardianLifecyclePreviewResult`
- `IntentEnvelopeCandidatePreview`
- `GuardianRequestPreview`
- `GuardianLifecyclePreviewEvent`

The design correctly treats these as internal implementation-preview objects until later review.

## Classification Review

The proposed classification is:

`method_level_dry_run_candidate`

This is the right classification because:

- the callable is reachable through an existing proof-public class
- the method is new and not yet covered by the public API manifest
- lifecycle preview result objects are not exported through `lima.kernel.__all__`
- Sparkbot and Arc Bot have not yet supplied consumer-owned dry-run proof packets for the current proof-public API
- immediate proof-public promotion would create a premature compatibility obligation

## Public API Model Review

The design proposes a future classification set:

- `proof_public`
- `dry_run_candidate`
- `method_level_dry_run_candidate`
- `experimental_internal`
- `forbidden_consumer_import`

This extends the existing model without weakening it.

The new classification is useful for method-level callables on already-approved public classes where the class is public but the new method behavior remains under review.

## Future Manifest Entry Review

The proposed future manifest entry is appropriate:

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

It records the callable without treating lifecycle preview result classes as proof-public imports.

## Result Object Stability Review

The design recommends:

`keep_result_objects_internal`

This is correct for the current stage.

Reasons:

- consumer proof packets have not been received from Sparkbot or Arc Bot
- lifecycle preview is not required for the current consumer-owned proof path
- return shape stability should not be promised before Guardian lifecycle semantics settle
- keeping raw dataclasses internal avoids unnecessary compatibility burden

## Consumer Proof Review

The design correctly says Sparkbot and Arc Bot proof branches should not require lifecycle preview evidence yet.

If a later metadata implementation and audit pass, consumer teams may use the method only with explicit evidence:

- exact LIMA commit or package version
- method call sample
- dry-run lifecycle preview result sample
- non-execution invariant evidence
- proof no real `IntentEnvelope` was created
- proof no real `GuardianDecision` was created
- proof no approval was enforced
- proof no dispatch, persistence, model call, tool call, connector access, shell wiring, device action, Robo-OS action, robotics, drones, or physical-world behavior occurred

This keeps consumer proof work bounded and audit-friendly.

## Non-Execution Review

The design preserves the required lifecycle preview invariants:

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

No execution or authority claim is introduced by the public API contract.

## Top-Level Export Review

The design correctly forbids adding:

```python
from lima import GuardianLifecyclePreviewResult
from lima import LimaKernel
```

Top-level `lima` should remain narrow.

## Forbidden Surface Review

The design does not approve:

- runtime behavior
- public export changes in this branch
- top-level runtime exports
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

## Implementation Readiness

The next implementation-shaped branch may be:

`implement-lima-guardian-lifecycle-public-api-metadata`

That branch should only:

- update `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- update `tests/fixtures/public_api/lima_public_api_manifest.json`
- update public API manifest tests
- add an implementation audit report
- classify `LimaKernel.preview_guardian_lifecycle(...)` as `method_level_dry_run_candidate`
- keep lifecycle preview dataclasses out of `lima.kernel.__all__`
- avoid top-level `lima` runtime exports

That branch must not:

- modify runtime behavior
- change `LimaKernel.preview_guardian_lifecycle(...)`
- add real GuardianDecision authority
- enforce approval
- dispatch work
- persist events
- call models
- execute tools
- access connectors
- wire Sparkbot or Arc Bot
- touch Robo-OS, devices, robotics, drones, or physical-world systems

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended audit report before commit

## Readiness Decision

Ready for:

`implement-lima-guardian-lifecycle-public-api-metadata`

Not ready for:

- proof-public lifecycle preview promotion
- lifecycle preview dataclass export
- top-level runtime exports
- Sparkbot product integration
- Arc Bot product integration
- public Sparkbot release wiring
- real GuardianDecision authority
- approval enforcement
- model/tool/connector execution
- persistence
- live discovery
- Robo-OS/device/robot/drone/physical-world behavior
