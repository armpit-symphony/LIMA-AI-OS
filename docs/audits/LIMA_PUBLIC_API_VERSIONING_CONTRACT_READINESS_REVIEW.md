# LIMA Public API Versioning Contract Readiness Review

## Branch

`design-lima-public-api-versioning-contract`

## Base Commit

`112981a938d735127c396e6a20d9dba9c8b30dfd`

## Scope

This readiness review evaluates the design-only public API and versioning contract for future Sparkbot and Arc Bot dependency proof work.

This branch adds only:

- `docs/design/LIMA_PUBLIC_API_VERSIONING_CONTRACT.md`
- `docs/audits/LIMA_PUBLIC_API_VERSIONING_CONTRACT_READINESS_REVIEW.md`

It does not modify `pyproject.toml`, `lima/`, tests/support helpers, consumer repositories, shell wiring, provider/model files, storage/persistence files, adapter files, scheduler/background files, browser/file/process/network behavior, live discovery, device behavior, Robo-OS files, robotics files, drone files, or physical-world behavior.

## Readiness Verdict

PASS.

The design is narrow enough for a later metadata/tests-only implementation branch that documents and tests the current public import manifest and versioning posture.

It does not approve a version bump or runtime behavior.

## Current Baseline Review

Verdict: PASS.

The design correctly records the current baseline:

- package name: `lima-runtime`
- package version: `0.0.1`
- Python requirement: `>=3.11`
- top-level `lima.__all__` exposes only `contracts`
- `from lima.kernel import LimaKernel` works
- current proof-stage imports live under `lima.kernel`

This prevents Sparkbot or Arc proof branches from assuming unreviewed top-level runtime exports.

## Version Stage Review

Verdict: PASS.

The design separates:

- `0.0.x` proof-only runtime candidates
- future `0.1.x` dry-run consumer API candidates
- future `1.0.0` production runtime contracts

It explicitly blocks production, live integration, model/tool/connector, Robo-OS, and physical-world claims for current `0.0.x` work.

## Public API Tier Review

Verdict: PASS.

The design defines:

- Tier 0 import-proof API
- Tier 1 future dry-run consumer API
- Tier 2 future governed runtime API

Tier 0 remains limited to dry-run proof branches. Tier 1 remains future and non-executing. Tier 2 is out of scope.

## Public Import Manifest Review

Verdict: PASS.

The design requires every consumer-visible import to be classified as:

- `proof_public`
- `dry_run_candidate`
- `experimental_internal`
- `forbidden_consumer_import`

It classifies current safe proof imports under `lima.kernel` and blocks `lima.io.*`, `lima.persistence.*`, and direct consumer execution surfaces from being treated as public proof APIs.

## Compatibility And Deprecation Review

Verdict: PASS.

The design requires exact commit/version pinning for `0.0.x` proof branches and requires compatibility review before future `0.1.x` public import or invariant changes.

The deprecation rule prevents silent removal of public dry-run APIs once classified as `dry_run_candidate` or higher.

## Consumer Pinning Review

Verdict: PASS.

The design requires Sparkbot and Arc Bot proof branches to record:

- LIMA repository URL
- LIMA commit
- package name
- package version
- public imports used
- proof branch name
- proof verdict
- non-execution invariant evidence

This matches the current consumer proof archive and intake response lanes.

## Non-Execution Review

Verdict: PASS.

The design carries forward the full current non-execution invariant set and states that no version bump may imply execution unless a separately approved runtime lane implements and audits it.

This preserves fail-closed posture.

## Forbidden Claim Review

Verdict: PASS.

The design forbids version claims for:

- production-ready AI OS
- Sparkbot integration
- Arc Bot integration
- live HumanInput bridge
- raw natural-language execution
- real GuardianDecision authority
- approval enforcement
- model/provider routing
- tool execution
- connector access
- storage/persistence
- live discovery
- connection/pairing
- credential use
- Robo-OS
- device/robot/drone/physical-world control

## Later Implementation Readiness

Verdict: PASS.

The next implementation-shaped branch may be:

`implement-lima-public-api-versioning-metadata`

Allowed files should be limited to:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- `tests/test_lima_public_api_versioning_contract.py`
- `docs/audits/LIMA_PUBLIC_API_VERSIONING_IMPLEMENTATION_AUDIT.md`

`pyproject.toml` may be modified only if a separate audit explicitly approves a metadata-only version declaration change.

## Forbidden Later Surfaces

Verdict: PASS.

The design keeps forbidden:

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

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2576 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except intended design/review docs before commit

## Recommended Next Branch

`audit-lima-public-api-versioning-contract`

That branch should independently audit this design before any public API manifest or versioning metadata implementation begins.
