# LIMA Controlled Build Backend Environment Verification Audit

## Branch

`verify-lima-controlled-build-backend-environment`

## Base Commit

`626195894b698edab9e3309e297b1ad75401786e`

## Scope

This branch performs the operator-approved controlled local package build-backend verification, wheel/sdist proof, and
isolated install/import proof for LIMA AI OS.

This branch does not modify `lima/`, package metadata, public exports, consumer repositories, Sparkbot, Arc Bot, LIMA
Robo OS, LIMA Office, providers/models, storage, Guardian authority, HumanInput bridges, connectors,
browser/file/network product behavior, external sends, live discovery, scanning, pairing, credential use, device
control, robot/drone/IoT/physical-world behavior, or product-readiness state.

## Approval Chain

The verification is allowed by:

- `docs/LIMA_CONSUMER_READINESS_SOURCE_OF_TRUTH.md`
- `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_RESPONSE_ARCHIVE_SOURCE.md`
- `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_RESPONSE_ARCHIVE_RECORD.md`
- `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_RESPONSE_ARCHIVE_RECORD_AUDIT.md`

The approval is limited to controlled local package proof only.

## Controlled Environment

Controlled build environment:

- `C:\Users\limap\.lima_build_envs\lima-ai-os-build-backend-20260609`

Base Python:

- Python 3.12.10

Build environment tools:

- pip 26.1.2
- setuptools 82.0.1
- build 1.5.0
- wheel 0.47.0

Backend import check:

- `import setuptools.build_meta` passed

Network/dependency installation:

- network access used: yes
- dependency installation used: yes
- installed into controlled build environment only
- no dependency artifacts were committed

## Build Proof

Build source:

- git-archived source copy of this branch, extracted outside the repo
- source root: `C:\Users\limap\lima_build_sources\lima-ai-os-build-source-20260609-202648`

Artifact root:

- `C:\Users\limap\lima_build_artifacts\lima-ai-os-build-backend-20260609-202648`

Build command:

- controlled environment Python
- `python -m build --no-isolation --sdist --wheel`
- output directory outside the repo

Artifacts produced outside the repo:

- `lima_runtime-0.0.1-py3-none-any.whl`
- `lima_runtime-0.0.1.tar.gz`
- source archive `lima-ai-os-head-source.tar`

Artifact sizes:

- wheel: 94,873 bytes
- sdist: 380,962 bytes
- source archive: 10,147,840 bytes

Build result:

- PASS. Wheel and sdist were built successfully.

Build warning:

- setuptools emitted a deprecation warning for `project.license` as a TOML table.
- The warning states this metadata style must be changed before 2027-02-18.
- This is not a blocker for the current proof, but it should be tracked before a future release-readiness decision.

## Isolated Install And Import Proof

Isolated install environment:

- `C:\Users\limap\lima_build_envs\lima-ai-os-isolated-install-20260609-202648`

Install command:

- `pip install --no-index --find-links <artifact-root> lima-runtime==0.0.1`

Network use during install proof:

- no index used
- local wheel artifact only

Install result:

- PASS. `lima-runtime==0.0.1` installed successfully.

Import checks:

- `import lima` passed
- `import lima.kernel` passed
- `from lima.kernel import LimaKernel` passed

Installed package metadata:

- name: `lima-runtime`
- version: `0.0.1`
- location: isolated install environment site-packages

## Repository Cleanliness

PASS.

Build artifacts, source archive, source copy, and isolated install environment were kept outside the repo.

No generated wheel, sdist, build directory, source archive, virtual environment, cache, or wheelhouse artifact is
committed.

## Consumer Readiness Boundary

This proof does not make LIMA ready for Sparkbot, Arc Bot, LIMA Robo OS, LIMA Office, or future shell integration.

Consumer repos remain readiness/proof-only until:

- public API compatibility freeze is complete
- Sparkbot-owned proof packet audit is complete
- Arc Bot-owned proof packet audit is complete
- LIMA Robo OS proof packet audit is complete if Robo OS integration is in scope
- LIMA Office proof packet audit is complete if Office integration is in scope
- any future shell has its own proof packet audit
- operator delivery confirmation is complete
- product-ready release decision is complete

## Forbidden Surfaces Checked

This branch does not add:

- Sparkbot wiring
- Arc Bot wiring
- LIMA Robo OS wiring
- LIMA Office wiring
- future shell wiring
- runtime integration
- provider/model behavior changes
- Guardian authority expansion
- HumanInput bridge activation
- connector actions
- browser/file/network product actions
- external sends
- live discovery
- scanning
- pairing
- credential use
- device control
- robot/drone/IoT/physical-world behavior
- product-readiness claims

## Validation Result

PASS.

Commands run after this report was added:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 3141 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only this verification audit report before commit

## Verification Verdict

PASS for package build-backend verification, wheel/sdist proof, and isolated install/import proof.

Not ready for consumer integration.

## Recommended Next Branch

`audit-lima-controlled-build-backend-environment-verification`
