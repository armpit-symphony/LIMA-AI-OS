# LIMA Guardian Decision Authority Public API Metadata Implementation Audit

## Branch

`implement-lima-guardian-decision-authority-public-api-metadata`

## Base Commit

`fe2cce0ebe71b2b3eae23909ebadefccea45a488`

## Files Changed

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- `tests/test_lima_public_api_versioning_contract.py`
- `tests/test_lima_consumer_proof_acceptance_gate_static.py`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_PUBLIC_API_METADATA_IMPLEMENTATION_AUDIT.md`

## Metadata Classification

The manifest now records `LimaKernel.preview_guardian_decision_authority(...)` as a
`method_level_dry_run_candidate`.

This classification is deliberately narrower than proof-public:

- the method is reachable through the already proof-public `LimaKernel`
- the method is not a standalone public export
- decision authority preview result dataclasses remain internal
- the method remains non-authoritative and optional for consumer proof work
- no real `GuardianDecision` authority is created
- no approval enforcement, execution, dispatch, or persistence is approved

## Public Export Status

- No top-level `lima` runtime export is added.
- No `lima.kernel.__all__` symbol is added.
- `GuardianDecisionAuthorityPreview` is not exported.
- `GuardianDecisionAuthorityPreviewEvent` is not exported.
- `GuardianDecisionAuthorityPreviewResult` is not exported.
- `preview_guardian_decision_authority` is not exported as a standalone public symbol.
- `LimaKernel` remains the only proof-public symbol used to reach the method.

## Non-Execution Guarantees

This branch is metadata-only.

It does not modify:

- `lima/`
- runtime behavior
- Guardian policy behavior
- real `GuardianDecision` authority
- approval enforcement
- provider/model routing
- model calls
- tool execution
- connector access
- storage or persistence
- event spine persistence
- adapter behavior
- Sparkbot wiring
- Arc Bot wiring
- Robo-OS wiring
- shell/browser/network/file mutation
- scheduler or background work
- device behavior
- robotics
- drones
- physical-world behavior

## Test Coverage Added

`tests/test_lima_public_api_versioning_contract.py` now verifies:

- both method-level dry-run candidates are documented
- `LimaKernel.preview_guardian_decision_authority(...)` resolves through proof-public `LimaKernel`
- decision authority preview metadata remains non-authoritative
- decision authority preview result dataclasses are not exported from `lima.kernel.__all__`
- the next review gate points to `audit-lima-guardian-decision-authority-public-api-metadata`

`tests/test_lima_consumer_proof_acceptance_gate_static.py` now treats public API method-level candidates as an extensible
manifest set while keeping the consumer acceptance gate's explicit optional-method list authoritative. This prevents a
new method-level candidate from being mistaken for a required consumer proof artifact.

## Forbidden Surfaces Checked

The implementation did not touch:

- public Sparkbot repository files
- Arc Bot repository files
- `lima/`
- provider/model adapters
- storage or persistence
- Guardian enforcement
- approval enforcement
- HumanInput bridge
- Sparkbot or Arc Bot wiring
- Robo-OS wiring
- tool execution
- driver execution
- scheduler/background work
- sockets, shell, browser, network, or file mutation
- device, robot, drone, or physical-world behavior

## Validation Result

PASS.

Validation commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests/test_lima_public_api_versioning_contract.py -p no:cacheprovider` - 14 passed
- `python -m pytest -q tests/test_lima_public_api_versioning_contract.py tests/test_lima_consumer_proof_acceptance_gate_static.py tests/test_lima_consumer_proof_compatibility_freeze_review_static.py tests/test_lima_consumer_proof_intake_ledger_closeout_static.py tests/test_lima_consumer_proof_readiness_closeout_package_static.py tests/test_lima_consumer_proof_ledger_package_readiness_gate_static.py -p no:cacheprovider` - 110 passed
- `python -m pytest -q tests -p no:cacheprovider` - 2863 passed
- `git diff --check` - passed
- `git status --short --branch` - metadata and audit files only before commit

## Remaining Blockers

LIMA still is not ready for Sparkbot or Arc Bot product use.

Remaining blockers include:

- this metadata implementation needs an independent audit
- consumer-owned Sparkbot and Arc Bot dry-run proof packets are still missing
- compatibility freeze remains blocked
- package/version posture still needs review before dependency-readiness claims
- real Guardian decision authority remains unimplemented
- approval enforcement remains unimplemented
- provider/model routing, storage, HumanInput bridge, Sparkbot wiring, Arc Bot wiring, Robo-OS access, live discovery,
  device control, robotics, drones, and physical-world behavior remain forbidden

## Recommended Next Branch

`audit-lima-guardian-decision-authority-public-api-metadata`
