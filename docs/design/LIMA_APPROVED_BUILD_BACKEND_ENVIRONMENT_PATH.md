# LIMA Approved Build Backend Environment Path

## Branch

`design-lima-approved-build-backend-environment-path`

## Purpose

This design defines how LIMA can later use an operator-approved environment that provides the declared package build
backend, `setuptools.build_meta`, without blurring the current no-network/no-mutation proof lane.

The active blocker is not package metadata and not LIMA runtime behavior. The blocker is that the current Python 3.12
environment cannot import the declared build backend because `setuptools` is not installed.

This branch is design-only. It does not install dependencies, run `pip install`, run `pip wheel`, run
`python -m build`, create virtual environments, build wheels, build sdists, publish packages, modify `pyproject.toml`,
modify `lima/`, modify tests, modify examples, touch consumer repositories, wire Sparkbot or Arc Bot, call models,
persist data, run live adapters, or add physical-world behavior.

## Current Evidence

`pyproject.toml` currently declares:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "lima-runtime"
version = "0.0.1"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
include = ["lima*"]
```

The backend preflight branch `verify-lima-local-package-build-backend-preflight` found:

- `python -m pip --version` succeeds with pip 25.0.1 on Python 3.12
- `python -m pip show setuptools` returns `Package(s) not found: setuptools`
- direct import of `setuptools.build_meta` fails with `ModuleNotFoundError: No module named 'setuptools'`
- the repo remains clean after the failed preflight

Therefore:

- local no-network wheel proof is still blocked
- package metadata should not be changed to work around the environment
- package build proof should wait for an approved backend environment

## Design Principle

Package build proof must stay separate from dependency installation.

Preflight may inspect the environment. Build proof may use an environment that already has the declared backend. Any
environment preparation that installs or makes `setuptools>=68` available requires explicit operator approval and a
separate branch.

No branch should convert a missing build backend into a silent package metadata change or a hidden dependency install.

## Approved Environment Options

### Option A: Existing Environment With Backend Already Available

Allowed future behavior:

- inspect pip/Python version
- inspect `pip show setuptools`
- import `setuptools.build_meta`
- run no-network wheel proof from a temporary tracked-source copy only if the backend is importable

Default state now:

- blocked because the active environment does not have `setuptools`

Risk:

- low if inspection and build proof remain no-network and temporary-artifact-only

### Option B: Operator-Prepared Local Environment

Allowed future behavior:

- operator prepares an environment outside this branch
- LIMA repo branch verifies the backend is present
- branch records exact evidence and may later run no-network build proof if separately scoped

Default state now:

- not approved for implementation in this design branch

Risk:

- medium because environment preparation can mutate local Python or create side effects if not controlled

Required:

- explicit operator approval
- target environment path or identifier
- confirmation that no wheel/sdist artifacts are committed
- confirmation that package metadata remains unchanged

### Option C: Temporary Isolated Environment Created By An Approved Branch

Allowed future behavior:

- create a temporary isolated environment only after explicit operator approval
- install or provide `setuptools>=68` only if the operator approves the source and network/offline policy
- run build proof from a tracked-source export
- delete or ignore temporary artifacts after recording evidence

Default state now:

- design-only; not approved here

Risk:

- medium/high because environment creation and dependency installation are stateful

Required:

- separate implementation branch
- explicit approval for dependency install and any network use
- no committed virtualenvs, wheels, sdists, caches, build directories, or downloaded packages

### Option D: Offline Wheelhouse Or Pre-Provisioned Build Backend

Allowed future behavior:

- use a pre-provisioned local/offline source for `setuptools>=68` only if the operator identifies and approves it
- verify package identity/version before use
- record source provenance in an audit

Default state now:

- not available in the current repo

Risk:

- medium because unverified local wheels can become supply-chain risk

Required:

- operator-provided source
- provenance record
- no secret material
- no package publication

## Required Approval Record

A later branch that prepares or uses an approved backend environment must record:

- operator approval statement or reference
- target environment
- Python version
- pip version
- `setuptools` version
- backend import result for `setuptools.build_meta`
- whether network access was used
- whether dependency installation occurred
- whether any temporary artifacts were created
- confirmation that no artifacts were committed
- confirmation that `pyproject.toml` was not changed
- confirmation that `lima/` was not changed
- confirmation that no consumer repositories were touched

If any field is missing, the branch must not claim package build readiness.

## Future Build Proof Flow

The later approved flow should be:

1. Confirm branch scope and clean repo.
2. Confirm operator approval if environment preparation is required.
3. Inspect Python and pip version.
4. Inspect `setuptools` presence and version.
5. Import `setuptools.build_meta`.
6. Export tracked source to a temporary directory.
7. Build wheel with no network, no dependency download, and no build isolation only if the backend is already available.
8. Verify wheel appears only in the temporary wheelhouse.
9. Optionally install/import from an isolated consumer-shaped environment only if separately approved.
10. Run repo validation.
11. Record proof and blockers without claiming Sparkbot, Arc Bot, or product readiness.

## Allowed Future Build Command Shape

Only after backend availability is proven:

```powershell
python -m pip wheel --no-index --no-deps --no-build-isolation <temp-src> --wheel-dir <temp-wheelhouse>
```

This command must run only from a temporary tracked-source export, not from a mutated repo tree.

## Forbidden In This Design Branch

This design branch must not:

- install `setuptools`
- run `pip install`
- run `pip wheel`
- run `python -m build`
- create virtual environments
- download dependencies
- access PyPI or registries
- build wheels or sdists
- publish packages
- commit wheel, sdist, build, cache, virtualenv, or wheelhouse artifacts
- modify `pyproject.toml`
- modify package metadata
- modify `lima/`
- modify tests or examples
- touch public Sparkbot
- touch Arc Bot repositories
- touch Robo-OS repositories
- wire Sparkbot or Arc Bot
- add provider/model calls
- add storage or persistence
- add Guardian enforcement
- add HumanInput runtime bridge
- add live adapters
- run shell/browser/network/file mutation behavior
- start background workers, subprocesses, threads, queues, daemons, or schedulers
- use credentials or secrets
- control devices, robots, drones, or physical-world systems

## Acceptance Criteria For A Later Approved Backend Branch

A later implementation or verification branch may pass only if:

- the declared backend `setuptools.build_meta` is importable
- `setuptools` version satisfies `setuptools>=68`
- any environment preparation is explicitly approved
- no package metadata change is made
- no runtime behavior change is made
- no consumer repo is touched
- no wheel/sdist/build artifacts are committed
- repo validation passes
- proof output explicitly distinguishes package build proof from Sparkbot/Arc product readiness

## Sparkbot And Arc Bot Impact

This design does not make LIMA ready for Sparkbot or Arc Bot.

It moves one package-readiness blocker toward closure by defining how to safely obtain or verify the package build
backend needed for a later wheel proof.

Sparkbot and Arc readiness still require:

- local package build proof
- isolated install/import proof
- Sparkbot-owned proof packet
- Arc Bot-owned proof packet
- operator delivery confirmation
- public API compatibility freeze
- product-ready release decision

## Recommended Next Branch

`audit-lima-approved-build-backend-environment-path`

