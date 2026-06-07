# LIMA Package and Example Shell Contract Audit

## Branch

`audit-lima-package-example-shell-contract`

## Base Commit

`df7cfaebd9685f19421be22207795a736a3b32d1`

## Scope

This independent audit reviews the package/example-shell contract before any example shell implementation, packaging proof, Sparkbot contract work, Arc Bot contract work, or runtime expansion begins.

This branch does not implement behavior. It does not modify `lima/`, tests, tests/support, package metadata, example shell files, Sparkbot wiring, Arc Bot wiring, provider/model files, storage/persistence files, live adapters, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Audit Verdict

PASS.

The design is safe to proceed to a narrow implementation proof:

`implement-lima-package-example-shell-proof`

The later implementation must remain limited to local package/example-shell proof artifacts. It must not touch the public Sparkbot repository, Arc Bot repositories, production shell wiring, `lima/` runtime behavior, provider/model calls, storage/persistence, live adapters, connector behavior, network access, credentials, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## 1. Scope and File Safety

The design branch added only:

- `docs/design/LIMA_PACKAGE_EXAMPLE_SHELL_CONTRACT.md`
- `docs/audits/LIMA_PACKAGE_EXAMPLE_SHELL_CONTRACT_READINESS_REVIEW.md`

Confirmed untouched by the design branch:

- `lima/`
- `tests/`
- `tests/support/`
- `pyproject.toml`
- `examples/`
- public Sparkbot repo
- Arc Bot repo surfaces
- provider/model implementation
- storage/persistence implementation
- Sparkbot/Arc/Robo-OS wiring

Audit finding:

- PASS. The branch stayed docs-only.

## 2. Dependency-Readiness Focus

The design targets the correct next readiness gap:

- prove LIMA can be packaged or imported as a dependency
- prove a local separate example shell can instantiate `LimaKernel`
- prove normalized metadata can be passed into `LimaKernel.evaluate(...)`
- prove optional explicit `SimulatedDiscoveryAdapter` use works from a shell-shaped caller
- prove output remains a dry-run `ExecutionResult`
- prove no execution or live integration occurs

Audit finding:

- PASS. This is aligned with getting LIMA ready for future Sparkbot and Arc Bot use without prematurely touching those repos.

## 3. Package Baseline Review

Current `pyproject.toml` already declares:

- project name: `lima-runtime`
- version: `0.0.1`
- Python: `>=3.11`
- build backend: `setuptools.build_meta`
- package discovery: `include = ["lima*"]`

The design requires the later implementation to verify current metadata first and change `pyproject.toml` only if a package proof fails for a specific minimal reason.

Audit finding:

- PASS. The design avoids packaging churn and does not authorize publishing.

## 4. Example Shell Contract Review

The future example shell is constrained to:

- local repo path `examples/minimal_shell/`
- deterministic inert Python example
- imports from `lima` only
- already-normalized `KernelRequest`
- dry-run `LimaKernel.evaluate(...)`
- optional explicit `SimulatedDiscoveryAdapter`
- dry-run invariant assertions
- redacted synthetic metadata display

The example shell must not:

- parse raw natural language
- import Sparkbot
- import Arc Bot
- call models/providers
- execute tools
- mutate files
- call networks
- connect to devices
- scan
- pair
- use credentials
- persist data
- start subprocesses/threads/workers/schedulers
- wire Robo-OS
- touch physical-world systems

Audit finding:

- PASS. The example shell contract is inert and dependency-shaped, not integration-shaped.

## 5. Sparkbot and Arc Bot Boundary Review

The design explicitly avoids:

- public Sparkbot repo changes
- Arc Bot repo changes
- Sparkbot production route wiring
- Arc Bot production workflow wiring
- raw chat-to-LIMA execution
- live HumanInput bridge
- model routing through LIMA
- tool calls through LIMA
- connector access through LIMA
- persistence through LIMA
- approval enforcement through LIMA
- real GuardianDecision creation through LIMA
- live discovery or device connection

Team-facing handoff notes are present and appropriate:

- LIMA is moving toward dependency-readiness, not integration-readiness.
- The first expected consumer shape is normalized metadata in, dry-run result out.
- Sparkbot/Arc should not send raw chat text into LIMA for execution.
- Sparkbot/Arc should not expect LIMA to call models, tools, connectors, storage, or devices yet.

Audit finding:

- PASS. The design preserves repo ownership boundaries and consumer-team separation.

## 6. Non-Execution Invariants

The future example shell must assert all non-execution fields remain safe, including:

- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `dry_run is True`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `live_discovery_executed is False`
- `connection_attempted is False`
- `pairing_attempted is False`
- `credentials_used is False`
- `session_opened is False`
- `device_control_executed is False`
- `physical_world_allowed is False`
- `physical_world_executed is False`
- `guardian_decision_created is False`
- `approval_enforced is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `robo_os_wiring_active is False`
- `adapter_active is False`
- `tool_execution_allowed is False`
- `driver_execution_allowed is False`
- `scheduler_active is False`
- `external_calls_allowed is False`

Audit finding:

- PASS. The required future example shell proof is built around non-execution evidence.

## 7. Future Acceptance Test Review

The design requires later tests to prove:

- `import lima` works
- `from lima.kernel import LimaKernel` works
- package metadata still declares `lima-runtime`
- example shell imports only from `lima`
- example shell creates already-normalized `KernelRequest`
- example shell receives dry-run `ExecutionResult`
- simulated example shell path returns synthetic surfaces only
- non-execution invariants remain false
- example shell does not import Sparkbot
- example shell does not import Arc Bot
- example shell does not import Robo-OS
- example shell does not use sockets, network APIs, subprocesses, threads, schedulers, storage, providers, model APIs, browser APIs, USB/serial/Bluetooth/MQTT/Matter/mDNS APIs, or device/robot/drone control

Audit finding:

- PASS. The test scope is specific enough for a later implementation branch.

## 8. Allowed Future Files

The later implementation branch may touch only:

- `examples/minimal_shell/README.md`
- `examples/minimal_shell/example_shell.py`
- `tests/test_lima_package_example_shell_contract.py`
- `docs/audits/LIMA_PACKAGE_EXAMPLE_SHELL_IMPLEMENTATION_AUDIT.md`
- `pyproject.toml` only if a packaging proof fails and the minimal metadata fix is required
- existing README/docs only if needed to link the example shell without claiming product readiness

Any `lima/` change requires separate approval.

Audit finding:

- PASS. The file map is narrow enough.

## 9. Forbidden Future Surfaces

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

Audit finding:

- PASS. Forbidden surfaces remain explicit.

## 10. Readiness Decision

Ready for:

- `implement-lima-package-example-shell-proof`

That branch may only implement a local package/example-shell proof and focused tests. It should not touch the public Sparkbot repository or Arc Bot repositories.

Not ready for:

- public Sparkbot integration
- Arc Bot integration
- live HumanInput
- IntentEnvelope runtime creation
- Guardian enforcement
- model calls
- provider routing
- tool execution
- persistence
- live discovery
- connector behavior
- Robo-OS access
- physical-world behavior

## Key Findings

- The contract is docs-only and safe.
- Package metadata already exists and should be verified before changed.
- The example shell proof is local, inert, deterministic, and dry-run only.
- The design moves LIMA toward Sparkbot/Arc dependency-readiness without crossing into integration.
- Handoff notes for Sparkbot/Arc teams are present and explicitly say not to integrate yet.

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2479 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except this audit report before commit

## Recommended Next Branch

`implement-lima-package-example-shell-proof`

After that implementation passes, run:

`audit-lima-package-example-shell-proof`

Only after that audit should LIMA move into a Sparkbot/Arc normalized request metadata contract lane.
