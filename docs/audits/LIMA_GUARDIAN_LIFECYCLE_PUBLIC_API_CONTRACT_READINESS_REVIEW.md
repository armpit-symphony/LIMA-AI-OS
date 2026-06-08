# LIMA Guardian Lifecycle Public API Contract Readiness Review

## Branch

`design-lima-guardian-lifecycle-public-api-contract`

## Base Commit

`ff1ef9a1017e8710186038067428a396b462bfb1`

## Review Verdict

READY FOR INDEPENDENT AUDIT.

The design is conservative and appropriate for the current readiness stage.

It does not promote Guardian lifecycle preview result objects to proof-public API. It recommends classifying `LimaKernel.preview_guardian_lifecycle(...)` as `method_level_dry_run_candidate` in a later metadata-only implementation branch.

## Scope Review

This branch adds only:

- `docs/design/LIMA_GUARDIAN_LIFECYCLE_PUBLIC_API_CONTRACT.md`
- `docs/audits/LIMA_GUARDIAN_LIFECYCLE_PUBLIC_API_CONTRACT_READINESS_REVIEW.md`

It does not modify:

- `lima/`
- `lima.kernel.__all__`
- top-level `lima`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- public API fixture JSON
- tests
- package metadata
- Sparkbot repositories
- Arc Bot repositories
- provider/model files
- adapter files
- storage/persistence files
- shell wiring files
- Robo-OS wiring files

## Public API Classification Review

The proposed classification is:

`method_level_dry_run_candidate`

This is appropriate because:

- the callable is reachable through proof-public `LimaKernel`
- the behavior is new and should not be treated as stable proof-public API yet
- the return objects are not exported from `lima.kernel.__all__`
- Sparkbot and Arc still need proof packets for existing proof-public APIs first

## Result Object Review

The design keeps these objects internal for now:

- `GuardianLifecyclePreviewResult`
- `IntentEnvelopeCandidatePreview`
- `GuardianRequestPreview`
- `GuardianLifecyclePreviewEvent`

This avoids expanding the compatibility burden before the lifecycle preview is needed by consumer proof branches.

## Non-Execution Review

The design requires future public API metadata or consumer proof use to preserve:

- dry-run only
- no execution
- no dispatch
- no persistence
- no model calls
- no real GuardianDecision
- no approval enforcement
- no ApprovalMetadata recording
- no tool execution
- no connector access
- no event spine persistence
- no HumanInput bridge
- no Sparkbot wiring
- no Arc Bot wiring
- no Robo-OS wiring
- no live discovery
- no connection, pairing, or credential use
- no device control
- no physical-world behavior

This preserves the current Guardian-safe posture.

## Consumer Proof Review

The design correctly says Sparkbot and Arc proof branches should not require lifecycle preview evidence yet.

If a later metadata implementation and audit pass, proof branches may use the method only with explicit evidence:

- exact LIMA commit or version
- method call sample
- dry-run lifecycle preview result sample
- non-execution invariant evidence
- proof no real `IntentEnvelope`, real `GuardianDecision`, approval enforcement, dispatch, persistence, model/tool/connector call, shell wiring, Robo-OS, or physical-world behavior occurred

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

The design is narrow enough for:

`implement-lima-guardian-lifecycle-public-api-metadata`

That later branch should only update:

- public API manifest doc
- public API manifest fixture JSON
- public API tests
- implementation audit report

It should not change runtime behavior or exports.

## Validation Plan

Required validation:

- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git status --short --branch`

## Readiness Decision

Ready for:

`audit-lima-guardian-lifecycle-public-api-contract`

Not ready for:

- implementation until independent audit passes
- proof-public lifecycle preview classification
- top-level runtime exports
- Sparkbot or Arc product integration
- real GuardianDecision authority
- approval enforcement
- model/tool/connector execution
- persistence
- Robo-OS/device/robot/drone/physical-world behavior
