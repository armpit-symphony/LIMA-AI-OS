# LIMA Local Package Build Preflight Readiness Review

## Branch

`design-lima-local-package-build-preflight`

## Base Commit

`e207e5d3517da29f214cd7b4d073e227a09edd28`

## Scope

This readiness review evaluates the design-only package build preflight lane before any build-preflight tests,
dependency installation, wheel build, or packaging implementation work begins.

Files added in this branch:

- `docs/design/LIMA_LOCAL_PACKAGE_BUILD_PREFLIGHT.md`
- `docs/audits/LIMA_LOCAL_PACKAGE_BUILD_PREFLIGHT_READINESS_REVIEW.md`

No runtime, package metadata, test, example, consumer repo, adapter, provider, storage, Guardian enforcement,
HumanInput, shell wiring, network, device, robotics, drone, or physical-world behavior is implemented.

## Readiness Verdict

PASS for independent audit.

The design is narrow enough to proceed to:

`audit-lima-local-package-build-preflight`

It is not approval for dependency installation, wheel build execution, package publication, public Sparkbot work, Arc
Bot work, product readiness claims, runtime expansion, model/provider calls, storage, live adapters, or physical-world
behavior.

## Does The Design Preserve The Actual Blocker?

PASS.

The design records the current failed package proof accurately:

- declared backend: `setuptools.build_meta`
- declared build requirement: `setuptools>=68`
- current local `pip show setuptools`: package not found
- failure: `BackendUnavailable: Cannot import 'setuptools.build_meta'`
- no wheel produced
- source tree remained clean

The failure is treated as a packaging-environment blocker, not a runtime behavior issue.

## Does It Avoid Dependency Installation?

PASS.

The design explicitly forbids this branch from running:

- `pip install`
- `pip wheel`
- `python -m build`
- virtualenv creation
- dependency download
- registry access
- package publication

Mode C requires explicit operator approval before any dependency installation or environment preparation.

## Does It Avoid Runtime Behavior?

PASS.

The design forbids changes to:

- `lima/`
- public exports
- package metadata
- examples
- tests
- public Sparkbot
- Arc Bot repositories
- Robo-OS repositories
- providers/models
- storage/persistence
- Guardian enforcement
- HumanInput bridge
- live adapters
- shell/browser/network/file mutation
- background work
- device/robot/drone/physical-world behavior

## Is The Preflight Narrow Enough?

PASS.

The safe next check is Mode B: preflight-only environment inspection. It may inspect whether the declared build backend
is available, but it must not install dependencies or build artifacts.

Allowed future Mode B checks:

- `python -m pip --version`
- `python -m pip show setuptools`
- import check for `setuptools.build_meta`
- metadata check that `pyproject.toml` still declares `setuptools>=68`

Mode B should return a clear PASS/FAIL blocker status and leave the source tree clean.

## What Exact Files Would Be Allowed Later?

For `implement-lima-local-package-build-preflight-static-tests`, allowed files should be limited to:

- `tests/fixtures/local_package_build_preflight/`
- `tests/test_lima_local_package_build_preflight_static.py`
- `docs/audits/LIMA_LOCAL_PACKAGE_BUILD_PREFLIGHT_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

For `verify-lima-local-package-build-with-approved-build-backend`, allowed files should be limited to:

- `docs/audits/LIMA_LOCAL_PACKAGE_BUILD_WITH_APPROVED_BACKEND_AUDIT.md`
- optional temporary paths outside the repo for build artifacts, never committed

Any package metadata change must be separately scoped and reviewed before implementation.

## What Surfaces Remain Forbidden?

Forbidden until separately approved:

- dependency installation
- network dependency download
- package publication
- committed wheel or sdist artifacts
- `pyproject.toml` changes
- `lima/` runtime changes
- public export changes
- tests/support runtime helpers
- public Sparkbot repository changes
- Arc Bot repository changes
- Robo-OS wiring
- provider/model calls
- storage/persistence
- Guardian enforcement
- HumanInput runtime bridge
- live adapters
- tool execution
- shell/browser/network/file mutation
- background workers, subprocesses, threads, queues, daemons, schedulers
- credentials or secret storage
- device control
- robot/drone control
- physical-world behavior

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 3078 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only the two intended docs before commit

## Remaining Blockers To Sparkbot And Arc Bot Use

This preflight does not resolve:

- missing Sparkbot-owned proof packet
- missing Arc Bot-owned proof packet
- missing operator delivery confirmation
- missing wheel-build proof in the active environment
- missing isolated install proof
- missing public API compatibility freeze
- missing product-ready release decision

## Recommended Next Branch

`audit-lima-local-package-build-preflight`

After that audit passes, choose one narrow lane:

- `implement-lima-local-package-build-preflight-static-tests`
- `verify-lima-local-package-build-with-approved-build-backend`
