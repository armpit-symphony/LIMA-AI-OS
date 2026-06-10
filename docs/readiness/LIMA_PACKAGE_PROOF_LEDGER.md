# LIMA Package Proof Ledger And Delivery Evidence

## Branch

`docs-lima-package-proof-ledger-and-delivery-evidence`

## Source Checkpoints

This ledger consolidates package proof evidence after:

- consumer readiness source-of-truth checkpoint:
  `7c5841be240f50a59d77fd90fb4b244f235f0c97`
- operator build-backend approval response archive:
  `3e57899587b8f52eb034cc66da02661b5940cdf4`
- operator response archive audit:
  `626195894b698edab9e3309e297b1ad75401786e`
- controlled build-backend verification:
  `16dd7270886f0c08db8464cb696354739ba674c1`
- independent controlled build-backend verification audit:
  `fdff07bd8fa75a8e8ce6d2e6652b07cae5a4665c`

## Package Metadata Summary

Current package metadata from `pyproject.toml`:

- package name: `lima-runtime`
- package version: `0.0.1`
- Python requirement: `>=3.11`
- package include pattern: `lima*`
- package description: Phase 0 contracts for the LIMA Runtime / LIMA Kernel.

## Declared Build Backend

Declared build backend:

- `setuptools.build_meta`

Declared build requirement:

- `setuptools>=68`

The controlled environment verification confirmed `import setuptools.build_meta` passed.

## Controlled Environment Boundary

The controlled build environment was created outside the repository:

- `C:\Users\limap\.lima_build_envs\lima-ai-os-build-backend-20260609`

The isolated install environment was created outside the repository:

- `C:\Users\limap\lima_build_envs\lima-ai-os-isolated-install-20260609-202648`

The build source copy and package artifacts were also outside the repository:

- source copy: `C:\Users\limap\lima_build_sources\lima-ai-os-build-source-20260609-202648`
- artifact root: `C:\Users\limap\lima_build_artifacts\lima-ai-os-build-backend-20260609-202648`

This ledger does not move, copy, normalize, publish, or commit package artifacts.

## Wheel And Sdist Proof Summary

Controlled build command:

- `python -m build --no-isolation --sdist --wheel`

Artifacts produced outside the repository:

- `lima_runtime-0.0.1-py3-none-any.whl`
- `lima_runtime-0.0.1.tar.gz`
- source archive `lima-ai-os-head-source.tar`

Build result:

- PASS. Wheel and sdist were built successfully in the controlled local environment.

## Isolated Install Proof Summary

Isolated install command:

- `pip install --no-index --find-links <artifact-root> lima-runtime==0.0.1`

Install boundary:

- no package index was used
- local wheel artifact only
- install occurred in the isolated environment outside the repository

Install result:

- PASS. `lima-runtime==0.0.1` installed successfully.

## Import Proof Summary

The isolated install proof confirmed:

- `import lima` passed
- `import lima.kernel` passed
- `from lima.kernel import LimaKernel` passed

These import checks prove package importability only. They do not prove product readiness or consumer integration
readiness.

## Validation Summary

The controlled build-backend verification branch passed:

- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider` with 3141 tests
- `git diff --check`
- `git status --short --branch` with a clean working tree after commit

The independent audit branch also passed:

- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider` with 3141 tests
- `git diff --check`
- `git status --short --branch`

## Artifact Handling Rule

Package artifacts are proof evidence only and must not be committed.

Forbidden committed artifacts include:

- wheels
- sdists
- source archives
- `build/`
- `dist/`
- `*.egg-info`
- wheelhouses
- virtual environments
- controlled build environments
- isolated install environments

Any future package proof must keep artifacts outside the repository unless a separate release-packaging policy approves a
different artifact handling path.

## Warning Tracker

Known warning:

- setuptools emitted a deprecation warning for `project.license` as a TOML table.
- The warning states this metadata style must be changed before 2027-02-18.
- This warning is not a current package-proof blocker.
- This warning must be resolved or explicitly dispositioned before release readiness.

## Non-Authorization Statements

Package proof is not runtime integration.

Package proof is not product readiness.

Package proof does not authorize consumer wiring.

Package proof does not authorize Sparkbot, Arc Bot, LIMA Robo OS, LIMA Office, or future shell integration.

Package proof does not authorize provider/model routing, Guardian authority expansion, HumanInput bridge activation,
storage/persistence runtime, connectors, browser/file/network behavior, external sends, live discovery, scanning,
pairing, credential use, device control, robot/drone/IoT/physical-world behavior, or product-readiness claims.

## Current Ledger Verdict

COMPLETE_WITH_AUDIT for controlled package proof evidence.

NOT_READY for runtime integration.

BLOCKED for consumer integration.

NOT_READY for product readiness.

## Recommended Next Branch

`design-lima-public-api-freeze-candidate`
