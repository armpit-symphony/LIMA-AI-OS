# LIMA Guardian Decision Authority Public API Contract Readiness Review

## Branch

`design-lima-guardian-decision-authority-public-api-contract`

## Base Commit

`8532b897138864a1fdca3016b456913cac2998d3`

## Readiness Verdict

PASS for design-only readiness.

The public API contract is conservative. It recommends classifying
`LimaKernel.preview_guardian_decision_authority(...)` as `method_level_dry_run_candidate` only, while keeping internal
decision authority preview result objects out of proof-public imports.

This branch does not change exports, public API manifest metadata, package metadata, runtime behavior, or consumer
repositories.

## Scope Review

This branch adds only:

- `docs/design/LIMA_GUARDIAN_DECISION_AUTHORITY_PUBLIC_API_CONTRACT.md`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_PUBLIC_API_CONTRACT_READINESS_REVIEW.md`

It does not modify:

- `lima/`
- `tests/`
- `tests/support/`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
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

## Does The Design Preserve Public API Boundaries?

Yes.

The design keeps:

- `LimaKernel` proof-public
- `LimaKernel.preview_guardian_decision_authority(...)` as a proposed method-level dry-run candidate only
- result dataclasses internal
- top-level `lima` unchanged
- `lima.kernel.__all__` unchanged
- public API manifest unchanged in this branch

## Does It Avoid Real Guardian Authority Claims?

Yes.

The design explicitly states that the method must not be documented as:

- real `GuardianDecision` creation
- Guardian enforcement
- approval enforcement
- execution authority
- dispatch authority
- persistence authority
- production API

It keeps all current non-execution invariants.

## Does It Preserve Sparkbot And Arc Boundaries?

Yes.

Sparkbot and Arc Bot remain consumer-owned proof paths. The design does not approve touching public Sparkbot or Arc
repositories and does not approve production route wiring, model/tool/connector behavior, storage, external sends, live
discovery, Robo-OS, device control, robotics, drones, or physical-world behavior.

## Is The Result Shape Kept Internal?

Yes.

The design recommends:

`keep_result_objects_internal`

The following must not become proof-public imports in the first metadata update:

- `GuardianDecisionAuthorityPreview`
- `GuardianDecisionAuthorityPreviewEvent`
- `GuardianDecisionAuthorityPreviewResult`
- `preview_guardian_decision_authority`

## Is It Narrow Enough For Metadata Implementation?

Yes.

A later implementation branch should be metadata-only and limited to:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- `tests/test_lima_public_api_versioning_contract.py`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_PUBLIC_API_METADATA_IMPLEMENTATION_AUDIT.md`

It should only classify `LimaKernel.preview_guardian_decision_authority(...)` as method-level dry-run candidate.

## Forbidden Later Surfaces

Forbidden in the later metadata branch:

- runtime behavior changes
- `lima/` implementation changes
- `lima.kernel.__all__` export expansion
- top-level `lima` runtime exports
- decision authority result dataclass public exports
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
- `python -m pytest -q tests/test_lima_guardian_decision_authority_preview.py -p no:cacheprovider` - passed, 15 tests
- `python -m pytest -q tests/test_lima_public_api_versioning_contract.py -p no:cacheprovider` - passed, 14 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2863 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended design and readiness review files before commit

## Recommended Next Branch

`audit-lima-guardian-decision-authority-public-api-contract`
