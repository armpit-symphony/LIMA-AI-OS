# LIMA Package and Example Shell Contract Readiness Review

## Branch

`design-lima-package-example-shell-contract`

## Base Commit

`0d47974da2297c8485244b3f4848f1038e973736`

## Scope

This readiness review evaluates the design-only package/example-shell contract before any implementation branch.

This branch does not implement packaging changes, example shell code, tests, Sparkbot wiring, Arc Bot wiring, provider/model calls, storage/persistence, live adapters, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Readiness Verdict

PASS for independent audit.

The design is narrow enough to proceed to:

`audit-lima-package-example-shell-contract`

It is not ready for implementation until that independent audit passes.

## Dependency-Readiness Focus

Question: Does the design move LIMA toward future Sparkbot and Arc Bot use?

Answer: Yes.

The design targets the next missing proof: an external-consumer-shaped package and example-shell contract. That is the right next step before Sparkbot or Arc Bot integration because LIMA must first prove that a shell can import it, instantiate `LimaKernel`, pass normalized metadata, and receive a dry-run `ExecutionResult`.

## Design-Only Scope

Question: Does the branch avoid implementation?

Answer: Yes.

The branch is limited to:

- `docs/design/LIMA_PACKAGE_EXAMPLE_SHELL_CONTRACT.md`
- `docs/audits/LIMA_PACKAGE_EXAMPLE_SHELL_CONTRACT_READINESS_REVIEW.md`

No package metadata, example code, tests, runtime code, or shell code is changed in this branch.

## Sparkbot and Arc Bot Boundaries

Question: Does the design avoid touching public Sparkbot or Arc Bot repos?

Answer: Yes.

The design explicitly says:

- no public Sparkbot repo changes
- no Arc Bot repo changes
- no production shell wiring
- no raw chat-to-LIMA execution
- no live integration before package/example-shell proof and audit

It provides team-facing notes that can be archived and delivered separately.

## Example Shell Safety

Question: Does the design keep the future example shell inert?

Answer: Yes.

The future example shell may only:

- import LIMA
- instantiate `LimaKernel`
- construct already-normalized `KernelRequest`
- optionally pass explicit `SimulatedDiscoveryAdapter`
- assert dry-run result invariants
- display redacted synthetic metadata

It must not parse raw natural language, call models, execute tools, mutate files, call networks, connect to devices, use credentials, persist data, run background work, or touch physical-world systems.

## Package Proof Safety

Question: Does the design avoid unsafe package/release behavior?

Answer: Yes.

The design does not approve:

- PyPI publishing
- release tags
- deployment scripts
- Docker images
- external downloads without approval
- public Sparkbot dependency changes
- Arc Bot dependency changes

It allows packaging proof only as a local install/build/import check in a later approved implementation branch.

## Non-Execution Invariants

Question: Does the design preserve LIMA non-execution invariants?

Answer: Yes.

The future example shell must assert that all execution, dispatch, model, adapter, persistence, scheduler, Sparkbot, Robo-OS, and physical-world flags remain false. It may only display dry-run results and synthetic surfaces.

## Exact Files Allowed Later

The later implementation branch may touch only:

- `examples/minimal_shell/README.md`
- `examples/minimal_shell/example_shell.py`
- `tests/test_lima_package_example_shell_contract.py`
- `docs/audits/LIMA_PACKAGE_EXAMPLE_SHELL_IMPLEMENTATION_AUDIT.md`
- `pyproject.toml` only if a packaging proof fails and the minimal metadata fix is required
- existing README/docs only if needed to link the example shell without claiming product readiness

Any `lima/` change requires separate approval.

## Exact Surfaces Still Forbidden

The later implementation branch must not add:

- Sparkbot repo changes
- Arc Bot repo changes
- production shell wiring
- `lima/` runtime behavior
- provider/model calls
- storage/persistence
- real Guardian enforcement
- real approval enforcement
- real HumanInput bridge
- live adapters
- tool execution
- connector access
- browser control
- file mutation
- network calls
- socket APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- scheduler/background workers
- subprocesses/threads
- device control
- robot/drone control
- physical-world behavior
- credentials or secret storage

## Remaining Product-Readiness Blockers

After this design, LIMA still needs:

- independent audit of this contract
- implementation of the local package/example-shell proof
- audit of the implementation
- formal Sparkbot/Arc normalized request metadata contract
- consumer compatibility tests that do not touch the public Sparkbot repo
- real Guardian decision lifecycle design and implementation
- HumanInput/IntentEnvelope runtime bridge
- provider/model harness
- event/spine persistence design
- shell manifest and capability profile contract

## Validation Result

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2479 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only the intended design and readiness review docs before staging.

## Recommended Next Branch

`audit-lima-package-example-shell-contract`

Do not proceed directly to example shell implementation until this contract is independently audited.
