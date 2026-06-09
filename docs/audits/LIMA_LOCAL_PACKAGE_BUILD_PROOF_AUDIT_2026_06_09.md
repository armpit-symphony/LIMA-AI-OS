# LIMA Local Package Build Proof Audit - 2026-06-09

## Branch

`audit-lima-local-package-build-proof-2026-06-09`

## Base Commit

`0bbf753f2dd6c3a47f9c57af8eafd67a190065bd`

## Audit Verdict

FAIL for local no-network wheel build proof in the current Python environment.

PASS for fail-closed handling and source tree safety.

The current repo still has package metadata, import proof, and a working minimal example shell proof. However, this
audit did not prove local wheel build readiness because the active Python 3.12 environment cannot import the declared
build backend `setuptools.build_meta` when build isolation and network access are disabled.

This is a packaging-environment blocker, not a runtime behavior blocker.

## Files Changed

This branch adds only:

- `docs/audits/LIMA_LOCAL_PACKAGE_BUILD_PROOF_AUDIT_2026_06_09.md`

## Build Proof Attempt

The build proof intentionally used a temporary archive of the tracked source so the repo working tree would not be
mutated by build artifacts.

Temporary path:

`C:\Users\limap\AppData\Local\Temp\lima_package_build_proof_20260609`

Commands attempted:

- create temporary directory
- export current tracked source with `git archive`
- expand the source archive into a temporary source tree
- run:

```powershell
python -m pip wheel --no-index --no-deps --no-build-isolation C:\Users\limap\AppData\Local\Temp\lima_package_build_proof_20260609\src --wheel-dir C:\Users\limap\AppData\Local\Temp\lima_package_build_proof_20260609\wheelhouse
```

The use of `--no-index`, `--no-deps`, and `--no-build-isolation` was intentional:

- no network lookup
- no dependency download
- no package publication
- no environment mutation
- no source tree mutation

## Result

The wheel build failed before producing a wheel.

Observed failure:

```text
BackendUnavailable: Cannot import 'setuptools.build_meta'
```

Follow-up checks:

- `python -m pip show setuptools` reported `Package(s) not found: setuptools`
- `python -m pip --version` reported `pip 25.0.1` on Python 3.12
- the temporary `wheelhouse` directory remained empty
- `git status --short --branch` showed no repo changes before this audit report was added

## Package Metadata Review

Current `pyproject.toml` declares:

- build backend: `setuptools.build_meta`
- build requirement: `setuptools>=68`
- project name: `lima-runtime`
- version: `0.0.1`
- Python requirement: `>=3.11`
- package discovery: `include = ["lima*"]`

The metadata is structurally reasonable, but this audit did not prove a no-network local wheel build because the build
backend is unavailable in the active environment.

## What Remains Proven

The current repo still has these separate proofs:

- `import lima` works.
- `from lima.kernel import LimaKernel` works.
- `examples/minimal_shell/example_shell.py` runs and emits redacted dry-run summaries.
- `tests/test_lima_package_example_shell_contract.py` passes.
- `tests/test_lima_external_consumer_install_verification.py` passes in subprocess-free import verification mode.
- `python -m compileall lima` passes.
- the full pytest suite passes.

These prove import and dependency-shape behavior from the repo checkout, not wheel-build readiness.

## What Is Not Proven

This audit does not prove:

- local wheel build readiness in the current no-network environment
- local sdist build readiness
- editable install readiness
- clean virtualenv install readiness
- published package readiness
- package registry readiness
- Sparkbot dependency-use readiness
- Arc Bot dependency-use readiness
- compatibility freeze readiness
- product readiness

## Runtime Behavior Review

PASS.

This branch does not modify:

- `lima/`
- examples
- tests
- tests/support
- package metadata
- public exports
- public Sparkbot repository files
- Arc Bot repository files
- provider/model implementation
- adapter implementation
- storage/persistence code
- shell wiring
- Robo-OS wiring

No runtime behavior, model call, provider routing, storage, persistence, Guardian enforcement, HumanInput bridge,
Sparkbot wiring, Arc Bot wiring, Robo-OS wiring, live discovery, connection attempt, pairing, credential use, device
control, robotics, drones, or physical-world behavior is added.

## Risk Assessment

This is a SEV-2 dependency-readiness blocker for claiming package build proof from this local environment.

It is not a SEV-1 runtime safety issue because:

- no execution path was added
- no external call was made
- no dependency was downloaded
- no environment install was performed
- no wheel was published
- no consumer repo was touched
- no product readiness claim was made

## Validation Result

PASS for repo validation after the failed package-build proof.

Validation commands run:

- `python -m examples.minimal_shell.example_shell` - passed, emitted redacted dry-run summaries only
- `python -m pytest -q tests/test_lima_package_example_shell_contract.py -p no:cacheprovider` - passed, 9 tests
- `python -m pytest -q tests/test_lima_external_consumer_install_verification.py -p no:cacheprovider` - passed, 7 tests
- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 3078 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only this audit report before commit

## Recommended Next Branch

For packaging proof:

`design-lima-local-package-build-preflight`

That branch should define a safe build-preflight path for one of:

- approving a local build dependency installation for `setuptools>=68`
- using an isolated environment that already has the build backend
- documenting that current proof-stage validation is limited to repo-checkout import proof until build dependencies are available

For Sparkbot/Arc proof readiness, next action remains input-dependent:

- If the operator explicitly confirms manual delivery and no proof packets are supplied:
  `record-lima-consumer-proof-delivery-confirmation-status`
- If Sparkbot or Arc Bot proof packets are supplied:
  `audit-consumer-owned-proof-results`
- If neither input is supplied:
  remain in waiting state and do not claim Sparkbot/Arc readiness.
