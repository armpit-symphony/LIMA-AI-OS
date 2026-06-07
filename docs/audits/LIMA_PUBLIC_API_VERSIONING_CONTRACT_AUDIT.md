# LIMA Public API Versioning Contract Audit

## Branch

`audit-lima-public-api-versioning-contract`

## Base Commit

`11772050145c6c1f8924e8ceedacb2e82b628591`

## Scope

This audit independently reviews the public API and versioning contract design before any public API manifest, fixture, metadata, or versioning implementation begins.

This audit branch adds only:

- `docs/audits/LIMA_PUBLIC_API_VERSIONING_CONTRACT_AUDIT.md`

It does not modify `pyproject.toml`, `lima/`, tests/support helpers, consumer repositories, shell wiring, provider/model files, storage/persistence files, adapter files, scheduler/background files, browser/file/process/network behavior, live discovery, device behavior, Robo-OS files, robotics files, drone files, or physical-world behavior.

## Audit Verdict

PASS.

The public API versioning contract is ready for a later metadata/tests-only public API manifest implementation branch.

It does not approve a version bump, package metadata change, top-level runtime re-export, runtime behavior, Sparkbot integration, Arc Bot integration, model calls, tool execution, connector access, persistence, live discovery, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Files Reviewed

Design branch files reviewed:

- `docs/design/LIMA_PUBLIC_API_VERSIONING_CONTRACT.md`
- `docs/audits/LIMA_PUBLIC_API_VERSIONING_CONTRACT_READINESS_REVIEW.md`

Current source/package files inspected:

- `pyproject.toml`
- `lima/__init__.py`
- `lima/kernel/__init__.py`

Diff reviewed from previous audit branch to design commit:

- `112981a938d735127c396e6a20d9dba9c8b30dfd..11772050145c6c1f8924e8ceedacb2e82b628591`

The design branch changed only the approved design and readiness-review docs.

## Scope And File Safety

Verdict: PASS.

The design branch did not modify:

- `pyproject.toml`
- `lima/`
- tests/support helpers
- public Sparkbot repository files
- Arc Bot repository files
- package build behavior
- shell wiring
- provider/model implementation
- storage/persistence implementation
- adapter implementation
- scheduler/background implementation
- browser/file/process/network implementation
- Robo-OS, robotics, drone, or physical-world implementation

## Current Package Baseline Review

Verdict: PASS.

The design correctly records current package metadata:

- package name: `lima-runtime`
- package version: `0.0.1`
- Python requirement: `>=3.11`
- build backend: `setuptools.build_meta`
- package discovery: `include = ["lima*"]`

The audit confirmed the current `pyproject.toml` matches those values.

## Top-Level Import Review

Verdict: PASS.

The design correctly records that:

- `import lima` works.
- top-level `lima.__all__` exposes only `contracts`.
- top-level `lima` does not re-export `LimaKernel`.

The audit confirmed `lima/__init__.py` currently contains:

`__all__ = ["contracts"]`

This prevents Sparkbot or Arc proof branches from assuming unreviewed top-level runtime exports.

## Kernel Import Review

Verdict: PASS.

The design correctly records the current proof-stage kernel imports, including:

- `LimaKernel`
- `CapabilityProfile`
- `KernelRequest`
- `ExecutionResult`
- `KernelEvent`
- `GuardianStubDecision`
- `SimulatedDiscoveryAdapter`

The audit confirmed `lima/kernel/__init__.py` exposes those names through `__all__`.

## Version Stage Review

Verdict: PASS.

The design separates:

- `0.0.x` proof-only runtime candidate
- future `0.1.x` dry-run consumer API candidate
- future `1.0.0` production runtime contract

The `0.0.x` line is correctly scoped to install/import proof, non-executing dry-run kernel proof, static contract/fixture proof, and exact commit/version pinning.

The future `0.1.x` line is correctly blocked behind a separate implementation and audit branch.

The future `1.0.0` line is correctly blocked behind product-readiness work that includes real Guardian lifecycle, approval flow, HumanInput bridge, provider/tool/connector boundaries, event/spine persistence, storage, shell audits, operational runbooks, rollback, and security closeout.

## Public API Tier Review

Verdict: PASS.

The design defines:

- Tier 0: import-proof API
- Tier 1: future dry-run consumer API
- Tier 2: future governed runtime API

Tier 0 remains proof-only and non-executing.

Tier 1 remains future and non-executing.

Tier 2 remains out of scope.

## Public Import Manifest Policy Review

Verdict: PASS.

The design requires every consumer-visible import to be classified as:

- `proof_public`
- `dry_run_candidate`
- `experimental_internal`
- `forbidden_consumer_import`

This is the right intermediate contract before Sparkbot or Arc teams consume LIMA as a dependency candidate.

The design keeps `lima.io.*` and `lima.persistence.*` out of the consumer proof API and prevents `lima.harness.*` or `lima.guardian.*` from being treated as direct consumer execution/authority surfaces.

## Compatibility And Deprecation Review

Verdict: PASS.

The design requires exact commit or exact package version pinning for `0.0.x` proof branches.

It requires future `0.1.x` compatibility review before public import changes, breaking field changes, result invariant changes, or removals.

It also requires deprecation records for public dry-run APIs classified as `dry_run_candidate` or higher.

This gives Sparkbot and Arc teams a stable review discipline without prematurely claiming semantic-versioned production stability.

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

It preserves the expected consumer-owned proof branches:

- `sparkbot-lima-dry-run-boundary-proof`
- `arc-lima-dry-run-boundary-proof`

## Non-Execution Invariant Review

Verdict: PASS.

The design carries forward the full current non-execution invariant set and states that no version bump may imply execution unless explicitly approved, implemented, and audited in a separate runtime lane.

This preserves the current fail-closed posture for Sparkbot and Arc dependency proof work.

## Forbidden Claim Review

Verdict: PASS.

The design forbids package versions from claiming:

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

Search review found these terms only in blocking language, not as approvals.

## Later Implementation Readiness

Verdict: PASS.

The next implementation-shaped branch may be:

`implement-lima-public-api-versioning-metadata`

Allowed files should remain limited to:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- `tests/test_lima_public_api_versioning_contract.py`
- `docs/audits/LIMA_PUBLIC_API_VERSIONING_IMPLEMENTATION_AUDIT.md`

`pyproject.toml` may be modified only if this audit or a later explicit scope approval allows a metadata-only version declaration change. This audit does not approve that change.

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
- `git status --short --branch` - clean except intended audit report before commit

## Key Findings

- The design branch was docs-only.
- The current package remains `lima-runtime` version `0.0.1`.
- Top-level `lima` remains narrow and does not re-export runtime APIs.
- Current proof-stage public kernel imports are documented and bounded.
- The design blocks production/live claims for `0.0.x` and future dry-run candidate versions.
- The design is ready for a manifest/tests-only implementation lane.

## Recommended Next Branch

`implement-lima-public-api-versioning-metadata`

That branch should implement only the public API manifest, fixture, static tests, and implementation audit. It should not change runtime behavior or bump package metadata unless separately approved.
