# LIMA Local Package Build Preflight

## Branch

`design-lima-local-package-build-preflight`

## Purpose

This design defines the safe preflight lane for proving local LIMA package build readiness after the 2026-06-09
no-network wheel build proof failed in the current Python environment.

The goal is to separate environment-readiness checks from package-build attempts so LIMA can move toward Sparkbot and
Arc Bot dependency readiness without mutating runtime behavior, installing dependencies without approval, publishing
artifacts, or claiming product readiness early.

This branch is design-only. It does not install packages, build wheels, modify package metadata, modify `lima/`, modify
examples, touch consumer repositories, wire Sparkbot or Arc Bot, call models, persist data, open networks, run live
adapters, or add physical-world behavior.

## Current Failed Evidence

The prior audit branch `audit-lima-local-package-build-proof-2026-06-09` attempted a local wheel build from a temporary
tracked-source archive with:

```powershell
python -m pip wheel --no-index --no-deps --no-build-isolation C:\Users\limap\AppData\Local\Temp\lima_package_build_proof_20260609\src --wheel-dir C:\Users\limap\AppData\Local\Temp\lima_package_build_proof_20260609\wheelhouse
```

The command intentionally avoided:

- network lookup
- dependency download
- build isolation dependency install
- package publication
- source tree mutation

Observed result:

```text
BackendUnavailable: Cannot import 'setuptools.build_meta'
```

Follow-up checks found:

- `pyproject.toml` declares build backend `setuptools.build_meta`.
- `pyproject.toml` declares build requirement `setuptools>=68`.
- `python -m pip show setuptools` reported `Package(s) not found: setuptools`.
- `python -m pip --version` reported `pip 25.0.1` on Python 3.12.
- no wheel was produced.
- the source tree remained clean.

This is a packaging-environment blocker, not a LIMA runtime safety blocker.

## Proof Modes

### Mode A: Repo-Checkout Import and Example Proof

Status: already passing.

This mode verifies from the current checkout:

- `import lima`
- `from lima.kernel import LimaKernel`
- `python -m examples.minimal_shell.example_shell`
- package/example shell contract tests
- external consumer import verification tests

This mode proves import and dry-run API shape from a repository checkout. It does not prove wheel build readiness,
sdist build readiness, editable install readiness, or consumer package install readiness.

### Mode B: Build Backend Preflight Only

Status: next safest verification lane.

This mode may check local environment readiness without installing dependencies or building artifacts:

- `python -m pip --version`
- `python -m pip show setuptools`
- a direct build-backend import check for `setuptools.build_meta`
- optional check that the declared build requirement in `pyproject.toml` remains `setuptools>=68`

Expected output:

- PASS if the declared backend is importable locally.
- FAIL, with explicit blocker, if the declared backend is unavailable.

This mode must not run `pip install`, `pip wheel`, `python -m build`, virtualenv creation, package publication, or
dependency downloads.

### Mode C: Approved Local Build Dependency Path

Status: not approved by this design.

This mode may be considered only after operator approval. It may install or make available the declared local build
backend dependency in a controlled environment.

Minimum approval requirements:

- explicit operator approval for dependency installation or environment preparation
- clear target environment
- no package publication
- no consumer repo mutation
- no runtime behavior changes
- no source-tree artifact commits

Network access remains disallowed unless separately and explicitly approved.

### Mode D: Isolated Build Proof With Backend Already Available

Status: allowed only after Mode B passes or an approved environment provides the backend.

This mode may build from a temporary tracked-source copy using no-network constraints:

- temporary source export from tracked files
- no package metadata edits
- no source tree mutation
- no dependency download
- no publish
- no committed wheel or sdist

Candidate command shape:

```powershell
python -m pip wheel --no-index --no-deps --no-build-isolation <temp-src> --wheel-dir <temp-wheelhouse>
```

Acceptance requires a wheel to be produced in the temporary wheelhouse only, followed by repo validation and a clean
working tree.

## Future Acceptance Criteria

A later local package build proof may pass only if:

- the build backend declared in `pyproject.toml` is available in the build environment
- the build is run from a temporary tracked-source copy or approved isolated environment
- no-network/no-dependency-download constraints are preserved unless separately approved
- no package is published
- no wheel, sdist, build directory, cache, or temporary artifact is committed
- the expected package name remains `lima-runtime`
- the built artifact imports `lima` and `lima.kernel` in an isolated consumer-shaped proof
- `LimaKernel.evaluate(...)` remains dry-run and non-executing
- validation passes
- the branch does not claim Sparkbot, Arc Bot, or product readiness

The expected wheel filename should be derived from packaging metadata and may resemble:

```text
lima_runtime-0.0.1-py3-none-any.whl
```

The exact filename must be verified from the produced artifact, not assumed as readiness proof.

## Forbidden In This Design Branch

This branch must not:

- install `setuptools`
- run `pip install`
- run `pip wheel`
- run `python -m build`
- create virtual environments
- commit wheel or sdist artifacts
- publish packages
- contact PyPI or another registry
- modify `pyproject.toml`
- modify package metadata
- modify `lima/`
- modify public exports
- modify tests or examples
- touch public Sparkbot
- touch Arc Bot repositories
- touch Robo-OS repositories
- add provider or model routing
- call models
- add storage or persistence
- add Guardian enforcement
- add HumanInput runtime bridge
- add live adapters
- execute tools
- call shell, browser, network, or file mutation APIs
- start subprocesses, queues, workers, daemons, threads, or schedulers
- use credentials or secrets
- control devices, robots, drones, or physical-world systems

## Later Implementation Branch Options

After independent audit, the next safe branch should be one of:

- `implement-lima-local-package-build-preflight-static-tests`
- `verify-lima-local-package-build-with-approved-build-backend`

The first option should add static tests around the preflight contract and current failed evidence. The second option
should be used only after the build backend is available or the operator explicitly approves environment preparation.

## Sparkbot and Arc Bot Impact

This preflight does not make LIMA ready for Sparkbot or Arc Bot.

It moves one blocker closer to closure:

- proving LIMA can be packaged and installed as a dependency

Consumer readiness still requires:

- operator delivery confirmation or proof packets
- Sparkbot-owned dependency proof
- Arc Bot-owned dependency proof
- public API compatibility freeze
- no product readiness claims until consumer-owned evidence exists

## Design Verdict

This design is safe for independent audit.

The next branch should be:

`audit-lima-local-package-build-preflight`

